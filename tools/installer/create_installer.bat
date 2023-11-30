@REM ファイル保存時に、エンコーディングを"Shift-JIS"にする

@REM コマンドを表示しない
@REM @echo off

@REM 文字コードを"Shift-JIS"に設定 メッセージは非表示
chcp 932 >nul

@REM 必要なファイルが存在しない場合、終了する
if not exist "installer_public.py" (
    msg * installer_public.pyが存在しません
    exit
)

if not exist "installer_private.py" (
    msg * installer_private.pyが存在しません
    exit
)

if not exist "app.ico" (
    msg * app.icoが存在しません
    exit
)

@REM 仮想環境作成
py -3.8 -m venv venv_installer
@REM カレントディレクトリを仮想環境のルートディレクトリにする
cd venv_installer
@REM 仮想環境の有効化
call Scripts\activate.bat

@REM パッケージインストール
@REM グラフィカルユーザーインターフェイス(GUI)を簡単に作成するためのツール
pip install PySimpleGUI

@REM Pythonプログラムをスタンドアロンの実行可能ファイル(exe, dmg, etc.)に変換するためのツール
pip install pyinstaller

@REM パッケージ一覧出力ファイルの作成
pip freeze > requirements.txt

@REM srcフォルダの作成
md src

@REM インストーラのスクリプトのコピー
copy ..\installer_public.py src
copy ..\installer_private.py src

@REM アイコンのコピー
copy ..\app.ico src

@REM exeファイルの作成(1つのファイルにまとめる、コンソール非表示、キャッシュの削除, 名前指定)
pyinstaller src\installer_public.py --onefile --noconsole --clean --name=installer_public.exe --icon=src\app.ico
pyinstaller src\installer_private.py --onefile --noconsole --clean --name=installer_private.exe --icon=src\app.ico

@REM exeファイルのコピー
copy dist\installer_public.exe ..\
copy dist\installer_private.exe ..\

@REM 仮想環境から抜け出す
call Scripts\deactivate.bat

@REM カレントディレクトリを仮想環境の外にする
cd ..

@REM 仮想環境の削除
RMDIR /S /Q venv_installer

msg * インストーラの作成が完了しました