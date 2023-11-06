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
from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class LanguageSettingWin(BaseWin):
    """言語設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
        # 言語情報一覧リストのリストの取得
        self.language_list = SystemSetting.language_list

        # 言語名のリスト作成
        self.language_name_list = []
        for language in self.language_list:
            self.language_name_list.append(language["ja_text"])  # 言語名取得

        # OCRソフトがAmazonTextractかどうか
        self.is_ocr_amazon_textract = self.user_setting.get_setting("ocr_soft") == "AmazonTextract"

        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.user_setting.get_setting("window_theme"))

        # 現在の翻訳前言語コードの取得
        now_source_language_code = self.user_setting.get_setting("source_language_code")
        # 現在の翻訳後言語コードの取得
        now_target_language_code = self.user_setting.get_setting("target_language_code")

        # 現在の翻訳前言語名の取得
        now_source_language_name = Fn.search_dict_in_list(
            self.language_list, "code", now_source_language_code
        )["ja_text"]

        # 現在の翻訳後言語名の取得
        now_target_language_name = Fn.search_dict_in_list(
            self.language_list, "code", now_target_language_code
        )["ja_text"]

        # 翻訳前言語設定のレイアウト
        source_language_layout = []

        # OCRがAmazonTextractでないなら
        if not self.is_ocr_amazon_textract:
            # 翻訳前言語設定のレイアウト
            source_language_layout = [
                [
                    sg.Listbox(
                        values=self.language_name_list,
                        size=(14, 5),
                        key="-source_language_code-",
                        default_values=now_source_language_name,  # デフォルト値
                    ),
                ],
            ]
        # OCRがAmazonTextractなら
        else:
            source_language_layout = [
                [
                    sg.Text(
                        text="自動検出",
                        size=(14, 1),
                        key="-source_language_code-",
                    ),
                ],
            ]

        # レイアウトの初期設定
        layout = []

        # OCRがAmazonTextractなら
        if self.user_setting.get_setting("ocr_soft") == "AmazonTextract":
            # OCRがAmazonTextractの場合に表示するメッセージを表示する
            layout += [[sg.Text("OCRソフト : AmazonTextract は\n非ラテン文字の言語に\n対応していません。")]]

        # レイアウト指定
        layout += [
            [
                # 翻訳前言語選択フレーム
                sg.Frame(title="翻訳前言語", layout=source_language_layout)
            ],
            [
                # 翻訳後言語選択フレーム
                sg.Frame(
                    title="翻訳後言語",
                    layout=[
                        [
                            sg.Listbox(
                                values=self.language_name_list,
                                size=(14, 5),
                                key="-target_language_code-",
                                default_values=now_target_language_name,  # デフォルト値
                            ),
                        ],
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

        # リストボックスの初期スクロール位置の設定
        for key in ("-source_language_code-", "-target_language_code-"):
            # OCRがAmazonTextractでないかつ、翻訳前言語選択リストボックスでないなら
            if not (self.is_ocr_amazon_textract and key == "-source_language_code-"):
                # 選択されている値の取得
                value = self.window[key].get()[0]
                # 最初に表示される要素番号の取得
                scroll_to_index = self.language_name_list.index(value) - 1
                # リストボックスの初期スクロール位置の設定
                self.window[key].update(scroll_to_index=scroll_to_index)

        # 終了処理が行われるまで繰り返す
        while not self.window.metadata["is_exit"]:
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            Fn.time_log("event=", event, "values=", values)
            # プログラム終了イベント処理
            if event == "-WINDOW CLOSE ATTEMPTED-":  # 閉じるボタン押下,Alt+F4イベントが発生したら
                self.window_close()  # プログラム終了イベント処理

            # 確定ボタン押下イベント
            elif event == "-confirm-":
                update_setting = self.get_update_setting(values)  # 更新する設定の取得
                self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存

            # 確定ボタン押下イベント
            elif event == "-back-":
                self.transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
                self.window_close()  # プログラム終了イベント処理

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

        # OCRがAmazonTextractでないなら
        if not self.is_ocr_amazon_textract:
            # 翻訳前言語名取得
            source_language_name = values["-source_language_code-"][0]
            # 翻訳前言語コード取得
            source_language_code = Fn.search_dict_in_list(
                self.language_list, "ja_text", source_language_name
            )["code"]
            # 翻訳前言語設定
            update_setting["source_language_code"] = source_language_code

        # 翻訳後言語名取得
        target_language_name = values["-target_language_code-"][0]
        # 翻訳後言語コード取得
        target_language_code = Fn.search_dict_in_list(
            self.language_list, "ja_text", target_language_name
        )["code"]

        # 翻訳後言語設定
        update_setting["target_language_code"] = target_language_code

        # 更新する設定
        return update_setting


# ! デバッグ用
if __name__ == "__main__":
    win_instance = LanguageSettingWin()
