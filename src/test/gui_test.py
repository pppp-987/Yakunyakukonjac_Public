import PySimpleGUI as sg

window_theme = "DarkBlue3"
# ウィンドウテーマの設定
sg.theme(window_theme)
# 1. レイアウト
layout = [
    [
        # テーマ一覧リストボックス
        sg.Listbox(
            values=sg.theme_list(),  # テーマ一覧
            size=(20, 12),  # サイズ
            key="-theme_list-",  # 識別子
            enable_events=True,  # イベントを取得する
        )
    ],
    [
        sg.Button("確定", size=(30, 3), key="BUTTON"),
    ],
]

# 2. ウィンドウの生成
window = sg.Window(
    title="Window title",
    layout=layout,
    grab_anywhere=True,
    return_keyboard_events=True,
    keep_on_top=True,
)
# 3. GUI処理
while True:
    event, values = window.read()
    # print(event, values)
    if event is None:
        break
    if event == "BUTTON":
        print(sg.theme())
    if event == "-theme_list-":
        sg.theme(values["-theme_list-"][0])
        print(values["-theme_list-"][0])
        # 画面更新
        window.refresh()

window.close()
