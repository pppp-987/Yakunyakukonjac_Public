import os  # ディレクトリ関連
import sys  # システム関連
import threading  # スレッドベースの並行処理を実装するためのモジュール

import PySimpleGUI as sg  # GUI

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

import PySimpleGUI as sg  # GUI
from package.error_log import ErrorLog  # エラーログに関するクラス
from package.fn import Fn  # 自作関数クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス
from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class CheckAccessAwsWin(BaseWin):
    """AWS接続テスト画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
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
                    text="AWS接続テスト中   ",
                    key="-text-",
                    metadata={
                        "message": "AWS接続テスト中",  # 表示メッセージ
                        "progress_indicator_dot_count": 0,  # 進捗インジケーターの点の数
                    },
                )
            ],
        ]
        return layout  # レイアウト

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

        # AWS接続テストを行うスレッド
        check_access_aws_thread = threading.Thread(
            # スレッド名
            name="AWS接続テストスレッド",
            # スレッドで実行するメソッド
            # AWSサービスにアクセス可能か確認する処理
            target=lambda: self.user_setting.check_access_aws_service(
                is_show_success_message=True,  # アクセス成功時にメッセージを表示するかどうか
            ),
            daemon=True,  # メインスレッド終了時に終了する
        )

        # AWS接続テストを行うスレッドの開始
        check_access_aws_thread.start()

        # 終了処理が行われるまで繰り返す
        while not self.window.metadata["is_exit"]:
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read(
                timeout=500,  # タイムアウトする間隔(ms)
                timeout_key="-timeout-",  # タイムアウトイベント名
            )

            # 共通イベントの処理が発生したら
            if self.base_event(event, values):
                continue

            # AWS接続テストを行うスレッドが終了したら
            elif event == "-check_access_aws_thread_end-":
                # ポップアップの表示
                sg.popup("\n".join(values["-check_access_aws_thread_end-"]))
                self.transition_target_win = "EnvironmentSettingWin"  # 遷移先ウィンドウ名
                self.window_close()  # プログラム終了イベント処理

            # タイムアウトしたら
            elif event == "-timeout-":
                # AWS接続テストを行うスレッドが存在するなら
                if check_access_aws_thread.is_alive():
                    # プロセスの進捗インジケーターの点の数を更新する処理
                    self.progress_dot_count_update()

    def progress_dot_count_update(self):
        """プロセスの進捗インジケーターの点の数を更新する処理"""

        # 進捗インジケーターの点の数の取得
        dot_count = self.window["-text-"].metadata["progress_indicator_dot_count"]
        # 進捗インジケーターの点の数の更新
        now_dot_count = (dot_count + 1) % 4
        # 進捗インジケーターの点の数の保存
        self.window["-text-"].metadata["progress_indicator_dot_count"] = now_dot_count

        # 表示メッセージの取得
        message = self.window["-text-"].metadata["message"]
        # インストール進捗状況の表示メッセージの更新
        self.window["-text-"].update(
            # メッセージ + 点 + 空白
            value=f"{message}{'.' * now_dot_count}{' ' * (3-now_dot_count)}"
        )


# ! デバッグ用
if __name__ == "__main__":
    # AWSの設定ファイルのパスの設定
    os.environ["AWS_CONFIG_FILE"] = SystemSetting.aws_config_file_path
    # AWSの認証情報ファイルのパスの設定
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = SystemSetting.aws_credentials_file_path

    win_instance = CheckAccessAwsWin()
