import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random
import streamlit.components.v1 as components

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

# 実際の日田市観光スポットの正確なGPS座標データ
TOURISM_SPOTS = {
    'ja': [
        {'name': '豆田町（重要伝統的建造物群保存地区）', 'lat': 33.3278, 'lon': 130.9472, 'entrance_fee': 0, 'parking': True, 'waiting_time': 5, 'description': '江戸時代の商家群が残る歴史ある街並み'},
        {'name': '日田温泉', 'lat': 33.3210, 'lon': 130.9380, 'entrance_fee': 500, 'parking': True, 'waiting_time': 15, 'description': '三隈川沿いの温泉街'},
        {'name': '日田祇園祭会館', 'lat': 33.3289, 'lon': 130.9463, 'entrance_fee': 300, 'parking': True, 'waiting_time': 8, 'description': 'ユネスコ無形文化遺産「日田祇園の曳山行事」の展示館'},
        {'name': '咸宜園跡', 'lat': 33.3295, 'lon': 130.9505, 'entrance_fee': 0, 'parking': True, 'waiting_time': 10, 'description': '江戸時代後期の私塾跡地'},
        {'name': '千年あかり', 'lat': 33.3250, 'lon': 130.9450, 'entrance_fee': 0, 'parking': False, 'waiting_time': 10, 'description': '竹灯籠で彩られる幻想的な秋のイベント会場'},
        {'name': '水郷公園', 'lat': 33.3180, 'lon': 130.9340, 'entrance_fee': 0, 'parking': True, 'waiting_time': 3, 'description': '三隈川の水辺公園'},
        {'name': '日田市立博物館', 'lat': 33.3240, 'lon': 130.9420, 'entrance_fee': 100, 'parking': True, 'waiting_time': 12, 'description': '日田の歴史と文化を展示'},
        {'name': 'サッポロビール九州日田工場', 'lat': 33.3089, 'lon': 130.9267, 'entrance_fee': 0, 'parking': True, 'waiting_time': 20, 'description': 'ビール工場見学（要予約）'}
    ],
    'en': [
        {'name': 'Mameda-machi Historic District', 'lat': 33.3278, 'lon': 130.9472, 'entrance_fee': 0, 'parking': True, 'waiting_time': 5, 'description': 'Historic merchant district from Edo period'},
        {'name': 'Hita Onsen Hot Springs', 'lat': 33.3210, 'lon': 130.9380, 'entrance_fee': 500, 'parking': True, 'waiting_time': 15, 'description': 'Hot spring resort along Mikuma River'},
        {'name': 'Hita Gion Festival Hall', 'lat': 33.3289, 'lon': 130.9463, 'entrance_fee': 300, 'parking': True, 'waiting_time': 8, 'description': 'Exhibition hall for UNESCO Intangible Cultural Heritage'},
        {'name': 'Kangien Academy Site', 'lat': 33.3295, 'lon': 130.9505, 'entrance_fee': 0, 'parking': True, 'waiting_time': 10, 'description': 'Site of famous Edo period private school'},
        {'name': 'Sennen Akari Festival Site', 'lat': 33.3250, 'lon': 130.9450, 'entrance_fee': 0, 'parking': False, 'waiting_time': 10, 'description': 'Bamboo lantern festival venue'},
        {'name': 'Suigo Park', 'lat': 33.3180, 'lon': 130.9340, 'entrance_fee': 0, 'parking': True, 'waiting_time': 3, 'description': 'Riverside park along Mikuma River'},
        {'name': 'Hita City Museum', 'lat': 33.3240, 'lon': 130.9420, 'entrance_fee': 100, 'parking': True, 'waiting_time': 12, 'description': 'Museum of Hita history and culture'},
        {'name': 'Sapporo Beer Kyushu Hita Brewery', 'lat': 33.3089, 'lon': 130.9267, 'entrance_fee': 0, 'parking': True, 'waiting_time': 20, 'description': 'Beer factory tour (reservation required)'}
    ],
    'ko': [
        {'name': '마메다마치 역사보존지구', 'lat': 33.3278, 'lon': 130.9472, 'entrance_fee': 0, 'parking': True, 'waiting_time': 5, 'description': '에도시대 상가 거리가 보존된 역사 지구'},
        {'name': '히타온천', 'lat': 33.3210, 'lon': 130.9380, 'entrance_fee': 500, 'parking': True, 'waiting_time': 15, 'description': '미쿠마강변의 온천가'},
        {'name': '히타기온축제회관', 'lat': 33.3289, 'lon': 130.9463, 'entrance_fee': 300, 'parking': True, 'waiting_time': 8, 'description': '유네스코 무형문화유산 전시관'},
        {'name': '간기엔 터', 'lat': 33.3295, 'lon': 130.9505, 'entrance_fee': 0, 'parking': True, 'waiting_time': 10, 'description': '에도시대 유명 사숙 터'},
        {'name': '센넨아카리 축제장', 'lat': 33.3250, 'lon': 130.9450, 'entrance_fee': 0, 'parking': False, 'waiting_time': 10, 'description': '대나무 등불 축제 장소'},
        {'name': '스이고공원', 'lat': 33.3180, 'lon': 130.9340, 'entrance_fee': 0, 'parking': True, 'waiting_time': 3, 'description': '미쿠마강변 공원'},
        {'name': '히타시립박물관', 'lat': 33.3240, 'lon': 130.9420, 'entrance_fee': 100, 'parking': True, 'waiting_time': 12, 'description': '히타의 역사와 문화 전시관'},
        {'name': '삿포로맥주 규슈히타공장', 'lat': 33.3089, 'lon': 130.9267, 'entrance_fee': 0, 'parking': True, 'waiting_time': 20, 'description': '맥주공장 견학 (예약 필요)'}
    ],
    'zh': [
        {'name': '豆田町历史保护区', 'lat': 33.3278, 'lon': 130.9472, 'entrance_fee': 0, 'parking': True, 'waiting_time': 5, 'description': '保存江户时代商家街道的历史地区'},
        {'name': '日田温泉', 'lat': 33.3210, 'lon': 130.9380, 'entrance_fee': 500, 'parking': True, 'waiting_time': 15, 'description': '三隈川畔的温泉街'},
        {'name': '日田祇园祭会馆', 'lat': 33.3289, 'lon': 130.9463, 'entrance_fee': 300, 'parking': True, 'waiting_time': 8, 'description': '联合国教科文组织非物质文化遗产展示馆'},
        {'name': '咸宜园遗址', 'lat': 33.3295, 'lon': 130.9505, 'entrance_fee': 0, 'parking': True, 'waiting_time': 10, 'description': '江户时代著名私塾遗址'},
        {'name': '千年明灯节会场', 'lat': 33.3250, 'lon': 130.9450, 'entrance_fee': 0, 'parking': False, 'waiting_time': 10, 'description': '竹灯笼节活动场所'},
        {'name': '水乡公园', 'lat': 33.3180, 'lon': 130.9340, 'entrance_fee': 0, 'parking': True, 'waiting_time': 3, 'description': '三隈川河滨公园'},
        {'name': '日田市立博物馆', 'lat': 33.3240, 'lon': 130.9420, 'entrance_fee': 100, 'parking': True, 'waiting_time': 12, 'description': '日田历史文化博物馆'},
        {'name': '札幌啤酒九州日田工厂', 'lat': 33.3089, 'lon': 130.9267, 'entrance_fee': 0, 'parking': True, 'waiting_time': 20, 'description': '啤酒工厂参观（需预约）'}
    ]
}

