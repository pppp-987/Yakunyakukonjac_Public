import datetime  # 現在時刻
import os  # ディレクトリ関連

import boto3  # AWSのAIサービス
import easyocr  # OCRライブラリ

from PIL import Image  # 画像処理


def easy_ocr(ss_file_path):
    """EasyOCRを使用して画像からテキスト情報を取得
    Args:
        user_setting(UserSetting): ユーザーが変更可能の設定
        ss_file_path(src): スクショ画像のファイルパス

    Returns:
        text_data_dict(List[text_list,text_region_list]): テキスト情報リスト
            - text_list(List[text(str)]) : テキスト内容のリスト
            - text_region_list(List[region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
    """
    ocr_lang_list = ["zh"]  # 抽出する言語のリスト

    text_list = []  # テキスト内容のリスト
    text_region_list = []  # テキスト範囲のリスト

    # ! NVIDIAのGPUの場合、処理速度高速
    reader = easyocr.Reader(lang_list=ocr_lang_list)  # OCRの作成
    result = reader.readtext(ss_file_path)  # # 画像内のテキストを抽出する

    # 段落ごとに走査
    for text_box in result:
        # テキスト範囲の取得
        text_region = {
            "left": int(text_box[0][0][0]),  # テキスト範囲の左側x座標
            "top": int(text_box[0][0][1]),  # テキスト範囲の上側y座標
            "width": int(text_box[0][2][0]) - int(text_box[0][0][0]),  # テキスト範囲の横幅
            "height": int(text_box[0][2][1]) - int(text_box[0][0][1]),  # テキスト範囲の縦幅
        }
        text = text_box[1]  # テキスト内容の取得
        # confidence = text_box[2] # 信頼度の取得

        text_list.append(text)  # テキスト内容のリスト
        text_region_list.append(text_region)  # テキスト範囲のリスト

    # テキスト情報のリスト作成
    text_data_list = {
        "text_list": text_list,  # テキスト内容のリスト
        "text_region_list": text_region_list,  # テキスト範囲のリスト
    }

    return text_data_list  # テキスト情報のリスト


image_path = os.path.dirname(__file__) + "/ch_sim.png"
print(easy_ocr(image_path)["text_list"])
