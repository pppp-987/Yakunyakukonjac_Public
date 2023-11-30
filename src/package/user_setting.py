import json  # jsonファイルの読み書き
import os  # ディレクトリ関連
import threading  # スレッド関連

import boto3  # AWSのAIサービス
import PySimpleGUI as sg  # GUI
from package.fn import Fn  # 自作関数クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス
from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス


class UserSetting:
    """ユーザーが変更可能の設定クラス"""

    # デフォルトの設定
    default_user_setting = {
        "ss_left_x": 0,  # 撮影範囲の左側x座標
        "ss_top_y": 0,  # 撮影範囲の上側y座標
        "ss_right_x": 1280,  # 撮影範囲の右側x座標
        "ss_bottom_y": 720,  # 撮影範囲の下側y座標
        "ocr_soft": "EasyOCR",  # OCRソフト
        "translation_soft": "GoogleTranslator",  # 翻訳ソフト
        "can_access_aws_service": None,  # AWSのサービスにアクセス可能かどうか
        "source_language_code": "en",  # 翻訳元言語
        "target_language_code": "ja",  # 翻訳先言語
        "window_left_x": None,  # ウィンドウの左側x座標
        "window_top_y": None,  # ウィンドウの上側y座標
        "window_width": 400,  # ウィンドウの横幅
        "window_height": 600,  # ウィンドウの縦幅
        "translation_interval_sec": 10,  # 翻訳間隔(秒)
        "max_file_size_mb": 100,  # 最大保存容量(MB)
        "max_file_count": 50,  # 最大保存枚数
        "max_file_retention_days": 30,  # 最大保存期間(日)
        "window_theme": "DarkBlue3",  # ウィンドウのテーマ
        "is_easy_ocr_model_exists": False,  # EasyOCRで使用されるモジュールが存在するかどうか
        # キーバインド設定情報の辞書
        "key_binding_info_list": [
            {
                "text": "翻訳",  # 説明文
                "gui_key": "-translate_key-",  # 識別子
                "key_name": "f1",  # キー名
                "scan_code": None,  # スキャンコード
            },
            {
                "text": "自動翻訳切替",
                "gui_key": "-auto_translation_toggle-",
                "key_name": "f2",
                "scan_code": None,
            },
            {
                "text": "撮影範囲設定",
                "gui_key": "-set_ss_region_key-",
                "key_name": "f3",
                "scan_code": None,
            },
            {
                "text": "撮影設定へ遷移",
                "gui_key": "-transition_to_shooting_key-",
                "key_name": "f4",
                "scan_code": None,
            },
            {
                "text": "言語設定へ遷移",
                "gui_key": "-transition_to_language_key-",
                "key_name": "f5",
                "scan_code": None,
            },
        ],
    }

    def __init__(self):
        """コンストラクタ 初期設定"""
        self.setting = self.load_setting_file()  # 設定ファイルを読み込む

    def get_setting(self, key):
        """設定を取得する

        Args:
            key(str): 設定辞書のキー

        Returns:
            setting(str): 設定辞書の値

        """
        return self.setting[key]  # 設定辞書の値

    def get_all_setting(self):
        """設定を全て取得する

        Returns:
            setting(dict): 設定
        """
        return self.setting  # 設定

    def create_setting_file(self):
        """設定ファイルを新規作成して辞書として返す

        Returns:
            default_setting(dict): デフォルトの設定
        """
        setting_file_path = SystemSetting.setting_file_path  # 設定ファイルのパス
        default_setting = self.default_user_setting  # デフォルトの設定の取得
        with open(file=setting_file_path, mode="w") as f:  # ファイルを開く(書き込み)
            json.dump(obj=default_setting, fp=f, indent=2)  # ファイルの新規作成
        return default_setting  # デフォルト設定を戻り値に指定

    def load_setting_file(self):
        """設定ファイルを読み込み辞書として返す
        設定ファイルが存在しない場合は新規作成する

        Returns:
            setting(dict): 読み込んだ設定
        """
        setting_file_path = SystemSetting.setting_file_path  # 設定ファイルのパス

        # 設定ファイルの読み込み処理（ファイルが存在しないなら新規作成）
        if os.path.isfile(setting_file_path):  # ファイルが存在するなら
            # ファイルが存在するなら読み込む
            with open(setting_file_path, "r") as f:  # ファイルを開く(読み込み)
                setting = json.load(f)  # ファイルを読み込む
        else:
            # ファイルが存在しないなら新規作成して読み込む
            Fn.time_log("設定ファイルが存在しません。作成します。")
            setting = self.create_setting_file()  # デフォルトを戻り値に指定
        return setting  # 設定を戻り値に指定

    def save_setting_file(self, update_setting):
        """現在の設定を更新して、jsonファイルに保存する

        Args:
            update_setting (dict): 更新する設定
        """

        setting_file_path = SystemSetting.setting_file_path  # 設定ファイルのパス
        self.setting.update(update_setting)  # 現在の設定を更新

        # 設定変更
        Fn.time_log(f"設定変更:{update_setting}")

        with open(setting_file_path, "w") as f:  # ファイルを開く(書き込み)
            json.dump(obj=self.setting, fp=f, indent=2)  # ファイルに読み込む

    def check_access_aws_service(self, is_show_success_message=False):
        """AWSサービスにアクセス可能か確認する処理

        Args:
            is_show_success_message (bool, optional): アクセス成功時にメッセージを表示するかどうか。
                - デフォルトはFalse
        """
        # AWSの設定ファイルのパスの設定
        os.environ["AWS_CONFIG_FILE"] = SystemSetting.aws_config_file_path
        # AWSの認証情報ファイルのパスの設定
        os.environ["AWS_SHARED_CREDENTIALS_FILE"] = SystemSetting.aws_credentials_file_path

        try:
            # OCRの動作チェックに使用する画像ファイルのパス
            image_file_path = SystemSetting.check_ocr_image_path

            # Textract サービスクライアントを作成
            textract = boto3.client("textract")

            # 画像ファイルを開く
            with open(image_file_path, "rb") as file:
                # 文字列を検出
                result = textract.detect_document_text(Document={"Bytes": file.read()})

            # Translate サービスクライアントを作成
            translate = boto3.client("translate")

            # 簡単な翻訳を試みる
            result = translate.translate_text(Text="Hello World", SourceLanguageCode="en", TargetLanguageCode="ja")

            # AWSサービスにアクセス時に発生した例外オブジェクト
            aws_service_exception = None

        # エラー発生時
        except Exception as e:
            # AWSサービスにアクセス時に発生した例外オブジェクト
            aws_service_exception = e

        # AWSのサービスにアクセス可能かどうか
        can_access_aws_service = aws_service_exception is None
        # 更新する設定
        update_setting = {"can_access_aws_service": can_access_aws_service}

        # AWSのサービスにアクセスできないなら
        if not can_access_aws_service:
            # "ocr_soft": "EasyOCR",  # OCRソフト
            # "translation_soft": "GoogleTranslator",  # 翻訳ソフト

            # 現在のOCRソフトがAWSのサービスなら
            if self.get_setting("ocr_soft") == "AmazonTextract":
                # デフォルトのOCRソフトに変更する
                update_setting["ocr_soft"] = self.default_user_setting["ocr_soft"]

            # 現在の翻訳ソフトがAWSのサービスなら
            if self.get_setting("translation_soft") == "AmazonTranslate":
                # デフォルトのOCRソフトに変更する
                update_setting["translation_soft"] = self.default_user_setting["translation_soft"]

        # 設定をjsonファイルに保存
        self.save_setting_file(update_setting)

        # AWSのサービスにアクセスできないなら
        if not can_access_aws_service:
            # 表示するメッセージ
            message = [
                "警告",
                "申し訳ありません、AWSへのアクセスに失敗しました。",
                "AWSにアクセスできないため、AWSのサービスは使用できません。",
                "AWS以外のサービスを使用します。",
                "AWSの設定ファイルに誤りがないか、確認してください。",
                "AWSの設定は環境設定画面からでも行えます。",
                "AWSの設定ディレクトリパス:",
                f"  {SystemSetting.aws_setting_directory_path}",
                "エラーメッセージ :",
                f"  {aws_service_exception}",
            ]
            # ログに表示させる
            print("\n".join(message))

        # AWSのサービスのアクセスに成功したなら
        else:
            # 表示するメッセージ
            message = [
                "AWSへのアクセスに成功しました。",
                "AWSのサービスは使用可能です。",
            ]
            # ログに表示させる
            print("\n".join(message))

            # AWSのサービスのアクセスに成功した場合、メッセージを表示しないなら
            if not is_show_success_message:
                return

        # AWSのサービスにアクセスできないまたは、AWSのサービスのアクセスに成功した場合、メッセージを表示するなら
        if not can_access_aws_service or is_show_success_message:
            # 現在のスレッドがメインスレッドかどうか
            is_main_thread = threading.current_thread() == threading.main_thread()
            # 現在のスレッドがメインスレッドなら
            if is_main_thread:
                # エラーポップアップの作成
                sg.popup("\n".join(message))

            # 現在のスレッドがメインスレッドでないなら
            else:
                # 現在開いているウィンドウクラスのインスタンスでウィンドウオブジェクトが作成されているかどうか
                if hasattr(GlobalStatus.win_instance, "window"):
                    # ウィンドウオブジェクトの取得
                    window = GlobalStatus.win_instance.window
                    # ウィンドウが閉じられていないなら
                    if not window.was_closed():
                        # スレッドから、キーイベントを送信
                        window.write_event_value(key="-check_access_aws_thread_end-", value=message)
