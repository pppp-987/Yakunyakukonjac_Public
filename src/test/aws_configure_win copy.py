import sys  # システム関連
import os  # ディレクトリ関連
import threading  # スレッドベースの並行処理を実装するためのモジュール
import subprocess  # 新しいプロセスを生成し、その入出力を管制するためのモジュール

import PySimpleGUI as sg  # GUI

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

import PySimpleGUI as sg  # GUI

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス
from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス
from package.error_log import ErrorLog  # エラーログに関するクラス


class AwsConfigureWin(BaseWin):
    """AWS設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
        # AWSの設定ファイルのパスの設定
        os.environ["AWS_CONFIG_FILE"] = SystemSetting.aws_config_file_path
        # AWSの認証情報ファイルのパスの設定
        os.environ["AWS_SHARED_CREDENTIALS_FILE"] = SystemSetting.aws_credentials_file_path
        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.user_setting.get_setting("window_theme"))
        # レイアウト指定
        layout = [
            [
                sg.Text(
                    text="コンソールからAWSの設定を行ってください。\n中断する場合、コンソール上でCtrl + Zを押してください。",
                    key="-text-",
                )
            ],
        ]
        return layout  # レイアウト

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

        # AWS設定を行うスレッド
        aws_configure_thread = threading.Thread(
            # スレッド名
            name="AWS設定スレッド",
            # スレッドで実行するメソッド
            # AWSサービスにアクセス可能か確認する処理
            target=lambda: AwsConfigureWin.aws_configure_thread(),
            daemon=True,  # メインスレッド終了時に終了する
        )

        # AWS設定を行うスレッドの開始
        aws_configure_thread.start()

        # 終了処理が行われるまで繰り返す
        while not self.window.metadata["is_exit"]:
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            # 共通イベントの処理が発生したら
            if self.base_event(event, values):
                continue

            # AWS設定を行うスレッドが終了したなら
            elif event == "-aws_configure_thread_end-":
                # AWS設定スレッドが終了した時の処理
                self.aws_configure_thread_end_event(
                    is_successful=values["-aws_configure_thread_end-"],  # AWSの設定の変更中に中断されてないかどう
                )

    def aws_configure_thread_end_event(self, is_successful):
        """AWS設定スレッドが終了した時の処理

        Args:
            is_successful (bool): AWSの設定の変更中に中断されてないかどうか
            check_access_aws_thread (threading.Thread) AWS接続テストを行うスレッド
        """
        # 終了コードをチェック
        # 中断されなかったなら
        if is_successful:
            # 表示メッセージの設定
            sg.popup("AWS設定の変更は正常に終了しました。\n設定の適用には再起動が必要です。")

        # 中断されたなら(ctrl + z, ctrl + cが押されたなら)
        else:
            # ポップアップの表示
            sg.popup("AWSの設定変更は中断されました。")

        self.transition_target_win = "EnvironmentSettingWin"  # 遷移先ウィンドウ名
        self.window_close()  # プログラム終了イベント処理

    @staticmethod  # スタティック(静的)メソッド
    @ErrorLog.decorator  # エラーログを取得するデコレータ
    def aws_configure_thread():
        """AWS設定を行うスレッド"""
        # awsの設定を行うバッチファイルの実行
        result = subprocess.run(
            args=[SystemSetting.tool_aws_config_path],  # コマンドリスト
            creationflags=subprocess.CREATE_NEW_CONSOLE,  # 新しいコンソールウィンドウを作成する
        )

        # 環境変数の更新
        # AWSの設定ファイルのパスの設定
        os.environ["AWS_CONFIG_FILE"] = SystemSetting.aws_config_file_path
        # AWSの認証情報ファイルのパスの設定
        os.environ["AWS_SHARED_CREDENTIALS_FILE"] = SystemSetting.aws_credentials_file_path

        # 中断されてないかどうか
        is_successful = result.returncode == 0

        # 現在開いているウィンドウクラスのインスタンスでウィンドウオブジェクトが作成されているかどうか
        if hasattr(GlobalStatus.win_instance, "window"):
            # ウィンドウオブジェクトの取得
            window = GlobalStatus.win_instance.window
            # ウィンドウが閉じられていないなら
            if not window.was_closed():
                # スレッドから、キーイベントを送信
                window.write_event_value(key="-aws_configure_thread_end-", value=is_successful)


# ! デバッグ用
if __name__ == "__main__":
    win_instance = AwsConfigureWin()
