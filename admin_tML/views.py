# coding=utf-8

import json
import os
import subprocess
from django.http import JsonResponse, HttpResponse
import pandas as pd
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from admin_tML.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, \
    UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Database, TrainingTask
from django.core.paginator import Paginator
from dtale.views import startup
from .utils import generate_python_script
from django.conf import settings


# index
def index(request):
    return HttpResponseRedirect("accounts/login")


# Dashboard
def dashboard(request):
    context = {
        'segment': 'dashboard'
    }
    return render(request, 'pages/dashboard/dashboard.html', context)

# 数据集管理模块
def db_manage(request):
    databases = Database.objects.all().order_by('-uploaded_at')
    paginator = Paginator(databases, 6)  # 每页显示 6 条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'parent': 'database',
        'segment': 'db_manage',
        'databases': databases,
        'page_obj': page_obj,
    }
    return render(request, 'pages/database/db_manage.html', context)


def db_preview(request, database_id):
    # id未找到则404
    database = get_object_or_404(Database, id=database_id)
    # 调用Database模型的转换函数，获得数据集数据的字典（json）
    db_dicts_list = database.get_preview_data()

    # paginator = Paginator(db_dicts_list, 10)  # 每页显示 6 条记录
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # page_to_json = page_obj.object_list
    # page_to_json = page_obj.object_list
    # Return the dataset data as JSON
    # return JsonResponse(page_to_json, safe=False)
    return JsonResponse(db_dicts_list, safe=False)


def update_record(request):
    if request.method == 'POST':
        record_id = request.POST.get('id')
        field_name = request.POST.get('field')
        new_value = request.POST.get('value')

        # 更新记录
        record = Database.objects.get(id=record_id)
        setattr(record, field_name, new_value)
        record.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def db_upload(request):
    if request.method == 'POST':
        upload = request.FILES.get('upload')
        name = upload.name
        if upload.name.endswith(('.xlsx', '.xls', 'csv', 'xlsm')):  # 确保是 Excel 文件
            database = Database.objects.create(name=name, upload=upload)
            return JsonResponse({'status': 'success', 'dataset_id': database.id})
        else:
            return JsonResponse({'status': 'error', 'message': '只允许上传 Excel 文件'})


# 数据探索性分析模块
def db_EDA(request):
    context = {
        'parent': 'database',
        'segment': 'db_EDA',
    }
    return render(request, 'pages/database/db_EDA.html', context)


def get_databases(request):
    databases = Database.objects.all().values('id', 'name')
    return JsonResponse(list(databases), safe=False)


def analyze_database(request):
    database_id = request.GET.get('database_id')
    database = Database.objects.get(id=database_id)
    try:
        df = pd.read_excel(database.file.path)
    except:
        df = pd.read_csv(database.upload.path)
    instance = startup(data=df, ignore_duplicate=True)
    return HttpResponseRedirect(f"/flask/dtale/main/{instance._data_id}")

# 模型训练
def ML_task(request):
    context = {
        'parent': 'ML',
        'segment': 'ML_task',
    }
    return render(request, 'pages/ML/ML_task.html', context)


def download_field(request, pk):
    # 获取模型实例
    instance = TrainingTask.objects.get(pk=pk)
    # 创建HTTP响应对象，内容为字段的内容
    response = HttpResponse(instance.parameters, content_type='application/json')
    # 设置HTTP头，提示浏览器以下载方式处理响应内容
    response['Content-Disposition'] = 'attachment; filename="parameters.txt"'
    return response


def instance_del(request, pk):
    obj = TrainingTask.objects.get(pk=pk)
    # obj = get_object_or_404(TrainingTask, pk=pk)
    obj.delete()
    return HttpResponseRedirect(reverse('ML_manage'))


