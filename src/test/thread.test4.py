import PySimpleGUI as sg
import time
import threading  # スレッド関連
import keyboard  # キーボード
import re  # 正規表現


# class Fn:
#     def search_dict_in_list(lst, key_name, value):
#         """与えられたリスト内の辞書から指定したキーと値に一致する辞書を取得

#         Args:
#             lst (list of dict): 検索対象の辞書要素が格納されたリスト
#             key_name (str): 検索に使用するキーの名前
#             value (任意の型) 検索する値

#         Returns:
#             dict: 一致する辞書（最初に見つかったもの）
#         """

#         for item in lst:  # リストから辞書を取り出す
#             if item[key_name] == value:
#                 # 辞書のキーと値が一致するなら一致する辞書を返す
#                 return item


class Thread_cls:
    # def get_key_event(window, setting_target_key):
    #     """キーイベントの取得

    #     Args:
    #         window(sg.Window): Windowオブジェクト
    #         setting_target_key (str): 設定変更対象のキー名
    #     """
    #     # 各キーの長押し状態を格納する辞書を初期化
    #     pressed_keys = {}
    #     # キーイベントの取得
    #     key_event = keyboard.read_event()

    #     while not (window.was_closed()) and window.metadata["is_key_input_waiting_state"]:
    #         # ウィンドウが閉じてないかつ、キー入力待ち状態なら
    #         event_type = key_event.event_type  # イベントタイプの取得
    #         key_name = key_event.name  # キー名の取得
    #         scan_code = key_event.scan_code  # スキャンコードの取得

    #         # キー名がASCII印字可能文字かどうか
    #         is_ascii_char_key = bool(re.match(r"^[!-~]$", key_name))
    #         # キー名がファンクションキーかどうか
    #         is_function_key = bool(re.match(r"^f([1-9]|1[0-2])$", key_name))

    #         # 押下されたキー名のチェック
    #         if is_ascii_char_key or is_function_key:
    #             # キーがASCII印字可能文字、ファンクションキーのどちらかなら
    #             if event_type == keyboard.KEY_DOWN:
    #                 # イベントがキーの押下イベントである場合
    #                 if scan_code not in pressed_keys:
    #                     # キーが長押しされていない場合

    #                     key = "-keyboard_event-"
    #                     value = {
    #                         "key_name": key_name,  # キー名
    #                         "scan_code": scan_code,  # スキャンコード
    #                         "setting_target_key": setting_target_key,  # 設定変更対象のキー名
    #                     }
    #                     print(pressed_keys)

    #                     # スレッドから、キーイベントを送信
    #                     window.write_event_value(key, value)

    #             elif event_type == keyboard.KEY_UP:
    #                 # イベントがキーの解放イベントである場合
    #                 # キーが離されたので、長押し状態をリセットする
    #                 pressed_keys.pop(scan_code, None)
    #                 print(pressed_keys)

    #         # キーイベントの取得
    #         key_event = keyboard.read_event()

    def watch_for_key_event(window, key_binding_info_list):
        """指定したキーイベントが発生するかどうか監視する処理

        Args:
            window(sg.Window): Windowオブジェクト
            key_binding_info_list (dict{key_name, scan_code, key_event}): キーボードイベントが発生するキー文字列
                - text(str) : 説明文
                - gui_key(str) : 識別子
                - key_name(str) : キー名
                - scan_code(int) : スキャンコード
        """
        # 各キーの長押し状態を格納する辞書を初期化
        pressed_keys = {}
        # キーイベントの取得
        key_event = keyboard.read_event()

        while not (window.was_closed()):
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

                        # キー長押し状態の保存
                        pressed_keys[scan_code] = key_name

                        # キーバインド設定情報の走査
                        for key_binding_info in key_binding_info_list:
                            # イベント発生処理
                            if (
                                # 現在押されているキー名とイベントが発生するキー名が一致するかどうか
                                key_binding_info["key_name"] in pressed_keys.values()
                                # 現在押されているキーのスキャンコードとイベントが発生するキーのスキャンコードが一致するかどうか
                                or key_binding_info["scan_code"] in pressed_keys.keys()
                            ):
                                # キー名かスキャンコードが一致するなら
                                # スレッドから、キーイベントを送信
                                window.write_event_value(
                                    key="-keyboard_event-",
                                    value=key_binding_info["gui_key"],  # 識別子
                                )

                elif event_type == keyboard.KEY_UP:
                    # イベントがキーの解放イベントである場合
                    # キーが押されているなら、長押し状態をリセットする
                    if scan_code in pressed_keys.keys():
                        pressed_keys.pop(scan_code)

            # キーイベントの取得
            key_event = keyboard.read_event()

            # キーイベント後に待機(処理軽減)
            time.sleep(0.05)


class Win1:
    def main():
        # キーバインド設定情報の辞書
        key_binding_info_list = [
            {"text": "キー設定1", "gui_key": "-key1-", "key_name": "f1", "scan_code": None},
            {"text": "キー設定2", "gui_key": "-key2-", "key_name": "A", "scan_code": 30},
            {"text": "キー設定3", "gui_key": "-key3-", "key_name": "f3", "scan_code": 61},
        ]

        layout = [
            [
                sg.Button(button_text="確定", size=(10, 1), key="-button1-"),
                sg.Button(button_text="戻る", size=(10, 1), key="-button2-"),
            ],
        ]

        window = sg.Window(
            "Window Title",
            layout,
            metadata={"is_key_input_waiting_state": False},  # キー入力待ち状態かどうか
        )

        # キーイベントを取得するスレッド作成
        thread = threading.Thread(
            # スレッド名
            name="キーイベント取得スレッド",
            # スレッドで実行するメソッド
            target=lambda: Thread_cls.watch_for_key_event(
                window,  # Windowオブジェクト
                key_binding_info_list,  # 設定変更対象のキー名
            ),
            daemon=True,  # メインスレッド終了時に終了する
        )
        # スレッド開始
        thread.start()

        while True:  # Event Loop
            event, values = window.read()

            print(event, values)
            if event == sg.WIN_CLOSED or event == "-button2-":
                break
            if event == "-button1-":
                print("確定")
                # キーイベントが発生したなら
            if "-keyboard_event-" in values:
                print(values["-keyboard_event-"])

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
