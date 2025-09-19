import requests
import json
import pandas as pd
import os

url = "https://www.jma.go.jp/bosai/quake/data/list.json"
location = "C:/my_project/Wether_App/data/"

r = requests.get(url)

data = r.json()

print(f"取得した地震データ数:{len(data)} 件")

#print(json.dumps(data[0]["int"],indent=2,ensure_ascii=False)) #データを見やすくし、日本語込みで見やすくする


df = pd.json_normalize(data)


#ネスト配列の解消
rows = []
for int_list in df["int"]:

    for int_key in int_list:
        code_key = int_key["code"]
        maxi_key = int_key["maxi"]

        #すべての組み合わせを検証
        for city_key in int_key["city"]:
            rows.append({
                "region_code" : code_key,
                "region_maxi" : maxi_key,
                "city_code" : city_key["code"],
                "city_maxi" : city_key["maxi"]
            })


#追加するrowsをデータフレームにする
columns_key = ["region_code","region_maxi","city_code","city_maxi"]
df_rows = pd.DataFrame(rows,columns=columns_key)


#intキーを削除する(ネストされているので別で保存)
df = df.drop(columns=["int"])


#CSVで保存
"""
if os.path.exists(location+"deta_of_des.csv"):
    df.to_csv(location+"data_of_des.csv",mode="a",header=False,index=False)
else:
    df.to_csv(location+"data_of_des.csv",index=False)
"""

#ネスト配列を分解したものを保存
"""
if os.path.exists(location+"region_data.csv"):
    df_rows.to_csv(location+"region_data.csv",mode="a",header=False,index=False)
else:
    df_rows.to_csv(location+"region_data.csv",index=False)
"""
