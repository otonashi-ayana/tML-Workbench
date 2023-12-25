from django.urls import path
from admin_tML import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Index
    path('', views.index, name="index"),

    # Pages
    path('pages/dashboard/', views.dashboard, name="dashboard"),

    # database
    path('database/db_manage', views.db_manage, name="db_manage"),
    path('database/db_manage/db_upload', views.db_upload, name='db_upload'),
    path('database/db_manage/db_preview/<int:database_id>', views.db_preview, name='db_preview'),
    path('database/db_manage/update-record/', views.update_record, name='update-record'),

    path('database/db_EDA', views.db_EDA, name="db_EDA"),
    path('api/get_databases', views.get_databases, name="get_databases"),
    path('api/get_dataset_columns/<int:dataset_id>/', views.get_dataset_columns, name='get_dataset_columns'),
    path('database/db_EDA/analyze_database', views.analyze_database, name="analyze_databases"),

    # ML
    path('ML/ML_task', views.ML_task, name="ML_task"),
    path('ML/ML_manage', views.ML_manage, name="ML_manage"),
    path('api/download/<int:pk>/', views.download_field, name="download_field"),
    path('api/submit_training_task', views.submit_training_task, name="submit_training_task"),
    path('api/instance-del/<int:pk>/', views.instance_del, name='instance_del'),
    path('ML/training_result', views.training_result, name="training_result"),
    path('ML/run_script', views.run_script, name="run_script"),
    path('ML/get_output', views.get_output, name="get_output"),

    # interface
    path('interface/interface_task', views.interface_task, name="interface_task"),
    path('interface/interface_manage', views.interface_manage, name="interface_manage"),

    # Authentication
    path('accounts/register/', views.register_view, name="register"),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('accounts/logout/', views.logout_view, name="logout"),
]
