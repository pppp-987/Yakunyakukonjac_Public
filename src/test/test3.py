import PySimpleGUI as sg

import traceback


def error_popup(e, is_output_error_log):
    """エラー発生ポップアップの作成

    Args:
        e (Exception): 例外
        is_output_error_log(bool): エラーログの出力に成功したかどうか
    """
    # メッセージの作成
    # エラーログファイルの出力に成功したなら
    if is_output_error_log:
        message = [
            "申し訳ありません、エラーが発生しました。",
            f"エラーメッセージ: {str(e)}",
            "エラーログファイルが作成されました。",
            "管理者にこのファイルを提供していただけると幸いです。",
        ]
    # エラーログファイルの出力に失敗したなら
    else:
        message = [
            "申し訳ありません、エラーが発生しました。",
            f"エラーメッセージ: {str(e)}",
            "エラーログファイルの作成に失敗しました。",
            "管理者に問題を報告していただけると幸いです。",
        ]
    # ポップアップの作成
    sg.popup("\n".join(message))


import traceback
import inspect


try:
    # ここで何らかの例外を発生させるためのサンプルコード
    x = 1 / 0
except Exception as e:
    error_popup(e, True)
