# ! デバッグ用
import sys  # システム関連
import os  # ディレクトリ関連

if __name__ == "__main__":
    src_path = os.path.dirname(__file__) + "\..\.."  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加
    print(src_path)

import PySimpleGUI as sg  # GUI

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス


class BaseWin:
    """ウィンドウの基本クラス"""

    def __init__(self):
        """コンストラクタ 初期設定"""
        self.user_setting = UserSetting()  # ユーザ設定のインスタンス化
        self.window_title = ""  # ウィンドウタイトル
        self.transition_target_win = None  # 遷移先ウィンドウ名

    def start_win(self):
        """ウィンドウ開始処理"""
        Fn.time_log("ウィンドウ開始")  # ログ出力
        self.window = self.make_win()  # GUIウィンドウ作成処理
        self.window.finalize()  # GUIウィンドウ表示
        self.event_start()  # イベント受付開始処理(終了処理が行われるまで繰り返す)

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """

    def make_win(self):
        """GUIウィンドウ作成処理

        Returns:
            window(sg.Window): GUIウィンドウ設定
        """

        # ウィンドウの位置とサイズの取得
        window_left_x = self.user_setting.get_setting("window_left_x")
        window_top_y = self.user_setting.get_setting("window_top_y")

        # GUIウィンドウ設定の引数の辞書
        window_args = {
            "title": "ヤクニャクコンジャック",  # ウィンドウタイトル
            "layout": self.get_layout(),  # レイアウト指定
            "resizable": True,  # ウィンドウサイズ変更可能
            "finalize": True,  # 入力待ち までの間にウィンドウを表示する
            "enable_close_attempted_event": True,  # タイトルバーの[X]ボタン押下,Alt+F4時にイベントが返される
            # メタデータ
            "metadata": {
                "is_exit": False,  # ウィンドウを閉じるかどうか
            },
        }

        # ウィンドウ位置が指定されている場合
        if (window_left_x is not None) and (window_top_y is not None):
            window_args["location"] = (window_left_x + 50, window_top_y + 50)
        # GUIウィンドウ設定
        window = sg.Window(**window_args)

        return window  # GUIウィンドウ設定

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

    def exit_event(self):
        """イベント終了処理"""
        # todo 終了設定(保存など)
        self.end_win()  # ウィンドウ終了処理

    def end_win(self):
        """ウィンドウ終了処理"""
        Fn.time_log("ウィンドウ終了")  # ログ出力
        self.window.close()  # ウィンドウを閉じる

    def get_transition_target_win(self):
        """遷移先ウィンドウ名の取得

        Returns:
            transition_target_win(str): 遷移先ウィンドウ名
        """
        return self.transition_target_win

    # todo イベント処理記述
    def window_close(self):
        """プログラム終了イベント処理

        閉じるボタン押下,Alt+F4イベントが発生したら
        """
        self.exit_event()  # イベント終了処理
        self.window.metadata["is_exit"] = True  # イベント受付終了

    def get_update_setting(self, values):
        """更新する設定の取得

        Args:
            values (dict): 各要素の値の辞書
        Returns:
            update_setting (dict): 更新する設定の値の辞書
        """

    def check_valid_number_event(self, window, event, values):
        """数字の入力値が有効かどうかを判定してGUI更新処理を行う処理

        エラーメッセージの表示や非表示、およびボタンの有効/無効の設定を行う

        Args:
            window(sg.Window): GUIウィンドウ設定
            event (str): 識別子
            values (dict): 各要素の値の辞書
        Return:
            is_error(bool): エラーが発生しているかどうか
        """

        min_value = window[event].metadata["min_value"]  # 入力範囲の最小値
        max_value = window[event].metadata["max_value"]  # 入力範囲の最大値
        message_key = window[event].metadata["message_key"]  # メッセージテキストの識別子
        is_add_newline_end = window[event].metadata["is_add_newline_end"]  # メッセージ末尾に改行を追加するかどうか

        # 入力値が空文字列でないなら
        if values[event] != "":
            # 文字列が数字のみなら
            if Fn.check_number_string(values[event]):
                # 先頭に0があるかつ文字数が2文字以上なら
                if values[event][0] == "0" and len(values[event]) >= 2:
                    # 先頭の0を削除する
                    window[event].update(value=int(values[event]))

                # 値が範囲内なら
                if min_value <= int(values[event]) <= max_value:
                    # エラーメッセージが表示されているなら
                    if window[message_key].visible:
                        # エラーメッセージを非表示にする
                        window[message_key].update(visible=False)

                    # 前回の値を保存する
                    window[event].metadata["before_input_value"] = values[event]
                    # エラーが発生しているかどうかを返す
                    return False
                # 値が範囲外なら
                else:
                    # メッセージテキスト
                    message_value = (
                        "  " + str(min_value) + "~" + str(max_value) + "の間で\n  入力してください。"
                    )

                    # メッセージ末尾に改行を追加するなら
                    if is_add_newline_end:
                        message_value += "\n "

                    # エラーメッセージを表示する
                    window[message_key].update(
                        value=message_value,
                        visible=True,  # 表示する
                    )

                    # 前回の値を保存する
                    window[event].metadata["before_input_value"] = values[event]
                    # エラーが発生しているかどうかを返す
                    return True

            # 文字列が数字のみでないなら
            else:
                # 数字以外を表示させないように処理

                # 値を前回の値に戻す
                window[event].update(value=window[event].metadata["before_input_value"])

                # エラー文が表示されているかどうかを返す
                return window[message_key].visible

        # 入力値が空文字列なら
        else:
            # 前回の値を保存する
            window[event].metadata["before_input_value"] = ""

            # メッセージテキスト
            message_value = "  半角数字のみを\n  入力してください。"

            # メッセージ末尾に改行を追加するなら
            if is_add_newline_end:
                message_value += "\n "

            # エラーメッセージを表示する
            window[message_key].update(
                value=message_value,
                visible=True,  # 表示する
            )

            # エラーが発生しているかどうかを返す
            return True
