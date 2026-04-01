import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from app.coffee_data import coffees

def build_features():
    df = pd.DataFrame(coffees)
    
    # 數值特徵（酸苦甜醇）
    scaler = MinMaxScaler()
    numeric = scaler.fit_transform(df[['acidity', 'bitterness', 'sweetness', 'body']])
    
    # 類別特徵（flavor, roast）
    encoder = OneHotEncoder(sparse_output=False)
    categorical = encoder.fit_transform(df[['flavor', 'roast']])
    
    # 合併成一個特徵矩陣
    features = np.hstack([numeric, categorical])
    
    return df, features, scaler, encoder

def recommend(user_prefs: dict, top_n: int = 3) -> list:
    df, features, scaler, encoder = build_features()
    
    # 把用戶偏好轉成向量
    numeric_input = scaler.transform([[
        user_prefs['acidity'],
        user_prefs['bitterness'],
        user_prefs['sweetness'],
        user_prefs['body']
    ]])
    categorical_input = encoder.transform([[
        user_prefs['flavor'],
        user_prefs['roast']
    ]])
    user_vector = np.hstack([numeric_input, categorical_input])
    
    # 計算相似度
    scores = cosine_similarity(user_vector, features)[0]
    top_indices = np.argsort(scores)[::-1][:top_n]
    
    results = []
    for i in top_indices:
        coffee = df.iloc[i].to_dict()
        coffee['score'] = round(float(scores[i]) * 100, 1)
        results.append(coffee)
    
    return results