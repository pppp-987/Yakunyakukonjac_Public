import os  # ディレクトリ関連
import sys  # システム関連

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.debug import Debug  # デバッグ用クラス
from package.fn import Fn  # 自作関数クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.translation.character_recognition import CharacterRecognition  # 文字認識機能関連のクラス
from package.translation.screenshot_capture import ScreenshotCapture  # スクリーンショット撮影機能関連のクラス
from package.translation.text_translation import TextTranslation  # テキスト翻訳機能関連のクラス
from package.translation.translation_image import TranslationImage  # オーバーレイ翻訳画像作成機能関連のクラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス


class Translation:
    """翻訳機能関連のクラス"""

    def save_history():
        """翻訳前,結果を履歴に保存する

        Returns:
            file_name(str): 保存ファイル名(撮影日時)
        """
        Fn.time_log("翻訳開始")

        user_setting = UserSetting()  # ユーザ設定のインスタンス化

        # 保存ファイルのベース名(撮影日時)の取得
        file_base_name = Fn.get_now_file_base_name()

        # 拡張子の取得
        file_extension = SystemSetting.image_file_extension

        # ファイル名の取得
        file_name = file_base_name + file_extension

        # スクショ撮影機能
        # screenshot_image = ScreenshotCapture.get_screenshot(user_setting)  # スクショ撮影
        # ss_file_path = ScreenshotCapture.save_screenshot(screenshot_image, file_name)  # スクショ保存
        # Fn.time_log("スクショ撮影")

        # ! デバック用
        # ss_file_path = Debug.ss_file_path  # スクショ画像パス
        # ss_file_path = os.path.join(Debug.debug_directory_path , "test.png")  # スクショ画像パス

        # ?
        # user_setting.save_setting_file({"ocr_soft": "AmazonTextract"})  # 設定をjsonファイルに保存
        # import time
        # start = time.time()
        # for i in range(10):
        #     text_data_dict = CharacterRecognition.get_text_data_dict(user_setting, ss_file_path)  # 画像からテキスト情報を取得
        # end = time.time()
        # print(end-start)
        # user_setting.save_setting_file({"ocr_soft": "EasyOCR"})  # 設定をjsonファイルに保存
        # start = time.time()
        # for i in range(10):
        # # Fn.time_log("スクショ撮影")
        #     # 文字認識機能
        #     text_data_dict = CharacterRecognition.get_text_data_dict(user_setting, ss_file_path)  # 画像からテキスト情報を取得
        # end = time.time()
        # print(end-start)
        # ?

        # Fn.time_log("スクショ撮影")
        # # 文字認識機能
        # text_data_dict = CharacterRecognition.get_text_data_dict(user_setting, ss_file_path)  # 画像からテキスト情報を取得
        # text_before_list = text_data_dict["text_list"]  # 翻訳前テキストリストの取得
        # text_region_list = text_data_dict["text_region_list"]  # テキスト範囲のリストの取得
        # Fn.time_log("文字取得")

        # ! デバック用
        text_before_list = Debug.text_before_list  # 翻訳前テキストリスト
        text_region_list = Debug.text_region_list  # テキスト範囲のリスト

        # ?
        user_setting.save_setting_file({"translation_soft": "AmazonTranslate"})  # 設定をjsonファイルに保存
        import time

        start = time.time()
        for i in range(10):
            text_after_list = TextTranslation.get_text_after_list(user_setting, text_before_list)  # 翻訳後テキストリストの取得
        end = time.time()
        print(end - start)
        user_setting.save_setting_file({"translation_soft": "GoogleTranslator"})  # 設定をjsonファイルに保存
        start = time.time()
        for i in range(10):
            # Fn.time_log("スクショ撮影")
            # 文字認識機能
            text_after_list = TextTranslation.get_text_after_list(user_setting, text_before_list)  # 翻訳後テキストリストの取得
        end = time.time()
        print(end - start)
        # ?

        # 翻訳機能
        # text_after_list = TextTranslation.get_text_after_list(user_setting, text_before_list)  # 翻訳後テキストリストの取得
        # Fn.time_log("翻訳")

        # ! デバック用
        # text_after_list = Debug.text_after_list  # 翻訳後テキストリスト

        # # 翻訳画像作成機能
        # overlay_translation_image = TranslationImage.get_overlay_translation_image(
        #     user_setting, ss_file_path, text_after_list, text_region_list
        # )  # 翻訳後画像作成

        # overlay_translation_image_path = TranslationImage.save_overlay_translation_image(
        #     overlay_translation_image, file_name
        # )  # 翻訳後画像保存

        # Fn.time_log("画像作成")

        # ! デバッグ用
        # overlay_translation_image.show()  # 画像表示

        return file_name  # 保存ファイル名(撮影日時)


# ! デバッグ用
if __name__ == "__main__":
    # AWSの設定ファイルのパスの設定
    os.environ["AWS_CONFIG_FILE"] = SystemSetting.aws_config_file_path
    # AWSの認証情報ファイルのパスの設定
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = SystemSetting.aws_credentials_file_path
    image_path = Translation.save_history()
