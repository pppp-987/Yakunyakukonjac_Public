import PySimpleGUI as sg
import time
import threading  # スレッド関連
import keyboard  # キーボード
import re  # 正規表現


class Fn:
    def search_dict_in_list(lst, key_name, value):
        """与えられたリスト内の辞書から指定したキーと値に一致する辞書を取得

        Args:
            lst (list of dict): 検索対象の辞書要素が格納されたリスト
            key_name (str): 検索に使用するキーの名前
            value (任意の型) 検索する値

        Returns:
            dict: 一致する辞書（最初に見つかったもの）
        """

        for item in lst:  # リストから辞書を取り出す
            if item[key_name] == value:
                # 辞書のキーと値が一致するなら一致する辞書を返す
                return item


class Thread_cls:
    def get_key_event(window, setting_target_key):
        """キーイベントの取得

        Args:
            window(sg.Window): Windowオブジェクト
            setting_target_key (str): 設定変更対象のキー名
        """
        # 各キーの長押し状態を格納する辞書を初期化
        pressed_keys = {}
        # キーイベントの取得
        key_event = keyboard.read_event()

        while not (window.was_closed()) and window.metadata["is_key_input_waiting_state"]:
            # ウィンドウが閉じてないかつ、キー入力待ち状態なら
            event_type = key_event.event_type  # イベントタイプの取得
            key_name = key_event.name  # キー名の取得
            scan_code = key_event.scan_code  # スキャンコードの取得

            # キー名がASCII印字可能文字かどうか
            is_ascii_char_key = bool(re.match(r"^[!-~]$", key_name))
            # キー名がファンクションキーかどうか
            is_function_key = bool(re.match(r"^f([1-9]|1[0-2])$", key_name))

            # 押下されたキー名のチェック
            if is_ascii_char_key or is_function_key:
                # キーがASCII印字可能文字、ファンクションキーのどちらかなら
                if event_type == keyboard.KEY_DOWN:
                    # イベントがキーの押下イベントである場合
                    if scan_code not in pressed_keys:
                        # キーが長押しされていない場合

                        key = "-keyboard_event-"
                        value = {
                            "key_name": key_name,  # キー名
                            "scan_code": scan_code,  # スキャンコード
                            "setting_target_key": setting_target_key,  # 設定変更対象のキー名
                        }
                        print(pressed_keys)
                        # スレッドから、キーイベントを送信
                        window.write_event_value(key, value)

                elif event_type == keyboard.KEY_UP:
                    # イベントがキーの解放イベントである場合
                    # キーが離されたので、長押し状態をリセットする
                    pressed_keys.pop(scan_code, None)
                    print(pressed_keys)

            # キーイベントの取得
            key_event = keyboard.read_event()

    def run(window, setting_target_key):
        """キーイベントの取得

        Args:
            window(sg.Window): Windowオブジェクト
            setting_target_key (str): 設定変更対象のキー名
        """
        # 各キーの長押し状態を格納する辞書を初期化
        pressed_keys = {}
        # キーイベントの取得
        key_event = keyboard.read_event()
        while not (window.was_closed()):
            # ウィンドウが閉じてないなら
            event_type = key_event.event_type  # イベントタイプの取得
            key_name = key_event.name  # キー名の取得
            scan_code = key_event.scan_code  # スキャンコードの取得
            if event_type == keyboard.KEY_DOWN:
                # イベントがキーの押下イベントである場合
                if scan_code not in pressed_keys:
                    # キーが長押しされていない場合
                    # キー名がASCII印字可能文字かどうか
                    is_ascii_char_key = bool(re.match(r"^[!-~]$", key_name))
                    # キー名がファンクションキーかどうか
                    is_function_key = bool(re.match(r"^f([1-9]|1[0-2])$", key_name))

                    # 押下されたキー名のチェック
                    if is_ascii_char_key or is_function_key:
                        # キーがASCII印字可能文字、ファンクションキーのどちらかなら
                        key = "-keyboard_event-"
                        value = {
                            "key_name": key_name,  # キー名
                            "scan_code": scan_code,  # スキャンコード
                            "setting_target_key": setting_target_key,  # 設定変更対象のキー名
                        }
                        # スレッドから、キーイベントを送信
                        window.write_event_value(key, value)
                        break

                elif event_type == keyboard.KEY_UP:
                    # イベントがキーの解放イベントである場合
                    # キーが離されたので、長押し状態をリセットする
                    pressed_keys.pop(scan_code, None)

            # キーイベントの取得
            key_event = keyboard.read_event()


