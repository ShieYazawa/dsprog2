import flet as ft
import json
import requests
from datetime import datetime   # 日付を扱うためのモジュール

def main(page: ft.Page):
    page.title = "天気予報"
    page.window.width = 950
    page.window.height = 650
    page.padding = 0
    page.bgcolor = "#F0F0F0"  # 背景色を設定

    # 天気コードと天気名の対応辞書
    weather_codes = {
        "100": "晴れ",
        "101": "晴時々曇",
        "102": "晴一時雨",
        "103": "晴時々雨",
        "104": "晴一時雪",
        "105": "晴時々雪",
        "106": "晴一時雨か雪",
        "107": "晴時々雨か雪",
        "108": "晴一時雨か雷雨",
        "110": "晴後時々曇",
        "111": "晴後曇",
        "112": "晴後一時雨",
        "113": "晴後時々雨",
        "114": "晴後雨",
        "115": "晴後一時雪",
        "116": "晴後時々雪",
        "117": "晴後雪",
        "118": "晴後雨か雪",
        "119": "晴後雨か雷雨",
        "120": "晴朝夕一時雨",
        "121": "晴朝の内一時雨",
        "122": "晴夕方一時雨",
        "123": "晴山沿い雷雨",
        "124": "晴山沿い雪",
        "125": "晴午後は雷雨",
        "126": "晴昼頃から雨",
        "127": "晴夕方から雨",
        "128": "晴夜は雨",
        "130": "朝の内霧後晴",
        "131": "晴明け方霧",
        "132": "晴朝夕曇",
        "140": "晴時々雨で雷を伴う",
        "160": "晴一時雪か雨",
        "170": "晴時々雪か雨",
        "181": "晴後雪か雨",
        "200": "曇り",
        "201": "曇時々晴",
        "202": "曇一時雨",
        "203": "曇時々雨",
        "204": "曇一時雪",
        "205": "曇時々雪",
        "206": "曇一時雨か雪",
        "207": "曇時々雨か雪",
        "208": "曇一時雨か雷雨",
        "209": "霧",
        "210": "曇後時々晴",
        "211": "曇後晴",
        "212": "曇後一時雨",
        "213": "曇後時々雨",
        "214": "曇後雨",
        "215": "曇後一時雪",
        "216": "曇後時々雪",
        "217": "曇後雪",
        "218": "曇後雨か雪",
        "219": "曇後雨か雷雨",
        "220": "曇朝夕一時雨",
        "221": "曇朝の内一時雨",
        "222": "曇夕方一時雨",
        "223": "曇日中時々晴",
        "224": "曇昼頃から雨",
        "225": "曇夕方から雨",
        "226": "曇夜は雨",
        "228": "曇昼頃から雪",
        "229": "曇夕方から雪",
        "230": "曇夜は雪",
        "231": "曇海上海岸は霧か霧雨",
        "240": "曇時々雨で雷を伴う",
        "250": "曇時々雪で雷を伴う",
        "260": "曇一時雪か雨",
        "270": "曇時々雪か雨",
        "281": "曇後雪か雨",
        "300": "雨",
        "301": "雨時々晴",
        "302": "雨時々止む",
        "303": "雨時々雪",
        "304": "雨か雪",
        "306": "大雨",
        "308": "雨で暴風を伴う",
        "309": "雨一時雪",
        "311": "雨後晴",
        "313": "雨後曇",
        "314": "雨後時々雪",
        "315": "雨後雪",
        "316": "雨か雪後晴",
        "317": "雨か雪後曇",
        "320": "朝の内雨後晴",
        "321": "朝の内雨後曇",
        "322": "雨朝晩一時雪",
        "323": "雨昼頃から晴",
        "324": "雨夕方から晴",
        "325": "雨夜は晴",
        "326": "雨夕方から雪",
        "327": "雨夜は雪",
        "328": "雨一時強く降る",
        "329": "雨一時みぞれ",
        "340": "雪か雨",
        "350": "雨で雷を伴う",
        "361": "雪か雨後晴",
        "371": "雪か雨後曇",
        "400": "雪",
        "401": "雪時々晴",
        "402": "雪時々止む",
        "403": "雪時々雨",
        "405": "大雪",
        "406": "風雪強い",
        "407": "暴風雪",
        "409": "雪一時雨",
        "411": "雪後晴",
        "413": "雪後曇",
        "414": "雪後雨",
        "420": "朝の内雪後晴",
        "421": "朝の内雪後曇",
        "422": "雪昼頃から雨",
        "423": "雪夕方から雨",
        "425": "雪一時強く降る",
        "426": "雪後みぞれ",
        "427": "雪一時みぞれ",
        "450": "雪で雷を伴う"
    }

    # 場所を取得する関数
    def load_areas():
        try:
            url = "https://www.jma.go.jp/bosai/common/const/area.json"
            response = requests.get(url).json()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error loading areas from URL: {e}")
            return {}

    def update_weather(e, area_id):
        try:
            url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_id}.json"
            weather_data = requests.get(url).json()

            # 天気予報カードを格納するリスト
            weather_cards = []

            # 予報データから天気カードを作成
            for i in range(7):   # 天気情報は7日分取得(固定)
                try:
                    # デフォルトの気温値を設定
                    max_temp = "--"
                    min_temp = "--"
                    # 今日の日付・天気・気温データを取得
                    if i == 0:
                        date = weather_data[0]['timeSeries'][0]['timeDefines'][i]
                        weather = weather_data[0]['timeSeries'][0]['areas'][0]['weatherCodes'][i]   # 天気を示すコードを取得
                        temps = weather_data[0]['timeSeries'][2]['areas'][0]['temps']
                        if len(temps) >= 4: # データが4つ以上あるか確認
                            min_temp = temps[2]  # 24時の気温
                            max_temp = temps[1]  # 12時の気温

                    # 明日以降の日付・天気・気温データを取得
                    elif i > 0:
                        week_index = i - 1
                        date = weather_data[1]['timeSeries'][0]['timeDefines'][week_index]
                        weather = weather_data[1]['timeSeries'][0]['areas'][0]['weatherCodes'][week_index]
                        if week_index < len(weather_data[1]['timeSeries'][1]['areas'][0]['tempsMax']):
                            max_temp = weather_data[1]['timeSeries'][1]['areas'][0]['tempsMax'][week_index]
                            min_temp = weather_data[1]['timeSeries'][1]['areas'][0]['tempsMin'][week_index]

                    # 空文字列の場合はデフォルト値を使用
                    if max_temp == "":
                        max_temp = "--"
                    if min_temp == "":
                        min_temp = "--"

                    # 日付をフォーマット
                    date_obj = datetime.fromisoformat(date) # ISO形式の日付文字列をdatetimeオブジェクトに変換
                    formatted_date = date_obj.strftime('%Y-%m-%d')  # YYYY-MM-DD形式に変換

                    # 天気アイコンのURL
                    icon_url = f"https://www.jma.go.jp/bosai/forecast/img/{weather}.png"

                    # 天気カードの作成
                    weather_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(f"{formatted_date}", size=14, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Image(src=icon_url, width=50, height=50),    # 天気アイコンURLで取得した画像を表示
                                    ft.Text(weather_codes.get(weather, weather),    # 天気コードに対応する天気名をget()で取得
                                            size=14, color="black"),  # 天気
                                    ft.Row(
                                        controls=[
                                            ft.Text(f"{min_temp}℃", size=14, color = "blue"),
                                            ft.Text(" / ", size=14, color = "black"),
                                            ft.Text(f"{max_temp}℃", size=14, color = "red")  # 最低気温 / 最高気温
                                                                                            # 最低気温は青色、最高気温は赤色で表示
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,  # 横の中央揃え
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,  # 縦の中央揃え
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # 横の中央揃え
                            ),
                            padding=10,   # カード内の余白
                            bgcolor="#FFFFFF",  # カードの背景色(白)
                        ),
                        width=150,  # カードの幅
                        height=200, # カードの高さ
                    )

                    # 天気カードをリストに追加
                    weather_cards.append(weather_card)

                except Exception as e:
                    print(f"Index error for day {i}: {e}")
                    continue

            # 天気カードの位置を整理
            # 上段3枚
            upper_row = ft.Row(
                controls=weather_cards[:3],  # 最初の3枚
                alignment=ft.MainAxisAlignment.CENTER,  # 横の中央揃え
                spacing=10  # カード間の距離
            )

            # 下段4枚
            lower_row = ft.Row(
                controls=weather_cards[3:],  # 残りの4枚
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )

            # 上下段を含むColumnを作成
            weather_display = ft.Column(
                controls=[upper_row, lower_row],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,  # 行間の距離
                horizontal_alignment=ft.CrossAxisAlignment.CENTER   # 縦の中央揃え
            )

            # UIの更新
            content_area.content = ft.Container(
                content=weather_display,
                padding=10, # カード内の余白
            )

            page.update()
        except Exception as e:
            print(f"Error getting weather: {e}")

    # サイドバーの作成
    areas_data = load_areas()   # 地域情報を取得
    nav_rail_items = []         # サイドバーのアイテムを格納するリスト

    # 地方ごとサイドバーに表示
    if "centers" in areas_data:
        # [地方コード:地方情報]の形式で取得
        for center_code, center_info in areas_data["centers"].items():
            prefecture_items = []
            
            if "children" in center_info:
                # 都道府県コードを取得
                for prefecture_code in center_info["children"]:
                    # "offices"がある場合は、都道府県情報を取得
                    # ない場合は空の辞書を返す
                    if prefecture_code in areas_data.get("offices", {}):
                        # 都道府県情報(コード以外の情報)を取得
                        prefecture_info = areas_data["offices"][prefecture_code]
                        # prefecture_itemsリストに追加
                        prefecture_items.append(
                            ft.Container(
                                content=ft.TextButton(
                                    text=prefecture_info["name"],   # 都道府県をボタンのテキストとして使用
                                    on_click=lambda e,  # ボタンがクリックされたときの処理
                                    code=prefecture_code: 
                                    update_weather(e, code),    # 天気情報を更新する関数を呼び出す
                                    # ボタンのスタイルを設定
                                    style=ft.ButtonStyle(
                                        color="white",
                                        padding=10, # ボタン内の余白
                                    )
                                ),
                                margin=ft.margin.only(left=20), # 左側の余白と字下げ効果を設定
                            )
                        )

            # サイドバーのアイテムを追加
            nav_rail_items.append(
                # クリックで展開するエリア
                ft.ExpansionTile(
                    # アイコンの設定
                    leading=ft.Icon(ft.icons.LOCATION_ON, color="white"),
                    # テキストの設定
                    title=ft.Text(
                        center_info["name"],
                        color="white",
                        size=16,
                    ),
                    bgcolor="#2B4F76",  # 青色の背景
                    controls=prefecture_items,
                )
            )

    # メインコンテンツエリア
    content_area = ft.Container(
        padding=20,
        expand=True,
    )

    # サイドバー全体のコンテナ
    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "天気予報",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="white"
                    ),
                    padding=20,
                    bgcolor="#2B4F76",  # ヘッダーの背景色
                ),
                *nav_rail_items     # 地方/都道府県のリスト( * を使用してリストをアンパック)
            ],
            scroll=ft.ScrollMode.AUTO,  # コンテンツが多い場合は自動的にスクロール可能にする
        ),
        # サイドバーのスタイル設定
        width=250,
        bgcolor="#2B4F76",  # サイドバーの背景色
        height=page.window.height,
    )

    # メインレイアウト
    # アプリのメインページにコンテンツを追加
    page.add(
        # サイドバーとコンテンツエリアを横に並べる
        ft.Row(
            [
                sidebar,    # サイドバー
                ft.VerticalDivider(width=1),    # 縦の区切り線
                content_area,   # メインコンテンツエリア
            ],
            expand=True,    # 横幅を最大にする(Rowを利用可能な空間いっぱいに広げる)
        )
    )

ft.app(target=main)