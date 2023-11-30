# 言語情報一覧リスト{日本語表記、英語表記、言語コード(ISO 639-1),フォントパス}
language_list = [
    {"ja_text": "アラビア語", "en_text": "Arabic", "code": "ar", "font_path": "font_Segoe_path"},
    {
        "ja_text": "中国語",
        "en_text": "Chinese",
        "code": "zh-CN",
        "font_path": "font_MicrosoftYaHei_path",
    },
    {"ja_text": "英語", "en_text": "English", "code": "en", "font_path": "font_Segoe_path"},
    {"ja_text": "フランス語", "en_text": "French", "code": "fr", "font_path": "font_Segoe_path"},
    {"ja_text": "ドイツ語", "en_text": "German", "code": "de", "font_path": "font_Segoe_path"},
    {"ja_text": "イタリア語", "en_text": "Italian", "code": "it", "font_path": "font_Segoe_path"},
    {"ja_text": "日本語", "en_text": "Japanese", "code": "ja", "font_path": "font_YuGothic_path"},
    {"ja_text": "韓国語", "en_text": "Korean", "code": "ko", "font_path": "font_MalgunGothic_path"},
    {"ja_text": "ポルトガル語", "en_text": "Portuguese", "code": "pt", "font_path": "font_Segoe_path"},
    {"ja_text": "ロシア語", "en_text": "Russian", "code": "ru", "font_path": "font_Segoe_path"},
    {"ja_text": "スペイン語", "en_text": "Spanish", "code": "es", "font_path": "font_Segoe_path"},
]

# EasyOCR用の言語コード(ISO 639-2)のリスト((ISO 639-1):(ISO 639-2))
easy_ocr_language_code = {"zh-CN": "ch_sim"}

# 言語情報一覧リストから言語コードのリストを作成
easy_ocr_language_code_list = [language_info["code"] for language_info in language_list]

# EasyOCR用の言語コードに変更する
for before_code, after_code in easy_ocr_language_code.items():
    # 更新箇所の要素番号の取得
    index = easy_ocr_language_code_list.index(before_code)
    # 言語コードの更新
    easy_ocr_language_code_list[index] = after_code

print(easy_ocr_language_code_list)
