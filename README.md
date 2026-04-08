# tML-Workbench

> 基于 Django 的机器学习训练实验平台

![tML-logo](https://github.com/otonashi-ayana/tML-Workbench/blob/master/img/tML-logo.jpg)

## 项目简介

tML-Workbench 是一个面向机器学习实验的 Web 平台，提供数据集管理、探索性数据分析（EDA）、模型训练配置、脚本自动生成与执行、训练结果可视化等功能，帮助用户在浏览器中完成完整的机器学习实验流程，无需手动编写训练代码。

## 主要功能

### 📁 数据集管理
- 上传 Excel（`.xlsx`、`.xls`、`.xlsm`）和 CSV 数据文件
- 数据集列表分页展示，支持在线预览数据内容
- 支持记录字段的在线编辑

### 🔍 探索性数据分析（EDA）
- 集成 [D-Tale](https://github.com/man-group/dtale)，在浏览器中对数据集进行可视化交互分析

### 🤖 模型训练
- 通过 Web 界面配置训练任务，支持：
  - **任务类型**：分类（Classification）、回归（Regression）
  - **回归算法**：Linear Regression、Ridge、Lasso、ElasticNet、Decision Tree Regressor
  - **分类算法**：Logistic Regression、KNN、SVC、Decision Tree Classifier、Random Forest Classifier
  - **评估指标**：MSE、R²、Accuracy、Precision-Recall Curve、ROC Curve
- 自动生成可复用的 Python 训练脚本（基于 scikit-learn Pipeline，含数据预处理）
- 在平台上直接运行脚本，实时查看输出日志与可视化图像

### 📋 任务管理
- 分页管理所有训练任务
- 下载训练参数配置（JSON）
- 删除任务记录

### 👤 用户认证
- 注册、登录、登出
- 受保护页面（训练任务管理、接口管理）需登录访问

## 技术栈

| 层级 | 技术 |
|------|------|
| Web 框架 | Django 4.1 |
| UI 主题 | Django Admin Volt (Bootstrap 5) |
| 数据处理 | pandas |
| 机器学习 | scikit-learn |
| EDA | D-Tale |
| 静态文件 | WhiteNoise |
| 应用服务器 | Gunicorn |
| 反向代理 | Nginx |
| 数据库 | SQLite（默认）/ MySQL / PostgreSQL（可配置）|
| 部署 | Docker / Docker Compose / Render |

## 快速开始

### 环境要求

- Python 3.9+

### 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/otonashi-ayana/tML-Workbench.git
cd tML-Workbench

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py migrate

# 4. 启动开发服务器
python manage.py runserver
```

浏览器访问 `http://127.0.0.1:8000/`，注册账号后即可使用。

### 环境变量（可选）

在项目根目录创建 `.env` 文件以覆盖默认配置：

```env
SECRET_KEY=your-secret-key

# 外部数据库（不配置则使用 SQLite）
DB_ENGINE=postgresql   # 或 mysql
DB_NAME=your_db_name
DB_USERNAME=your_db_user
DB_PASS=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Docker 部署

```bash
docker-compose up --build
```

服务将在 `http://localhost:5085` 上运行（Nginx 反向代理 Gunicorn）。

### Render 部署

项目已包含 `render.yaml` 与 `build.sh`，可直接在 [Render](https://render.com) 上一键部署。

## 项目结构

```
tML-Workbench/
├── core/                   # Django 项目配置（settings、urls、wsgi）
├── admin_tML/              # 核心应用
│   ├── models.py           # 数据模型（Database、TrainingTask）
│   ├── views.py            # 视图逻辑
│   ├── urls.py             # URL 路由
│   ├── utils.py            # Python 训练脚本生成器
│   ├── forms.py            # 表单
│   └── templates/          # HTML 模板
│       ├── pages/
│       │   ├── dashboard/  # 首页仪表盘
│       │   ├── database/   # 数据集管理与 EDA
│       │   └── ML/         # 模型训练与任务管理
│       └── accounts/       # 登录/注册页面
├── media/                  # 用户上传文件及训练输出
├── static/                 # 静态资源
├── nginx/                  # Nginx 配置
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

## 使用流程

1. **注册/登录** → 访问平台
2. **上传数据集** → 数据集管理页面上传 Excel/CSV 文件
3. **探索数据** → EDA 页面使用 D-Tale 进行可视化分析
4. **配置训练任务** → 选择数据集、目标列、特征列、任务类型、算法及评估指标
5. **生成并运行脚本** → 平台自动生成 scikit-learn 训练脚本并执行
6. **查看结果** → 实时查看控制台输出与评估图表（ROC、PR Curve 等）

## 许可证

本项目采用 [MIT License](LICENSE)。
