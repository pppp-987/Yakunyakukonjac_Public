import os  # ディレクトリ関連
import subprocess  # 新しいプロセスを生成し、その入出力を管制するためのモジュール
import sys  # システム関連
import threading  # スレッドベースの並行処理を実装するためのモジュール

import PySimpleGUI as sg  # GUI

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

import PySimpleGUI as sg  # GUI
from package.fn import Fn  # 自作関数クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス
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

        # 現在AWSサービスにアクセスできるかどうか
        now_can_access_aws_service = self.user_setting.get_setting("can_access_aws_service")

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
                        key=f"-{ocr_soft}-",  # 識別子
                        enable_events=True,  # イベントを取得する
                        # AWSサービスにアクセスできないかつ、AWSサービスならラジオボタンを無効化する
                        disabled=not now_can_access_aws_service and ocr_soft == "AmazonTextract",
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
                        key=f"-{translation_soft}-",  # 識別子
                        enable_events=True,  # イベントを取得する
                        # AWSサービスにアクセスできないかつ、AWSサービスならラジオボタンを無効化する
                        disabled=not now_can_access_aws_service and translation_soft == "AmazonTranslate",
                    ),
                ]
            )

        # レイアウト指定
        layout = [
            [
                # 表示/非表示切り替え時に再表示が必要ない
                sg.pin(
                    # AWSへのアクセスに失敗している場合に表示するメッセージ
                    sg.Text(
                        text="AWSにアクセスできないため、\nAWSのサービスは使用できません。",
                        key="-cannot_access_aws_service_message-",
                        # AWSへのアクセスに失敗している場合に表示する
                        visible=not now_can_access_aws_service,
                    ),
                )
            ],
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
                # AWS接続設定ボタン
                sg.Button("AWS接続設定", key="-aws_config_button-", size=(16, 1)),
            ],
            [
                # AWS接続テストボタン
                sg.Button("AWS接続テスト", key="-check_access_aws_service-", size=(16, 1)),
            ],
            [
                # 履歴削除ボタン
                sg.Button("履歴削除", key="-delete_history-", size=(16, 1)),
            ],
            [
                # 設定リセットボタン
                sg.Button("設定リセット", key="-reset_setting-", size=(16, 1)),
            ],
            [
                # 初期化ボタン
                sg.Button("初期化", key="-initialize_software-", size=(16, 1)),
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
                update_setting = self.get_update_setting(values)  # 更新する設定の取得
                self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存
                # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

            # 戻るボタン押下イベント
            elif event == "-back-":
                # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

            # OCRソフトラジオボタン押下イベント
            elif event in [f"-{ocr_soft}-" for ocr_soft in self.ocr_soft_list]:
                # OCRがAmazonTextractの場合に表示するメッセージの表示/非表示を切り替える
                self.ocr_amazon_textract_message_event(event)

            # AWS接続テストボタン押下イベント
            elif event == "-check_access_aws_service-":
                # AWS接続テストボタン押下イベント処理
                self.transition_target_win = "CheckAccessAwsWin"  # 遷移先ウィンドウ名
                self.window_close()  # プログラム終了イベント処理

            # AWS接続設定ボタン押下イベント
            elif event == "-aws_config_button-":
                # AWS接続設定ボタン押下イベント処理
                self.transition_target_win = "AwsConfigureWin"  # 遷移先ウィンドウ名
                self.window_close()  # プログラム終了イベント処理

            # 履歴削除ボタン押下イベント
            elif event == "-delete_history-":
                # バッチファイルを実行するイベントの処理
                self.bat_file_event(
                    popup_message="履歴を削除しますか？",  # ポップアップで表示するメッセージ
                    bat_file_path=SystemSetting.tool_delete_history_path,  #  バッチファイルのパス
                )

            # 設定リセットボタン押下イベント
            elif event == "-reset_setting-":
                # バッチファイルを実行するイベントの処理
                self.bat_file_event(
                    popup_message="設定をリセットしますか？",  # ポップアップで表示するメッセージ
                    bat_file_path=SystemSetting.tool_reset_setting_path,  #  バッチファイルのパス
                )

            # 初期化ボタン押下イベント
            elif event == "-initialize_software-":
                # バッチファイルを実行するイベントの処理
                self.bat_file_event(
                    popup_message="初期化しますか？\nAWSの設定やEasyOCRモデルのデータなどもリセットされます。",  # ポップアップで表示するメッセージ
                    bat_file_path=SystemSetting.tool_initialize_software_path,  #  バッチファイルのパス
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

        # OCRソフトの設定
        for ocr_soft in self.ocr_soft_list:  # OCRソフトの名前で走査
            if values[f"-{ocr_soft}-"]:  # ラジオボックスが選択されているなら
                update_setting["ocr_soft"] = ocr_soft  # OCRソフトの名前を取得
                break

        # 翻訳ソフトの設定
        for translation_soft in self.translation_soft_list:  # 翻訳ソフトの名前で走査
            if values[f"-{translation_soft}-"]:  # ラジオボックスが選択されているなら
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

    def bat_file_event(self, popup_message, bat_file_path):
        """バッチファイルを実行するイベントの処理

        Args:
            popup_message (str): ポップアップで表示するメッセージ
            bat_file_path (str): バッチファイルのパス
        """
        # ウィンドウを非表示にする
        self.window.hide()
        # ポップアップを表示する
        popup_status = sg.popup_yes_no(popup_message)

        # ポップアップウィンドウで閉じるボタン,Alt+F4が押されたなら
        if popup_status is None:
            self.window_close()  # プログラム終了イベント処理
            return  # メソッドの処理を終了する

        # ポップアップでYesが押されたなら
        elif popup_status == "Yes":
            # バッチファイルの実行
            subprocess.run(bat_file_path)

            # ポップアップの表示
            sg.popup("プログラムを再起動します。")

            # 現在のプログラムを終了して再起動する処理
            self.is_restart_program = True  # 再起動するかどうか
            self.window_close()  # プログラム終了イベント処理

            return # メソッドの処理を終了する

        # ウィンドウを表示する
        self.window.un_hide()


# ! デバッグ用
if __name__ == "__main__":
    # AWSの設定ファイルのパスの設定
    os.environ["AWS_CONFIG_FILE"] = SystemSetting.aws_config_file_path
    # AWSの認証情報ファイルのパスの設定
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = SystemSetting.aws_credentials_file_path
    win_instance = EnvironmentSettingWin()