SEASONAL_EVENTS = {
    'ja': [
        {'name': '日田川開き観光祭', 'start_date': '2025-05-24', 'end_date': '2025-05-25', 'lat': 33.3180, 'lon': 130.9340, 'description': '花火大会と屋形船で楽しむ三隈川の風物詩'},
        {'name': '日田祇園祭', 'start_date': '2025-07-19', 'end_date': '2025-07-20', 'lat': 33.3278, 'lon': 130.9472, 'description': 'ユネスコ無形文化遺産の山鉾巡行'},
        {'name': '千年あかり', 'start_date': '2025-11-08', 'end_date': '2025-11-16', 'lat': 33.3250, 'lon': 130.9450, 'description': '3万本の竹灯籠が豆田町を幻想的に照らす'}
    ],
    'en': [
        {'name': 'Hita River Opening Festival', 'start_date': '2025-05-24', 'end_date': '2025-05-25', 'lat': 33.3180, 'lon': 130.9340, 'description': 'Fireworks and boat rides on Mikuma River'},
        {'name': 'Hita Gion Festival', 'start_date': '2025-07-19', 'end_date': '2025-07-20', 'lat': 33.3278, 'lon': 130.9472, 'description': 'UNESCO Intangible Cultural Heritage yamaboko parade'},
        {'name': 'Sennen Akari Festival', 'start_date': '2025-11-08', 'end_date': '2025-11-16', 'lat': 33.3250, 'lon': 130.9450, 'description': '30,000 bamboo lanterns illuminate Mameda-machi'}
    ]
}

