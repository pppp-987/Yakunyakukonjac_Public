@REM AWSの設定
@REM aws configure

@REM 仮想環境作成
py -3.8 -m venv venv_YakunyakuKonjac
cd venv_YakunyakuKonjac
call Scripts\activate.bat

@REM パッケージインストール タイムアウトを100秒に変更

@REM AWS関連
pip --default-timeout=100 install awscli
pip --default-timeout=100 install boto3
@REM OCR関連
pip --default-timeout=100 install easyocr
@REM 翻訳関連
pip --default-timeout=100 install deep-translator
@REM GUI関連
pip --default-timeout=100 install keyboard
pip --default-timeout=100 install pyautogui
pip --default-timeout=100 install PySimpleGUI

@REM pip install black

@REM パッケージ一覧出力ファイルの作成
pip freeze > requirements.txt

@REM gitからクローン
git clone https://github.com/pppp-987/Yakunyakukonjac_Public.git

@REM プロジェクトファイルに移動
cd Yakunyakukonjac_Public


@REM ショートカット作成 VBScript使用

@REM ショートカットのリンク先パス
set ShortcutPath="%~dp0\YakunyakuKonjac.lnk"

@REM ショートカットの保存先パス
set TargetPath="%cd%\tools\app.bat"

@REM ショートカットのアイコンのパス
set ShortcutIconPath="%cd%\static\icon\app.ico"

@REM 作業フォルダのパス
set WorkingDirectoryPath="%cd%\tools"

@REM 一時的なVBScriptファイルの作成
copy nul CreateShortcut.vbs

@REM WScript.Shellオブジェクトの作成
echo Set WScriptShell = WScript.CreateObject("WScript.Shell") >> CreateShortcut.vbs

@REM ショートカットの作成
echo Set Shortcut = WScriptShell.CreateShortcut(%ShortcutPath%) >> CreateShortcut.vbs

@REM ショートカットのリンク先パスの設定
echo Shortcut.TargetPath = %TargetPath% >> CreateShortcut.vbs

@REM 作業フォルダの設定
echo Shortcut.WorkingDirectory = %WorkingDirectoryPath% >> CreateShortcut.vbs

@REM ショートカットアイコンの設定
echo Shortcut.IconLocation = %ShortcutIconPath% >> CreateShortcut.vbs

@REM ショートカットを保存
echo Shortcut.Save >> CreateShortcut.vbs

@REM VBSファイルを実行してショートカットを作成
cscript CreateShortcut.vbs

@REM 一時的に作成したVBSファイルを削除
del CreateShortcut.vbs

msg * インストールが完了しました

pause