import logging  # ログの機能を提供
import os  # ディレクトリ関連
import sys  # システム関連
import threading  # スレッドベースの並行処理を実装するためのモジュール

import easyocr  # OCRライブラリ
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


class EasyOcrModelDownloadWin(BaseWin):
    """EasyOCRモデルダウンロード画面クラス

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
                    text="EasyOCRの検出モデルをダウンロード中",
                    key="-text-",
                    size=(40, 1),
                    metadata={
                        "message": "EasyOCRの検出モデルをダウンロード中",  # 表示メッセージ
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

        # EasyOCRモデルをダウンロードするスレッド
        thread = threading.Thread(
            # スレッド名
            name="EasyOCRモデルダウンロードスレッド",
            # スレッドで実行するメソッド
            # EasyOCRモデルをダウンロードするスレッド処理
            target=lambda: self.easy_ocr_model_download(),
            daemon=True,  # メインスレッド終了時に終了する
        )

        # EasyOCRモデルをダウンロードするスレッドの開始
        thread.start()

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

            # スレッドが終了したら
            elif event == "-thread_end-":
                # ポップアップの表示
                sg.popup("EasyOCRモデルのダウンロードが完了しました。")

                # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

            # タイムアウトしたら
            elif event == "-timeout-":
                # スレッドが存在するなら
                if thread.is_alive():
                    # プロセスの進捗インジケーターの点の数を更新する処理
                    self.progress_dot_count_update()

    def progress_message_update(self, message):
        """プロセスの進捗状況メッセージの更新処理

        Args:
            message (src): 表示するメッセージ
        """
        # 表示メッセージの更新
        self.window["-text-"].metadata["message"] = message
        # 進捗インジケーターの点の数の更新
        self.window["-text-"].metadata["progress_indicator_dot_count"] = 0
        # 表示メッセージの更新
        self.window["-text-"].update(value=message)

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

    def easy_ocr_model_download(self):
        """EasyOCRモデルをダウンロードする処理"""
        # ダウンロードする言語のリスト
        language_list = SystemSetting.easy_ocr_language_list

        # ! NVIDIAのGPUの場合、処理速度高速
        # 警告ロギングを非表示にする
        logging.getLogger().setLevel(logging.ERROR)

        # テキストの検出モデルのダウンロード
        easyocr.Reader(
            lang_list=[],  # 抽出する言語のリスト
            recognizer=False,  # 言語モデルを読み込まない
            model_storage_directory=SystemSetting.easy_ocr_model_path,  # EasyOCRモデルのディレクトリパス
            user_network_directory=SystemSetting.easy_ocr_network_path,  # EasyOCRで使用するネットワークモデルのディレクトリ
        )

        # 言語リストから言語コードを取り出す
        for lang_info in language_list:
            # プロセスの進捗状況メッセージの更新処理
            self.progress_message_update(f"{lang_info['ja_text']}のEasyOCRモデルをダウンロード中")

            # 言語モデル(認識モデル)のダウンロード
            easyocr.Reader(
                lang_list=[lang_info["code"]],  # 抽出する言語のリスト
                detector=False,  # 検出モデルを読み込まない
                model_storage_directory=SystemSetting.easy_ocr_model_path,  # EasyOCRモデルのディレクトリパス
                user_network_directory=SystemSetting.easy_ocr_network_path,  # EasyOCRで使用するネットワークモデルのディレクトリ
            )
        # ロギングの設定をデフォルトに戻す
        logging.getLogger().setLevel(logging.WARNING)

        print()  # 改行

        # 更新する設定
        update_setting = {
            "is_easy_ocr_model_exists": True,  # EasyOCRで使用されるモジュールが存在するかどうか
        }

        self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存

        # 現在開いているウィンドウクラスのインスタンスでウィンドウオブジェクトが作成されているかどうか
        if hasattr(GlobalStatus.win_instance, "window"):
            # ウィンドウオブジェクトの取得
            window = GlobalStatus.win_instance.window
            # ウィンドウが閉じられていないなら
            if not window.was_closed():
                # スレッドから、キーイベントを送信
                window.write_event_value(key="-thread_end-", value=None)


# ! デバッグ用
if __name__ == "__main__":
    win_instance = EasyOcrModelDownloadWin()
