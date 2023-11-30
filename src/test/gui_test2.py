import PySimpleGUI as sg

# ウィンドウのレイアウトを定義
layout = [[sg.Text("ウィンドウが最大化されているか確認するためのテキスト。")], [sg.Button("確認")]]

# ウィンドウを作成
window = sg.Window("Window Title", layout, resizable=True)

# イベントループ
while True:
    event, values = window.read(timeout=500, timeout_key="timeout")
    if event == sg.WIN_CLOSED:
        break
    elif event == "確認" or event == "timeout":
        # ウィンドウの状態をチェック
        maximized = window.TKroot.state() == "zoomed"
        print(window.TKroot.state())

window.close()
