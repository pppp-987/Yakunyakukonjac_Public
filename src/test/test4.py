import os
from datetime import datetime, timedelta  # 日時
import time


class Fn:
    def get_now_file_base_name():
        """ファイルのベース名用現在時刻の取得
        Returns:
            now_file_base_name(str) : ファイルのベース名用現在時刻("yyyymmdd_hhmmss")
        """
        now = datetime.now()  # 現在の時刻を取得
        now_file_base_name = now.strftime("%Y%m%d_%H%M%S")  # 時刻の表示
        return now_file_base_name  # ファイルのベース名用現在時刻

    def convert_time_from_filename(file_name):
        """ファイル名から日時を取得

        Args:
            file_name (str): ファイル名("yyyymmdd_hhmmss.拡張子")

        Returns:
            file_time (str): 日時("%Y/%m/%d %H:%M:%S")
        """
        # ファイルのベース名の取得
        file_base_name = file_name.split(".")[0]
        # "yyyymmdd_hhmmss"の形式の文字列を解析してdatetimeオブジェクトに変換
        dt = datetime.strptime(file_base_name, "%Y%m%d_%H%M%S")

        # "%Y/%m/%d %H:%M:%S"の形式にフォーマット
        file_time = dt.strftime("%Y/%m/%d %H:%M:%S")
        return file_time  # 日時("%Y/%m/%d %H:%M:%S")

    def convert_filename_from_time(file_time):
        """日時からファイル名を取得

        Args:
            file_time (str): 日時("%Y/%m/%d %H:%M:%S")

        Returns:
            file_name (str): ファイル名("yyyymmdd_hhmmss.拡張子")
        """
        # "%Y/%m/%d %H:%M:%S"の形式の文字列を解析してdatetimeオブジェクトに変換
        dt = datetime.strptime(file_time, "%Y/%m/%d %H:%M:%S")
        # "yyyymmdd_hhmmss"の形式にフォーマット
        file_base_name = dt.strftime("%Y%m%d_%H%M%S")
        # 拡張子の取得
        image_file_extension = ".png"
        # ファイル名の取得
        file_name = file_base_name + image_file_extension

        return file_name  # ファイル名("yyyymmdd_hhmmss.拡張子")

    def check_file_limits(directory_path, max_size_mb, max_file_count, max_days):
        """指定された制限を超えているかどうかをチェックして結果を返すメソッド

        Args:
            directory_path (str): ディレクトリパス
            max_file_size_mb (int): 最大保存容量(MB)
            max_file_count (int): 最大保存枚数
            max_file_retention_days (int): 最大保存期間(日)

        Returns:
            check_file_limit_dict(dict{file_name:bool})
                - 指定された制限を超えているかどうかを保存する辞書
        """
        # ファイル名のリストを降順で取得
        file_name_list = sorted(os.listdir(directory_path), reverse=True)

        # .gitkeepが存在するなら削除する
        if ".gitkeep" in file_name_list:
            file_name_list.remove(".gitkeep")

        # ファイル数
        file_count = 0

        # 現在の日付の取得
        now_date = datetime.now()

        # 履歴を保存する最も古い日時の取得
        oldest_date = now_date - timedelta(days=max_days)

        # 合計サイズ
        total_size_kb = 0

        # 指定された制限を超えているかどうかを保存する辞書
        check_file_limit_dict = {}

        # 指定された制限を超えたかどうか
        is_limit_over = False

        # ファイルごとに確認
        for file_name in file_name_list:
            if not is_limit_over:
                # 指定された制限を超えていないなら
                # ファイル数の加算
                file_count += 1

                # ファイルのベース名の取得
                file_base_name = file_name.split(".")[0]
                # datetimeオブジェクトの取得
                file_date = datetime.strptime(file_base_name, "%Y%m%d_%H%M%S")

                # ファイルサイズの取得
                file_size = os.path.getsize(directory_path + file_name) / (1024)

                # 合計サイズの
                total_size_kb += int(file_size) + 1

                # 指定された制限を超えているかどうかの情報をまとめた辞書
                file_limit_info_dict = {
                    # ファイルサイズがオーバーしているかどうか
                    "is_file_size_over": total_size_kb > max_size_mb * 1024,
                    # ファイル数がオーバーしているかどうか
                    "is_file_count_over": file_count > max_file_count,
                    # ファイル保存期間がオーバーしているかどうか
                    "is_file_time_over": file_date < oldest_date,
                }

                if True not in file_limit_info_dict.values():
                    # 指定された制限を超えているかどうかを保存
                    check_file_limit_dict[file_name] = False
                else:
                    # 指定された制限を超えたかどうか
                    is_limit_over = True
                    # 指定された制限を超えているかどうかを保存
                    check_file_limit_dict[file_name] = True
            else:
                # 指定された制限を超えているなら
                # 指定された制限を超えているかどうかを保存
                check_file_limit_dict[file_name] = True

        # 指定された制限を超えているかどうかを保存する辞書
        return check_file_limit_dict


package_path = os.path.dirname(__file__) + "/"  # パッケージディレクトリパス
# デバッグ用ディレクトリパス
debug_directory_path = package_path + "../debug_history/"

history_directory_path = package_path + "../history/"  # 履歴ディレクトリパス

# 翻訳前画像保存先設定
image_before_directory_path = history_directory_path + "image_before/"  # ディレクトリパス


directory_path = image_before_directory_path
# file_name_list = os.listdir(debug_directory_path)

print(Fn.check_file_limits(directory_path, 0.25, 2, 2))

# print(file_name_list)

# # ファイルサイズを取得
# file_size = os.path.getsize(debug_directory_path)

# # byteをKBに変換して小数点以下2位に四捨五入
# file_size = round(file_size / 1024, 2)

# print(file_size)


# for file_name in file_name_list:
#     file = debug_directory_path + file_name
#     # ファイルサイズを取得
#     file_size = os.path.getsize(file)

#     # byteをKBに変換して小数点以下2位に四捨五入
#     file_size = round(file_size / 1024, 2)

#     print(file_name, file_size)
