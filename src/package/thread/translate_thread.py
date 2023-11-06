import os  # ディレクトリ関連

from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.translation.translation import Translation  # 翻訳機能関連のクラス

from package.error_log import ErrorLog  # エラーログに関するクラス


class TranslateThread:
    """翻訳処理を行うスレッドクラス"""

    @staticmethod  # スタティックメソッドの定義
    # @ErrorLog.parameter_decorator(None)  # エラーログを取得するデコレータ
    @ErrorLog.decorator  # エラーログを取得するデコレータ
    def run(window):
        """翻訳処理
        Args:
            window(sg.Window): Windowオブジェクト
                - デコレータで使用するためキーワード引数で渡す
        """
        # 翻訳処理
        file_name = Translation.save_history()
        # ウィンドウが開いてあるかつ、自動翻訳トグルボタンがオンなら

        if not (window.was_closed()):
            # ウィンドウが開いているなら
            key = "-translate_thread_end-"
            value = file_name
            # スレッドから、翻訳イベントを送信
            window.write_event_value(key, value)
        else:
            # ウィンドウが閉じてあるなら
            for dir_path in [
                SystemSetting.image_before_directory_path,  # 翻訳前履歴画像フォルダパス
                SystemSetting.image_after_directory_path,  # 翻訳後履歴画像フォルダパス
            ]:
                # ファイルパス
                file_path = dir_path + file_name
                # ファイルが存在するかチェック
                if os.path.exists(file_path):
                    # ファイルを削除
                    os.remove(file_path)
                else:
                    print(f"{file_path} は存在しません。")
