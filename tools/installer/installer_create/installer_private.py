import os  # オペレーティングシステムの機能にアクセスするためのモジュール（環境変数の管理、ファイルパスの操作など）
import subprocess  # 新しいプロセスを生成し、その入出力を管制するためのモジュール
import sys  # Pythonのインタプリタや環境にアクセスするためのモジュール（引数の取得、システムパスの操作など）
import threading  # スレッドベースの並行処理を実装するためのモジュール
import traceback  # プログラムが例外を投げた際にスタックトレースを取得し、表示するためのモジュール

import PySimpleGUI as sg  # グラフィカルユーザーインターフェイス(GUI)を簡単に作成するためのツール


class Fn:
    """自作関数クラス"""

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

    @staticmethod  # スタティック(静的)メソッド
    def check_is_python_installed():
        """Pythonがインストールされているかどうかを取得する

        Returns:
            is_python_installed(bool): 指定されたバージョンのPythonがインストールされているかどうか
        """

        try:
            # コマンドを実行してPythonのバージョンを取得
            result = subprocess.run(
                args=[Setting.PYTHON_PATH, f"-{Setting.PYTHON_VERSION}", "--version"],  # コマンドのリスト
                capture_output=True,  # コマンドの標準出力と標準エラー出力を取得する
                text=True,  # 出力を文字列として処理する
            )
            # バージョン情報が正常に取得できたかチェック
            if result.returncode == 0:
                return True  # 指定されたバージョンのPythonがインストールされているかどうか

        # コマンドの実行に失敗した場合、Falseを返す
        except Exception as e:
            print(f"コマンド実行に失敗しました: {e}\n{traceback.format_exc()}")

            # エラーメッセージの作成
            error_message = [
                "コマンド実行に失敗しました",
                e,  # 例外
                traceback.format_exc(),  # トレースバック
                result.stdout,  # 標準出力
                result.stderr,  # エラー出力
            ]
            # エラーログの作成
            with open(file="error.log", mode="a", encoding="utf-8") as file:  # ファイルを開く(追記)
                error_message = ["-" * 50] + error_message + [("-" * 50) + "\n"]  # 文字列に外線と改行を追加
                file.write("\n".join(error_message))  # ファイルの末尾に文字列を追加

        return False  # 指定されたバージョンのPythonがインストールされているかどうか


class Setting:
    """設定クラス"""

    #! デバッグ用 インストーラーが公開用かどうか

    # デフォルトの設定を適用
    # インストーラーが公開用かどうかの設定
    is_public = False

    # pythonの場所
    PYTHON_PATH = "py"
    # pythonのバージョン
    PYTHON_VERSION = "3.8"

    # プロジェクトが存在するGitのURLとリポジトリ名の取得
    # 公開用なら
    if is_public:
        git_url = "https://github.com/pppp-987/Yakunyakukonjac_Public.git"  # URL
        git_repository_name = "Yakunyakukonjac_Public"  # リポジトリ名

    # 公開用でないなら
    else:
        git_url = "https://github.com/pppp-987/Yakunyakukonjac.git"  # URL
        git_repository_name = "Yakunyakukonjac"  # リポジトリ名

    # 仮想環境のディレクトリパス
    venv_path = os.path.join(
        Fn.get_script_directory_path(),  # 現在のスクリプトファイルが存在するディレクトリのパス
        "venv_YakunyakuKonjac",  # 仮想環境名
    )

    # 一時的なVBScriptファイルのパス
    vbs_path = os.path.join(Fn.get_script_directory_path(), "tmp_create_shortcut.vbs")
    # ショートカットの保存先パス
    shortcut_path = os.path.join(Fn.get_script_directory_path(), "YakunyakuKonjac.lnk")
    # ショートカットのリンク先パス
    target_path = os.path.join(venv_path, git_repository_name, "tools", "app.bat")
    # 作業フォルダのパス
    working_directory_path = os.path.join(venv_path, git_repository_name, "tools")
    # ショートカットのアイコンのパス
    shortcut_icon_path = os.path.join(venv_path, git_repository_name, "static", "icon", "app.ico")


