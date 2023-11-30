import os  # ディレクトリ関連
import sys  # システム関連

import PySimpleGUI as sg  # GUI

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class UserInfoWin(BaseWin):
    """利用者情報画面クラス

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
                sg.Text("ocr_soft"),
                sg.Input(
                    key="-ocr_soft-",  # 識別子
                    enable_events=True,  # テキストボックスの変更をイベントとして受け取れる
                    # size=(8, 1),  # 要素のサイズ=(文字数, 行数)
                    default_text=self.user_setting.get_setting("ocr_soft"),  # デフォルト
                ),
            ],
            [
                sg.Text("translation_soft"),
                sg.Input(
                    key="-translation_soft-",  # 識別子
                    enable_events=True,  # テキストボックスの変更をイベントとして受け取れる
                    # size=(8, 1),  # 要素のサイズ=(文字数, 行数)
                    default_text=self.user_setting.get_setting("translation_soft"),  # デフォルト
                ),
            ],
            [
                sg.Push(),  # 右に寄せる
                sg.Button("確定", key="-confirm-"),  # 変更ボタン
                sg.Button("戻る", key="-back-"),  # 戻るボタン
            ],
        ]
        return layout  # レイアウト

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """
        # 終了処理が行われるまで繰り返す
        while not self.window.metadata["is_exit"]:
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            # Fn.time_log("event=", event, "values=", values)

            # 共通イベントの処理が発生したら
            if self.base_event(event, values):
                continue

            # 確定ボタン押下イベント
            elif event == "-confirm-":
                update_setting = values  # 更新する設定
                # * update_setting = self.get_update_setting(values)  # 更新する設定の取得
                self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存
                # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

            # 戻るボタン押下イベント
            elif event == "-back-":
                # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

    # todo イベント処理記述


# ! デバッグ用
if __name__ == "__main__":
    win_instance = UserInfoWin()
