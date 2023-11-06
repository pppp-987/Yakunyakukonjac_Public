import logging
import sys
import traceback
import inspect


class MessageFilter(logging.Filter):
    """
    メッセージが指定した内容と一致する場合のみ通過させるフィルター。
    """

    def __init__(self, message):
        super().__init__()
        self.message = message

    def filter(self, record):
        return record.getMessage() == self.message


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# ログの出力フォーマットを設定
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


# 詳細なログを出力するためのハンドラ
detailed_log_file_handler = logging.FileHandler("detailed_app.log", encoding="utf-8")
detailed_log_file_handler.setLevel(logging.DEBUG)
detailed_log_file_handler.setFormatter(formatter)
logger.addHandler(detailed_log_file_handler)

# シンプルなログを出力するためのハンドラ
simple_log_file_handler = logging.FileHandler("simple_app.log", encoding="utf-8")
simple_log_file_handler.setLevel(logging.ERROR)
simple_log_file_handler.setFormatter(formatter)
# このハンドラにフィルターを追加
simple_log_file_handler.addFilter(MessageFilter("エラー発生"))
logger.addHandler(simple_log_file_handler)

try:
    # ここで何らかのエラーを発生させます
    x = 1 / 0

except Exception as e:
    logger.exception("エラー発生")
