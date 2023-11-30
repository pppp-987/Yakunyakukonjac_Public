import os  # ディレクトリ管理
import sys  # システム関連

# 翻訳されたテキストを日本語で表示するためにフォントとサイズを指定
from PIL import Image, ImageDraw, ImageFont

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.debug import Debug  # デバッグ用クラス
from package.fn import Fn  # 自作関数クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス


class TranslationImage:
    """オーバーレイ翻訳画像作成機能関連のクラス"""

    def get_overlay_translation_image(user_setting, ss_file_path, text_after_list, text_region_list):
        """オーバーレイ翻訳画像の取得

        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            ss_file_path(str): スクショ画像のファイルパス
            text_after_list(List[text_after(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲

        Returns:
            overlay_translation_image(Image): オーバーレイ翻訳画像
        """

        image_out = Image.open(ss_file_path)  # 出力画像を作成

        draw = ImageDraw.Draw(image_out)  # 画像に図形やテキストを描画するオブジェクトの作成

        # 言語情報一覧リストの取得
        language_list = SystemSetting.language_list
        # 翻訳後言語の取得
        target_language_code = user_setting.get_setting("target_language_code")
        # フォントパスの取得
        font_path = Fn.search_dict_in_list(language_list, "code", target_language_code)["font_path"]

        # フォントサイズの計算
        font_size_list = TranslationImage.find_max_font_size(font_path, text_after_list, text_region_list)

        # フォントサイズが0である要素の削除
        TranslationImage.remove_empty_text_data(font_size_list, text_after_list, text_region_list)

        # 画像内のテキストボックスを塗りつぶす処理
        TranslationImage.fill_text_box_image(draw, text_region_list)

        # 画像にテキストを描画する処理
        TranslationImage.draw_text_image(draw, font_path, text_after_list, text_region_list, font_size_list)

        return image_out

    def get_font_ja_size_list(font_path, text_after_list, text_region_list):
        """日本語フォントサイズのリストの取得

        Args:
            font_path(str) : フォントファイルのパス
            text_after_list(List[text_after(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲

        Returns:
            font_size_list (list[font_size]): フォントサイズのリスト
                - font_size(int): フォントサイズ(偶数)
        """
        font_size_list = []  # フォントサイズのリスト
        # ブロックごとに走査
        for text_after, text_region in zip(text_after_list, text_region_list):
            max_w_font_size = text_region["width"] // len(text_after)  # 横の最大フォントサイズ
            max_h_font_size = text_region["height"]  # 縦の最大フォントサイズ

            font_size = min(max_w_font_size, max_h_font_size)  # 最大フォントサイズが小さい方に設定する

            # フォントサイズが偶数になるように処理
            if font_size % 2 == 1:  # フォントサイズが奇数なら
                font_size -= 1  # フォントサイズを1小さくする

            font_size_list.append(font_size)  # フォントサイズの保存
        return font_size_list  # フォントサイズのリスト

    def find_max_font_size(font_path, text_after_list, text_region_list):
        """テキストボックスに収まる最大のフォントサイズのリストの取得

        日本語以外のフォントに使用

        Args:
            font_path(str) : フォントファイルのパス
            text_after_list(List[text_after(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲

        Returns:
            font_size_list (list[font_size]): 最大のフォントサイズのリスト
                - font_size(int): 最大のフォントサイズ(偶数)
        """
        font_size_list = []  # フォントサイズのリスト
        # ブロックごとに走査
        for text_after, text_region in zip(text_after_list, text_region_list):
            if text_after is not None:
                # 翻訳後テキストが存在するなら
                # テキストボックスの幅と高さを取得
                text_box_width = text_region["width"]
                text_box_height = text_region["height"]

                font_size = 2  # フォントサイズの初期値
                font_image = ImageFont.truetype(font_path, font_size)  # フォントオブジェクトの作成

                # テキストボックスと同じサイズの、テキスト描画用イメージオブジェクトを作成
                image = Image.new("RGB", (text_box_width, text_box_height))
                # 画像に図形やテキストを描画するオブジェクトの作成
                draw = ImageDraw.Draw(image)

                while True:
                    # 指定したフォントサイズでテキストのバウンディングボックスを計算
                    font_image = font_image.font_variant(size=font_size)  # フォントサイズの更新
                    # テキスト範囲の取得
                    now_text_region = draw.textbbox((0, 0), text=text_after, font=font_image)
                    # 現在のフォントでのテキストサイズの取得
                    now_text_width = now_text_region[2] - now_text_region[0]  # テキストサイズの横幅取得
                    # テキストサイズの縦幅
                    # ? 欧米文字などは文字によって縦幅が違う
                    now_text_height = font_size * 1.5  # テキストサイズの横幅取得

                    if now_text_width < text_box_width and now_text_height < text_box_height:
                        # テキストボックスに収まらないなら
                        font_size += 2
                    else:
                        # テキストボックスに収まるなら
                        font_size_list.append(font_size - 2)  # 収まるサイズに戻して保存
                        break

        return font_size_list  # テキストボックスに収まる最大のフォントサイズのリスト

    def remove_empty_text_data(font_size_list, text_after_list, text_region_list):
        """フォントサイズが0である要素の削除

        Args:
            font_size_list (list[font_size]): 最大のフォントサイズのリスト
                - font_size(int): 最大のフォントサイズ(偶数)
            text_after_list(List[text_after(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
        """
        # フォントサイズが0である要素番号のリストの取得
        zero_font_size_index_list = [index for index, font_size in enumerate(font_size_list) if font_size == 0]

        # フォントサイズが0である要素番号で走査（削除後の要素番号のずれを防ぐために逆順にソート）
        for delete_index in zero_font_size_index_list[::-1]:
            # フォントサイズが0の要素を削除
            del font_size_list[delete_index]
            del text_after_list[delete_index]
            del text_region_list[delete_index]

    def fill_text_box_image(draw, text_region_list):
        """画像内のテキストボックスを塗りつぶす処理

        Args:
            draw (ImageDraw): 画像に図形やテキストを描画するオブジェクト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
        """
        background_color = "#FFF"  # 背景色
        background_border_color = "#FFF"  # 背景の枠線の色

        # ブロックごとに走査
        for text_region in text_region_list:
            # テキストボックスの背景の描画
            draw.rectangle(
                # 背景描画座標
                xy=(
                    text_region["left"],  # テキストボックスの左側x座標の取得
                    text_region["top"],  # テキストボックスの上側y座標の取得
                    text_region["left"] + text_region["width"],  # テキストボックスの右側x座標の取得
                    text_region["top"] + text_region["height"],  # テキストボックスの下側y座標の取得
                ),
                fill=background_color,  # 背景色
                outline=background_border_color,  # 背景の枠線の色
            )

    def draw_text_image(draw, font_path, text_after_list, text_region_list, font_size_list):
        """画像にテキストを描画する処理

        Args:
            draw (ImageDraw): 画像に図形やテキストを描画するオブジェクト
            font_path(str) : フォントファイルのパス
            text_after_list(List[text_after(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
            font_size_list (list[font_size]): フォントサイズのリスト
        """
        font_color = "#000"  # フォントカラー

        # ブロックごとに走査
        for text_after, text_region, font_size in zip(
            text_after_list,  # 翻訳語テキスト内容のリスト
            text_region_list,  # テキスト範囲のリスト
            font_size_list,  # フォントサイズのリスト
        ):
            if text_after is not None:
                # 翻訳後テキストが存在するなら
                # フォントの設定
                font_image = ImageFont.truetype(font_path, font_size)

                # 翻訳されたテキストを指定した座標に描画
                draw.text(
                    (text_region["left"], text_region["top"]),
                    text_after,
                    fill=font_color,
                    font=font_image,
                )

    def save_overlay_translation_image(overlay_translation_image, file_name):
        """オーバーレイ翻訳画像の保存
        Args:
            overlay_translation_image(Image): オーバーレイ翻訳画像
            file_name(src): ファイル名(撮影日時)
        Returns:
            overlay_translation_image_path(str): オーバーレイ翻訳画像のファイルパス
        """
        directory_path = SystemSetting.image_after_directory_path  # 翻訳後画像のディレクトリパス
        overlay_translation_image_path = os.path.join(directory_path, file_name)  # ファイルパス(絶対参照)

        overlay_translation_image.save(overlay_translation_image_path)  # 翻訳後画像保存

        return overlay_translation_image_path  # 翻訳後画像ファイルパス


# ! デバッグ用
if __name__ == "__main__":
    user_setting = UserSetting()  # ユーザ設定のインスタンス化
    ss_file_path = Debug.ss_file_path  # スクショ画像パス
    text_after_list = Debug.text_before_list  # 翻訳後テキストリスト
    text_region_list = Debug.text_region_list  # テキスト範囲のリスト

    # オーバーレイ翻訳画像の取得
    overlay_translation_image = TranslationImage.get_overlay_translation_image(
        user_setting, ss_file_path, text_after_list, text_region_list
    )
    # オーバーレイ翻訳画像の表示
    overlay_translation_image.show()
