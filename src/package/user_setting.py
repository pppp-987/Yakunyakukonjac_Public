import json  # jsonファイルの読み書き
import os  # ディレクトリ関連

from package.fn import Fn  # 自作関数クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス


class UserSetting:
    """ユーザーが変更可能の設定クラス"""

    # デフォルトの設定
    default_user_setting = {
        "ss_left_x": 0,  # 撮影範囲の左側x座標
        "ss_top_y": 0,  # 撮影範囲の上側y座標
        "ss_right_x": 1280,  # 撮影範囲の右側x座標
        "ss_bottom_y": 720,  # 撮影範囲の下側y座標
        "ocr_soft": "AmazonTextract",  # OCRソフト
        "translation_soft": "AmazonTranslate",  # 翻訳ソフト
        "source_language_code": "en",  # 翻訳元言語
        "target_language_code": "ja",  # 翻訳先言語
        "window_left_x": None,  # ウィンドウの左側x座標
        "window_top_y": None,  # ウィンドウの上側y座標
        "window_width": None,  # ウィンドウの横幅
        "window_height": None,  # ウィンドウの縦幅
        "translation_interval_sec": 10,  # 翻訳間隔(秒)
        "max_file_size_mb": 100,  # 最大保存容量(MB)
        "max_file_count": 50,  # 最大保存枚数
        "max_file_retention_days": 30,  # 最大保存期間(日)
        "window_theme": "DarkBlue3",  # ウィンドウのテーマ
        # キーバインド設定情報の辞書
        "key_binding_info_list": [
            {
                "text": "翻訳",  # 説明文
                "gui_key": "-translate_key-",  # 識別子
                "key_name": "f1",  # キー名
                "scan_code": None,  # スキャンコード
            },
            {
                "text": "自動翻訳切替",
                "gui_key": "-auto_translation_toggle-",
                "key_name": "f2",
                "scan_code": None,
            },
            {
                "text": "撮影範囲設定",
                "gui_key": "-set_ss_region_key-",
                "key_name": "f3",
                "scan_code": None,
            },
            {
                "text": "撮影設定へ遷移",
                "gui_key": "-transition_to_shooting_key-",
                "key_name": "f4",
                "scan_code": None,
            },
            {
                "text": "言語設定へ遷移",
                "gui_key": "-transition_to_language_key-",
                "key_name": "f5",
                "scan_code": None,
            },
        ],
    }

    def __init__(self):
        """コンストラクタ 初期設定"""
        self.setting = self.load_setting_file()  # 設定ファイルを読み込む

    def get_setting(self, key):
        """設定を取得する

        Args:
            key(str): 設定辞書のキー

        Returns:
            setting(str): 設定辞書の値

        """
        return self.setting[key]  # 設定辞書の値

    def get_all_setting(self):
        """設定を全て取得する

        Returns:
            setting(dict): 設定
        """
        return self.setting  # 設定

    def create_setting_file(self):
        """設定ファイルを新規作成して辞書として返す

        Returns:
            default_setting(dict): デフォルトの設定
        """
        setting_file_path = SystemSetting.setting_file_path  # 設定ファイルのパス
        default_setting = self.default_user_setting  # デフォルトの設定の取得
        with open(file=setting_file_path, mode="w") as f:  # ファイルを開く(書き込み)
            json.dump(obj=default_setting, fp=f, indent=2)  # ファイルの新規作成
        return default_setting  # デフォルト設定を戻り値に指定

    def load_setting_file(self):
        """設定ファイルを読み込み辞書として返す
        設定ファイルが存在しない場合は新規作成する

        Returns:
            setting(dict): 読み込んだ設定
        """
        setting_file_path = SystemSetting.setting_file_path  # 設定ファイルのパス

        # 設定ファイルの読み込み処理（ファイルが存在しないなら新規作成）
        if os.path.isfile(setting_file_path):  # ファイルが存在するなら
            # ファイルが存在するなら読み込む
            with open(setting_file_path, "r") as f:  # ファイルを開く(読み込み)
                setting = json.load(f)  # ファイルを読み込む
        else:
            # ファイルが存在しないなら新規作成して読み込む
            Fn.time_log("設定ファイルが存在しません。作成します。")
            setting = self.create_setting_file()  # デフォルトを戻り値に指定
        return setting  # 設定を戻り値に指定

    def save_setting_file(self, update_setting):
        """現在の設定を更新して、jsonファイルに保存する

        Args:
            update_setting (dict): 更新する設定
        """

        setting_file_path = SystemSetting.setting_file_path  # 設定ファイルのパス
        self.setting.update(update_setting)  # 現在の設定を更新

        with open(setting_file_path, "w") as f:  # ファイルを開く(書き込み)
            json.dump(obj=self.setting, fp=f, indent=2)  # ファイルに読み込む
