class Class1:
    def decorator_with_args(arg1, arg2):
        def real_decorator(func):
            def wrapper(*args, **kwargs):
                print(f"デコレータの引数: {arg1}, {arg2}")
                return func(*args, **kwargs)

            return wrapper

        return real_decorator

    # @staticmethod  # スタティック(静的)メソッドの定義
    # def parameter_decorator(is_main_thread, event_window=None):  # デコレータの引数を取得する関数の宣言
    #     """デコレータの引数を取得する関数

    #     Args:
    #         is_main_thread (bool): メインスレッドかどうか
    #         window (sg.Window, None): ポップアップイベントを返すWindowオブジェクト
    #     """

    #     def decorator(func):  # デコレータ関数の宣言。
    #         """デコレータ関数。このデコレータを使用した関数は、'wrapper'関数に置き換えられる。

    #         Args:
    #             func (func): デコレートされる関数
    #         """

    #         def wrapper(*args, **kwargs):
    #             """デコレータの内部関数。任意の位置引数(*args)とキーワード引数(**kwargs)を受け取る。"""
    #             try:
    #                 # エラーログ作成
    #                 error_log = ErrorLog.create_error_log()
    #                 # 元の関数実行前の処理
    #                 func(*args, **kwargs)  # 元々のデコレートされる関数を実行
    #             # エラー発生時
    #             except Exception as e:
    #                 # エラーログの出力処理
    #                 ErrorLog.output_error_log(error_log, e, window)

    #         return wrapper  # デコレータの内部関数を返す。

    #     return decorator  # デコレータ関数を返す。


class Class2:
    @Class1.decorator_with_args(1, "引数2")
    def my_function(age1):
        print("関数が実行されました")


Class2.my_function(1)
