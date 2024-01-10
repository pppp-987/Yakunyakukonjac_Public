import os  # ディレクトリ関連


class SystemSetting:
    """ユーザーが変更不可能の設定クラス"""

    debug = True  # デバッグモード

    # 画像ファイル形式
    image_file_extension = ".png"

    # パッケージのルートディレクトリ
    package_path = os.path.dirname(__file__)  # パッケージディレクトリパス

    # ソースコードを格納するディレクトリ
    src_path = os.path.normpath(os.path.join(package_path, ".."))  # 上位レベル参照の正規化

    # 設定ファイル保存先設定
    setting_directory_path = os.path.join(src_path, "config")  # ディレクトリパス
    setting_file_path = os.path.join(setting_directory_path, "setting.json")  # 設定ファイルパス

    # 履歴ディレクトリパス
    history_directory_path = os.path.join(src_path, "history")
    # 翻訳前画像保存先設定
    image_before_directory_path = os.path.join(history_directory_path, "image_before")  # ディレクトリパス
    # 翻訳後画像保存先設定
    image_after_directory_path = os.path.join(history_directory_path, "image_after")  # ディレクトリパス

    # デバッグ用ディレクトリパス
    debug_directory_path = os.path.join(src_path, "debug_history")

    # プロジェクトのルートディレクトリ
    project_path = os.path.normpath(os.path.join(src_path, ".."))  # 上位レベル参照の正規化

    # エラーログのディレクトリパス
    error_log_directory_path = os.path.join(project_path, "log")  # ディレクトリパス
    # エラー基本情報のログファイルの保存場所
    simple_error_log_file_path = os.path.join(error_log_directory_path, "error_simple.log")
    # エラー詳細情報のログファイルの保存場所
    detailed_error_log_file_path = os.path.join(error_log_directory_path, "error_detailed.log")

    # 静的ファイル保存先設定
    static_path = os.path.join(project_path, "static")

    # フォントディレクトリパス
    font_path = os.path.join(static_path, "font")
    # Yu Gothic のパス 和文フォント 游ゴシック
    font_YuGothic_path = os.path.join(font_path, "YuGothM.ttc")
    # Segoe のパス 欧文フォント
    font_Segoe_path = os.path.join(font_path, "segoeui.ttf")
    # Microsoft YaHei のパス 簡体字フォント
    font_MicrosoftYaHei_path = os.path.join(font_path, "msyh.ttc")
    # Malgun Gothic のパス ハングルフォント
    font_MalgunGothic_path = os.path.join(font_path, "malgun.ttf")

    # 画像ファイルが格納されるディレクトリのパス
    image_path = os.path.join(static_path, "image")
    # OCRの動作チェックに使用する画像ファイルのパス
    check_ocr_image_path = os.path.join(image_path, "check_ocr.png")
    # デフォルトの翻訳前画像ファイルのパス
    default_image_before_path = os.path.join(image_path, "default_image_before.png")
    # デフォルトの翻訳後画像ファイルのパス
    default_image_after_path = os.path.join(image_path, "default_image_after.png")

    # アイコン画像ファイルが格納されるディレクトリのパス
    icon_path = os.path.join(static_path, "icon")
    # アプリケーションのアイコン画像ファイルのパス
    app_icon_file_path = os.path.join(icon_path, "app.ico")

    # プロジェクトに関連するスクリプトが格納されるディレクトリのパス
    tool_path = os.path.join(project_path, "tools")
    # AWSの設定を行うbatファイルのパス
    tool_aws_config_path = os.path.join(tool_path, "aws_configure.bat")
    # 履歴の削除を行うbatファイルのパス
    tool_delete_history_path = os.path.join(tool_path, "delete_history.bat")
    # ソフトウェアの初期化を行うbatファイルのパス
    tool_initialize_software_path = os.path.join(tool_path, "initialize_software.bat")
    # 設定のリセットを行うbatファイルのパス
    tool_reset_setting_path = os.path.join(tool_path, "reset_setting.bat")

    # 仮想環境のルートディレクトリ
    venv_path = os.path.normpath(os.path.join(project_path, ".."))  # 上位レベル参照の正規化

    # AWSの認証情報や設定ファイルのディレクトリパス
    aws_setting_directory_path = os.path.join(venv_path, ".aws")
    # AWSの設定ファイルのパス
    aws_config_file_path = os.path.join(aws_setting_directory_path, "config")
    # AWSの認証情報ファイルのパス
    aws_credentials_file_path = os.path.join(aws_setting_directory_path, "credentials")

    # EasyOCRモデルのディレクトリパス
    easy_ocr_model_path = os.path.join(venv_path, ".EasyOCR")
    # EasyOCRで使用するネットワークモデルのディレクトリ
    easy_ocr_network_path = os.path.join(easy_ocr_model_path, "user_network")

    # アプリケーションの名前
    app_name = "ヤクミャクコンジャック"

    # 翻訳スレッドの最大数
    translation_thread_max = 4

    # 言語情報一覧リスト{日本語表記、英語表記、言語コード(ISO 639-1),フォントパス}
    language_list = [
        {"ja_text": "アラビア語", "en_text": "Arabic", "code": "ar", "font_path": font_Segoe_path},
        {
            "ja_text": "中国語",
            "en_text": "Chinese",
            "code": "zh-CN",
            "font_path": font_MicrosoftYaHei_path,
        },
        {"ja_text": "英語", "en_text": "English", "code": "en", "font_path": font_Segoe_path},
        {"ja_text": "フランス語", "en_text": "French", "code": "fr", "font_path": font_Segoe_path},
        {"ja_text": "ドイツ語", "en_text": "German", "code": "de", "font_path": font_Segoe_path},
        {"ja_text": "イタリア語", "en_text": "Italian", "code": "it", "font_path": font_Segoe_path},
        {"ja_text": "日本語", "en_text": "Japanese", "code": "ja", "font_path": font_YuGothic_path},
        {"ja_text": "韓国語", "en_text": "Korean", "code": "ko", "font_path": font_MalgunGothic_path},
        {"ja_text": "ポルトガル語", "en_text": "Portuguese", "code": "pt", "font_path": font_Segoe_path},
        {"ja_text": "ロシア語", "en_text": "Russian", "code": "ru", "font_path": font_Segoe_path},
        {"ja_text": "スペイン語", "en_text": "Spanish", "code": "es", "font_path": font_Segoe_path},
    ]

    # EasyOCR用の言語コード(ISO 639-2)のリスト((ISO 639-1):(ISO 639-2))
    easy_ocr_update_language_code = {"zh-CN": "ch_sim"}

    # EasyOCR用言語情報一覧リストの作成
    # EasyOCR用言語情報一覧リスト（一部箇所でISO 639-2を使用）
    easy_ocr_language_list = []
    # 言語情報で走査
    for language_info in language_list:
        # 言語コードの取得
        language_code = language_info["code"]
        # EasyOCR用の言語情報の取得
        easy_ocr_language_info = language_info.copy()

        # 言語コードがEasyOCR用言語コードのリストに存在するなら
        if language_code in easy_ocr_update_language_code:
            # EasyOCR用言語コードに置き換える
            easy_ocr_language_info["code"] = easy_ocr_update_language_code[language_code]
        # EasyOCR用言語情報一覧リストに追加する
        easy_ocr_language_list.append(easy_ocr_language_info)
