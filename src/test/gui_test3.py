import PySimpleGUI as sg
import os
from PIL import Image, ImageTk
import time
import threading


class Test:
    window_resize_thread_stop = False

    def __init__(self):
        """コンストラクタ 初期設定"""
        self.main()

    def resize_and_refresh_gui(self, image, user_zoom_scale):
        """画像のサイズを変更してウィンドウを更新する処理

        Args:
            image (Image): 拡大率を計算する元の画像オブジェクト
            user_zoom_scale (int): 利用者が変更できる拡大率
        """

        # スクロールバーの幅を含まないカラムサイズの計算
        column_size = [
            value - self.window["-COLUMN-"].metadata["scrollbar_width"]  # 全体のカラムサイズからスクロールバーの幅を引く
            for value in self.window["-COLUMN-"].get_size()  # 全体のカラムサイズを取得してその値で走査
        ]

        # 画像を与えられた範囲に収まるようにするための拡大率
        fit_zoom_scale = self.get_fit_zoom_scale(image, max_size=column_size)

        # 拡大率の計算
        zoom_scale = fit_zoom_scale * user_zoom_scale
        # 新しいサイズを計算
        new_size = (int(image.size[0] * zoom_scale), int(image.size[1] * zoom_scale))
        # 画像をリサイズ
        resized_img = image.resize(new_size, Image.LANCZOS)
        # GUIの画像要素を更新
        self.window["-IMAGE-"].update(data=ImageTk.PhotoImage(resized_img))
        # Columnのスクロール可能領域の更新
        self.window["-COLUMN-"].Widget.canvas.config(scrollregion=(0, 0, new_size[0], new_size[1]))
        self.window.refresh()  # ウィンドウを強制的に更新

    def get_fit_zoom_scale(self, image, max_size):
        """画像を与えられた範囲に収まるようにするための拡大率を取得

        Args:
            image (Image): 拡大率を計算する元の画像オブジェクト
            max_size (list[int, int]): 画像の最大サイズを指定する整数のリスト
                - max_width (int): 画像の最大幅
                - max_height (int): 画像の最大高さ

        Returns:
            fit_zoom_scale(int): 画像を与えられた範囲に収まるようにするための拡大率
        """

        # 拡大率の取得
        width_zoom_scale = max_size[0] / image.size[0]  # 表示サイズを超えない横幅の拡大率
        height_zoom_scale = max_size[1] / image.size[1]  # 表示サイズを超えない縦幅の拡大率
        fit_zoom_scale = min(width_zoom_scale, height_zoom_scale)  # 小さいほうの拡大率を適用

        return fit_zoom_scale  # 画像を与えられた範囲に収まるようにするための拡大率

    def main(self):
        # # 画像ファイルのパス
        # image_path = os.path.join(os.path.dirname(__file__), "test1.png")

        # # 画像を開く
        # image = Image.open(image_path)

        image_list = ["test1.png", "test2.png", "test3.png", "test4.png"]
        image_index = 0

        # 画像ファイルのパス
        image_path = os.path.join(os.path.dirname(__file__), image_list[image_index])

        # 画像を開く
        image = Image.open(image_path)

        # 表示サイズ
        START_COLUMN_SIZE = (128, 72)

        # スクロール可能なカラムレイアウトを作成
        column = [
            [
                sg.Image(
                    key="-IMAGE-",
                    enable_events=True,
                )
            ]
        ]

        # メインレイアウト
        layout = [
            [
                sg.Column(
                    layout=column,
                    key="-COLUMN-",
                    size=START_COLUMN_SIZE,
                    scrollable=True,  # スクロールバーの有効化
                    sbar_width=13,  # スクロールバーの幅
                    expand_x=True,  # 横方向に自動的に拡大
                    expand_y=True,  # 縦方向に自動的に拡大
                    size_subsample_width=1,  # スクロール可能な横の幅
                    size_subsample_height=1,  # スクロール可能な縦の幅
                    background_color="#888",  # 背景色
                    metadata={
                        "scrollbar_width": 15,  # スクロールバー用のスペース
                    },
                )
            ],
            [
                sg.Button("change", key="-change-", size=(6, 1)),
                # sg.Button("resize", key="-window_resize-", size=(6, 1)),
            ],
        ]

        # ウィンドウの作成
        self.window = sg.Window("スクロール可能な画像", layout, resizable=True, finalize=True)

        # ウィンドウサイズ変更イベントをバインド
        self.window.bind("<Configure>", "-window_resize-")

        # 利用者が変更できる拡大率
        user_zoom_scale = 1

        # 画像のサイズを変更してウィンドウを更新する処理
        self.resize_and_refresh_gui(image, user_zoom_scale)

        # 直前のカラムサイズの保存
        previous_column_size = self.window["-COLUMN-"].get_size()

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            # 画像のリサイズと更新
            if event == "-IMAGE-":
                # 利用者が変更できる拡大率
                if user_zoom_scale == 1:
                    user_zoom_scale = 2
                elif user_zoom_scale == 2:
                    user_zoom_scale = 4
                elif user_zoom_scale == 4:
                    user_zoom_scale = 1

                # 画像のサイズを変更してウィンドウを更新する処理
                self.resize_and_refresh_gui(image, user_zoom_scale)

            if event == "-change-":
                image_index = (image_index + 1) % len(image_list)
                # 画像ファイルのパス
                image_path = os.path.join(os.path.dirname(__file__), image_list[image_index])
                # 画像を開く
                image = Image.open(image_path)

                # 画像のサイズを変更してウィンドウを更新する処理
                self.resize_and_refresh_gui(image, user_zoom_scale)

            if event == "-window_resize-":
                # 現在のカラムサイズの取得
                current_column_size = self.window["-COLUMN-"].get_size()
                # 直前のカラムサイズと現在のカラムサイズが異なるなら
                if previous_column_size != current_column_size:
                    # 直前のカラムサイズの保存
                    previous_column_size = current_column_size

                    # 画像のサイズを変更してウィンドウを更新する処理
                    self.resize_and_refresh_gui(image, user_zoom_scale)
                    print("ウィンドウ更新")

        self.window.close()


if __name__ == "__main__":
    Test()
