import os

from django.db import models

# Create your models here.
from django.db import models
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


class Database(models.Model):
    name = models.CharField(max_length=100)
    upload = models.FileField(upload_to='databases/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_preview_data(self):
        # pandas读取数据集
        try:
            df = pd.read_excel(self.upload.path)
        except:
            df = pd.read_csv(self.upload.path)
        # 将DataFrame转换为字典
        data = df.to_dict(orient='records')
        return data

    def get_columns(self):
        try:
            print(111)
            df = pd.read_excel(self.upload.path)
        except:
            print(222)
            df = pd.read_csv(self.upload.path)
        columns = list(df.columns)
        print(columns)
        return columns

    def get_file_size(self):
        return os.path.getsize(self.upload.path)

    def get_url(self):
        return self.upload.url


class TrainingTask(models.Model):
    name = models.CharField(max_length=100)
    dataset_id = models.IntegerField()
    # dataset_name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    target_column = models.CharField(max_length=100)
    feature_columns = models.TextField()  # 存储为逗号分隔的字符串
    task_type = models.CharField(max_length=50)
    model_algorithms = models.TextField()  # 存储为逗号分隔的字符串
    evaluation_methods = models.TextField()  # 存储为逗号分隔的字符串
    parameters = models.TextField()  # JSON格式或其他格式

    def dataset_name(self):
        dataset = Database.objects.get(pk=self.dataset_id)
        dataset_name = dataset.name
        return dataset_name
