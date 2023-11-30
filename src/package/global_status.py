class GlobalStatus:
    """グローバル変数保存用クラス"""

    win_instance = None  # 現在開いているウィンドウクラスのインスタンス
    is_main_thread_running = True  # メインスレッドが実行中かどうか
    is_sub_thread_error = False  # サブスレッドでエラーが発生したかどうか
    sub_thread_error_message = ""  # サブスレッドでエラー発生時の表示エラーメッセージ
