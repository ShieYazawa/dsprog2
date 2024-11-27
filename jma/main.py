import flet as ft
import requests

def main(page: ft.Page):

    # 地域データの取得
    URL = "http://www.jma.go.jp/bosai/common/const/area.json"
    data_json = requests.get(URL).json()
    
    # 天気データの取得（例：東京の場合）
    weather_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
    weather_data = requests.get(weather_URL).json()

    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))


ft.app(main)
