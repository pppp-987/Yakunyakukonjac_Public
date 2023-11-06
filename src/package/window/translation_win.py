# ! デバッグ用
import sys  # システム関連
import os  # ディレクトリ関連
import threading  # スレッド関連
import bisect  # 二分探索

import PySimpleGUI as sg  # GUI

if __name__ == "__main__":
    src_path = os.path.dirname(__file__) + "\..\.."  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加


from package.fn import Fn  # 自作関数クラス
from package.debug import Debug  # デバッグ用クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.translation.translation import Translation  # 翻訳機能関連のクラス

from package.window.base_win import BaseWin  # ウィンドウの基本クラス

from package.thread.translate_timing_thread import TranslateTimingThread  # 自動翻訳のタイミングを取得するスレッドクラス
from package.thread.translate_thread import TranslateThread  # 翻訳処理を行うスレッドクラス

# 指定したキーイベントが発生するかどうか監視するスレッドクラス
from package.thread.watch_for_key_event_thread import WatchForKeyEventThread
from package.thread.get_drag_area_thread import GetDragAreaThread  # ドラッグした領域の座標を取得するスレッド


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

        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.user_setting.get_setting("window_theme"))
        # 履歴ファイル名のリストの取得

        # 画像パスの取得
        if len(self.history_file_name_list) >= 1:
            # 履歴が存在するなら
            # 最新の翻訳後画像名の取得
            now_image_name = max(self.history_file_name_list)
            # 履歴が存在するなら最新の画像パスを取得
            now_after_image_path = (
                SystemSetting.image_after_directory_path + now_image_name
            )  # 翻訳後画像の保存先パス
            now_before_image_path = (
                SystemSetting.image_before_directory_path + now_image_name
            )  # 翻訳前画像の保存先パス
            # ファイル日時の取得
            now_file_time = Fn.convert_time_from_filename(now_image_name)

        else:
            # 履歴が存在しないならデフォルトの画像パスを取得
            now_after_image_path = Debug.overlay_translation_image_path  # 翻訳後画像の保存先パス
            now_before_image_path = Debug.ss_file_path  # 翻訳前画像の保存先パス
            now_file_time = None  # ファイル日時

        # 翻訳前の画像のフレーム
        image_before_frame = sg.Frame(
            title="翻訳前画像",
            layout=[
                [
                    sg.Column(
                        [
                            [
                                sg.Image(
                                    source=now_before_image_path,  # 翻訳前画像の保存先パス
                                    key="-before_image-",  # 識別子
                                    enable_events=True,  # イベントを取得する
                                    subsample=1,  # 画像のサイズを縮小する量
                                    # メタデータ
                                    metadata={
                                        "source": now_before_image_path,  # 翻訳前画像の保存先パス
                                        "subsample": 1,  # 画像のサイズを縮小する量
                                    },
                                ),
                            ],
                        ],
                        size=(400, 225),  # 表示サイズ
                        scrollable=True,  # スクロールバーの有効化
                        background_color="#888",  # 背景色
                    ),
                ]
            ],
        )

        # 翻訳後の画像のフレーム
        image_after_frame = (
            sg.Frame(
                title="翻訳後画像",
                layout=[
                    [
                        sg.Column(
                            [
                                [
                                    sg.Image(
                                        source=now_after_image_path,  # 翻訳後画像の保存先パス
                                        key="-after_image-",  # 識別子
                                        enable_events=True,  # イベントを取得する
                                        subsample=1,  # 画像縮小率 サイズ/n
                                        metadata={
                                            "source": now_after_image_path,  # 翻訳後画像の保存先パス
                                            "subsample": 1,  # 画像のサイズを縮小する量
                                        },  # メタデータ
                                    ),
                                ],
                            ],
                            size=(400, 225),  # 表示サイズ
                            scrollable=True,  # スクロールバーの有効化
                            background_color="#888",  # 背景色
                        ),
                    ]
                ],
            ),
        )  # 翻訳後の画像表示
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
                # 翻訳用ボタン
                sg.Button(
                    button_text="翻訳",  # ボタンテキスト
                    key="-translation_button-",  # 識別子
                    size=(4 * 5, 2 * 2),  # サイズ(フォントサイズ)(w,h)
                    # expand_x = True, #  Trueの場合、要素はx方向に自動的に拡大
                    # expand_y = True, #  Trueの場合、要素はy方向に自動的に拡大
                ),
                # 自動翻訳用トグルボタン
                sg.Button(
                    button_text="自動翻訳開始",  # ボタンテキスト
                    key="-toggle_auto_translation-",  # 識別子
                    size=(4 * 5, 2 * 2),  # サイズ(フォントサイズ)(w,h)
                    # メタデータ
                    metadata={
                        "is_toggle_on": False,  # トグルボタンがオンかどうか
                        "toggle_button_text": {False: "自動撮影開始", True: "自動撮影停止"},  # トグルボタンテキスト
                    },
                ),
            ],
            [
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
                )
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

        # ウィンドウの位置とサイズの取得
        window_left_x = self.user_setting.get_setting("window_left_x")
        window_top_y = self.user_setting.get_setting("window_top_y")
        window_width = self.user_setting.get_setting("window_width")
        window_height = self.user_setting.get_setting("window_height")

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

        # ウィンドウ位置が指定されているなら
        if (window_left_x is not None) and (window_top_y is not None):
            window_args["location"] = (window_left_x, window_top_y)

        # ウィンドウサイズが指定されている場合
        if (window_width is not None) and (window_height is not None):
            window_args["size"] = (window_width, window_height)

        window = sg.Window(**window_args)
        return window  # GUIウィンドウ設定

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

        # todo ウィンドウ初期設定
        # 画像縮小率の変更
        self.image_size_change("-after_image-")
        self.image_size_change("-before_image-")

        # 履歴ファイル選択リストの最初に表示される要素番号の取得
        self.window["-history_file_time_list-"].update(
            scroll_to_index=len(self.history_file_time_list) - 1
        )

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
            # Fn.time_log(event)

            # プログラム終了イベント処理
            if event == "-WINDOW CLOSE ATTEMPTED-":  # 閉じるボタン押下,Alt+F4イベントが発生したら
                self.window_close()  # プログラム終了イベント処理

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
            elif event in ("-after_image-", "-before_image-"):
                self.image_size_change(event)  # 画像縮小率の変更

            # 履歴ファイル選択リストボックスイベント
            elif event == "-history_file_time_list-":
                self.history_file_list_box(values)  # 履歴ファイル選択リストボックスイベント
            # 履歴ファイル選択ボタンイベント
            elif event in ("-history_file_time_list_sub-", "-history_file_time_list_add-"):
                self.history_file_select_botton(event)  # 履歴ファイル選択ボタンイベント

            # サブスレッドでエラーが発生したら
            elif event == "-thread_error_event-":
                # エラーポップアップの表示
                sg.popup("\n".join(values["-thread_error_event-"]))
                self.window_close()  # プログラム終了イベント処理

            # キーイベントが発生したなら
            if "-keyboard_event-" in values:
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

    # todo イベント処理記述

    def window_close(self):
        """プログラム終了イベント処理

        閉じるボタン押下,Alt+F4イベントが発生したら
        """
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
        if self.thread_count < self.thread_max:
            # 翻訳スレッド最大数を超えていないなら
            self.thread_count += 1
            Fn.time_log("スレッド開始 : " + str(self.thread_count))

            # 翻訳処理を行うスレッド作成
            self.translate_thread = threading.Thread(
                # スレッド名
                name="翻訳スレッド : " + str(self.thread_count),
                target=lambda: TranslateThread.run(
                    window=self.window,
                ),  # スレッドで実行するメソッド
                daemon=True,  # メインスレッド終了時に終了する
            )

            # 翻訳処理を行うスレッド開始、処理終了時にイベントを返す
            self.translate_thread.start()

        else:
            # 翻訳スレッド最大数を超えているなら
            Fn.time_log("スレッド数オーバー")
            self.is_thread_over = True  # スレッド数がオーバーするかどうか

    def translate_thread_end(self, values):
        """翻訳処理のスレッド終了イベント処理

        Args:
            values (dict): 各要素の値の辞書
        """

        # スレッド数のカウント
        self.thread_count -= 1
        Fn.time_log("スレッド終了 : " + str(self.thread_count))

        # 余裕が出来たスレッドで翻訳処理を開始する処理
        if self.is_thread_over:
            # スレッド数がオーバーしていたなら
            if self.window["-toggle_auto_translation-"].metadata["is_toggle_on"]:
                # 自動翻訳トグルボタンがオンなら
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
            os.remove(SystemSetting.image_before_directory_path + "/" + file_name)
            # 翻訳後画像フォルダから削除
            os.remove(SystemSetting.image_after_directory_path + "/" + file_name)

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
        button_text = self.window["-toggle_auto_translation-"].metadata["toggle_button_text"][
            is_toggle_on
        ]
        # トグルボタンのテキスト切り替え
        self.window["-toggle_auto_translation-"].update(text=button_text)

        # トグルボタンがオンなら
        if is_toggle_on:
            # 自動翻訳のタイミングを取得するスレッドの開始
            self.translate_timing_thread_start()

    def translate_timing_thread_start(self):
        """自動翻訳のタイミングを取得するスレッドの開始処理"""
        # 自動翻訳トグルボタンがオンかどうか取得
        is_toggle_auto_translation = self.window["-toggle_auto_translation-"].metadata[
            "is_toggle_on"
        ]
        if is_toggle_auto_translation:
            # 自動翻訳がオンなら

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
        before_image_path = SystemSetting.image_before_directory_path + file_name
        # 翻訳後画像パスの取得
        after_image_path = SystemSetting.image_after_directory_path + file_name

        # 出力画像の変更
        for key in (
            "-before_image-",
            "-after_image-",
        ):
            # メタデータ更新(画像パス)
            if key == "-before_image-":
                self.window[key].metadata["source"] = before_image_path
            else:
                self.window[key].metadata["source"] = after_image_path

            # 要素の更新
            self.window[key].update(
                source=self.window[key].metadata["source"],  # 画像パス
                subsample=self.window[key].metadata["subsample"],  # 画像縮小率
            )

    def image_size_change(self, key):
        """画像縮小率の変更

        Args:
            key (str): 要素識別子
        """
        # 画像縮小率の取得 サイズ/n
        subsample = self.window[key].metadata["subsample"]

        # 変更する画像縮小率の取得・変更
        new_subsample = None
        if subsample == 1:
            new_subsample = 4
        elif subsample == 2:
            new_subsample = 1
        elif subsample == 4:
            new_subsample = 2

        # メタデータ更新(画像縮小率)
        self.window[key].metadata["subsample"] = new_subsample

        # 要素の更新
        self.window[key].update(
            source=self.window[key].metadata["source"],  # 画像パス
            subsample=self.window[key].metadata["subsample"],  # 画像縮小率
        )

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
            target=lambda: GetDragAreaThread.run(window=self.window),
            daemon=True,  # メインスレッド終了時に終了する
        )
        # スレッド開始
        thread.start()
        # スレッドが終了するまで停止
        thread.join()

        # 撮影範囲がドラッグ選択されたなら
        if GetDragAreaThread.region is not None:
            # 更新する設定
            update_setting = {}
            update_setting["ss_left_x"] = GetDragAreaThread.region["left"]
            update_setting["ss_top_y"] = GetDragAreaThread.region["top"]
            update_setting["ss_right_x"] = GetDragAreaThread.region["right"]
            update_setting["ss_bottom_y"] = GetDragAreaThread.region["bottom"]

            self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存


# ! デバッグ用
if __name__ == "__main__":
    win_instance = TranslationWin()
