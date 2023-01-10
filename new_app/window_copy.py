import PySimpleGUI as sg


ウィンドウのテーマ
sg.theme('DarkRed')
# filename='new_app/test1.png'
# ウィンドウのレイアウト
layout = [
    [sg.Image(filename='new_app/test1.png')]
]

# ウィンドウオブジェクトの作成
window = sg.Window('title', layout, size=(1600, 1500))

# イベントのループ
while True:
    # イベントの読み込み
    event, values = window.read()
    # ウィンドウの×ボタンクリックで終了
    if event == sg.WIN_CLOSED:
        break

# ウィンドウ終了処理
window.close()