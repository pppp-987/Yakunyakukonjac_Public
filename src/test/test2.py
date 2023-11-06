class BaseTest:
    @staticmethod  # スタティック(静的)メソッドの定義
    def parameter_decorator(arg1=None):  # デコレータの引数を取得する関数の宣言
        def decorator(func):  # デコレータ関数の宣言。
            """デコレータ関数。このデコレータを使用した関数は、'wrapper'関数に置き換えられる。

            Args:
                func (func): デコレートされる関数
            """

            def wrapper(*args, **kwargs):
                """デコレータの内部関数。任意の位置引数(*args)とキーワード引数(**kwargs)を受け取る。"""
                print("start")
                print(args)
                print(kwargs)
                # 元の関数実行前の処理
                func(*args, **kwargs)  # 元々のデコレートされる関数を実行
                # 元の関数実行後の処理
                # print("end")

            return wrapper  # デコレータの内部関数を返す。

        return decorator  # デコレータ関数を返す。


class Test1:
    @staticmethod
    @BaseTest.parameter_decorator()
    def run():
        a = 1
        # 複雑な処理部分
        print(1)


class Test2:
    @staticmethod
    @BaseTest.parameter_decorator()
    def run(i1):
        a = 1
        # 複雑な処理部分
        print(2)


class Test3:
    @staticmethod
    @BaseTest.parameter_decorator()
    def run(i1):
        a = 1
        # 複雑な処理部分
        print(3)


class Test4:
    @staticmethod
    @BaseTest.parameter_decorator()
    def run(i1, i2):
        a = 1
        # 複雑な処理部分
        print(4)


Test1.run()
Test2.run(1)
Test3.run(i1=1)
Test4.run(1, i2=2)
