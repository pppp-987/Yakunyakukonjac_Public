from package.fn import Fn  # 自作関数クラス
from package.error_log import ErrorLog  # エラーログに関するクラス


class TranslateTimingThread:
    """自動翻訳のタイミングを取得するスレッドクラス"""

    @staticmethod  # スタティックメソッドの定義
    # @ErrorLog.parameter_decorator(None)  # エラーログを取得するデコレータ
    @ErrorLog.decorator  # エラーログを取得するデコレータ
    def run(user_setting, window):
        """自動翻訳のタイミングを取得
        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            window(sg.Window): Windowオブジェクト
                - デコレータで使用するためキーワード引数で渡す
        """
        # 翻訳間隔(秒)の取得
        translation_interval_sec = user_setting.get_setting("translation_interval_sec")

        while (
            # ウィンドウが閉じているかどうか
            not (window.was_closed())
            # 自動翻訳トグルボタンがオンかどうか
            and window["-toggle_auto_translation-"].metadata["is_toggle_on"]
        ):
            # ウィンドウが開いてあるかつ、自動翻訳トグルボタンがオンなら
            # スレッドから、翻訳イベントを送信
            key = "-translate_thread_start-"
            value = None
            window.write_event_value(key, value)

            # 一時停止
            Fn.sleep(translation_interval_sec * 1000)
