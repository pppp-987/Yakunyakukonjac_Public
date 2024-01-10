import os  # ディレクトリ関連
import sys  # システム関連
import threading  # スレッド関連

import PySimpleGUI as sg  # GUI

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.fn import Fn  # 自作関数クラス
from package.thread.get_key_event_thread import GetKeyEventThread  # キーイベントの取得処理を行うスレッドクラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class KeySettingWin(BaseWin):
    """キー設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
        # キーバインド設定情報の辞書
        self.key_binding_info_list = self.user_setting.get_setting("key_binding_info_list")

        # キーバインド設定のイベントのリスト
        self.key_binding_event_list = [key_binding_info["gui_key"] for key_binding_info in self.key_binding_info_list]
        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.user_setting.get_setting("window_theme"))

        # キーバインド設定のレイアウト
        key_binding_layout = []
        # キーバインド設定情報の走査
        for key_binding_info in self.key_binding_info_list:
            # ボタンテキストの取得
            button_text = key_binding_info["key_name"]
            # キーが存在しないときのボタンテキストの設定
            if button_text is None:
                button_text = "未設定"

            # ボタン要素の追加
            key_binding_layout.append(
                [
                    # 説明テキスト
                    sg.Text(
                        text=key_binding_info["text"],
                        size=(14, 1),
                    ),
                    # キー設定変更ボタン
                    sg.Button(
                        button_text=button_text,
                        size=(12, 1),
                        key=key_binding_info["gui_key"],
                    ),
                ]
            )
        # レイアウト指定
        layout = [
            [key_binding_layout],
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
        # メタデータの追加
        window_args["metadata"]["is_key_input_waiting_state"] = False  # キー入力待ち状態かどうか
        window_args["metadata"]["is_key_input_waiting_event"] = None  # キー入力待ち状態のイベント名

        # ウィンドウの位置の取得
        window_left_x = self.user_setting.get_setting("window_left_x")
        window_top_y = self.user_setting.get_setting("window_top_y")

        # ウィンドウ位置が指定されている場合
        if (window_left_x is not None) and (window_top_y is not None):
            # 翻訳画面の座標位置から少し右下にずらす（設定画面用）
            window_args["location"] = (window_left_x + 50, window_top_y + 50)

        # GUIウィンドウ設定
        window = sg.Window(**window_args)

        return window  # GUIウィンドウ設定

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

        # 終了処理が行われるまで繰り返す
        while not self.window.metadata["is_exit"]:
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            # 共通イベントの処理が発生したら
            if self.base_event(event, values):
                continue

            # 戻るボタン押下イベント
            elif event == "-back-":
                # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

            # キー設定処理
            # キー入力待ち状態でないなら
            elif not self.window.metadata["is_key_input_waiting_state"]:
                # 確定ボタン押下イベント
                if event == "-confirm-":
                    # 更新する設定の取得
                    update_setting = self.get_update_setting(self.key_binding_info_list)
                    self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存
                    # 翻訳画面に遷移する処理
                    self.transition_to_translation_win()

                # キー設定ボタン押下イベント
                elif event in self.key_binding_event_list:
                    # キーイベントを取得するスレッドを開始する処理
                    self.key_event_start(event)

            # キー入力待ち状態なら
            elif self.window.metadata["is_key_input_waiting_state"]:
                # キー押下イベントなら
                if event == "-keyboard_event-":
                    # キー名とスキャンコードが他と重複していないなら
                    if not self.is_duplicate(values):
                        # キーバインド設定の表示の更新処理
                        self.update_key_binding_view(
                            # 設定変更対象のキー名
                            setting_target_key=values["-keyboard_event-"]["setting_target_key"],
                            key_name=values["-keyboard_event-"]["key_name"],  # 押下されたキー名
                            scan_code=values["-keyboard_event-"]["scan_code"],  # 押下されたスキャンコード
                        )

                # 変更対象のキー設定ボタン押下イベントが発生した場合
                elif event in self.window.metadata["is_key_input_waiting_event"]:
                    # キーバインド設定の表示の更新処理
                    self.update_key_binding_view(
                        # 設定変更対象のキー名
                        setting_target_key=self.window.metadata["is_key_input_waiting_event"],
                        key_name=None,  # キー名
                        scan_code=None,  # スキャンコード
                    )

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
        update_setting["key_binding_info_list"] = values

        # 更新する設定
        return update_setting

    def key_event_start(self, event):
        """キーイベントを取得するスレッドを開始する処理

        Args:
            event (str): 識別子
        """
        # 設定変更対象のキー名
        setting_target_key = event
        # キー設定ボタンテキスト変更
        self.window[event].update(text="キーを入力")
        # キー入力待ち状態かどうか
        self.window.metadata["is_key_input_waiting_state"] = True
        # キー入力待ちのイベント名
        self.window.metadata["is_key_input_waiting_event"] = event

        # 更新ボタンを入力不可に変更
        self.window["-confirm-"].update(disabled=True)

        # 選択したキー設定変更ボタン以外を入力不可に設定
        for event_name in self.key_binding_event_list:
            if self.window.metadata["is_key_input_waiting_event"] != event_name:
                # 選択したキー設定変更ボタンでないなら
                self.window[event_name].update(disabled=True)

        # キーイベントを取得するスレッド作成
        thread = threading.Thread(
            # スレッド名
            name="入力キー名取得スレッド",
            # スレッドで実行するメソッド
            target=lambda: GetKeyEventThread.run(
                setting_target_key=setting_target_key,  # 設定変更対象のキー名
            ),
            daemon=True,  # メインスレッド終了時に終了する
        )
        # スレッド開始
        thread.start()

    def is_duplicate(self, values):
        """キー名とスキャンコードの重複チェックを行う

        Args:
            values (dict): 各要素の値の辞書
        Returns:
            is_duplicate (bool): 重複しているかどうか
        """

        # 設定変更対象のキー名
        setting_target_key = values["-keyboard_event-"]["setting_target_key"]
        key_name = values["-keyboard_event-"]["key_name"]  # 押下されたキー名
        scan_code = values["-keyboard_event-"]["scan_code"]  # 押下されたスキャンコード

        # 他のキーバインド設定のキー名リスト作成
        another_key_name_list = []

        # 他のキーバインド設定のスキャンコードリスト作成
        another_scan_code_list = []

        # 他のキーバインド設定の取得
        for key_binding_info in self.key_binding_info_list:
            # 設定を変更するキー以外なら
            if key_binding_info["gui_key"] != setting_target_key:
                # 他のキーバインド設定のキー名リスト
                another_key_name_list.append(key_binding_info["key_name"])
                # 他のキーバインド設定のスキャンコードリスト
                another_scan_code_list.append(key_binding_info["scan_code"])

        # キー名とスキャンコードが他と重複しているかどうか
        return (key_name in another_key_name_list) or (scan_code in another_scan_code_list)

    def update_key_binding_view(self, setting_target_key, key_name, scan_code):
        """キーバインド設定の表示の更新処理

        Args:
            setting_target_key (str): 設定変更対象のキー名
            key_name (str): 押下されたキー名
            scan_code (int): 押下されたスキャンコード
        """

        # ボタンテキストの取得
        button_text = key_name
        # キーが存在しないときのボタンテキストの設定
        if button_text is None:
            button_text = "未設定"
        # キー設定ボタンのテキスト更新
        self.window[setting_target_key].update(text=button_text)

        # 変更前のキーバインド設定の取得
        old_key_binding_info = Fn.search_dict_in_list(self.key_binding_info_list, "gui_key", setting_target_key)

        # 更新するキーバインド設定の作成
        new_key_binding_info = old_key_binding_info
        new_key_binding_info["key_name"] = key_name
        new_key_binding_info["scan_code"] = scan_code

        # キーバインド設定リストの更新箇所の要素番号の取得
        update_index = self.key_binding_event_list.index(self.window.metadata["is_key_input_waiting_event"])

        # キーバインド設定リストの更新
        self.key_binding_info_list[update_index] = new_key_binding_info

        # 選択したキー設定変更ボタン以外を入力不可に設定
        for event_name in self.key_binding_event_list:
            if self.window.metadata["is_key_input_waiting_event"] != event_name:
                # 選択したキー設定変更ボタンでないなら
                self.window[event_name].update(disabled=False)

        # キー入力待ち状態かどうか
        self.window.metadata["is_key_input_waiting_state"] = False
        # キー入力待ちのイベント名
        self.window.metadata["is_key_input_waiting_event"] = None
        # 更新ボタンを入力可能に変更
        self.window["-confirm-"].update(disabled=False)


# ! デバッグ用
if __name__ == "__main__":
    win_instance = KeySettingWin()
