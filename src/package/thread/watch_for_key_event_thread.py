import keyboard  # キーボード
import re  # 正規表現

from package.fn import Fn  # 自作関数クラス
from package.error_log import ErrorLog  # エラーログに関するクラス


class WatchForKeyEventThread:
    """指定したキーイベントが発生するかどうか監視するスレッドクラス"""

    @staticmethod  # スタティックメソッドの定義
    # @ErrorLog.parameter_decorator(None)  # エラーログを取得するデコレータ
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

        # 各キーの長押し状態を格納する辞書を初期化
        pressed_keys = {}
        # キーイベントの取得
        key_event = keyboard.read_event()

        # キーイベント後に待機(処理軽減)
        Fn.sleep(50)

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
            Fn.sleep(50)
