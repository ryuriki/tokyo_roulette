# 東京の地区から一つを選択する

import streamlit as st
import json
import folium
from folium import plugins
import pandas as pd
import time
import random
from streamlit_folium import folium_static

# 日本のの位置情報データを読み込み
map = pd.read_csv('mapdata.csv', sep='\t')
#東京都のJIScodeは13○○○なのでそれのみを抽出
tokyo_map = map.query('13000 <= jiscode < 14000')


st.title('集まれ関東の民！東京ルーレット旅')

option = st.selectbox("範囲",('東京全域','東京２３区'))

# 東京のエリアをリストとして取得する関数
def get_tokyo_areas(option = '東京全域'):
    '''
    return : list
    '''
    if option == '東京全域':    
        tokyo_areas = list(tokyo_map['name'])
    else:
    # 区のみのリスト
        tokyo_areas = list(tokyo_map[tokyo_map['name'].str.endswith('区')]['name'])
    return tokyo_areas

tokyo_areas= get_tokyo_areas(option = option)

# エリアリストからランダムにエリアを抽出する関数
def spin_reel(stime):
    '''
    parameter:
     stime : sleep_time
    '''
    select_area = random.choice(tokyo_areas)
    st.markdown(f"# {select_area}")
    time.sleep(stime)
    return select_area

# 選択されたエリアの緯度経度を取得する関数
def get_latlong(area):
    lat = tokyo_map.loc[tokyo_map['name']==area, 'lat'].values
    long = tokyo_map.loc[tokyo_map['name']==area, 'long'].values
    return lat, long


# main処理　スタートボタンが押されたら処理が行われる
if st.button("ルーレットスタート"):
    with st.empty():
        i = 0
        # リールを回す
        for _ in range(70):  # 70回転させる
            i += 1
            if i < 40:
                spin_reel(0.1)
                
            elif i < 50:
                spin_reel(0.2)
            elif i < 60:
                spin_reel(0.4)
            elif i < 65:
                spin_reel(0.5)
            elif i < 72:
                area = spin_reel(0.8)
    # 緯度経度取得
    lat, long = get_latlong(area=area)

    # mapを表示
    m = folium.Map(location=[lat, long])
    folium.Marker(
        location=[lat, long],
        popup="This is Simple Marker",
    ).add_to(m)
    folium_static(m)


                