EVACUATION_SHELTERS = [
    {'name': '日田市民文化会館', 'lat': 33.3305, 'lon': 130.9425, 'capacity': 500, 'address': '日田市三本松1-8-11'},
    {'name': '三芳小学校', 'lat': 33.3355, 'lon': 130.9515, 'capacity': 300, 'address': '日田市三芳小迫町965'},
    {'name': '咸宜小学校', 'lat': 33.3200, 'lon': 130.9350, 'capacity': 250, 'address': '日田市港町1-23'},
    {'name': '桂林小学校', 'lat': 33.3168, 'lon': 130.9498, 'capacity': 280, 'address': '日田市田島2-3-5'},
    {'name': '日田市総合体育館', 'lat': 33.3145, 'lon': 130.9380, 'capacity': 800, 'address': '日田市田島2-6-1'}
]

DANGEROUS_AREAS = [
    {'name': '三隈川沿い低地（隈町周辺）', 'lat': 33.3210, 'lon': 130.9380, 'risk_type': '洪水・浸水', 'risk_level': '高'},
    {'name': '花月川合流点周辺', 'lat': 33.3195, 'lon': 130.9445, 'risk_type': '洪水・浸水', 'risk_level': '高'},
    {'name': '山間部急斜面地域（大山町）', 'lat': 33.3400, 'lon': 130.9600, 'risk_type': '土砂災害', 'risk_level': '中'},
    {'name': '求来里地区急傾斜地', 'lat': 33.3050, 'lon': 130.9200, 'risk_type': '土砂災害', 'risk_level': '中'},
    {'name': '有田川沿い低地', 'lat': 33.3330, 'lon': 130.9520, 'risk_type': '洪水・浸水', 'risk_level': '中'}
]

