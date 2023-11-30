import os  # ディレクトリ関連
import re  # 正規表現
import subprocess  # 新しいプロセスを生成し、その入出力を管制するためのモジュール
import sys  # Pythonのインタプリタや環境にアクセスするためのモジュール（引数の取得、システムパスの操作など）
import time  # 時間測定
from datetime import datetime, timedelta  # 日時, 時間差

from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス


class Fn:
    """自作関数クラス
    全体に適応される"""

    def sleep(ms):
        """指定された時間だけプログラムを一時停止

        Args:
            ms (int): 停止時間(ミリ秒)
        """
        time.sleep(ms / 1000)

    def log(*text):
        """ログの表示
            デバッグモードでのみ動作する
        Args:
            text (*str): 出力文字
        """
        if SystemSetting.debug:  # デバッグモードなら
            if len(text) == 1:
                # 要素数が1なら文字列にする
                print(text[0])
            else:
                # 要素数が2以上ならタプルにする
                print(text)

    def time_log(*text):
        """ログと現在時刻の表示
            デバッグモードでのみ動作する
        Args:
            text (*str): 出力文字
        """
        if SystemSetting.debug:  # デバッグモードなら
            now = datetime.now()  # 現在の時刻を取得
            if len(text) == 1:
                # 要素数が1なら文字列にする
                print(text[0], now.strftime("%H:%M:%S.%f")[:-3])  # 時刻の表示（ミリ秒三桁まで）
            else:
                # 要素数が2以上ならタプルにする
                print(text, now.strftime("%H:%M:%S.%f")[:-3])  # 時刻の表示（ミリ秒三桁まで）

    def check_number_string(value):
        """数字文字列かどうかを判定する

        Args:
            value (str): 判定する文字列

        Returns:
            is_valid_number_string(bool): 数字文字列かどうか
        """

        # 文字列が数字のみで構成され、かつ少なくとも1文字以上の数字を含むかどうかを返す
        return bool(re.match(r"^[0-9]+$", value))

    def get_now_file_base_name():
        """ファイルのベース名用現在時刻の取得
        Returns:
            now_file_base_name(str) : ファイルのベース名用現在時刻("yyyymmdd_hhmmss")
        """
        now = datetime.now()  # 現在の時刻を取得
        now_file_base_name = now.strftime("%Y%m%d_%H%M%S")  # 時刻の表示
        return now_file_base_name  # ファイルのベース名用現在時刻

    def save_text_file(text_list, file_path):
        """テキストファイルへの保存
        Args:
            text_list(list[text:str]): テキストリスト
            filepath(src): ファイルパス
        """
        file = open(file_path, "w", encoding="utf-8")  # 新規書き込みでテキストファイルを開く
        # file = open(text_filepath, "w",)  # 新規書き込みでテキストファイルを開く
        for text_before in text_list:  # テキストで走査
            if text_before is not None:
                # テキストが存在するなら
                file.write(text_before + "\n")  # ファイルに書き込む
        file.close()  # ファイルを閉じる

    def get_max_file_name(dir_path):
        """辞書順で最大のファイル名を取得
        Args:
            dir_path (str): ディレクトリパス

        Returns:
            max_file_name: 辞書順で最大のファイル名
        """
        file_list = os.listdir(dir_path)  # ファイル名のリストを取得
        max_file_name = max(file_list)  # 辞書順で最大のファイル名を取得
        return max_file_name  # 辞書順で最大のファイル名

    def get_history_file_name_list():
        """履歴ファイル名のリストを取得

        翻訳前、後画像の両方が存在する履歴ファイル名を取得
        存在しない、もしくは、ファイル名の形式が正しくない場合、該当ファイルを削除

        Returns:
            history_file_name_list(list[file_name:str]): 履歴ファイル名のリスト
        """

        # 翻訳前画像保存先設定
        image_before_directory_path = SystemSetting.image_before_directory_path  # ディレクトリパス

        # 翻訳後画像保存先設定
        image_after_directory_path = SystemSetting.image_after_directory_path  # ディレクトリパス

        # 翻訳前画像ファイル名のリスト
        before_file_name_list = os.listdir(image_before_directory_path)
        # 翻訳後画像ファイル名のリスト
        after_file_name_list = os.listdir(image_after_directory_path)

        # .gitkeepが存在する場合、ファイル名のリストから削除する
        if ".gitkeep" in before_file_name_list:
            before_file_name_list.remove(".gitkeep")
        if ".gitkeep" in after_file_name_list:
            after_file_name_list.remove(".gitkeep")

        # 集合型に変換
        before_file_name_set = set(before_file_name_list)
        after_file_name_set = set(after_file_name_list)

        # 共通要素の取得
        common_file_name_set = before_file_name_set & after_file_name_set

        # 履歴ファイル名のリストを取得
        history_file_name_list = list(common_file_name_set)

        # 昇順に並び替え
        history_file_name_list.sort()

        # 履歴ファイル名のリスト
        return history_file_name_list

    def get_history_file_time_list(history_file_name_list):
        """履歴ファイル日時のリストを取得

        Args:
            history_file_name_list(list[file_name:str]): 履歴ファイル名のリスト

        Returns:
            history_file_time_list(list[file_timr:str]): 履歴ファイル日時のリスト
        """
        # 履歴ファイル日時のリスト取得
        history_file_time_list = []
        for file_name in history_file_name_list:
            # ファイル名から日時を取得
            file_time = Fn.convert_time_from_filename(file_name)
            history_file_time_list.append(file_time)
        return history_file_time_list  # 履歴ファイル日時のリスト

    def delete_unique_history_file():
        """翻訳前、後画像の両方が存在しない履歴ファイルを削除"""
        # 翻訳前画像保存先設定
        image_before_directory_path = SystemSetting.image_before_directory_path  # ディレクトリパス

        # 翻訳後画像保存先設定
        image_after_directory_path = SystemSetting.image_after_directory_path  # ディレクトリパス

        # 翻訳前画像ファイル名のリスト
        before_file_name_list = os.listdir(image_before_directory_path)
        # 翻訳後画像ファイル名のリスト
        after_file_name_list = os.listdir(image_after_directory_path)

        # .gitkeepが存在する場合、ファイル名のリストから削除する
        if ".gitkeep" in before_file_name_list:
            before_file_name_list.remove(".gitkeep")
        if ".gitkeep" in after_file_name_list:
            after_file_name_list.remove(".gitkeep")

        # 集合型に変換
        before_file_name_set = set(before_file_name_list)
        after_file_name_set = set(after_file_name_list)

        # 共通要素の取得
        common_file_name_set = before_file_name_set & after_file_name_set

        # 片方のみに存在する要素の取得
        before_only_file_name_set = before_file_name_set - common_file_name_set  # 翻訳前画像のみのファイル名の取得
        after_only_file_name_set = after_file_name_set - common_file_name_set  # 翻訳後画像のみのファイル名の取得

        # 翻訳前画像のみのファイルの削除
        for before_file_name in before_only_file_name_set:
            os.remove(os.path.join(image_before_directory_path, before_file_name))
        # 翻訳後画像のみのファイルの削除
        for after_file_name in after_only_file_name_set:
            os.remove(os.path.join(image_after_directory_path, after_file_name))

        # ファイル名の形式が正しくないファイル名のリスト
        invalid_file_name_list = []

        # 共通要素からファイル名を取得
        for file_name in common_file_name_set:
            # 正規表現で"yyyymmdd_hhmmss.拡張子"の形式に一致するかチェック
            match = re.match(r"^(\d{8})_(\d{6})\..+$", file_name)
            if not match:
                # 形式がただしくないなら
                # ファイル名の形式が正しくないファイル名を保存
                invalid_file_name_list.append(file_name)

            # ファイルのベース名の取得
            file_base_name = file_name.split(".")[0]

            # 日付と時刻の形式が正しいかチェック
            try:
                # "yyyymmdd_hhmmss"の形式の文字列を解析してdatetimeオブジェクトに変換
                dt = datetime.strptime(file_base_name, "%Y%m%d_%H%M%S")
            except ValueError:
                # ファイル名の形式が正しくないファイル名を保存
                invalid_file_name_list.append(file_name)

        # ファイル名の形式が正しくないファイルの削除
        for file_name in invalid_file_name_list:
            # 翻訳前画像フォルダから削除
            os.remove(os.path.join(image_before_directory_path, file_name))
            # 翻訳後画像フォルダから削除
            os.remove(os.path.join(image_after_directory_path, file_name))

    def search_dict_in_list(lst, key_name, value):
        """与えられたリスト内の辞書から指定したキーと値に一致する辞書を取得

        Args:
            lst (list of dict): 検索対象の辞書要素が格納されたリスト
            key_name (str): 検索に使用するキーの名前
            value (任意の型) 検索する値

        Returns:
            dict: 一致する辞書（最初に見つかったもの）
        """

        for item in lst:  # リストから辞書を取り出す
            if item[key_name] == value:
                # 辞書のキーと値が一致するなら一致する辞書を返す
                return item

    def check_file_limits(directory_path, max_file_size_mb, max_file_count, max_file_retention_days):
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
        oldest_date = now_date - timedelta(days=max_file_retention_days)

        # 最大サイズ
        # KBに直した上で、翻訳前、翻訳後の2つのディレクトリがあるので、1/2にする
        max_file_size_kb = max_file_size_mb * 1024 / 2

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
                file_size = os.path.getsize(os.path.join(directory_path, file_name)) / (1024)

                # 合計サイズの
                total_size_kb += file_size + 1

                # 指定された制限を超えているかどうかの情報をまとめた辞書
                file_limit_info_dict = {
                    # ファイルサイズがオーバーしているかどうか
                    "is_file_size_over": total_size_kb > max_file_size_kb,
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
                    # is_limit_over = True
                    # 指定された制限を超えているかどうかを保存
                    check_file_limit_dict[file_name] = True
            else:
                # 指定された制限を超えているなら
                # 指定された制限を超えているかどうかを保存
                check_file_limit_dict[file_name] = True

        # 指定された制限を超えているかどうかを保存する辞書
        return check_file_limit_dict

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

    @staticmethod  # スタティック(静的)メソッド
    def command_run(command_list, file_path=None):
        """与えられたコマンドのリストを実行する

        Args:
            command_list (list[command:str]): 実行するコマンドのリスト。
            file_path (str, optional): 結果を書き込むファイルのパス。デフォルトではNone（ファイルへの書き込みは行われない）。

        """

        # 結果を書き込むファイルのパスが指定されている場合、そのファイルに出力する
        if file_path is not None:
            with open(file_path, "w") as f:  # 指定されたファイルを書き込みモードで開く
                subprocess.run(
                    args=command_list,  # コマンドのリスト
                    check=True,  # 終了コードが0以外の時に例外を起こす
                    stdout=f,  # 外部コマンドの標準出力のリダイレクト先
                    creationflags=subprocess.CREATE_NO_WINDOW,  # コンソールウィンドウを開かない
                )  # コマンドを実行、ファイルに出力

        # 結果を書き込むファイルのパスが指定されていない場合、標準出力に出力
        else:
            subprocess.run(
                args=command_list,  # コマンドのリスト
                check=True,  # 終了コードが0以外の時に例外を起こす
                creationflags=subprocess.CREATE_NO_WINDOW,  # コンソールウィンドウを開かない
            )  # コマンドを実行

    @staticmethod  # スタティック(静的)メソッド
    def get_script_directory_path():
        """現在のスクリプトファイルが存在するディレクトリのパスを取得する処理

        Returns:
            directory_path(src): 現在のスクリプトファイルが存在するディレクトリのパス
        """
        # ファイルが凍結(exe)なら
        if getattr(sys, "frozen", False):
            # 実行可能ファイルが存在するディレクトリのパス
            return os.path.dirname((sys.executable))
        else:
            # スクリプトファイルが存在するディレクトリのパス
            return os.path.dirname(__file__)

    def create_aws_file():
        """AWSの空の設定ファイルを作成する処理"""

        # AWSの認証情報や設定ファイルのディレクトリが存在しないなら作成する
        if not os.path.exists(SystemSetting.aws_setting_directory_path):
            os.makedirs(SystemSetting.aws_setting_directory_path)

        # 空のAWS設定ファイルを作成（既に存在する場合は何もしない）
        with open(SystemSetting.aws_config_file_path, "a"):
            pass

        # 空のAWS認証情報ファイルを作成（既に存在する場合は何もしない）
        with open(SystemSetting.aws_credentials_file_path, "a"):
            pass
