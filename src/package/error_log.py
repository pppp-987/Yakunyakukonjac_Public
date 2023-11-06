import os  # オペレーティングシステム関連
import sys  # システム関連の機能を提供
import logging  # ログの機能を提供
import traceback  # 例外情報の取得と表示
import inspect  # 関数やクラスの情報を取得
import platform  # プラットフォーム情報の取得
import PySimpleGUI as sg  # GUI
import threading  # スレッド関連

from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


class ErrorLog:
    """エラーログに関するクラス"""

    def __init__(self):
        """コンストラクタ ロガーの設定を行う"""
        # 基本的な情報のみを出力するロガーの設定
        # ロギングモジュールから 'simple' という名前のロガーインスタンスを取得
        self.simple_logger = logging.getLogger("simple")

        # ロガーのログレベルを DEBUG に設定
        self.simple_logger.setLevel(logging.DEBUG)

        # 基本情報用のロガーの出力フォーマットを設定
        simple_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ログファイルパスの取得
        simple_log_file_path = SystemSetting.simple_error_log_file_path
        # 基本的なログ情報を出力するためのファイルハンドラを作成
        simple_file_handler = logging.FileHandler(simple_log_file_path, encoding="utf-8")

        # 基本情報用のファイルハンドラにフォーマッタをセット
        simple_file_handler.setFormatter(simple_formatter)

        # 'simple' ロガーにファイルハンドラを追加
        # このロガーがキャッチしたログは 'error.log' に書き込まれる
        self.simple_logger.addHandler(simple_file_handler)

        # 詳細な情報を出力するロガーの設定

        # ロギングモジュールから 'detailed' という名前のロガーインスタンスを取得
        self.detailed_logger = logging.getLogger("detailed")

        # ロガーのログレベルを DEBUG に設定
        self.detailed_logger.setLevel(logging.DEBUG)

        # 詳細情報用のロガーの出力フォーマットを設定
        detailed_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ログファイルパスの取得
        detailed_log_file_path = SystemSetting.detailed_error_log_file_path
        # ログを出力するためのファイルハンドラを作成
        detailed_file_handler = logging.FileHandler(detailed_log_file_path, encoding="utf-8")

        # 作成したファイルハンドラに上で定義したフォーマッタをセット
        detailed_file_handler.setFormatter(detailed_formatter)

        # 'detailed' ロガーにファイルハンドラを追加
        # これにより、このロガーがキャッチしたログは 'error_detailed.log' に書き込まれる
        self.detailed_logger.addHandler(detailed_file_handler)

    def self_output_error_log(self):
        """ログに出力する処理"""
        # 基本的な情報のみを出力
        self.simple_logger.exception("エラー発生")

        # 詳細情報

        # 環境情報をログに出力
        self.detailed_logger.error("Python version: %s", sys.version)
        self.detailed_logger.error("OS: %s", os.name)
        self.detailed_logger.error("Platform: %s", platform.platform())

        # 例外オブジェクトの属性や関連情報をログに出力
        exc_type, exc_value, exc_traceback = sys.exc_info()
        self.detailed_logger.error("Exception Type: %s", exc_type)
        self.detailed_logger.error("Exception Value: %s", exc_value)

        # トレースバックの詳細情報を文字列として取得
        tb_string = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_string = "".join(tb_string)
        self.detailed_logger.error("Traceback details:\n%s", tb_string)

        # inspectモジュールを使って現在のフレーム情報を取得
        current_frame = inspect.currentframe()

        # 一つ前のフレーム（例外が発生した位置）の情報を取得
        previous_frame = current_frame.f_back

        if previous_frame:
            # 前のフレームの局所変数を取得
            local_vars = previous_frame.f_locals
            for var_name, var_value in local_vars.items():
                self.detailed_logger.error("Variable [%s]: %s", var_name, var_value)

    @staticmethod  # スタティック(静的)メソッドの定義
    def create_error_log(window=None):
        """ErrorLogのインスタンス化を行う関数

        Args:
            window (sg.Window, None): ポップアップイベントを返すWindowオブジェクト
        """
        try:
            return ErrorLog()
        except Exception as e:
            print("Failed to create ErrorLog:", e)
            # エラー発生ポップアップの作成
            ErrorLog.error_popup(e, is_output_error_log=False, window=window)
            raise  # 例外を発生させる

    @staticmethod  # スタティック(静的)メソッドの定義
    def output_error_log(error_log_instance, e, window=None):
        """エラーログの出力を行う関数

        Args:
            error_log_instance (RrrorLog): エラーログに関するクラスのインスタンス
            e (Exception): 例外
            window (sg.Window, None): ポップアップイベントを返すWindowオブジェクト
        """
        try:
            error_log_instance.self_output_error_log()

            # エラー発生ポップアップの作成
            ErrorLog.error_popup(e, is_output_error_log=True, window=window)
        # エラーログの出力に失敗したなら
        except Exception as e:
            print("Failed to output ErrorLog:", e)
            # エラー発生ポップアップの作成
            ErrorLog.error_popup(e, is_output_error_log=False, window=window)
        raise  # 例外を発生させる

    @staticmethod  # スタティック(静的)メソッドの定義
    def error_popup(e, is_output_error_log, window=None):
        """エラー発生ポップアップの作成

        Args:
            e (Exception): 例外
            is_output_error_log(bool): エラーログの出力に成功したかどうか
            window (sg.Window, None): ポップアップイベントを返すWindowオブジェクト
        """
        # メッセージの作成
        # エラーログファイルの出力に成功したなら
        if is_output_error_log:
            message = [
                "申し訳ありません、エラーが発生しました。",
                f"エラーメッセージ: {str(e)}",
                "エラーログファイルが作成されました。",
                "管理者にこのファイルを提供していただけると幸いです。",
            ]
        # エラーログファイルの出力に失敗したなら
        else:
            message = [
                "申し訳ありません、エラーが発生しました。",
                f"エラーメッセージ: {str(e)}",
                "エラーログファイルの作成に失敗しました。",
                "管理者に問題を報告していただけると幸いです。",
            ]

        # ポップアップイベントを返すWindowオブジェクトが存在しないなら
        if window is None:
            # エラーポップアップの作成
            sg.popup("\n".join(message))
        else:
            print("ポップアップ表示")
            # スレッドから、キーイベントを送信
            window.write_event_value(key="-thread_error_event-", value=message)

    # @staticmethod  # スタティック(静的)メソッドの定義
    # def parameter_decorator(is_main_thread, event_window=None):  # デコレータの引数を取得する関数の宣言
    #     """デコレータの引数を取得する関数

    #     Args:
    #         is_main_thread (bool): メインスレッドかどうか
    #         window (sg.Window, None): ポップアップイベントを返すWindowオブジェクト
    #     """

    #     def decorator(func):  # デコレータ関数の宣言。
    #         """デコレータ関数。このデコレータを使用した関数は、'wrapper'関数に置き換えられる。

    #         Args:
    #             func (func): デコレートされる関数
    #         """

    #         def wrapper(*args, **kwargs):
    #             """デコレータの内部関数。任意の位置引数(*args)とキーワード引数(**kwargs)を受け取る。"""
    #             try:
    #                 # エラーログ作成
    #                 error_log = ErrorLog.create_error_log()
    #                 # 元の関数実行前の処理
    #                 func(*args, **kwargs)  # 元々のデコレートされる関数を実行
    #             # エラー発生時
    #             except Exception as e:
    #                 # エラーログの出力処理
    #                 ErrorLog.output_error_log(error_log, e, window)

    #         return wrapper  # デコレータの内部関数を返す。

    #     return decorator  # デコレータ関数を返す。

    @staticmethod  # スタティック(静的)メソッドの定義
    def decorator(func):  # デコレータ関数の宣言。
        """デコレータ関数。このデコレータを使用した関数は、'wrapper'関数に置き換えられる。

        Args:
            func (func): デコレートされる関数
        """

        def wrapper(*args, **kwargs):
            """デコレータの内部関数。任意の位置引数(*args)とキーワード引数(**kwargs)を受け取る。"""
            try:
                # 現在のスレッドがメインスレッドかどうか
                is_main_thread = threading.current_thread() == threading.main_thread()
                # 現在のスレッドがメインスレッドなら
                if is_main_thread:
                    # ポップアップイベントを返すWindowオブジェクト
                    window = None
                # 現在のスレッドがサブスレッドなら
                else:
                    # ポップアップイベントを返すWindowオブジェクトが指定されているなら
                    if "window" in kwargs:
                        window = kwargs["window"]
                    # ポップアップイベントを返すWindowオブジェクトが指定されていないなら
                    else:
                        window = None

                # エラーログ作成
                error_log = ErrorLog.create_error_log(window)
                # 元の関数実行前の処理
                func(*args, **kwargs)  # 元々のデコレートされる関数を実行
            # エラー発生時
            except Exception as e:
                # エラーログの出力処理
                ErrorLog.output_error_log(error_log, e, window)

        return wrapper  # デコレータの内部関数を返す。
