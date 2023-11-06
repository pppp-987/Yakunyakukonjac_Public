import boto3  # AWSのAIサービス

from deep_translator import GoogleTranslator  # google翻訳

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


class TextTranslation:
    """テキスト翻訳機能関連のクラス"""

    def get_text_after_list(user_setting, text_before_list):
        """翻訳後テキストの取得

        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            text_before_list(List[text_before]) : 翻訳前テキストのリスト
                - text_before(str) : 翻訳前テキスト
        Returns:
            text_after_list(List[text_after]) : 翻訳後テキストのリスト
                - text_after(str) : 翻訳後テキスト
        """

        translation_soft = user_setting.get_setting("translation_soft")  # 翻訳ソフト

        # OCRソフトによって分岐
        if translation_soft == "AmazonTranslate":  # 翻訳ソフトがAmazonTranslateなら
            # AmazonTranslateを使用して、翻訳後テキストを取得
            text_after_list = TextTranslation.amazon_translate(user_setting, text_before_list)
        elif translation_soft == "GoogleTranslator":
            # GoogleTranslatorを使用して、翻訳後テキストを取得
            text_after_list = TextTranslation.google_translator(user_setting, text_before_list)
        return text_after_list  # 翻訳後テキストのリスト

    def amazon_translate(user_setting, text_before_list):
        """AmazonTranslateを使用して、翻訳後テキストを取得

        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            text_before_list(List[text_before]) : 翻訳前テキストのリスト
                - text_before(str) : 翻訳前テキスト
        Returns:
            text_after_list(List[text_after]) : 翻訳後テキストのリスト
                - text_after(str) : 翻訳後テキスト
        """
        source_language_code = user_setting.get_setting("source_language_code")  # 翻訳前言語
        target_language_code = user_setting.get_setting("target_language_code")  # 翻訳後言語

        text_after_list = []  # 翻訳語テキストのリスト作成

        translate = boto3.client("translate")  # Translate サービスクライアントを作成

        for text_before in text_before_list:  # 翻訳前テキストで走査
            # 英語から日本語に翻訳
            result = translate.translate_text(
                Text=text_before,  # 翻訳テキスト
                SourceLanguageCode=source_language_code,  # 翻訳前言語
                TargetLanguageCode=target_language_code,  # 翻訳後言語
            )
            text_after_list.append(result["TranslatedText"])  # 翻訳後テキストのリスト作成

        return text_after_list  # 翻訳後テキストのリスト

    def google_translator(user_setting, text_before_list):
        """GoogleTranslatorを使用して、翻訳後テキストを取得

        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            text_before_list(List[text_before]) : 翻訳前テキストのリスト
                - text_before(str) : 翻訳前テキスト
        Returns:
            text_after_list(List[text_after]) : 翻訳後テキストのリスト
                - text_after(str) : 翻訳後テキスト
        """
        source_language_code = user_setting.get_setting("source_language_code")  # 翻訳前言語
        target_language_code = user_setting.get_setting("target_language_code")  # 翻訳後言語

        text_after_list = []  # 翻訳語テキストのリスト作成

        # 翻訳オブジェクト作成
        google_translator = GoogleTranslator(
            source=source_language_code, target=target_language_code
        )

        for text_before in text_before_list:  # 翻訳前テキストで走査
            # 英語から日本語に翻訳
            result = google_translator.translate(text=text_before)
            text_after_list.append(result)  # 翻訳後テキストのリスト作成

        return text_after_list  # 翻訳後テキストのリスト
