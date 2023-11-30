import threading  # スレッド関連
import tkinter as tk  # GUI

from package.error_log import ErrorLog  # エラーログに関するクラス


class GetDragAreaThread:
    """ドラッグした領域の座標を取得するスレッド"""

    # ドラッグ領域の座標を保存するクラス変数
    region = None

    def __init__(self, root):
        # 主要なウィンドウの設定
        self.root = root
        self.root.attributes("-alpha", 0.5)  # ウィンドウの透明度を設定
        self.root.attributes("-fullscreen", True)  # フルスクリーンモードでウィンドウを表示
        self.root.attributes("-topmost", True)  # ウィンドウを最前面に表示

        # Canvasの設定（ドラッグ範囲を表示するためのキャンバス）
        self.canvas = tk.Canvas(root, bg="black", bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

        # ドラッグ時の四角形と座標の初期値
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        # マウスイベントのバインド
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        # キーバインド
        # self.root.bind("<KeyPress>", self.on_key_press)

    def on_button_press(self, event):
        """マウスの左ボタンが押されたときのイベントハンドラ"""
        # ドラッグの開始地点を記録
        self.start_x = event.x_root
        self.start_y = event.y_root

        # まだ矩形がなければ、新しい矩形を作成
        if not self.rect:
            self.rect = self.canvas.create_rectangle(
                self.start_x,
                self.start_y,
                self.start_x,
                self.start_y,
                fill="white",
                outline="white",
            )

    def on_mouse_drag(self, event):
        """マウスがドラッグされている間のイベントハンドラ"""
        # 現在のマウスの座標を取得
        cur_x = event.x_root
        cur_y = event.y_root

        # 矩形のサイズを更新
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        """マウスの左ボタンが離されたときのイベントハンドラ"""
        # ドラッグの終了地点を記録
        self.end_x = event.x_root
        self.end_y = event.y_root

        # 座標を辞書にして保存
        self.get_region()

        # アプリケーションを終了
        self.root.quit()

        # アプリケーションを削除
        self.root.destroy()

    def get_region(self):
        """ドラッグの開始地点と終了地点の座標を辞書にして返す"""

        # ドラッグされたなら
        if self.start_x != self.end_x and self.start_y != self.end_y:
            # 座標をクラス変数に保存
            GetDragAreaThread.region = {
                "left": min(self.start_x, self.end_x),  # ドラッグ範囲の左側x座標
                "top": min(self.start_y, self.end_y),  # ドラッグ範囲の上側y座標
                "right": max(self.start_x, self.end_x),  # ドラッグ範囲の右側x座標
                "bottom": max(self.start_y, self.end_y),  # ドラッグ範囲の下側y座標
            }
        else:
            # 戻り値なし
            GetDragAreaThread.region = None

    @staticmethod  # スタティックメソッドの定義
    @ErrorLog.decorator  # エラーログを取得するデコレータ
    def run():
        """ドラッグした領域の座標を取得する

        Returns:
            GetDragAreaThread.region(dict{left, top, width, height})
                - スクリーンショット撮影範囲(クラス変数)
        """
        root = tk.Tk()
        app = GetDragAreaThread(root)
        root.mainloop()
        # ドラッグ領域の座標を返す
        # return cls.region