def get_dataset_columns(request, dataset_id):
    try:
        dataset = Database.objects.get(pk=dataset_id)
        columns = dataset.get_columns()
        return JsonResponse({'columns': columns})
    except Database.DoesNotExist:
        return JsonResponse({'error': 'Dataset not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def submit_training_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        task = TrainingTask.objects.create(
            name=data['modelName'],
            dataset_id=data['datasetId'],
            # dataset_name=,
            target_column=data['targetColumn'],
            feature_columns=','.join(data['featureColumns']),
            task_type=data['taskType'],
            model_algorithms=','.join(data['modelAlgorithms']),
            evaluation_methods=','.join(data['evaluationMethods']),
            parameters=json.dumps(data['parameters'])
        )

        return JsonResponse({
            'status': 'success',
            'task_id': task.id,
        })
    return JsonResponse({'status': 'error'}, status=400)


def training_result(request):
    task_id = request.GET.get('task_id')
    # 根据 task_id 获取训练结果，生成脚本等
    task = TrainingTask.objects.get(id=task_id)
    script_content, script_filename = generate_python_script(task)

    # 创建一个文件来保存脚本
    script_path = os.path.join(settings.MEDIA_ROOT + '\\' + task.name + '\\' + "scripts", script_filename)
    print(script_path, '0000')
    # script_path = os.path.join(settings.MEDIA_ROOT, f'{task.name}/scripts', script_filename)
    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    with open(script_path, "w", encoding='utf-8') as file:
        file.write(script_content)

    context = {
        'task': task,
        'script_path': script_path,
        'script_filename': script_filename,
    }
    return render(request, 'pages/ML/ML_task.html', context)


def run_script(request):
    script_filename = request.GET.get('script_filename')
    # script_path = request.GET.get('script_path')
    task_name = request.GET.get('task_name')
    script_path = os.path.join(settings.MEDIA_ROOT + '\\' + task_name + '\\' + "scripts", script_filename)

    output_file_path = os.path.join(f'{settings.MEDIA_ROOT}\\{task_name}\\outputs\\', task_name + '.txt')
    # print(output_file_path, '1111')
    image_dir_path = os.path.join(f'{settings.MEDIA_ROOT}\\{task_name}\\outputs\\')

    # 启动脚本并将输出重定向到文件
    os.makedirs(os.path.dirname(image_dir_path), exist_ok=True)
    with open(output_file_path, "w+") as output_file:
        subprocess.Popen(['python', script_path], stdout=output_file, stderr=output_file)

    return JsonResponse(
        {'status': 'Script is running', 'output_file_path': output_file_path, 'image_dir_path': image_dir_path})


def get_output(request):
    output_file_path = request.GET.get('output_file_path')
    image_dir_path = request.GET.get('image_dir_path')
    task_name = request.GET.get('task_name')
    try:
        with open(output_file_path, "r") as file:
            output = file.read()
    except:
        print('output_file_path ', output_file_path)

    # output_file_url = settings.MEDIA_URL + task_name + '/outputs/' + task_name + '.txt'
    image_urls = [f'{settings.MEDIA_URL}{task_name}/outputs/' + img for img in os.listdir(image_dir_path) if
                  img.endswith(".png")]

    return JsonResponse({
        'output': output,
        'image_urls': image_urls
    })


# 训练任务管理模块
@login_required(login_url="/accounts/login/")
def ML_manage(request):
    ML_tasks = TrainingTask.objects.all().order_by('-uploaded_at')
    paginator = Paginator(ML_tasks, 6)  # 每页显示 6 条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'parent': 'ML',
        'segment': 'ML_manage',
        # 'ML_tasks': ML_tasks,
        'page_obj': page_obj,

    }
    return render(request, 'pages/ML/ML_manage.html', context)


# 训练任务管理模块
@login_required(login_url="/accounts/login/")
def interface_manage(request):
    context = {
        'parent': 'interface',
        'segment': 'interface_manage',
    }
    return render(request, 'pages/tables/bootstrap-tables.html', context)


@login_required(login_url="/accounts/login/")
def interface_task(request):
    context = {
        'parent': 'interface',
        'segment': 'interface_task',
    }
    return render(request, 'pages/tables/bootstrap-tables.html', context)


# Authentication
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 检查用户名是否已经存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'fail', 'message': '用户名已存在，请选择其他用户名'})
        User.objects.create_superuser(username=username, password=password)
        return JsonResponse({'status': 'success', 'message': '注册成功，请登录'})
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        # 处理登录逻辑
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # 返回错误信息
            return render(request, 'accounts/login.html', {'error': '无效的用户名或密码'})
    else:
        return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')
