import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random

# 多言語対応の辞書
LANGUAGES = {
    'ja': {
        'app_title': '日田市観光防災アプリ',
        'mode_selection': 'モード選択',
        'tourism_mode': '観光モード',
        'disaster_mode': '防災モード',
        'language_selection': '言語選択',
        'current_location': '現在地',
        'select_destination': '目的地を選択',
        'route_navigation': 'ルートナビゲーション',
        'recommended_places': 'おすすめスポット',
        'seasonal_events': '期間限定イベント',
        'waiting_time': '待ち時間情報',
        'travel_time': '移動時間',
        'by_bicycle': '自転車',
        'by_car': '車',
        'by_public_transport': '公共交通機関',
        'transport_fee': '交通費',
        'parking_available': '駐車場有り',
        'parking_unavailable': '駐車場無し',
        'entrance_fee': '入場料',
        'evacuation_shelters': '避難所',
        'dangerous_areas': '危険箇所',
        'safe_route': '安全なルート',
        'minutes': '分',
        'yen': '円',
        'map_view': 'マップ表示'
    },
    'en': {
        'app_title': 'Hita City Tourism & Disaster Prevention App',
        'mode_selection': 'Mode Selection',
        'tourism_mode': 'Tourism Mode',
        'disaster_mode': 'Disaster Prevention Mode',
        'language_selection': 'Language Selection',
        'current_location': 'Current Location',
        'select_destination': 'Select Destination',
        'route_navigation': 'Route Navigation',
        'recommended_places': 'Recommended Places',
        'seasonal_events': 'Seasonal Events',
        'waiting_time': 'Waiting Time',
        'travel_time': 'Travel Time',
        'by_bicycle': 'By Bicycle',
        'by_car': 'By Car',
        'by_public_transport': 'By Public Transport',
        'transport_fee': 'Transport Fee',
        'parking_available': 'Parking Available',
        'parking_unavailable': 'No Parking',
        'entrance_fee': 'Entrance Fee',
        'evacuation_shelters': 'Evacuation Shelters',
        'dangerous_areas': 'Dangerous Areas',
        'safe_route': 'Safe Route',
        'minutes': 'min',
        'yen': 'JPY',
        'map_view': 'Map View'
    },
    'ko': {
        'app_title': '히타시 관광방재 앱',
        'mode_selection': '모드 선택',
        'tourism_mode': '관광 모드',
        'disaster_mode': '방재 모드',
        'language_selection': '언어 선택',
        'current_location': '현재 위치',
        'select_destination': '목적지 선택',
        'route_navigation': '경로 안내',
        'recommended_places': '추천 장소',
        'seasonal_events': '기간한정 이벤트',
        'waiting_time': '대기시간',
        'travel_time': '이동시간',
        'by_bicycle': '자전거',
        'by_car': '자동차',
        'by_public_transport': '대중교통',
        'transport_fee': '교통비',
        'parking_available': '주차장 있음',
        'parking_unavailable': '주차장 없음',
        'entrance_fee': '입장료',
        'evacuation_shelters': '대피소',
        'dangerous_areas': '위험지역',
        'safe_route': '안전한 경로',
        'minutes': '분',
        'yen': '엔',
        'map_view': '지도 보기'
    },
    'zh': {
        'app_title': '日田市观光防灾应用',
        'mode_selection': '模式选择',
        'tourism_mode': '观光模式',
        'disaster_mode': '防灾模式',
        'language_selection': '语言选择',
        'current_location': '当前位置',
        'select_destination': '选择目的地',
        'route_navigation': '路线导航',
        'recommended_places': '推荐景点',
        'seasonal_events': '限时活动',
        'waiting_time': '等待时间',
        'travel_time': '出行时间',
        'by_bicycle': '骑自行车',
        'by_car': '开车',
        'by_public_transport': '公共交通',
        'transport_fee': '交通费',
        'parking_available': '有停车场',
        'parking_unavailable': '无停车场',
        'entrance_fee': '门票',
        'evacuation_shelters': '避难所',
        'dangerous_areas': '危险区域',
        'safe_route': '安全路线',
        'minutes': '分钟',
        'yen': '日元',
        'map_view': '地图显示'
    }
}

