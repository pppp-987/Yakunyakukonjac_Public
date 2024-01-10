import bisect  # 二分探索
import os  # ディレクトリ関連
import sys  # システム関連
import threading  # スレッド関連
import time  # 時間関係

import PySimpleGUI as sg  # GUI
from PIL import Image, ImageTk  # 画像処理

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加


from package.debug import Debug  # デバッグ用クラス
from package.fn import Fn  # 自作関数クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.thread.get_drag_area_thread import GetDragAreaThread  # ドラッグした領域の座標を取得するスレッド
from package.thread.translate_thread import TranslateThread  # 翻訳処理を行うスレッドクラス
from package.thread.translate_timing_thread import TranslateTimingThread  # 自動翻訳のタイミングを取得するスレッドクラス
from package.thread.watch_for_key_event_thread import WatchForKeyEventThread  # 指定したキーイベントが発生するかどうか監視するスレッドクラス
from package.translation.translation import Translation  # 翻訳機能関連のクラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class TranslationWin(BaseWin):
    """メインウィンドウクラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
        # 履歴ファイル名のリスト取得
        self.history_file_name_list = Fn.get_history_file_name_list()

        # 履歴ファイル日時のリスト取得
        self.history_file_time_list = Fn.get_history_file_time_list(self.history_file_name_list)

        # 現在の翻訳スレッド数
        self.thread_count = 0
        # 翻訳スレッド数の最大数
        self.thread_max = SystemSetting.translation_thread_max

        # 自動翻訳のタイミングを取得するスレッド
        self.translate_timing_thread = None

        # スレッド数がオーバーするかどうか
        self.is_thread_over = False

        # 利用者が変更できる画像の拡大率
        self.user_zoom_scale = 1

        # 最後に翻訳処理を行った時間
        self.last_translation_time = None

        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.user_setting.get_setting("window_theme"))

        # 画像パスの取得処理
        # 履歴が存在するなら
        if len(self.history_file_name_list) >= 1:
            # 最新の翻訳後画像名の取得
            now_image_name = max(self.history_file_name_list)

            # 履歴が存在するなら最新の画像パスを取得
            # 翻訳前画像の保存先パス
            now_image_before_path = os.path.join(SystemSetting.image_before_directory_path, now_image_name)
            # 翻訳後画像の保存先パス
            now_image_after_path = os.path.join(SystemSetting.image_after_directory_path, now_image_name)

            # ファイル日時の取得
            now_file_time = Fn.convert_time_from_filename(now_image_name)

        # 履歴が存在しないなら
        else:
            # デフォルトの画像パスを取得
            now_image_before_path = SystemSetting.default_image_before_path  # 翻訳前画像の保存先パス
            now_image_after_path = SystemSetting.default_image_after_path  # 翻訳後画像の保存先パス
            now_file_time = None  # ファイル日時

        # 画像オブジェクトの保存
        self.image_obj_list = {
            "image_before": Image.open(now_image_before_path),  # 翻訳前画像
            "image_after": Image.open(now_image_after_path),  # 翻訳後画像
        }

        # 翻訳前の画像のフレーム
        image_before_frame = sg.Frame(
            title="翻訳前画像",
            layout=[
                [
                    sg.Column(
                        layout=[
                            [
                                sg.Image(
                                    key="-image_before-",  # 識別子
                                    enable_events=True,  # イベントを取得する
                                ),
                            ],
                        ],
                        key="-image_before_column-",  # 識別子
                        size=(128, 72),  # 最小の表示サイズ
                        expand_x=True,  # 横方向に自動的に拡大
                        expand_y=True,  # 縦方向に自動的に拡大
                        scrollable=True,  # スクロールバーの有効化
                        sbar_width=13,  # スクロールバーの幅
                        size_subsample_width=1,  # スクロール可能な横の幅
                        size_subsample_height=1,  # スクロール可能な縦の幅
                        background_color="#888",  # 背景色
                        metadata={
                            "scrollbar_width": 15,  # スクロールバー用のスペース (1pxのマージン)
                        },
                    )
                ]
            ],
            expand_x=True,  # 横方向に自動的に拡大
            expand_y=True,  # 縦方向に自動的に拡大
        )

        # 翻訳後の画像のフレーム5
        image_after_frame = sg.Frame(
            title="翻訳後画像",
            layout=[
                [
                    sg.Column(
                        layout=[
                            [
                                sg.Image(
                                    key="-image_after-",  # 識別子
                                    enable_events=True,  # イベントを取得する
                                ),
                            ],
                        ],
                        key="-image_after_column-",  # 識別子
                        size=(128, 72),  # 最小の表示サイズ
                        expand_x=True,  # 横方向に自動的に拡大
                        expand_y=True,  # 縦方向に自動的に拡大
                        scrollable=True,  # スクロールバーの有効化
                        sbar_width=13,  # スクロールバーの幅
                        size_subsample_width=1,  # スクロール可能な横の幅
                        size_subsample_height=1,  # スクロール可能な縦の幅
                        background_color="#888",  # 背景色
                        metadata={
                            "scrollbar_width": 15,  # スクロールバー用のスペース (1pxのマージン)
                        },
                    ),
                ]
            ],
            expand_x=True,  # 横方向に自動的に拡大
            expand_y=True,  # 縦方向に自動的に拡大
        )

        # todo ウィンドウのテーマの設定

        # メニューバー設定
        menuber = [
            [
                "設定 (&C)",
                [
                    "撮影設定 (&Q)::transition_ShootingSettingWin::",
                    "言語設定 (&W)::transition_LanguageSettingWin::",
                    # "表示設定 (&E)::transition_DisplaySettingWin::",
                    "キー設定 (&R)::transition_KeySettingWin::",
                    "テーマ設定 (&T)::transition_ThemeSettingWin::",
                    "保存設定 (&Y)::transition_SaveSettingWin::",
                    "環境設定 (&U)::transition_EnvironmentSettingWin::",
                    # "利用者情報 (&I)::transition_UserInfoWin::",
                ],
            ],
        ]

        # レイアウト指定
        layout = [
            [[sg.Menu(menuber, key="-menu-")]],  # メニューバー
            [
                sg.Push(),  # 中央に寄せる
                # 翻訳用ボタン
                sg.Button(
                    button_text="翻訳",  # ボタンテキスト
                    key="-translation_button-",  # 識別子
                    size=(12, 3),  # サイズ(フォントサイズ)(w,h)
                    # expand_x = True, #  Trueの場合、要素はx方向に自動的に拡大
                    # expand_y = True, #  Trueの場合、要素はy方向に自動的に拡大
                ),
                # 自動翻訳用トグルボタン
                sg.Button(
                    button_text="自動翻訳開始",  # ボタンテキスト
                    key="-toggle_auto_translation-",  # 識別子
                    size=(12, 3),  # サイズ(フォントサイズ)(w,h)
                    # メタデータ
                    metadata={
                        "is_toggle_on": False,  # トグルボタンがオンかどうか
                        "toggle_button_text": {False: "自動撮影開始", True: "自動撮影停止"},  # トグルボタンテキスト
                        "toggle_on_count": 0,  # トグルボタンがオンに切り替わった回数
                    },
                ),
                sg.Push(),  # 中央に寄せる
            ],
            [
                sg.Push(),  # 中央に寄せる
                # 履歴ファイル選択フレーム
                sg.Frame(
                    title="履歴ファイル選択",
                    layout=[
                        [
                            # 前の履歴を表示するボタン
                            sg.Button(
                                button_text="◀",  # ボタンテキスト
                                key="-history_file_time_list_sub-",  # 識別子
                            ),
                            # 履歴ファイル選択リストボックス
                            sg.Listbox(
                                values=self.history_file_time_list,  # ファイル日時のリスト
                                size=(18, 1),
                                key="-history_file_time_list-",
                                default_values=now_file_time,  # デフォルト値
                                no_scrollbar=True,  # スクロールバーの非表示
                                enable_events=True,  # イベントを取得する
                            ),
                            # 後の履歴を表示するボタン
                            sg.Button(
                                button_text="▶",  # ボタンテキスト
                                key="-history_file_time_list_add-",  # 識別子
                            ),
                        ],
                    ],
                ),
                sg.Push(),  # 中央に寄せる
            ],
            [
                # 翻訳前の画像のフレーム
                image_before_frame
            ],
            [
                # 翻訳後の画像のフレーム
                image_after_frame
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

        # ウィンドウの位置とサイズの取得
        window_left_x = self.user_setting.get_setting("window_left_x")
        window_top_y = self.user_setting.get_setting("window_top_y")
        window_width = self.user_setting.get_setting("window_width")
        window_height = self.user_setting.get_setting("window_height")

        # ウィンドウ位置が指定されているなら
        if (window_left_x is not None) and (window_top_y is not None):
            window_args["location"] = (window_left_x, window_top_y)

        # ウィンドウサイズが指定されている場合
        if (window_width is not None) and (window_height is not None):
            window_args["size"] = (window_width, window_height)

        # GUIウィンドウ設定
        window = sg.Window(**window_args)

        # ウィジェットのサイズ変更イベントをバインド
        window.bind("<Configure>", "-window_resize-")

        return window  # GUIウィンドウ設定

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

        # todo ウィンドウ初期設定
        # 履歴ファイル選択リストの最初に表示される要素番号の取得
        self.window["-history_file_time_list-"].update(scroll_to_index=len(self.history_file_time_list) - 1)

        # 直前のウィンドウサイズの保存
        previous_window_size = self.window.current_size_accurate()

        # 画像のサイズを変更してウィンドウを更新する処理
        self.resize_and_refresh_gui()

        # 指定したキーイベントが発生するかどうか監視するスレッド
        thread = threading.Thread(
            # スレッド名
            name="キーイベント取得スレッド",
            # スレッドで実行するメソッド
            target=lambda: WatchForKeyEventThread.run(
                window=self.window,  # Windowオブジェクト
                # キーバインド情報のリスト
                key_binding_info_list=self.user_setting.get_setting("key_binding_info_list"),
            ),
            daemon=True,  # メインスレッド終了時に終了する
        )
        # スレッド開始
        thread.start()

        # 終了処理が行われるまで繰り返す
        while not self.window.metadata["is_exit"]:
            # 実際に画面が表示され、ユーザーの入力待ちになる
            # ! タイムアウト処理の削除
            event, values = self.window.read()

            # ! デバッグログ
            # Fn.time_log(event,values)

            # 共通イベントの処理が発生したら
            if self.base_event(event, values):
                continue

            # メニューバーの押下イベント
            elif values["-menu-"] is not None:  # 選択された項目があるなら
                # メニューバーのイベント処理
                menu_key = event.split("::")[1]  # メニュー項目の識別子取得
                # 画面遷移を行うかどうか
                if menu_key.startswith("transition_"):  # menu_keyにtransitionが含まれるなら
                    self.transition_target_win = menu_key.split("_")[1]  # 遷移先ウィンドウ名
                    Fn.time_log(self.transition_target_win, "に画面遷移")
                    self.window_close()  # プログラム終了イベント処理

            # 翻訳ボタン押下イベント
            elif event == "-translation_button-":
                self.translate_thread_start()  # 翻訳処理を別スレッドで開始

            # 自動翻訳ボタン押下イベント
            elif event == "-toggle_auto_translation-":
                self.toggle_auto_translation_event()  # 自動翻訳ボタン押下イベント

            # 翻訳開始タイミングイベント
            elif event == "-translate_thread_start-":
                self.translate_thread_start()  # 翻訳処理を別スレッドで開始

            # 翻訳処理のスレッド終了イベント
            elif event == "-translate_thread_end-":
                self.translate_thread_end(values)  # 翻訳処理のスレッド終了イベント

            # 画像クリックイベント
            elif event in ("-image_after-", "-image_before-"):
                # 利用者が変更できる拡大率の変更
                self.user_zoom_scale_change()

            # 履歴ファイル選択リストボックスイベント
            elif event == "-history_file_time_list-":
                self.history_file_list_box(values)  # 履歴ファイル選択リストボックスイベント

            # 履歴ファイル選択ボタンイベント
            elif event in ("-history_file_time_list_sub-", "-history_file_time_list_add-"):
                self.history_file_select_botton(event)  # 履歴ファイル選択ボタンイベント

            # キーイベントが発生したなら
            elif "-keyboard_event-" in values:
                event_name = values["-keyboard_event-"]  # 対応するイベント名
                # 翻訳イベント
                if event_name == "-translate_key-":
                    self.translate_thread_start()  # 翻訳処理を別スレッドで開始
                # 自動翻訳切替イベント
                elif event_name == "-auto_translation_toggle-":
                    self.toggle_auto_translation_event()  # 自動翻訳ボタン押下イベント
                # 撮影範囲設定イベント
                elif event_name == "-set_ss_region_key-":
                    # 撮影範囲設定イベント処理
                    self.set_ss_region_event()
                # 撮影設定へ遷移するイベント
                elif event_name == "-transition_to_shooting_key-":
                    self.transition_target_win = "ShootingSettingWin"  # 遷移先ウィンドウ名
                    self.window_close()  # プログラム終了イベント処理
                # 言語設定へ遷移するイベント
                elif event_name == "-transition_to_language_key-":
                    self.transition_target_win = "LanguageSettingWin"  # 遷移先ウィンドウ名
                    self.window_close()  # プログラム終了イベント処理

            # ウィジェットのサイズ変更イベント
            elif "-window_resize-":
                # ウィンドウサイズが変更されているなら画像サイズを更新する
                # 現在のウィンドウサイズの取得
                current_window_size = self.window.current_size_accurate()
                # 直前のウィンドウサイズと現在のウィンドウサイズが異なるなら
                if previous_window_size != current_window_size:
                    # 直前のウィンドウサイズの保存
                    previous_window_size = current_window_size
                    # 画像のサイズを変更してウィンドウを更新する処理
                    self.resize_and_refresh_gui()

    # todo イベント処理記述

    def window_close(self):
        """プログラム終了イベント処理

        閉じるボタン押下,Alt+F4イベントが発生したら
        """

        # ウィンドウ位置、サイズを保存する処理
        # ウィンドウの最小化や最大化が行われていないなら
        if self.window.TKroot.state() == "normal":
            # ウィンドウ位置、サイズの取得
            location = self.window.CurrentLocation()  # ウィンドウ位置
            size = self.window.current_size_accurate()  # ウィンドウサイズ

            # 更新する設定
            update_setting = {}
            update_setting["window_left_x"] = location[0]
            update_setting["window_top_y"] = location[1]
            update_setting["window_width"] = size[0]
            update_setting["window_height"] = size[1]

            self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存

        self.exit_event()  # イベント終了処理
        self.window.metadata["is_exit"] = True  # イベント受付終了

    def translate_thread_start(self):
        """翻訳処理を別スレッドで開始する処理"""

        # 現在の時間を取得
        current_time = time.time()

        # 最後に翻訳処理を行った時間が設定されていないか、1秒以上経過しているなら
        if self.last_translation_time is None or current_time - self.last_translation_time >= 1:
            # 最後に処理した時間を更新
            self.last_translation_time = current_time

            # 翻訳スレッド最大数を超えていないなら
            if self.thread_count < self.thread_max:
                # 翻訳スレッド数更新
                self.thread_count += 1
                Fn.time_log(f"スレッド開始 : {self.thread_count}")

                # 翻訳処理を行うスレッド作成
                self.translate_thread = threading.Thread(
                    # スレッド名
                    name=f"翻訳スレッド : {str(self.thread_count)}",
                    # スレッドで実行するメソッド
                    target=lambda: TranslateThread.run(),
                    daemon=True,  # メインスレッド終了時に終了する
                )

                # 翻訳処理を行うスレッド開始、処理終了時にイベントを返す
                self.translate_thread.start()

            # 翻訳スレッド最大数を超えているなら
            else:
                Fn.time_log("スレッド数オーバー")
                self.is_thread_over = True  # スレッド数がオーバーするかどうか

        # 最後に翻訳処理を行った時間から、1秒以上経過していないなら
        else:
            Fn.time_log("前回の翻訳からの経過時間が短すぎます。1秒以上の待機が必要です。")

    def translate_thread_end(self, values):
        """翻訳処理のスレッド終了イベント処理

        Args:
            values (dict): 各要素の値の辞書
        """

        # スレッド数のカウント
        self.thread_count -= 1
        Fn.time_log(f"スレッド終了 : {str(self.thread_count)}")

        # 余裕が出来たスレッドで翻訳処理を開始する処理
        # スレッド数がオーバーしていたなら
        if self.is_thread_over:
            # 自動翻訳トグルボタンがオンなら
            if self.window["-toggle_auto_translation-"].metadata["is_toggle_on"]:
                # 翻訳処理を別スレッドで開始
                self.translate_thread_start()

            # スレッド数がオーバーするかどうか
            self.is_thread_over = False

        # 履歴ファイル名取得
        file_name = values["-translate_thread_end-"]

        # 履歴ファイル日時取得
        file_time = Fn.convert_time_from_filename(file_name)

        # 二分探索を使用して新しい要素を挿入する位置を探す
        insert_index = bisect.bisect_left(self.history_file_name_list, file_name)

        # 履歴ファイル名のリストの更新
        self.history_file_name_list.insert(insert_index, file_name)
        # 履歴ファイル日時のリストの更新
        self.history_file_time_list.insert(insert_index, file_time)

        # 指定された制限を超えているかどうかをチェックして結果を返す
        check_file_limit_dict = Fn.check_file_limits(
            # ディレクトリパス
            directory_path=SystemSetting.image_after_directory_path,
            # 最大保存容量(MB)
            max_file_size_mb=int(self.user_setting.get_setting("max_file_size_mb")),
            # 最大保存枚数
            max_file_count=int(self.user_setting.get_setting("max_file_count")),
            # 最大保存期間(日)
            max_file_retention_days=int(self.user_setting.get_setting("max_file_retention_days")),
        )

        # 削除するファイルのリスト
        delete_file_list = []
        # 指定された制限を超えているかどうかを走査
        for file_name in check_file_limit_dict:
            # 指定された制限を超えているなら、ファイル名を保存する
            if check_file_limit_dict[file_name]:
                delete_file_list.append(file_name)

        # 削除するファイルを取得
        for file_name in delete_file_list:
            # 翻訳前画像フォルダから削除
            os.remove(os.path.join(SystemSetting.image_before_directory_path, file_name))
            # 翻訳後画像フォルダから削除
            os.remove(os.path.join(SystemSetting.image_after_directory_path, file_name))

        # 履歴ファイル名のリスト取得
        self.history_file_name_list = Fn.get_history_file_name_list()

        # 履歴ファイル日時のリスト取得
        self.history_file_time_list = Fn.get_history_file_time_list(self.history_file_name_list)

        # 履歴ファイル選択リストの更新
        self.window["-history_file_time_list-"].update(
            values=self.history_file_time_list,
            # 最新の画像を表示する
            set_to_index=len(self.history_file_time_list) - 1,  # 値の設定
            scroll_to_index=len(self.history_file_time_list) - 1,  # 最初に表示される要素番号の取得
        )

        # 翻訳前、後画像の変更処理
        self.image_change(max(self.history_file_name_list))

    def toggle_auto_translation_event(self):
        """自動翻訳トグルボタン押下イベント処理"""
        # トグルボタンがオンかどうか取得
        is_toggle_on = self.window["-toggle_auto_translation-"].metadata["is_toggle_on"]
        # オンオフ切り替え
        is_toggle_on = not is_toggle_on

        # トグルボタンに状態を保存
        self.window["-toggle_auto_translation-"].metadata["is_toggle_on"] = is_toggle_on
        # トグルボタンの変更先テキスト取得
        button_text = self.window["-toggle_auto_translation-"].metadata["toggle_button_text"][is_toggle_on]
        # トグルボタンのテキスト切り替え
        self.window["-toggle_auto_translation-"].update(text=button_text)

        # トグルボタンがオンなら
        if is_toggle_on:
            # トグルボタンがオンに切り替わった回数の加算
            self.window["-toggle_auto_translation-"].metadata["toggle_on_count"] += 1
            # 自動翻訳のタイミングを取得するスレッドの開始
            self.translate_timing_thread_start()

    def translate_timing_thread_start(self):
        """自動翻訳のタイミングを取得するスレッドの開始処理"""
        # 自動翻訳トグルボタンがオンかどうか取得
        is_toggle_auto_translation = self.window["-toggle_auto_translation-"].metadata["is_toggle_on"]
        # 自動翻訳がオンなら
        if is_toggle_auto_translation:
            # 自動翻訳のタイミングを取得するスレッド作成
            self.translate_timing_thread = threading.Thread(
                # スレッド名
                name="自動翻訳タイミング取得スレッド",
                # スレッドで実行するメソッド
                target=lambda: TranslateTimingThread.run(
                    user_setting=self.user_setting,
                    window=self.window,
                ),
                daemon=True,  # メインスレッド終了時に終了する
            )
            # 自動翻訳のタイミングを取得するスレッド開始、タイミング毎にイベントを返す
            self.translate_timing_thread.start()

    def image_change(self, file_name):
        """翻訳前、後画像の変更処理

        Args:
            file_name (str): ファイル名(撮影日時)
        """

        # 翻訳前画像パスの取得
        image_before_path = os.path.join(SystemSetting.image_before_directory_path, file_name)
        # 翻訳後画像パスの取得
        image_after_path = os.path.join(SystemSetting.image_after_directory_path, file_name)

        # 画像オブジェクトの保存
        self.image_obj_list = {
            "image_before": Image.open(image_before_path),  # 翻訳前画像
            "image_after": Image.open(image_after_path),  # 翻訳後画像
        }

        # 画像のサイズを変更してウィンドウを更新する処理
        self.resize_and_refresh_gui()

    def user_zoom_scale_change(self):
        """利用者が変更できる拡大率の変更"""
        # 利用者が変更できる拡大率
        if self.user_zoom_scale == 1:
            self.user_zoom_scale = 2
        elif self.user_zoom_scale == 2:
            self.user_zoom_scale = 4
        elif self.user_zoom_scale == 4:
            self.user_zoom_scale = 1

        # 画像のサイズを変更してウィンドウを更新する処理
        self.resize_and_refresh_gui()

    def resize_and_refresh_gui(self):
        """画像のサイズを変更してウィンドウを更新する処理"""
        # 繰り返しに使う識別子の情報をまとめた辞書
        key_info_dict = {
            # 翻訳前画像
            "image_before": {
                "column": "-image_before_column-",  # 画像を表示するカラム
                "image_gui_key": "-image_before-",  # 画像のGUI用識別子
            },
            # 翻訳後画像
            "image_after": {
                "column": "-image_after_column-",  # 画像を表示するカラム
                "image_gui_key": "-image_after-",  # 画像のGUI用識別子
            },
        }

        # 識別子の情報で走査
        for image_key in key_info_dict.keys():
            # カラムのキーの取得
            column_key = key_info_dict[image_key]["column"]

            # 画像のGUI用キーの取得
            image_gui_key = key_info_dict[image_key]["image_gui_key"]

            # 画像オブジェクトの取得
            image = self.image_obj_list[image_key]

            # スクロールバーの幅を含まないカラムサイズの計算
            no_scrollbar_column_size = [
                # 全体のカラムサイズからスクロールバーの幅を引く
                value - self.window[column_key].metadata["scrollbar_width"]
                # 全体のカラムサイズを取得してその値で走査
                for value in self.window[column_key].get_size()
            ]

            # 画像を与えられた範囲に収まるようにするための拡大率
            fit_zoom_scale = self.get_fit_zoom_scale(image, max_size=no_scrollbar_column_size)

            # 拡大率の計算
            # 範囲に収まるようにするための拡大率 * 利用者が変更できる拡大率
            zoom_scale = fit_zoom_scale * self.user_zoom_scale

            # 新しいサイズを計算
            new_size = (int(image.size[0] * zoom_scale), int(image.size[1] * zoom_scale))

            # 画像表示サイズが1px以上なら
            if new_size[0] > 0 and new_size[1] > 0:
                # 画像をリサイズ
                resized_img = image.resize(new_size, Image.LANCZOS)
                # GUIの画像要素を更新
                self.window[image_gui_key].update(data=ImageTk.PhotoImage(resized_img))
                # Columnのスクロール可能領域の更新
                self.window[column_key].Widget.canvas.config(scrollregion=(0, 0, new_size[0], new_size[1]))
        # ウィンドウを強制的に更新
        self.window.refresh()

    def get_fit_zoom_scale(self, image, max_size):
        """画像を与えられた範囲に収まるようにするための拡大率を取得

        Args:
            image (Image): 拡大率を計算する元の画像オブジェクト
            max_size (list[int, int]): 画像の最大サイズを指定する整数のリスト
                - max_width (int): 画像の最大幅
                - max_height (int): 画像の最大高さ

        Returns:
            fit_zoom_scale(int): 画像を与えられた範囲に収まるようにするための拡大率
        """

        # 拡大率の取得
        width_zoom_scale = max_size[0] / image.size[0]  # 表示サイズを超えない横幅の拡大率
        height_zoom_scale = max_size[1] / image.size[1]  # 表示サイズを超えない縦幅の拡大率
        fit_zoom_scale = min(width_zoom_scale, height_zoom_scale)  # 小さいほうの拡大率を適用

        return fit_zoom_scale  # 画像を与えられた範囲に収まるようにするための拡大率

    def history_file_list_box(self, values):
        """履歴ファイル選択リストボックスイベントの処理

        Args:
            values (dict): 各要素の値の辞書
        """
        # ファイルが選択されているなら
        if values["-history_file_time_list-"]:
            # ファイル日時の取得
            file_time = values["-history_file_time_list-"][0]
            # ファイル名(撮影日時)の取得
            file_name = Fn.convert_filename_from_time(file_time)

            # 翻訳前、後画像の変更処理
            self.image_change(file_name)

    def history_file_select_botton(self, key):
        """履歴ファイル選択リストボックスイベントの処理

        Args:
            key (str): 要素識別子
        """
        if len(self.history_file_name_list) >= 1:
            # 履歴が存在するなら
            # 現在の履歴ファイル選択リストボックスの要素番号の取得
            now_list_box_index = self.window["-history_file_time_list-"].get_indexes()[0]

            # 変更先の要素番号
            list_box_index = None

            if key == "-history_file_time_list_sub-":
                # 前の履歴を表示するボタン押下イベントなら
                if now_list_box_index != 0:
                    # 最も古い履歴でないなら
                    list_box_index = now_list_box_index - 1
            elif key == "-history_file_time_list_add-":
                # 後の履歴を表示するボタン押下イベントなら
                if now_list_box_index != len(self.history_file_time_list) - 1:
                    # 最も最新の履歴でないなら
                    list_box_index = now_list_box_index + 1

            if list_box_index is not None:
                # 変更先の要素番号が存在するなら
                file_name = self.history_file_name_list[list_box_index]

                # 履歴ファイル選択リストの更新
                self.window["-history_file_time_list-"].update(
                    set_to_index=list_box_index,  # 値の設定
                    scroll_to_index=list_box_index,  # 最初に表示される要素番号の取得
                )
                # 翻訳前、後画像の変更処理
                self.image_change(file_name)

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
                # 更新する設定
                update_setting = {}
                update_setting["ss_left_x"] = GetDragAreaThread.region["left"]
                update_setting["ss_top_y"] = GetDragAreaThread.region["top"]
                update_setting["ss_right_x"] = GetDragAreaThread.region["right"]
                update_setting["ss_bottom_y"] = GetDragAreaThread.region["bottom"]

                self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存

        # サブスレッドでエラーが発生したら
        else:
            return "error"


# ! デバッグ用
if __name__ == "__main__":
    win_instance = TranslationWin()
