import os  # ディレクトリ関連
import sys  # システム関連
import threading  # スレッド関連

import PySimpleGUI as sg  # GUI

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

import pyautogui as pag  # マウスやキーボードを操作
import PySimpleGUI as sg  # GUI
from package.fn import Fn  # 自作関数クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス
from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス
from package.thread.get_drag_area_thread import GetDragAreaThread  # ドラッグした領域の座標を取得するスレッド
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class ShootingSettingWin(BaseWin):
    """撮影設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
        # 撮影範囲の座標情報の辞書
        self.ss_region_info_dict = {
            "left": {
                "text": "左上x座標",
                "key": "-ss_left_x-",
                "value": self.user_setting.get_setting("ss_left_x"),
            },
            "top": {
                "text": "左上y座標",
                "key": "-ss_top_y-",
                "value": self.user_setting.get_setting("ss_top_y"),
            },
            "right": {
                "text": "右下x座標",
                "key": "-ss_right_x-",
                "value": self.user_setting.get_setting("ss_right_x"),
            },
            "bottom": {
                "text": "右下y座標",
                "key": "-ss_bottom_y-",
                "value": self.user_setting.get_setting("ss_bottom_y"),
            },
        }

        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.user_setting.get_setting("window_theme"))

        # 撮影範囲表示テキストの作成
        ss_region_text = ""
        # 撮影範囲情報取得
        for ss_region_info in self.ss_region_info_dict.values():
            ss_region_text += f"{ss_region_info['text']} : {ss_region_info['value']}\n"

        # 末尾の改行を削除
        ss_region_text = ss_region_text.rstrip("\n")

        # レイアウト指定
        layout = [
            [
                sg.Frame(
                    title="翻訳間隔(秒)",
                    layout=[
                        [
                            sg.Input(
                                key="-translation_interval_sec-",
                                size=(6, 1),
                                # デフォルト
                                default_text=self.user_setting.get_setting("translation_interval_sec"),
                                enable_events=True,  # イベントを取得する
                                metadata={
                                    # 前回の値の保存
                                    "before_input_value": self.user_setting.get_setting("translation_interval_sec"),
                                    "min_value": 1,  # 入力範囲の最小値
                                    "max_value": 3600,  # 入力範囲の最大値
                                    "message_key": "-translation_interval_sec_message-",  # メッセージテキストの識別子
                                    "is_add_newline_end": False,  # メッセージ末尾に改行を追加するかどうか
                                },
                            ),
                        ],
                        [
                            # 表示/非表示切り替え時に再表示が必要ない
                            sg.pin(
                                # エラー発生時に表示するメッセージ
                                sg.Text(
                                    text="",
                                    key="-translation_interval_sec_message-",
                                    visible=False,  # 非表示にする
                                )
                            )
                        ],
                    ],
                )
            ],
            [
                sg.Frame(
                    title="撮影座標",
                    layout=[
                        # 撮影範囲設定ボタン
                        [sg.Button("撮影範囲設定", key="-set_ss_region-")],
                        # 撮影範囲表示テキスト
                        [sg.Text(text=ss_region_text, key="-ss_region_text-")],
                    ],
                )
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

            # ! デバッグログ
            # if event != "__TIMEOUT__":
            #     Fn.time_log(event, values)

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

            # 撮影範囲設定ボタン押下イベント
            elif event == "-set_ss_region-":
                # 撮影範囲設定ボタン押下イベント処理
                self.set_ss_region_event()
            # 翻訳間隔入力ボックス変更イベント
            elif event == "-translation_interval_sec-":
                # 数字の入力値が有効かどうかを判定してGUI更新処理を行う処理
                self.input_text_event(event, values)

    def get_ss_region_text(self):
        """撮影範囲表示テキストの取得

        Returns:
            ss_region_text(str): 撮影範囲表示テキスト
        """

        # 撮影範囲表示テキストの作成
        ss_region_text = ""
        # 撮影範囲情報取得
        for ss_region_info in self.ss_region_info_dict.values():
            ss_region_text += f"{ss_region_info['text']} : {ss_region_info['value']}\n"

        # 末尾の改行を削除
        ss_region_text = ss_region_text.rstrip("\n")
        return ss_region_text  # 撮影範囲表示テキスト

    def set_ss_region_event(self):
        """撮影範囲設定ボタン押下イベント処理"""
        # ドラッグした領域の座標を取得するスレッド作成
        thread = threading.Thread(
            # スレッド名
            name="撮影範囲設定スレッド",
            # スレッドで実行するメソッド
            target=lambda: GetDragAreaThread.run(),
            daemon=True,  # メインスレッド終了時に終了する
        )
        # スレッド開始
        thread.start()

        # メインスレッドが実行中かどうか
        GlobalStatus.is_main_thread_running = False

        # 0.5秒ごとにスレッドでエラーが発生したかどうかをチェックする
        # スレッドが存在するかつ、サブスレッドでエラーが発生していないなら
        while thread.is_alive() and not GlobalStatus.is_sub_thread_error:
            # スレッドが終了するまで停止(最大0.5秒)
            thread.join(timeout=0.5)

        # サブスレッドでエラーが発生しなかったら
        if not GlobalStatus.is_sub_thread_error:
            # メインスレッドが実行中かどうか
            GlobalStatus.is_main_thread_running = True

            # 撮影範囲がドラッグ選択されたなら
            if GetDragAreaThread.region is not None:
                # 撮影範囲の座標情報の更新
                for region_key in ["left", "top", "right", "bottom"]:
                    self.ss_region_info_dict[region_key]["value"] = GetDragAreaThread.region[region_key]

                # 撮影範囲表示テキストの取得
                ss_region_text = self.get_ss_region_text()
                # 撮影範囲表示テキストの更新
                self.window["-ss_region_text-"].update(value=ss_region_text)

        # サブスレッドでエラーが発生したら
        else:
            return "error"

    def get_update_setting(self, values):
        """更新する設定の取得

        Args:
            values (dict): 各要素の値の辞書
        Returns:
            update_setting (dict): 更新する設定の値の辞書
        """
        # 更新する設定
        update_setting = {}
        # キー名の両端のハイフンを取り除く
        update_setting["translation_interval_sec"] = int(values["-translation_interval_sec-"])  # 翻訳間隔(秒)
        # 撮影範囲の左側x座標
        update_setting["ss_left_x"] = int(self.ss_region_info_dict["left"]["value"])
        # 撮影範囲の上側y座標
        update_setting["ss_top_y"] = int(self.ss_region_info_dict["top"]["value"])
        # 撮影範囲の右側x座標
        update_setting["ss_right_x"] = int(self.ss_region_info_dict["right"]["value"])
        # 撮影範囲の下側y座標
        update_setting["ss_bottom_y"] = int(self.ss_region_info_dict["bottom"]["value"])
        # 更新する設定
        return update_setting

    def input_text_event(self, event, values):
        """数字の入力値が有効かどうかを判定してGUI更新処理を行う処理

        Args:
            event (_type_): 識別子
            values (dict): 各要素の値の辞書
        """
        # 継承元の数字の入力値が有効かどうかを判定してGUI更新処理を行う処理を呼び出す
        # エラーが発生したかどうかの取得
        is_error = super().check_valid_number_event(
            window=self.window,  # GUIウィンドウ設定
            event=event,  # 識別子
            values=values,  # 各要素の値の辞書
        )

        # エラーの発生状況によって確定ボタンの有効化、無効化を切り替える
        self.window["-confirm-"].update(disabled=is_error)


# ! デバッグ用
if __name__ == "__main__":
    win_instance = ShootingSettingWin()
