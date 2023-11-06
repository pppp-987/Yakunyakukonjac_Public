from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス


class Debug:
    """デバッグ用クラス"""

    # デバッグ用ディレクトリパス
    debug_directory_path = SystemSetting.package_path + "../debug_history/"

    # 翻訳前画像パス
    ss_file_path = debug_directory_path + "/image_before.png"

    # 翻訳前テキストリスト
    text_before_list = [
        "MARLEY'S GHOST",
        "Marley was dead: to begin with. There is no",
        "doubt whatever about that. The register of his",
        "burial was signed by the clergyman, the clerk,",
        "the undertaker, and the chief mourner. Scrooge",
        "signed it: and Scrooge's name was good upon",
        "'Change, for anything he chose to put his hand to.",
        "Old Marley was as dead as a door-nail.",
        '" A CHRISTMAS CAROL"',
        "by Charles Dickens",
    ]

    # テキスト範囲のリスト
    text_region_list = [
        {"left": 503, "top": 130, "width": 538, "height": 69},
        {"left": 175, "top": 297, "width": 1056, "height": 56},
        {"left": 177, "top": 368, "width": 1089, "height": 57},
        {"left": 177, "top": 440, "width": 1101, "height": 58},
        {"left": 176, "top": 512, "width": 1124, "height": 57},
        {"left": 176, "top": 583, "width": 1091, "height": 58},
        {"left": 176, "top": 655, "width": 1184, "height": 58},
        {"left": 177, "top": 727, "width": 932, "height": 57},
        {"left": 608, "top": 897, "width": 673, "height": 61},
        {"left": 754, "top": 988, "width": 466, "height": 60},
    ]

    # 翻訳後テキストリスト
    text_after_list = [
        "マーリーの幽霊",
        "そもそも、マーリーは死んでいた。誰もいない",
        "それについては疑う余地はありません。彼の記録だ",
        "埋葬は牧師と事務員によって署名されました",
        "葬儀屋と主任会葬者スクルージ",
        "サインをして、スクルージの名前が好評だったんです",
        "「彼が選んだものは何でも変えなさい。",
        "オールド・マーリーはまるで釘のように死んでいた。",
        "「クリスマス・キャロル」",
        "チャールズ・ディケンズ",
    ]

    # 翻訳後画像パス
    overlay_translation_image_path = debug_directory_path + "/image_after.png"
