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
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class EnvironmentSettingWin(BaseWin):
    """環境設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    # OCRソフトの名前のリスト
    ocr_soft_list = ["AmazonTextract", "EasyOCR"]

    # OCRソフトの名前のリスト
    translation_soft_list = ["AmazonTranslate", "GoogleTranslator"]

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

        # 現在のOCRソフトの取得
        now_ocr_soft = self.user_setting.get_setting("ocr_soft")
        # 現在の翻訳ソフトの取得
        now_translation_soft = self.user_setting.get_setting("translation_soft")

        # OCRソフト設定フレームのレイアウトの作成
        ocr_soft_layout = []
        for ocr_soft in self.ocr_soft_list:  # OCRソフトの名前で走査
            ocr_soft_layout.append(
                [
                    # ラジオボタン
                    sg.Radio(
                        text=ocr_soft,  # テキスト
                        group_id="ocr_radio",  # グループID
                        default=(ocr_soft == now_ocr_soft),  # デフォルトの設定
                        key="-" + ocr_soft + "-",  # 識別子
                        enable_events=True,  # イベントを取得する
                    ),
                ]
            )

        # 翻訳ソフト設定フレームのレイアウトの作成
        translation_soft_layout = []
        for translation_soft in self.translation_soft_list:  # 翻訳ソフトの名前で走査
            translation_soft_layout.append(
                [
                    # ラジオボタン
                    sg.Radio(
                        text=translation_soft,  # テキスト
                        group_id="translation_radio",  # グループID
                        default=(translation_soft == now_translation_soft),  # デフォルトの設定
                        key="-" + translation_soft + "-",  # 識別子
                        enable_events=True,  # イベントを取得する
                    ),
                ]
            )

        # レイアウト指定
        layout = [
            [
                # 表示/非表示切り替え時に再表示が必要ない
                sg.pin(
                    # OCRがAmazonTextractの場合に表示するメッセージ
                    sg.Text(
                        text="AmazonTextract は\n非ラテン文字の言語に\n対応していません。",
                        key="-ocr_amazon_textract_message-",
                        # OCRがAmazonTextractの場合に表示する
                        visible=now_ocr_soft == "AmazonTextract",
                    ),
                )
            ],
            [
                # OCRソフト設定フレーム
                sg.Frame(title="OCRソフト", layout=ocr_soft_layout),
            ],
            [
                # 翻訳ソフト設定フレーム
                sg.Frame(title="翻訳ソフト", layout=translation_soft_layout),
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

            # OCRソフトラジオボタン押下イベント
            if event in ["-" + ocr_soft + "-" for ocr_soft in self.ocr_soft_list]:
                # OCRがAmazonTextractの場合に表示するメッセージの表示/非表示を切り替える
                self.ocr_amazon_textract_message_event(event)
                # if event == "-AmazonTextract-":
                #     "-ocr_amazon_textract_message-"
                #     self.window['-TXT-'].update(visible=not window['-TXT-'].visible)

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

        # OCRソフトの設定
        for ocr_soft in self.ocr_soft_list:  # OCRソフトの名前で走査
            if values["-" + ocr_soft + "-"]:  # ラジオボックスが選択されているなら
                update_setting["ocr_soft"] = ocr_soft  # OCRソフトの名前を取得
                break

        # 翻訳ソフトの設定
        for translation_soft in self.translation_soft_list:  # 翻訳ソフトの名前で走査
            if values["-" + translation_soft + "-"]:  # ラジオボックスが選択されているなら
                update_setting["translation_soft"] = translation_soft  # 翻訳ソフトの名前を取得
                break

        # 更新する設定
        return update_setting

    def ocr_amazon_textract_message_event(self, event):
        """OCRがAmazonTextractの場合に表示するメッセージの表示/非表示を切り替える

        Args:
            event (str): 識別子
        """
        # 現在メッセージが表示されているかどうか
        now_visible = self.window["-ocr_amazon_textract_message-"].visible
        # 表示/非表示切り替え処理
        # 表示されている、かつ、OCRソフトがAmazonTextractでないなら
        if now_visible and event != "-AmazonTextract-":
            # 非表示状態に変更
            self.window["-ocr_amazon_textract_message-"].update(visible=False)
        # 表示されていない、かつ、OCRソフトがAmazonTextractであるなら
        elif not now_visible and event == "-AmazonTextract-":
            # 表示状態に変更
            self.window["-ocr_amazon_textract_message-"].update(visible=True)


# ! デバッグ用
if __name__ == "__main__":
    win_instance = EnvironmentSettingWin()
