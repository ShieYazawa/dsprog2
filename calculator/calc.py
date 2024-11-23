import flet as ft

# カスタムボタンクラス
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()  # 基本的な機能を初期化
        self.text = text    # ボタンのテキストを指定する変数(数字や演算子)
        self.expand = expand    # ボタンの幅を指定する変数
        self.on_click = button_clicked  # ボタンがクリックされたときに実行される関数
        self.data = text

# 数字ボタン用クラス
# 見た目をカスタマイズ
class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        # 親クラスの呼び出し
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24    # ボタンの背景色を指定
        self.color = ft.colors.WHITE        # ボタンの文字色を指定

# 演算子ボタン用クラス
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE   
        self.color = ft.colors.WHITE      

# 特殊ボタン用クラス
class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK

# アプリケーションクラス
# 全体的なレイアウト(見た目)を設定
class CalculatorApp(ft.Container):
    # 親クラス(ft.Container)の初期化
    def __init__(self):
        super().__init__()
        # reset()メソッドの初期化
        self.reset()

        # 計算結果を表示するテキスト
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)

        # アプリケーションの基本的な設定
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)   # 角丸の設定
        self.padding = 20   # 内側の余白の設定

        # 横に配置するボタンのリスト
        # 各行(Row)は縦に配置
        # Columnは下に重ねていくイメージ
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),    # 計算結果を右寄せで表示
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked  
                        ),  # 0ボタンは幅2倍
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    # ボタンがクリックされた時に実行される関数
    def button_clicked(self, e):
        data = e.control.data
        # デバック用のprint文
        # data=ボタンのtext
        print(f"Button clicked with data = {data}")
        # "Error"か"AC"が押された場合は計算結果を0にリセット
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        # 数値または小数点が入力された場合
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            # 表示が0または新しい入力開始時は入力値で置き換え
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            # それ以外は既存の値に追加
            else:
                self.result.value = self.result.value + data

        # 四則演算子が入力された場合
        elif data in ("+", "-", "*", "/"):
            # calculate関数を呼び出す
            # 現在の値・保存値・演算子を引数として渡す
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data    # 押されたボタン(data)を次回の演算に使う演算子として設定
            # エラーが発生した場合は0にリセット
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)    # 表示されている値は浮動小数点数に変換
            # 次の数値入力の準備
            self.new_operand = True

        # "="が押されたとき
        elif data in ("="):
            # 計算を実行
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()    # 状態をリセット

        # "%"が押されたとき
        elif data in ("%"):
            self.result.value = float(self.result.value) / 100  # 現在の値を100で割る
            self.reset()

        # "+/-"が押されたとき
        elif data in ("+/-"):
            # 正の数は負の数に、負の数は正の数に変換
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )   # abs：絶対値を取得
                    # str：文字列に変換

        self.update()   # 表示画面を更新

    # 数値のフォーマットを整えて見やすくする関数
    def format_number(self, num):
        # 小数点以下が0の場合は整数に変換
        if num % 1 == 0:
            return int(num)
        # 小数点以下が0でない場合はそのまま表示
        else:
            return num

    # 計算を実行する関数(各演算子の計算処理を設定)
    def calculate(self, operand1, operand2, operator):

        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "*":
            return self.format_number(operand1 * operand2)

        elif operator == "/":
            if operand2 == 0:
                return "Error"  # 割る数が0のときはエラーを返す
            else:
                return self.format_number(operand1 / operand2)

    # 初期設定
    def reset(self):
        self.operator = "+" # 演算子の初期値
        self.operand1 = 0   # 最初の数値の初期値
        self.new_operand = True # 数値入力開始のフラグ

# メイン関数
# メイン関数とは、プログラムが実行されると最初に呼び出される関数
def main(page: ft.Page):
    # タイトルの設定
    page.title = "Calc App"
    # アプリケーションのインスタンスを作成
    calc = CalculatorApp()

    # アプリケーションをページ(表示領域)に追加
    page.add(calc)

# アプリケーションを起動
ft.app(target=main)
