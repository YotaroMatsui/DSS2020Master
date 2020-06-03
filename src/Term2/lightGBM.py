# -*- coding: utf-8 -*-

import lightgbm as lgb
#from lightgbm import LGBMRegressor as lbg

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import numpy as np
import pandas as pd

"""LightGBM を使った回帰のサンプルコード"""

# データセットを読み込む
df_x = pd.read_csv('../../resource/Term2/train_processed.csv') # x:説明変数
df_y = df_x[['賃料']] # y:目的変数
df_x = df_x.drop('賃料', axis=1)
#df_x = df_x.drop('id', axis=1)

#df_test = pd.read_csv('../../resource/Term2/test_processed_2.csv')

# Object型のデータを全てダミー変数か
df_x = pd.get_dummies(df_x)


# 訓練データとテストデータに分割する
X_train, X_test, y_train, y_test = train_test_split(df_x, df_y)

# 上記のパラメータでモデルを学習する
model = lgb.LGBMRegressor()
model.fit(X_train, y_train)

# テストデータを予測する
y_pred = model.predict(X_test)

# RMSE を計算する
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(rmse)



# sigante 提出用
df_test = pd.read_csv('../../resource/Term2/test_processed.csv') # x:説明変数
df_test = pd.get_dummies(df_test)
y_pred = model.predict(df_x)

print(y_pred)

