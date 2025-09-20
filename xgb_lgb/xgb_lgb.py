import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
import xgboost as xgb
import lightgbm as lgb
import shap
import matplotlib.pyplot as plt

# ====== 1. 数据加载 ======
# 读取合法和非法的 CSV
df_l = pd.read_csv("legit_abstract.csv")
df_f = pd.read_csv("fraud_abstract.csv")

# 合并
df = pd.concat([df_l, df_f], axis=0).reset_index(drop=True)

X = df[["similarity_mean", "similarity_max", "similarity_min", "logical_mean", "logical_max", "logical_min", "specificity_mean", "specificity_max", "specificity_min"]]
y = df["label"]
#0是非法 1是合法

# ====== 2. 划分训练/测试集 ======
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ====== 3.1 XGBoost ======
xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.1,
    random_state=42
)
xgb_model.fit(X_train, y_train)

y_pred_xgb = xgb_model.predict(X_test)
y_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]

print("XGBoost 准确率:", accuracy_score(y_test, y_pred_xgb))
print("XGBoost AUC:", roc_auc_score(y_test, y_prob_xgb))
print("XGBoost 混淆矩阵:\n", confusion_matrix(y_test, y_pred_xgb))

# ====== 3.2 LightGBM ======
lgb_model = lgb.LGBMClassifier(
    max_depth=-1,           # 不限制树深度
    num_leaves=31,          # 叶子数多一些
    min_data_in_leaf=5,     # 每个叶子至少 5 个样本（默认 20，可能太严格了）
    n_estimators=200,       # 多训练几棵树
    learning_rate=0.05
)
lgb_model.fit(X_train, y_train)

y_pred_lgb = lgb_model.predict(X_test) #predict → 给出最后的分类结果（0/1 标签）
y_prob_lgb = lgb_model.predict_proba(X_test)[:, 1]  #predict_proba → 给出属于每一类的概率，[:, 1] 取的是合法类的概率

print("\nLightGBM 准确率:", accuracy_score(y_test, y_pred_lgb))
print("LightGBM AUC:", roc_auc_score(y_test, y_prob_lgb))
print("LightGBM 混淆矩阵:\n", confusion_matrix(y_test, y_pred_lgb))


X_train = X_train.astype(float)

# 对 XGBoost 模型解释
explainer_xgb = shap.TreeExplainer(xgb_model)
shap_values_xgb = explainer_xgb.shap_values(X_train)

# XGBoost SHAP 分析
# 条形图：整体重要性
shap.summary_plot(shap_values_xgb, X_train, plot_type="bar")
# 散点图：不同取值对预测的影响
shap.summary_plot(shap_values_xgb, X_train)

# 对 LightGBM 模型解释
explainer_lgb = shap.TreeExplainer(lgb_model)
shap_values_lgb = explainer_lgb.shap_values(X_train)
shap_values_lgb = shap_values_lgb[1]
# LightGBM SHAP 分析
shap.summary_plot(shap_values_lgb, X_train, plot_type="bar")
shap.summary_plot(shap_values_lgb, X_train)