# サンプルデータ（実際のアプリケーションでは外部APIやデータベースから取得）
TOURISM_SPOTS = {
    'ja': [
        {'name': '日田温泉', 'lat': 33.3233, 'lon': 130.9417, 'entrance_fee': 500, 'parking': True, 'waiting_time': 15},
        {'name': '豆田町', 'lat': 33.3278, 'lon': 130.9472, 'entrance_fee': 0, 'parking': True, 'waiting_time': 5},
        {'name': '千年あかり', 'lat': 33.3250, 'lon': 130.9450, 'entrance_fee': 0, 'parking': False, 'waiting_time': 10},
        {'name': '日田祇園祭会館', 'lat': 33.3289, 'lon': 130.9463, 'entrance_fee': 300, 'parking': True, 'waiting_time': 8}
    ],
    'en': [
        {'name': 'Hita Onsen', 'lat': 33.3233, 'lon': 130.9417, 'entrance_fee': 500, 'parking': True, 'waiting_time': 15},
        {'name': 'Mameda-machi', 'lat': 33.3278, 'lon': 130.9472, 'entrance_fee': 0, 'parking': True, 'waiting_time': 5},
        {'name': 'Sennen Akari', 'lat': 33.3250, 'lon': 130.9450, 'entrance_fee': 0, 'parking': False, 'waiting_time': 10},
        {'name': 'Hita Gion Festival Hall', 'lat': 33.3289, 'lon': 130.9463, 'entrance_fee': 300, 'parking': True, 'waiting_time': 8}
    ]
}

SEASONAL_EVENTS = {
    'ja': [
        {'name': '日田川開き観光祭', 'start_date': '2024-05-25', 'end_date': '2024-05-26', 'lat': 33.3233, 'lon': 130.9417},
        {'name': '日田祇園祭', 'start_date': '2024-07-20', 'end_date': '2024-07-21', 'lat': 33.3278, 'lon': 130.9472}
    ]
}

EVACUATION_SHELTERS = [
    {'name': '日田市民文化会館', 'lat': 33.3300, 'lon': 130.9400, 'capacity': 500},
    {'name': '三芳小学校', 'lat': 33.3350, 'lon': 130.9500, 'capacity': 300},
    {'name': '咸宜小学校', 'lat': 33.3200, 'lon': 130.9350, 'capacity': 250}
]

DANGEROUS_AREAS = [
    {'name': '三隈川沿い低地', 'lat': 33.3210, 'lon': 130.9380, 'risk_type': '洪水'},
    {'name': '急斜面地域', 'lat': 33.3400, 'lon': 130.9600, 'risk_type': '土砂災害'}
]

def get_text(key, lang):
    """指定された言語のテキストを取得"""
    return LANGUAGES.get(lang, LANGUAGES['ja']).get(key, key)

def calculate_travel_time(start_lat, start_lon, end_lat, end_lon):
    """移動時間を計算（簡易版）"""
    # 実際のアプリケーションでは外部ルーティングAPIを使用
    distance = np.sqrt((end_lat - start_lat)**2 + (end_lon - start_lon)**2) * 100  # km換算（簡易）
    
    bicycle_time = int(distance * 4)  # 自転車: 15km/h想定
    car_time = int(distance * 2)      # 車: 30km/h想定
    public_time = int(distance * 3)   # 公共交通機関: 20km/h想定
    public_fee = int(distance * 50)   # 1kmあたり50円想定
    
    return bicycle_time, car_time, public_time, public_fee

def create_map(center_lat=33.3233, center_lon=130.9417, zoom=13):
    """マップを作成"""
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)
    return m

