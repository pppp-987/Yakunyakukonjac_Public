import os  # オペレーティングシステム関連
import sys  # システム関連

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス


class Debug:
    """デバッグ用クラス"""

    # デバッグ用ディレクトリパス
    debug_directory_path = SystemSetting.debug_directory_path

    # 翻訳前画像パス
    ss_file_path = os.path.join(debug_directory_path, "image_before.png")

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
    overlay_translation_image_path = os.path.join(debug_directory_path, "image_after.png")

    def create_text_image(size, text, font_path, font_size, image_save_path):
        """テキストを描画した画像を作成、保存する処理

        Args:
            size (Tuple[int, int]): 画像のサイズを指定するタプル
                - width (int): 画像の幅
                - height (int): 画像の高さ
            text (str): 描画するテキスト
            font_path (str): フォントパス
            font_size (int): フォントサイズ
            image_save_path (str): 作成された画像を保存するパス
        """

        width, height = size  # 画像のサイズ
        background_color = "#FFF"  # 背景色

        # 新しい画像を作成
        image = Image.new("RGB", (width, height), background_color)
        # 画像に図形やテキストを描画するオブジェクトの作成
        draw = ImageDraw.Draw(image)

        # フォントの設定
        font_color = "#000"
        font_image = ImageFont.truetype(font_path, font_size)

        # テキストを描画する領域サイズの取得
        text_bbox = draw.textbbox((0, 0), text, font_image)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # テキスト位置の計算
        text_x = (width - text_width) / 2
        text_y = (height - text_height) / 2

        # テキストの描画
        draw.text((text_x, text_y), text, fill=font_color, font=font_image)

        # 画像の保存
        image.save(image_save_path)

        # 画像の表示
        # image.show()


# ! デバッグ用
if __name__ == "__main__":
    # 翻訳されたテキストを日本語で表示するためにフォントとサイズを指定
    from PIL import Image, ImageDraw, ImageFont

    # OCRで動作チェックに使用する画像を画像を作成、保存
    Debug.create_text_image(
        size=(256, 144),
        text="Hello world",
        font_path=SystemSetting.font_Segoe_path,  # 欧文フォント
        font_size=40,
        image_save_path=SystemSetting.check_ocr_image_path,  # OCRの動作チェックに使用する画像ファイルの保存場所
    )
    # OCRで動作チェックに使用する画像を画像を作成、保存
    Debug.create_text_image(
        size=(256, 144),
        text="No history found",
        font_path=SystemSetting.font_Segoe_path,  # 欧文フォント
        font_size=30,
        image_save_path=SystemSetting.default_image_before_path,  # デフォルトの翻訳前画像ファイル
    )
