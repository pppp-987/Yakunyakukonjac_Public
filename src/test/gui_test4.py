import logging
import PySimpleGUI as sg
import sys
import traceback
import inspect
import os
import platform
import threading  # スレッド関連


class Thread1:
    def thread_run():
        print("a")
        a = 1 / 0
class Win:


    def main():
        layout = [[sg.Button("エラー1", key="-button1-")], [sg.Button("エラー2", key="-button2-")]]

        window = sg.Window("テスト", layout)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event == "-button1-":
                # スレッド作成
                thread = threading.Thread(
                    # スレッド名
                    name="自動翻訳タイミング取得スレッド",
                    # スレッドで実行するメソッド
                    target=lambda: Thread1.thread_run(),
                    daemon=True,  # メインスレッド終了時に終了する
                )
                # スレッド開始
                thread.start()
                # スレッド終了
                thread.join()

            elif event == "-button2-":
                l = [1, 2]
                a = l[3]

        window.close()


class Log:
    def get_logger():
        # 基本的な情報のみを出力するロガーの設定

        # ロギングモジュールから 'simple' という名前のロガーインスタンスを取得
        simple_logger = logging.getLogger("simple")

        # ロガーのログレベルを DEBUG に設定
        simple_logger.setLevel(logging.DEBUG)

        # 基本情報用のロガーの出力フォーマットを設定
        simple_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 'error.log' という名前のファイルに基本的なログ情報を出力するためのファイルハンドラを作成
        simple_file_handler = logging.FileHandler("error.log", encoding="utf-8")

        # 基本情報用のファイルハンドラにフォーマッタをセット
        simple_file_handler.setFormatter(simple_formatter)

        # 'simple' ロガーにファイルハンドラを追加
        # このロガーがキャッチしたログは 'error.log' に書き込まれる
        simple_logger.addHandler(simple_file_handler)

        # 詳細な情報を出力するロガーの設定

        # ロギングモジュールから 'detailed' という名前のロガーインスタンスを取得
        detailed_logger = logging.getLogger("detailed")

        # ロガーのログレベルを DEBUG に設定
        # これにより、DEBUG レベル以上のすべてのログメッセージがこのロガーによってキャッチされる
        detailed_logger.setLevel(logging.DEBUG)

        # ログメッセージの出力フォーマットを設定するためのフォーマッタを作成
        # ログのタイムスタンプ、ログレベル、そしてメッセージ自体を含む形式としている
        detailed_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 'error_detailed.log' という名前のファイルにログを出力するためのファイルハンドラを作成
        # このハンドラは utf-8 でエンコードされる
        detailed_file_handler = logging.FileHandler("error_detailed.log", encoding="utf-8")

        # 作成したファイルハンドラに上で定義したフォーマッタをセット
        detailed_file_handler.setFormatter(detailed_formatter)

        # 'detailed' ロガーにファイルハンドラを追加
        # これにより、このロガーがキャッチしたログは 'error_detailed.log' に書き込まれる
        detailed_logger.addHandler(detailed_file_handler)

        return simple_logger, detailed_logger

    def output_log(simple_logger, detailed_logger):
        # 基本的な情報のみを出力
        simple_logger.exception("エラー発生")

        # 詳細な情報を出力
        detailed_logger.exception("エラー発生")

        # 環境情報をログに出力
        detailed_logger.error("Python version: %s", sys.version)
        detailed_logger.error("OS: %s", os.name)
        detailed_logger.error("Platform: %s", platform.platform())

        # 例外オブジェクトの属性や関連情報をログに出力
        exc_type, exc_value, exc_traceback = sys.exc_info()
        detailed_logger.error("Exception Type: %s", exc_type)
        detailed_logger.error("Exception Value: %s", exc_value)

        # トレースバックの詳細情報を文字列として取得
        tb_string = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_string = "".join(tb_string)
        detailed_logger.error("Traceback details:\n%s", tb_string)

        # inspectモジュールを使って現在のフレーム情報を取得
        current_frame = inspect.currentframe()

        # 一つ前のフレーム（例外が発生した位置）の情報を取得
        previous_frame = current_frame.f_back

        if previous_frame:
            # 前のフレームの局所変数を取得
            local_vars = previous_frame.f_locals
            for var_name, var_value in local_vars.items():
                detailed_logger.error("Variable [%s]: %s", var_name, var_value)


class Main:
    def main():
        simple_logger, detailed_logger = Log.get_logger()
        try:
            # 処理内容、エラー内容不明
            Win.main()
        except Exception as e:
            Log.output_log(simple_logger, detailed_logger)


if __name__ == "__main__":
    Main.main()