class InstallThread:
    """インストール処理を行うスレッド"""

    @staticmethod  # スタティック(静的)メソッド
    def run(window):
        """インストール処理

        Args:
            window (sg.Window): Windowオブジェクト
        """

        try:
            # インストール状況のメッセージの更新処理
            Main.install_progress_message_update(window, message="仮想環境作成中。")

            # 仮想環境のディレクトリパス
            venv_path = Setting.venv_path

            # 仮想環境の作成
            Fn.command_run([Setting.PYTHON_PATH, f"-{Setting.PYTHON_VERSION}", "-m", "venv", venv_path])

            # カレントディレクトリを仮想環境に変更
            os.chdir(venv_path)

            # pipのパス
            pip_path = os.path.join(venv_path, "Scripts", "pip.exe")

            # インストールするパッケージの一覧
            packages_to_install = [
                # AWS関連
                "awscli",  # コマンドラインからAmazon Web Services(AWS)を操作するためのツール
                "boto3",  # PythonでAmazon Web Services(AWS)を使用するためのSDK
                # OCR関連
                "easyocr",  # 画像内のテキストを認識するための光学文字認識(OCR)ツール
                # 翻訳関連
                "deep-translator",  # 複数のオンライン翻訳サービスを利用するためのテキスト翻訳ライブラリ
                # GUI関連
                "keyboard",  # Pythonでキーボードイベントをモニタリングやシミュレートするためのモジュール
                "pyautogui",  # プログラムによるマウスやキーボード操作を自動化するためのモジュール
                "PySimpleGUI",  # グラフィカルユーザーインターフェイス(GUI)を簡単に作成するためのツール
                # "black",  # PythonコードをPEP 8スタイルガイドに沿って自動整形するためのフォーマッタ
            ]

            # パッケージのインストール タイムアウトの時間を100秒に変更
            for index, package in enumerate(packages_to_install):
                # インストール状況のメッセージの更新処理
                Main.install_progress_message_update(
                    window, message=f"パッケージインストール中: {index + 1}/{len(packages_to_install)}"
                )
                # パッケージのインストール
                Fn.command_run([pip_path, "--default-timeout=100", "install", package])

            # パッケージ一覧を出力ファイルに保存
            Fn.command_run([pip_path, "freeze"], file_path="requirements.txt")

            # インストール状況のメッセージの更新処理
            Main.install_progress_message_update(window, message="ソフトウェアダウンロード中")

            # プロジェクトディレクトリが存在しないなら
            if not os.path.isdir(os.path.join(venv_path, Setting.git_repository_name)):
                # gitからクローンする
                Fn.command_run(["git", "clone", Setting.git_url])

            # プロジェクトディレクトリが存在するなら
            else:
                # カレントディレクトリをプロジェクトディレクトリに変更
                os.chdir(os.path.join(venv_path, Setting.git_repository_name))

                # gitからプルする
                Fn.command_run(["git", "pull", "origin"])

            #! 公開用(デバッグ用)でないなら
            if not Setting.is_public:
                # カレントディレクトリをプロジェクトディレクトリに変更
                os.chdir(os.path.join(venv_path, Setting.git_repository_name))

                # ブランチ変更
                Fn.command_run(["git", "checkout", "environment"])

            # インストール状況のメッセージの更新処理
            Main.install_progress_message_update(window, message="ショートカット作成中")

            # VBScriptのソースコード作成
            vbs_script = [
                # WScript.Shellオブジェクトの作成
                'Set WScriptShell = WScript.CreateObject("WScript.Shell")',
                # ショートカットの作成
                f'Set Shortcut = WScriptShell.CreateShortcut("{Setting.shortcut_path}")',
                # ショートカットのリンク先パスの設定
                f'Shortcut.TargetPath = "{Setting.target_path}"',
                # 作業フォルダの設定
                f'Shortcut.WorkingDirectory = "{Setting.working_directory_path}"',
                # ショートカットアイコンの設定
                f'Shortcut.IconLocation = "{Setting.shortcut_icon_path}"',
                # ショートカットを保存
                "Shortcut.Save",
            ]

            # 一時的なVBScriptファイルの作成
            with open(Setting.vbs_path, "w") as file:
                # ソースコードを1行ずつ書き込む
                for line in vbs_script:
                    file.write(line + "\n")

            # VBSファイルを実行してショートカットを作成
            Fn.command_run(["cscript", Setting.vbs_path])

            # 一時的に作成したVBSファイルを削除
            os.remove(Setting.vbs_path)

            # インストール状況のメッセージの更新処理
            Main.install_progress_message_update(window, message="インストール完了")

            # スレッドから、キーイベントを送信
            window.write_event_value(key="-install_thread_end-", value={"is_error": False})

        # エラーが発生したら
        except Exception as e:
            # エラーメッセージの作成
            error_message = [
                "エラー発生",
                str(e),  # 例外
                str(traceback.format_exc()),  # トレースバック
            ]
            # エラーログの作成
            with open(file="error.log", mode="a", encoding="utf-8") as file:  # ファイルを開く(追記)
                error_message = ["-" * 50] + error_message + [("-" * 50) + "\n"]  # 文字列に外線と改行を追加
                file.write("\n".join(error_message))  # ファイルの末尾に文字列を追加

            # スレッドから、キーイベントを送信
            window.write_event_value(
                key="-install_thread_end-",
                value={
                    "is_error": True,  # エラーが発生したかどうか
                    "exception": e,  # 例外オブジェクト
                    "traceback": traceback.format_exc(),  # トレースバック
                },
            )
            raise  # 例外を発生させる