class Win1:
    def main():
        # キーバインド設定情報の辞書
        key_binding_info_list = [
            {"text": "翻訳キー設定", "gui_key": "-key1-", "key_name": "f1", "scan_code": 59},
            {"text": "撮影キー設定", "gui_key": "-key2-", "key_name": "f2", "scan_code": 60},
        ]
        # キーバインド設定のレイアウト
        key_binding_layout = []
        # キーバインド設定情報の走査
        for key_binding_info in key_binding_info_list:
            key_binding_layout.append(
                [
                    sg.Text(
                        key_binding_info["text"],
                    ),
                    sg.Button(
                        button_text=key_binding_info["key_name"],
                        size=(20, 1),
                        key=key_binding_info["gui_key"],
                    ),
                ]
            )
        layout = key_binding_layout

        # キーバインド設定のイベントのリスト
        key_binding_event_list = [
            key_binding_info["gui_key"] for key_binding_info in key_binding_info_list
        ]

        # layout = [
        #     [
        #         sg.Text(
        #             "翻訳キー設定",
        #         ),
        #         sg.Button(button_text="f1", size=(10, 1), key="-key_text1-"),
        #     ],
        #     [
        #         sg.Text(
        #             "撮影キー設定",
        #         ),
        #         sg.Button(button_text="f2", size=(10, 1), key="-key_text2-"),
        #     ],
        # ]

        window = sg.Window(
            "Window Title",
            layout,
            metadata={"is_key_input_waiting_state": False},  # キー入力待ち状態かどうか
        )

        while True:  # Event Loop
            event, values = window.read()

            print(event, values)
            if event == sg.WIN_CLOSED:
                break

            # キー入力待ち状態でないなら
            if not window.metadata["is_key_input_waiting_state"]:
                # キー設定ボタン押下イベント
                if event in key_binding_event_list:
                    # 設定変更対象のキー名
                    setting_target_key = event
                    # キー設定ボタンテキスト変更
                    window[event].update(text="キーを入力")
                    # キー入力待ち状態かどうか
                    window.metadata["is_key_input_waiting_state"] = True
                    # キーイベントを取得するスレッド作成
                    thread = threading.Thread(
                        # スレッドで実行するメソッド
                        target=lambda: Thread_cls.get_key_event(
                            window,  # Windowオブジェクト
                            setting_target_key,  # 設定変更対象のキー名
                        ),
                        daemon=True,  # メインスレッド終了時に終了する
                    )
                    # スレッド開始
                    thread.start()

            # キー入力待ち状態なら
            else:
                # キー押下イベント
                if event == "-keyboard_event-":
                    # 設定変更対象のキー名
                    setting_target_key = values["-keyboard_event-"]["setting_target_key"]
                    key_name = values["-keyboard_event-"]["key_name"]  # 押下されたキー名
                    scan_code = values["-keyboard_event-"]["scan_code"]  # 押下されたスキャンコード

                    # スキャンコード重複チェック処理
                    # 他のキーバインド設定のスキャンコードリスト作成
                    key_binding_scan_code_list = []
                    # キーバインド設定の走査
                    for key_binding_info in key_binding_info_list:
                        # 設定を変更するキー以外なら
                        if key_binding_info["gui_key"] != setting_target_key:
                            key_binding_scan_code_list.append(key_binding_info["scan_code"])
                    # スキャンコードが他と重複していないなら
                    if scan_code not in key_binding_scan_code_list:
                        # キー入力待ち状態かどうか
                        window.metadata["is_key_input_waiting_state"] = False
                        # キー設定ボタンのテキスト更新
                        window[setting_target_key].update(text=key_name)

                        # 変更前のキーバインド設定の取得
                        old_key_binding_info = Fn.search_dict_in_list(
                            key_binding_info_list, "gui_key", setting_target_key
                        )

                        # 更新するキーバインド設定の作成
                        new_key_binding_info = old_key_binding_info
                        new_key_binding_info["key_name"] = key_name
                        new_key_binding_info["scan_code"] = scan_code

                        # キーバインド設定リストの更新箇所の要素番号の取得
                        update_index = key_binding_info_list.index(old_key_binding_info)

                        # キーバインド設定リストの更新
                        key_binding_info_list[update_index] = new_key_binding_info
                        print(key_binding_info_list)

        window.close()


class Win2:
    def main():
        layout = [
            [sg.Text("test")],
        ]

        window = sg.Window("Window2", layout)

        while True:  # Event Loop
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break


if __name__ == "__main__":
    Win1.main()
    Win2.main()
