import re  # 正規表現

import keyboard  # キーボード
from package.error_log import ErrorLog  # エラーログに関するクラス
from package.fn import Fn  # 自作関数クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス


class GetKeyEventThread:
    """キーイベントの取得処理を行うスレッドクラス"""

    @staticmethod  # スタティックメソッドの定義
    @ErrorLog.decorator  # エラーログを取得するデコレータ
    def run(setting_target_key):
        """キーイベントの取得

        Args:
            setting_target_key (str): 設定変更対象のキー名
        """

        # ウィンドウオブジェクトの取得
        window = GlobalStatus.win_instance.window
        # 各キーの長押し状態を格納する辞書を初期化
        pressed_keys = {}
        # キーイベントの取得
        key_event = keyboard.read_event()

        while (
            (not window.was_closed())  # ウィンドウが閉じていない
            and window.metadata["is_key_input_waiting_state"]  # キー入力待ち状態なら
            # 設定変更対象のキー名が等しいなら
            and window.metadata["is_key_input_waiting_event"] == setting_target_key
        ):
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
                        # スレッドから、キーイベントを送信
                        window.write_event_value(key, value)

                elif event_type == keyboard.KEY_UP:
                    # イベントがキーの解放イベントである場合
                    # キーが押されているなら、長押し状態をリセットする
                    if scan_code in pressed_keys.keys():
                        pressed_keys.pop(scan_code, None)

            # キーイベントの取得
            key_event = keyboard.read_event()