class Main:
    """メイン処理"""

    @staticmethod  # スタティック(静的)メソッド
    def run():
        """実行処理"""
        # Pythonがインストールされていないなら
        if not Fn.check_is_python_installed():
            sg.popup(f"このアプリケーションを実行するにはPython {Setting.PYTHON_VERSION}が必要です。")
            return

        # デバッグ用のメッセージ

        # 公開用なら
        if Setting.is_public:
            public_message = "(公開用)"
        else:
            public_message = "(デバッグ用)"

        # GUIのレイアウトを定義
        layout = [
            [sg.Text(text=f"インストーラー {public_message}", key="-text-", size=(24, 2))],
            # インストールの進捗状況の表示
            [
                sg.Text(
                    text=f"AWS CLIのアクセスキーは\n手動で設定してください。",
                    key="-install_progress-",
                    size=(34, 2),
                    metadata={
                        "message": "AWS CLIのアクセスキーは\n手動で設定してください。",  # 表示メッセージ
                        "progress_indicator_dot_count": 0,  # 進捗インジケーターの点の数
                    },
                )
            ],
            [
                sg.Push(),  # 右に寄せる
                sg.Button("install", key="-install-"),  # 変更ボタン
                sg.Button("cancel", key="-cancel-"),  # 戻るボタン
            ],
        ]

        # ウィンドウの作成
        window = sg.Window(
            title="Installer",  # タイトル
            layout=layout,  # レイアウト
            finalize=True,  # 入力待ち までの間にウィンドウを表示する
        )

        # インストールスレッドの作成
        install_thread_obj = threading.Thread(
            name="インストールスレッド",  # スレッド名
            target=lambda: InstallThread.run(window),  # スレッドで実行するメソッド
            daemon=True,  # メインスレッド終了時に終了する
        )

        # イベントループ
        while True:
            event, values = window.read(
                timeout=500,  # タイムアウトする間隔(ms)
                timeout_key="-timeout-",  # タイムアウトイベント名
            )

            if event == sg.WIN_CLOSED or event == "-cancel-":
                break
            # タイムアウトしたら
            elif event == "-timeout-":
                # インストールスレッドが存在するなら
                if install_thread_obj.is_alive():
                    # インストール状況を表す進捗インジケーターの点の数を更新する処理
                    Main.install_progress_dot_count_update(window)

            # インストールボタンが押されたら
            elif event == "-install-":
                # スレッドの処理を開始
                install_thread_obj.start()
                # ボタンの無効化
                window["-install-"].update(disabled=True)
                # テキストの更新
                window["-text-"].update(value="インストール中です。\nしばらくお待ちください。")

                # インストールスレッドが終了したなら
            elif event == "-install_thread_end-":
                window.hide()  # ウィンドウを非表示にする
                # インストール中にエラーが発生していないなら
                if not values["-install_thread_end-"]["is_error"]:
                    sg.popup("インストールが完了しました。")

                # インストール中にエラーが発生したなら
                else:
                    print(values["-install_thread_end-"]["exception"])
                    message = [
                        "申し訳ありません、エラーが発生しました。",
                        "エラーログファイルが作成されました。",
                        "管理者にこのファイルを提供していただけると幸いです。",
                    ]
                    # エラーポップアップの作成
                    sg.popup("\n".join(message))
                break

        # ウィンドウのクローズ
        window.close()

    @staticmethod  # スタティック(静的)メソッド
    def install_progress_message_update(window, message):
        """インストール状況のメッセージの更新処理

        Args:
            window (sg.Window): Windowオブジェクト
            message (src): 表示するメッセージ
        """
        # 表示メッセージの更新
        window["-install_progress-"].metadata["message"] = message
        # 進捗インジケーターの点の数の更新
        window["-install_progress-"].metadata["progress_indicator_dot_count"] = 0
        # インストール進捗状況の更新
        window["-install_progress-"].update(value=message)

    @staticmethod  # スタティック(静的)メソッド
    def install_progress_dot_count_update(window):
        """インストール状況を表す進捗インジケーターの点の数を更新する処理"""

        # 進捗インジケーターの点の数の取得
        dot_count = window["-install_progress-"].metadata["progress_indicator_dot_count"]
        # 進捗インジケーターの点の数の更新
        now_dot_count = (dot_count + 1) % 4
        # 進捗インジケーターの点の数の保存
        window["-install_progress-"].metadata["progress_indicator_dot_count"] = now_dot_count

        # 表示メッセージの取得
        message = window["-install_progress-"].metadata["message"]
        # インストール進捗状況の表示メッセージの更新
        window["-install_progress-"].update(
            # メッセージ + 点 + 空白
            value=f"{message}{'.' * now_dot_count}{' ' * (3-now_dot_count)}"
        )


if __name__ == "__main__":
    Main.run()
