import re  # 正規表現

import keyboard  # キーボード
from package.error_log import ErrorLog  # エラーログに関するクラス
from package.fn import Fn  # 自作関数クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス


class WatchForKeyEventThread:
    """指定したキーイベントが発生するかどうか監視するスレッドクラス"""

    @staticmethod  # スタティックメソッドの定義
    @ErrorLog.decorator  # エラーログを取得するデコレータ
    def run(window, key_binding_info_list):
        """指定したキーイベントが発生するかどうか監視する処理

        Args:
            window(sg.Window): Windowオブジェクト
            key_binding_info_list (dict{key_name, scan_code, key_event}): キーボードイベントが発生するキー文字列
                - text(str) : 説明文
                - gui_key(str) : 識別子
                - key_name(str) : キー名
                - scan_code(int) : スキャンコード
        """

        # ウィンドウオブジェクトの取得
        window = GlobalStatus.win_instance.window

        # 各キーの長押し状態を格納する辞書を初期化
        pressed_keys = {}

        # キーイベントの取得
        key_event = keyboard.read_event()

        # ウィンドウが閉じてないなら
        while not (window.was_closed()):
            event_type = key_event.event_type  # イベントタイプの取得
            key_name = key_event.name  # キー名の取得
            scan_code = key_event.scan_code  # スキャンコードの取得
            # キー名がASCII印字可能文字かどうか
            is_ascii_char_key = bool(re.match(r"^[!-~]$", key_name))
            # キー名がファンクションキーかどうか
            is_function_key = bool(re.match(r"^f([1-9]|1[0-2])$", key_name))

            # キーがASCII印字可能文字、ファンクションキーのどちらかなら
            if is_ascii_char_key or is_function_key:
                # イベントがキーの押下イベントである場合
                if event_type == keyboard.KEY_DOWN:
                    if scan_code not in pressed_keys:
                        # キーが長押しされていない場合

                        # キー長押し状態の保存
                        pressed_keys[scan_code] = key_name

                        # メインスレッドが実行中なら
                        if GlobalStatus.is_main_thread_running:
                            # キーバインド設定情報の走査
                            for key_binding_info in key_binding_info_list:
                                # キー名かスキャンコードが一致するかつ、押されているキーの数が1つだけなら
                                if (
                                    # 現在押されているキー名とイベントが発生するキー名が一致するかどうか
                                    (
                                        key_binding_info["key_name"] in pressed_keys.values()
                                        # 現在押されているキーのスキャンコードとイベントが発生するキーのスキャンコードが一致するかどうか
                                        or key_binding_info["scan_code"] in pressed_keys.keys()
                                    )
                                    # 押されているキーの数が1つだけなら
                                    and len(pressed_keys) == 1
                                ):
                                    # スレッドから、キーイベントを送信
                                    window.write_event_value(
                                        key="-keyboard_event-",
                                        value=key_binding_info["gui_key"],  # 識別子
                                    )

                # イベントがキーの解放イベントである場合
                elif event_type == keyboard.KEY_UP:
                    # キーが押されているなら、長押し状態をリセットする
                    if scan_code in pressed_keys.keys():
                        pressed_keys.pop(scan_code)

            # キーイベントの取得
            key_event = keyboard.read_event()