def main():
    # セッション状態の初期化
    if 'language' not in st.session_state:
        st.session_state.language = 'ja'
    if 'mode' not in st.session_state:
        st.session_state.mode = 'tourism'
    if 'current_location' not in st.session_state:
        st.session_state.current_location = [33.3233, 130.9417]  # 日田市役所周辺

    # サイドバー
    st.sidebar.title(get_text('language_selection', st.session_state.language))
    st.session_state.language = st.sidebar.selectbox(
        '',
        options=['ja', 'en', 'ko', 'zh'],
        format_func=lambda x: {'ja': '日本語', 'en': 'English', 'ko': '한국어', 'zh': '中文'}[x],
        index=['ja', 'en', 'ko', 'zh'].index(st.session_state.language)
    )

    # メインタイトル
    st.title(get_text('app_title', st.session_state.language))

    # モード選択
    st.subheader(get_text('mode_selection', st.session_state.language))
    mode_options = [get_text('tourism_mode', st.session_state.language), 
                   get_text('disaster_mode', st.session_state.language)]
    selected_mode = st.radio('', mode_options, horizontal=True)
    st.session_state.mode = 'tourism' if selected_mode == mode_options[0] else 'disaster'

    # 現在地設定
    st.subheader(get_text('current_location', st.session_state.language))
    col1, col2 = st.columns(2)
    with col1:
        current_lat = st.number_input('Latitude', value=st.session_state.current_location[0], format="%.6f")
    with col2:
        current_lon = st.number_input('Longitude', value=st.session_state.current_location[1], format="%.6f")
    
    st.session_state.current_location = [current_lat, current_lon]

    if st.session_state.mode == 'tourism':
        tourism_mode()
    else:
        disaster_mode()

