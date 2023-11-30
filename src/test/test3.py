import PySimpleGUI as sg

# ウィンドウのレイアウトを設定
layout = [
    [sg.Text("リサイズイベントをテストする"), sg.Button("OK")],
    [sg.pin(sg.Text("", size=(1, 1), key="-RESIZE-"))],  # リサイズイベントをトリガーするためのピン留めされたText要素
]

# ウィンドウを作成し、リサイズ可能に設定
window = sg.Window("ウィンドウリサイズイベントテスト", layout, resizable=True, finalize=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "OK":
        break
    elif event == "-RESIZE-":  # ピン留めされた要素が生成するイベント
        print("ウィンドウがリサイズされました。")

window.close()
