import os  # ディレクトリ関連


class SystemSetting:
    """ユーザーが変更不可能の設定クラス"""

    debug = True  # デバッグモード

    # 画像ファイル形式
    image_file_extension = ".png"

    package_path = os.path.dirname(__file__) + "/"  # パッケージディレクトリパス

    history_directory_path = package_path + "../history/"  # 履歴ディレクトリパス

    # 翻訳前画像保存先設定
    image_before_directory_path = history_directory_path + "image_before/"  # ディレクトリパス

    # 翻訳後画像保存先設定
    image_after_directory_path = history_directory_path + "image_after/"  # ディレクトリパス

    # 設定ファイル保存先設定
    setting_file_name = "setting.json"  # ファイル名
    setting_directory_path = package_path + "../config/"  # ディレクトリパス
    setting_file_path = setting_directory_path + setting_file_name  # 設定ファイルパス

    # 静的ファイル保存先設定
    static_path = package_path + "../../static/"

    # フォントディレクトリパス
    font_path = static_path + "/font/"

    # 使用するフォントファイルのパス MS明朝
    font_msmincho_path = font_path + "msmincho.ttc"

    # Yu Gothic のパス 和文フォント 游ゴシック
    font_YuGothic_path = font_path + "YuGothM.ttc"

    # Segoe のパス 欧文フォント
    font_Segoe_path = font_path + "segoeui.ttf"
    # Microsoft YaHei のパス 簡体字フォント
    font_MicrosoftYaHei_path = font_path + "msyh.ttc"
    # Malgun Gothic のパス ハングルフォント
    font_MalgunGothic_path = font_path + "malgun.ttf"

    # アプリケーションの名前
    app_name = "ヤクミャクコンジャック"

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
    EasyOCR_language_code = {"zh-CN": "ch_sim"}

    # 翻訳スレッドの最大数
    translation_thread_max = 4

    # エラーログのディレクトリパス
    error_log_directory_path = package_path + "../log/"  # ディレクトリパス

    # エラー基本情報のログファイルの保存場所
    simple_error_log_file_path = error_log_directory_path + "error_simple.log"
    # エラー詳細情報のログファイルの保存場所
    detailed_error_log_file_path = error_log_directory_path + "error_detailed.log"
