from package.error_log import ErrorLog  # エラーログに関するクラス
from package.fn import Fn  # 自作関数クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス


class TranslateTimingThread:
    """自動翻訳のタイミングを取得するスレッドクラス"""

    @staticmethod  # スタティックメソッドの定義
    @ErrorLog.decorator  # エラーログを取得するデコレータ
    def run(user_setting, window):
        """自動翻訳のタイミングを取得
        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            window(sg.Window): Windowオブジェクト
        """

        # ウィンドウオブジェクトの取得
        window = GlobalStatus.win_instance.window

        # トグルボタンがオンに切り替わった回数の取得
        toggle_on_count = window["-toggle_auto_translation-"].metadata["toggle_on_count"]

        # 翻訳間隔(秒)の取得
        translation_interval_sec = user_setting.get_setting("translation_interval_sec")

        while (
            # ウィンドウが閉じているかどうか
            not (window.was_closed())
            # 自動翻訳トグルボタンがオンかどうか
            and window["-toggle_auto_translation-"].metadata["is_toggle_on"]
            # 自動翻訳トグルボタンが押されていないかどうか
            and toggle_on_count == window["-toggle_auto_translation-"].metadata["toggle_on_count"]
        ):
            # ウィンドウが開いてあるかつ、自動翻訳トグルボタンがオンなら
            # スレッドから、翻訳イベントを送信
            key = "-translate_thread_start-"
            value = None
            window.write_event_value(key, value)

            # 翻訳間隔の秒数だけ繰り返す
            for _ in range(translation_interval_sec):
                Fn.sleep(1000)
                if (  # ウィンドウが閉じているかどうか
                    window.was_closed()
                    # 自動翻訳トグルボタンがオンかどうか
                    or not (window["-toggle_auto_translation-"].metadata["is_toggle_on"])
                ):
                    # ウィンドウが閉じている、または、自動翻訳トグルボタンがオフなら
                    break

            # 待機時間の間、ウィンドウが開いてあるかつ、自動翻訳トグルボタンがオンなら
            else:
                # 次のループに進む
                continue

            # ウィンドウが閉じている、または、自動翻訳トグルボタンがオフならスレッドを終了させる
            break