def tourism_mode():
    lang = st.session_state.language
    
    st.header(get_text('tourism_mode', lang))
    
    # 期間限定イベント
    st.subheader(get_text('seasonal_events', lang))
    if lang in SEASONAL_EVENTS and SEASONAL_EVENTS[lang]:
        for event in SEASONAL_EVENTS[lang]:
            st.write(f"🎭 {event['name']}")
            st.write(f"📅 {event['start_date']} - {event['end_date']}")
    else:
        st.write("現在開催中の期間限定イベントはありません。")

    # おすすめスポット
    st.subheader(get_text('recommended_places', lang))
    
    spots_key = lang if lang in TOURISM_SPOTS else 'ja'
    spots = TOURISM_SPOTS[spots_key]
    
    # スポット一覧表示
    for i, spot in enumerate(spots):
        with st.expander(f"📍 {spot['name']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**{get_text('waiting_time', lang)}:** {spot['waiting_time']}{get_text('minutes', lang)}")
                parking_status = get_text('parking_available', lang) if spot['parking'] else get_text('parking_unavailable', lang)
                st.write(f"**🚗:** {parking_status}")
            
            with col2:
                if spot['entrance_fee'] > 0:
                    st.write(f"**{get_text('entrance_fee', lang)}:** {spot['entrance_fee']}{get_text('yen', lang)}")
                else:
                    st.write(f"**{get_text('entrance_fee', lang)}:** 無料")
            
            with col3:
                # 移動時間計算
                bicycle_time, car_time, public_time, public_fee = calculate_travel_time(
                    st.session_state.current_location[0], st.session_state.current_location[1],
                    spot['lat'], spot['lon']
                )
                
                st.write(f"**{get_text('travel_time', lang)}:**")
                st.write(f"🚲 {bicycle_time}{get_text('minutes', lang)}")
                st.write(f"🚗 {car_time}{get_text('minutes', lang)}")
                st.write(f"🚌 {public_time}{get_text('minutes', lang)} ({public_fee}{get_text('yen', lang)})")

    # マップ表示
    st.subheader(get_text('map_view', lang))
    m = create_map()
    
    # 現在地をマーカーで表示
    folium.Marker(
        st.session_state.current_location,
        popup="現在地",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # 観光スポットをマーカーで表示
    for spot in spots:
        folium.Marker(
            [spot['lat'], spot['lon']],
            popup=spot['name'],
            icon=folium.Icon(color='blue', icon='star')
        ).add_to(m)
    
    st_folium(m, width=700, height=500)

def disaster_mode():
    lang = st.session_state.language
    
    st.header(get_text('disaster_mode', lang))
    
    # 避難所情報
    st.subheader(get_text('evacuation_shelters', lang))
    
    shelter_data = []
    for shelter in EVACUATION_SHELTERS:
        bicycle_time, car_time, public_time, public_fee = calculate_travel_time(
            st.session_state.current_location[0], st.session_state.current_location[1],
            shelter['lat'], shelter['lon']
        )
        
        shelter_data.append({
            '避難所名': shelter['name'],
            '収容人数': f"{shelter['capacity']}人",
            '徒歩時間': f"{bicycle_time * 2}分",  # 徒歩は自転車の2倍時間
            '車での時間': f"{car_time}分"
        })
    
    st.dataframe(pd.DataFrame(shelter_data))
    
    # 危険箇所
    st.subheader(get_text('dangerous_areas', lang))
    
    danger_data = []
    for danger in DANGEROUS_AREAS:
        danger_data.append({
            '場所': danger['name'],
            '災害種別': danger['risk_type']
        })
    
    st.dataframe(pd.DataFrame(danger_data))
    
    # 防災マップ
    st.subheader(get_text('map_view', lang))
    m = create_map()
    
    # 現在地
    folium.Marker(
        st.session_state.current_location,
        popup="現在地",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # 避難所
    for shelter in EVACUATION_SHELTERS:
        folium.Marker(
            [shelter['lat'], shelter['lon']],
            popup=f"{shelter['name']} (収容人数: {shelter['capacity']}人)",
            icon=folium.Icon(color='green', icon='home')
        ).add_to(m)
    
    # 危険箇所
    for danger in DANGEROUS_AREAS:
        folium.Marker(
            [danger['lat'], danger['lon']],
            popup=f"{danger['name']} ({danger['risk_type']})",
            icon=folium.Icon(color='orange', icon='warning-sign')
        ).add_to(m)
    
    st_folium(m, width=700, height=500)

    # 最寄りの避難所への経路案内
    if st.button(get_text('safe_route', lang)):
        # 最寄りの避難所を計算（簡易版）
        min_distance = float('inf')
        nearest_shelter = None
        
        for shelter in EVACUATION_SHELTERS:
            distance = np.sqrt(
                (shelter['lat'] - st.session_state.current_location[0])**2 + 
                (shelter['lon'] - st.session_state.current_location[1])**2
            )
            if distance < min_distance:
                min_distance = distance
                nearest_shelter = shelter
        
        if nearest_shelter:
            st.success(f"最寄りの避難所: {nearest_shelter['name']}")
            
            # 簡易ルート表示
            route_map = create_map()
            
            # 現在地と避難所をマーカーで表示
            folium.Marker(
                st.session_state.current_location,
                popup="現在地",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(route_map)
            
            folium.Marker(
                [nearest_shelter['lat'], nearest_shelter['lon']],
                popup=f"避難所: {nearest_shelter['name']}",
                icon=folium.Icon(color='green', icon='home')
            ).add_to(route_map)
            
            # 簡易ルートライン
            folium.PolyLine(
                [st.session_state.current_location, [nearest_shelter['lat'], nearest_shelter['lon']]],
                weight=5,
                color='blue',
                opacity=0.8
            ).add_to(route_map)
            
            st_folium(route_map, width=700, height=400)

if __name__ == "__main__":
    st.set_page_config(
        page_title="日田市観光防災アプリ",
        page_icon="🏔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main()