def get_gps_location():
    """GPS位置情報を取得するJavaScript関数"""
    gps_html = """
    <div style="padding: 20px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #f9f9f9;">
        <h4 style="color: #4CAF50; margin-top: 0;">📍 GPS位置情報取得</h4>
        <button onclick="getLocation()" style="
            background-color: #4CAF50; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer;
            font-size: 16px;
            margin-bottom: 10px;
        ">🌐 現在地を取得</button>
        
        <div id="location-status" style="margin: 10px 0; font-weight: bold;"></div>
        <div id="location-info" style="
            background-color: white; 
            padding: 10px; 
            border-radius: 5px; 
            border: 1px solid #ddd;
            min-height: 50px;
        ">
            ボタンをクリックして現在地を取得してください
        </div>
        
        <div id="coordinates" style="margin-top: 10px; font-family: monospace; font-size: 14px;"></div>
    </div>

    <script>
    let currentLat = null;
    let currentLon = null;
    
    function getLocation() {
        const statusDiv = document.getElementById("location-status");
        const infoDiv = document.getElementById("location-info");
        const coordDiv = document.getElementById("coordinates");
        
        statusDiv.innerHTML = '🔄 位置情報を取得中...';
        statusDiv.style.color = '#FFA500';
        
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    currentLat = position.coords.latitude;
                    currentLon = position.coords.longitude;
                    const accuracy = Math.round(position.coords.accuracy);
                    
                    statusDiv.innerHTML = '✅ 位置情報取得成功！';
                    statusDiv.style.color = '#4CAF50';
                    
                    infoDiv.innerHTML = 
                        '<strong>取得した位置情報:</strong><br>' +
                        '緯度: ' + currentLat.toFixed(6) + '<br>' +
                        '経度: ' + currentLon.toFixed(6) + '<br>' +
                        '精度: 約' + accuracy + 'm<br>' +
                        '<small>※ 下記の座標をコピーして手動入力してください</small>';
                    
                    coordDiv.innerHTML = 
                        '<strong>コピー用座標:</strong><br>' +
                        '緯度: <span style="background-color: #FFEB3B; padding: 2px 4px; cursor: pointer;" onclick="copyToClipboard(\'' + 
                        currentLat.toFixed(6) + '\')">' + currentLat.toFixed(6) + '</span><br>' +
                        '経度: <span style="background-color: #FFEB3B; padding: 2px 4px; cursor: pointer;" onclick="copyToClipboard(\'' + 
                        currentLon.toFixed(6) + '\')">' + currentLon.toFixed(6) + '</span>';
                    
                    // Google Mapsで現在地を確認するリンクを追加
                    const mapsLink = 'https://maps.google.com/?q=' + currentLat + ',' + currentLon;
                    coordDiv.innerHTML += '<br><a href="' + mapsLink + '" target="_blank" style="color: #1976D2; text-decoration: none;">🗺️ Google Mapsで確認</a>';
                },
                function(error) {
                    statusDiv.style.color = '#F44336';
                    switch(error.code) {
                        case error.PERMISSION_DENIED:
                            statusDiv.innerHTML = '❌ 位置情報の使用が拒否されました';
                            infoDiv.innerHTML = '設定で位置情報の使用を許可してから再試行してください。<br><small>Chrome: アドレスバー左の🔒をクリック → 位置情報を許可</small>';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            statusDiv.innerHTML = '❌ 位置情報が利用できません';
                            infoDiv.innerHTML = 'GPSやネットワーク接続を確認してください。';
                            break;
                        case error.TIMEOUT:
                            statusDiv.innerHTML = '⏰ 位置情報の取得がタイムアウト';
                            infoDiv.innerHTML = '時間内に位置情報を取得できませんでした。再試行してください。';
                            break;
                        default:
                            statusDiv.innerHTML = '❌ 不明なエラー';
                            infoDiv.innerHTML = '不明なエラーが発生しました。';
                            break;
                    }
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 60000
                }
            );
        } else {
            statusDiv.innerHTML = '❌ このブラウザは位置情報をサポートしていません';
            statusDiv.style.color = '#F44336';
            infoDiv.innerHTML = '位置情報に対応したブラウザ（Chrome、Firefox、Safari等）をご使用ください。';
        }
    }
    
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            alert('座標をクリップボードにコピーしました: ' + text);
        }).catch(function() {
            // フォールバック: テキストを選択状態にする
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert('座標をコピーしました: ' + text);
        });
    }
    </script>
    """
    return gps_html

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

    # 現在地設定（GPS機能付き）
    st.subheader(get_text('current_location', st.session_state.language))
    
    # GPS取得セクション
    gps_col, manual_col = st.columns([1, 1])
    
    with gps_col:
        st.markdown("### 🌐 GPS自動取得")
        # GPS取得のHTML componentを表示
        components.html(get_gps_location(), height=350)
        
        st.info("💡 **使用方法:**\n1. 上のボタンをクリック\n2. ブラウザで位置情報使用を許可\n3. 表示された座標を右側の入力欄にコピー")
    
    with manual_col:
        st.markdown("### ✏️ 手動入力")
        current_lat = st.number_input(
            '🌍 緯度 (Latitude)', 
            value=st.session_state.current_location[0], 
            format="%.6f", 
            step=0.000001,
            help="GPS取得した緯度をここに入力してください"
        )
        current_lon = st.number_input(
            '🌏 経度 (Longitude)', 
            value=st.session_state.current_location[1], 
            format="%.6f", 
            step=0.000001,
            help="GPS取得した経度をここに入力してください"
        )
        
        # 座標