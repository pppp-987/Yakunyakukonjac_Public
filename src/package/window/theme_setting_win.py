import os  # ディレクトリ関連
import random  # 乱数関連
import sys  # システム関連

import PySimpleGUI as sg  # GUI

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class ThemeSettingWin(BaseWin):
    """テーマ設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
        # 変更前テーマの保存
        self.current_theme = self.user_setting.get_setting("window_theme")
        # ウィンドウの位置とサイズの取得
        self.window_left_x = self.user_setting.get_setting("window_left_x") + 50
        self.window_top_y = self.user_setting.get_setting("window_top_y") + 50
        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.current_theme)

        # レイアウト指定
        layout = [
            [
                # 使用ソフト表示フレーム
                sg.Frame(
                    title="テーマ設定",
                    layout=[
                        [
                            # テーマ一覧リストボックス
                            sg.Listbox(
                                values=sg.theme_list(),  # テーマ一覧
                                size=(20, 12),  # サイズ
                                key="-theme_list-",  # 識別子
                                enable_events=True,  # イベントを取得する
                                default_values=[self.current_theme],  # デフォルト値
                            ),
                        ],
                    ],
                ),
            ],
            # ランダムテーマボタン
            [
                sg.Button("ランダム", key="-theme_random-"),
            ],
            [
                sg.Push(),  # 右に寄せる
                sg.Button("確定", key="-confirm-"),  # 変更ボタン
                sg.Button("戻る", key="-back-"),  # 戻るボタン
            ],
        ]
        return layout  # レイアウト

    def make_win(self):
        """GUIウィンドウ作成処理

        Returns:
            window(sg.Window): GUIウィンドウ設定
        """
        #  基本となるGUIウィンドウで設定する引数の辞書の取得
        window_args = self.get_base_window_args()

        # ウィンドウ位置が指定されている場合
        if (self.window_left_x is not None) and (self.window_top_y is not None):
            # 座標位置に画面を表示する
            window_args["location"] = (self.window_left_x, self.window_top_y)

        # GUIウィンドウ設定
        window = sg.Window(**window_args)

        return window  # GUIウィンドウ設定

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

        # テーマ選択リストボックスの最初に表示される要素番号の取得
        theme_list_index = sg.theme_list().index(self.current_theme)

        # テーマ選択リストボックスの更新
        self.window["-theme_list-"].update(
            set_to_index=theme_list_index,  # 値の設定
            scroll_to_index=theme_list_index - 3,  # 最初に表示される要素番号の取得
        )

        # 終了処理が行われるまで繰り返す
        while not self.window.metadata["is_exit"]:
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            # 共通イベントの処理が発生したら
            if self.base_event(event, values):
                continue

            # 確定ボタン押下イベント
            elif event == "-confirm-":
                update_setting = self.get_update_setting(values)  # 更新する設定の取得
                self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存
                # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

            # 戻るボタン押下イベント
            elif event == "-back-":
                # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

            # テーマ変更リストボックス選択イベント
            elif event == "-theme_list-":
                # 変更先テーマの取得
                new_theme = values["-theme_list-"][0]
                # テーマが変更されているなら
                if new_theme != self.current_theme:
                    # テーマの更新
                    self.current_theme = new_theme

                    # ウィンドウ位置、サイズの取得
                    window_location = self.window.CurrentLocation()  # ウィンドウ位置

                    # ウィンドウの位置の更新
                    self.window_left_x = window_location[0]
                    self.window_top_y = window_location[1]

                    # ウィンドウを閉じる
                    self.window.close()
                    # ウィンドウ開始処理
                    self.start_win()

            # ランダムテーマボタン押下イベント
            elif event == "-theme_random-":
                # リストからランダムな要素番号を取得
                random_index = random.randint(0, len(sg.theme_list()) - 1)
                # テーマ選択リストボックスの更新
                self.window["-theme_list-"].update(
                    set_to_index=random_index,  # 値の設定
                    scroll_to_index=random_index - 3,  # 最初に表示される要素番号の取得
                )
                # 変更先テーマの取得
                new_theme = sg.theme_list()[random_index]

                # テーマが変更されているなら
                if new_theme != self.current_theme:
                    # テーマの更新
                    self.current_theme = new_theme

                    # ウィンドウ位置、サイズの取得
                    window_location = self.window.CurrentLocation()  # ウィンドウ位置

                    # ウィンドウの位置の更新
                    self.window_left_x = window_location[0]
                    self.window_top_y = window_location[1]

                    # ウィンドウを閉じる
                    self.window.close()
                    # ウィンドウ開始処理
                    self.start_win()

    # todo イベント処理記述
    def get_update_setting(self, values):
        """更新する設定の取得

        Args:
            values (dict): 各要素の値の辞書
        Returns:
            update_setting (dict): 更新する設定の値の辞書
        """

        # 更新する設定
        update_setting = {}
        # ウィンドウのテーマ
        update_setting["window_theme"] = values["-theme_list-"][0]

        # 更新する設定
        return update_setting


# ! デバッグ用
if __name__ == "__main__":
    win_instance = ThemeSettingWin()
