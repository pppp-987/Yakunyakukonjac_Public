import PySimpleGUI as sg


def create_window(theme):
    sg.theme(theme)
    layout = [
        [
            sg.Listbox(
                values=sg.theme_list(),
                size=(20, 12),
                key="-theme_list-",
                enable_events=True,
                default_values=["DarkBlue3"],
            )
        ],
        [
            sg.Button("確定", key="BUTTON"),
        ],
    ]

    return sg.Window(
        title="Window title",
        layout=layout,
        finalize=True,  # 入力待ち までの間にウィンドウを表示する
        return_keyboard_events=True,
        keep_on_top=True,
    )


# 変更前のテーマの保存
current_theme = "DarkBlue3"

# ウィンドウの作成
window = create_window(current_theme)


# テーマ選択リストボックスの最初に表示される要素番号の取得
theme_list_index = sg.theme_list().index(current_theme)
# テーマ選択リストボックスの更新
window["-theme_list-"].update(
    set_to_index=theme_list_index, # 値の設定
    scroll_to_index=theme_list_index - 3,  # 最初に表示される要素番号の取得
)

while True:
    event, values = window.read()

    if event is None:
        break
    if event == "BUTTON":
        print(sg.theme())
    if event == "-theme_list-":
        # テーマの取得
        new_theme = values["-theme_list-"][0]
        # テーマが変更されているなら
        if new_theme != current_theme:
            # ウィンドウを閉じる
            window.close()
            # ウィンドウを再度開く
            window = create_window(new_theme)
            # テーマの保存
            current_theme = new_theme

            # テーマ選択リストボックスの要素番号取得
            theme_list_index = sg.theme_list().index(new_theme)
            print(theme_list_index)
            # テーマ選択リストボックスの最初に表示される要素番号の取得
            theme_list_index = sg.theme_list().index(current_theme)
            # テーマ選択リストボックスの更新
            window["-theme_list-"].update(
                set_to_index=theme_list_index, # 値の設定
                scroll_to_index=theme_list_index - 3,  # 最初に表示される要素番号の取得
            )

window.close()
