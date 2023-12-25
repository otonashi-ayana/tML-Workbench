
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, roc_auc_score, roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay, precision_recall_curve
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os


# 加载数据集
try:
    df = pd.read_csv('/django-tML-Workbench/media/databases/heart_ZCqIf6Y.csv')
except:
    df = pd.read_excel('D:\Code\Project\PycharmWorkspaces\PycharmMisc\django-volt-dashboard-master/databases/heart_ZCqIf6Y.csv')


model_inits = {'LinearRegression': 'LinearRegression(fit_intercept=True, normalize=False)\n', 'Ridge': 'Ridge(alpha=1.0, solver="auto")\n', 'Lasso': 'Lasso(alpha=1.0, max_iter=1000)\n', 'ElasticNet': 'ElasticNet(alpha=1.0, l1_ratio=0.5)\n', 'DecisionTreeRegressor': 'DecisionTreeRegressor(max_depth=None, min_samples_split=2)\n', 'LogisticRegression': 'LogisticRegression(penalty="l2", C=1.0)\n', 'KNeighborsClassifier': 'KNeighborsClassifier(n_neighbors=5, weights="uniform")\n', 'SVC': 'SVC(C=1.0, kernel="rbf", probability=True)\n', 'DecisionTreeClassifier': 'DecisionTreeClassifier(max_depth=None, min_samples_split=2)\n', 'RandomForestClassifier': 'RandomForestClassifier(n_estimators=100, max_depth=None)\n'}

algorithms = ['LogisticRegression', 'KNeighborsClassifier']

# 确定数值和分类特征
numeric_features = df.drop('HeartDisease', axis=1).select_dtypes(include=['int64', 'float64']).columns
categorical_features = df.drop('HeartDisease', axis=1).select_dtypes(include=['object']).columns

# 构建预处理管道
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    
y = df['HeartDisease']
X = df.drop(columns=['HeartDisease'])

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
model_pipelines = {alg: Pipeline(steps=[('preprocessor', preprocessor), ('model', eval(model_inits[alg]))]) for alg
                       in algorithms}

# 训练模型
model_LogisticRegression = model_pipelines['LogisticRegression'].fit(X_train, y_train)
model_KNeighborsClassifier = model_pipelines['KNeighborsClassifier'].fit(X_train, y_train)

# 评估模型
print('Accuracy for LogisticRegression:', accuracy_score(y_test, model_LogisticRegression.predict(X_test)))

precision, recall, _ = precision_recall_curve(y_test, model_LogisticRegression.predict_proba(X_test)[:, 1])
plt.figure()
plt.plot(recall, precision, marker='.')
plt.title('Precision-Recall for LogisticRegression')
plt.xlabel('Recall')
plt.ylabel('Precision')
os.makedirs(f'../outputs',exist_ok=True)
plt.savefig(f'../outputs/Precision-Recall for LogisticRegression.png')
plt.close()

fpr, tpr, _ = roc_curve(y_test, model_LogisticRegression.predict_proba(X_test)[:, 1])
roc_auc = auc(fpr, tpr)
RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name='LogisticRegression').plot()
plt.title('ROC Curve for LogisticRegression')
os.makedirs(f'../outputs',exist_ok=True)
plt.savefig(f'../outputs/ROC Curve for LogisticRegression.png')
plt.close()

print('Accuracy for KNeighborsClassifier:', accuracy_score(y_test, model_KNeighborsClassifier.predict(X_test)))

precision, recall, _ = precision_recall_curve(y_test, model_KNeighborsClassifier.predict_proba(X_test)[:, 1])
plt.figure()
plt.plot(recall, precision, marker='.')
plt.title('Precision-Recall for KNeighborsClassifier')
plt.xlabel('Recall')
plt.ylabel('Precision')
os.makedirs(f'../outputs',exist_ok=True)
plt.savefig(f'../outputs/Precision-Recall for KNeighborsClassifier.png')
plt.close()

fpr, tpr, _ = roc_curve(y_test, model_KNeighborsClassifier.predict_proba(X_test)[:, 1])
roc_auc = auc(fpr, tpr)
RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name='KNeighborsClassifier').plot()
plt.title('ROC Curve for KNeighborsClassifier')
os.makedirs(f'../outputs',exist_ok=True)
plt.savefig(f'../outputs/ROC Curve for KNeighborsClassifier.png')
plt.close()


