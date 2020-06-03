import lightgbm as lgb
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import numpy as np
import pandas as pd

df_x = pd.read_csv('../../resource/Term2/train_processed.csv') # x:説明変数
df_test = pd.read_csv('../../resource/Term2/test_processed.csv')  # testデータ

df = pd.concat([df_x, df_test], axis=0)
# Object型のデータを全てダミー変数か
df = pd.get_dummies(df)

df_x = df[0:31470]
df_test = df[31470:]

df_y = df_x[['賃料']] # y:目的変数
df_x = df_x.drop('賃料', axis=1)
df_x = df_x.drop('id', axis=1)


# 訓練データとテストデータに分割する
X_train, X_test, y_train, y_test = train_test_split(df_x, df_y, test_size=2)

# モデルを学習する
model = lgb.LGBMRegressor()
model.fit(X_train, y_train)

# テストデータを予測する
y_pred = model.predict(X_test)

# RMSE を計算する
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(rmse)



# sigante 提出用
df_id = df_test[['id']]
df_test = df_test.drop('賃料', axis=1)
df_test = df_test.drop('id', axis=1)
#print(len(df_id))
#print(df_test)

y_pred = model.predict(df_test)
y_pred = [int(n) for n in y_pred]
#print(len(y_pred))
df = pd.DataFrame(y_pred)

df = pd.concat([df_id, df], axis=1)
#print(df)
df.to_csv('submit.csv', index=None, header=None)

