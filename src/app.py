from package.error_log import ErrorLog  # エラーログに関するクラス


# # エラーログを取得するデコレータ
# @ErrorLog.parameter_decorator(
#     is_main_thread=True, # メインスレッドかどうか
#     event_window=None, # ポップアップイベントを返すWindowオブジェクト
# )
@ErrorLog.decorator
def main():
    """メインの処理"""
    # 必要クラスのインポート
    from package.fn import Fn  # 自作関数クラス

    from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス

    from package.window.translation_win import TranslationWin  # 翻訳画面ウィンドウクラス
    from package.window.display_setting_win import DisplaySettingWin  # 表示設定画面ウィンドウクラス
    from package.window.environment_setting_win import EnvironmentSettingWin  # 環境設定画面ウィンドウクラス
    from package.window.key_setting_win import KeySettingWin  # キー設定画面ウィンドウクラス
    from package.window.language_setting_win import LanguageSettingWin  # 言語設定画面ウィンドウクラス
    from package.window.save_setting_win import SaveSettingWin  # 保存設定画面ウィンドウクラス
    from package.window.shooting_setting_win import ShootingSettingWin  # 撮影設定画面ウィンドウクラス
    from package.window.theme_setting_win import ThemeSettingWin  # テーマ設定画面ウィンドウクラス
    from package.window.user_info_win import UserInfoWin  # 利用者情報画面ウィンドウクラス

    # ウィンドウクラスのマッピング辞書
    WIN_CLASS_DICT = {
        "TranslationWin": TranslationWin,  # 翻訳画面ウィンドウクラス
        "DisplaySettingWin": DisplaySettingWin,  # 表示設定画面ウィンドウクラス
        "EnvironmentSettingWin": EnvironmentSettingWin,  # 環境設定画面ウィンドウクラス
        "KeySettingWin": KeySettingWin,  # キー設定画面ウィンドウクラス
        "LanguageSettingWin": LanguageSettingWin,  # 言語設定画面ウィンドウクラス
        "SaveSettingWin": SaveSettingWin,  # 保存設定画面ウィンドウクラス
        "ShootingSettingWin": ShootingSettingWin,  # 撮影設定画面ウィンドウクラス
        "ThemeSettingWin": ThemeSettingWin,  # テーマ設定画面ウィンドウクラス
        "UserInfoWin": UserInfoWin,  # 利用者情報画面ウィンドウクラス
    }
    # ユーザ設定のインスタンス化
    user_setting = UserSetting()

    Fn.time_log("システム開始")

    # 翻訳前、後画像の両方が存在しない履歴ファイルを削除
    Fn.delete_unique_history_file()

    # メインウィンドウの処理
    transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
    win_class = WIN_CLASS_DICT[transition_target_win]  # 遷移先ウィンドウクラスの取得
    win_instance = win_class()  # ウィンドウ作成
    transition_target_win = win_instance.get_transition_target_win()  # 遷移先ウィンドウ名取得

    # 遷移先ウィンドウが存在する間、繰り返す
    while transition_target_win is not None:
        win_class = WIN_CLASS_DICT[transition_target_win]  # 遷移先ウィンドウクラス
        win_instance = win_class()  # ウィンドウ作成
        transition_target_win = win_instance.get_transition_target_win()  # 遷移先ウィンドウ名取得
    Fn.time_log("システム終了")


if __name__ == "__main__":
    main()  # メイン処理
