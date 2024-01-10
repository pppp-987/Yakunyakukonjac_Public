import PySimpleGUI as sg

# 1. レイアウト
layout = [
    [
        sg.Button("押してね", size=(30, 3), key="BUTTON"),
    ],
    [
        # 松竹梅から選択する。初期値'梅'
        sg.Spin(["松", "竹", "梅"], "梅", readonly=False, key="SPIN_1"),
        # range()の返り値をそのまま渡すとバグるのでリストに変換しておく
        sg.Spin(list(range(100)), 0, readonly=False, key="SPIN_2"),
    ],
    [
        # 松竹梅から選択する。初期値'梅'
        sg.Combo(["松", "竹", "梅"], "梅", readonly=True, key="COMBO")
    ],
    [sg.Listbox(["松", "竹", "梅"], size=(15, 3), key="-list-")],
    [
        sg.Radio("松", "group_1", True, key="RADIO_MATSU"),
        sg.Radio("竹", "group_1", False, key="RADIO_TAKE"),
        sg.Radio("梅", "group_1", False, key="RADIO_UME"),
    ],
]

# 2. ウィンドウの生成
window = sg.Window(
    title="Window title",
    layout=layout,
    grab_anywhere=True,
    #  Trueの場合、キーボードのキー操作がRead呼び出しからイベントとして返されます
    return_keyboard_events=True,
    icon="C:\\Users\\student\\Documents\\venv_YakunyakuKonjac\\Yakunyakukonjac\\static\\icon\\app.ico",
    # no_titlebar=True,
    # disable_close=True,
    # Trueの場合、ウィンドウは画面上のすべての他のウィンドウの上に作成されます。このパラメータを使用して別のパラメータで作成されたウィンドウが下に押しやられる可能性があります
    # keep_on_top=True,
    # use_custom_titlebar=True,
    # Trueの場合、ウィンドウは「X」をクリックして閉じられません。代わりに、window.readからWINDOW_CLOSE_ATTEMPTED_EVENTが返されます
    # enable_close_attempted_event = True
)
window.finalize()

# 3. GUI処理
while True:
    event, values = window.read(timeout=None)
    print(event, values)
    if event is None:
        break

window.close()
