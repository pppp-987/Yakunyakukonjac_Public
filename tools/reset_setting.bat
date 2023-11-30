@REM ファイル保存時に、エンコーディングを"Shift-JIS"にする

@REM コマンドを表示しない
@echo off

@REM 文字コードを"Shift-JIS"に設定 メッセージは非表示
chcp 932 >nul

@REM 仮想環境が有効でないなら
if not defined VIRTUAL_ENV (
    @REM 仮想環境のルートディレクトリへ移動
    cd ../..
    @REM 仮想環境の有効化
    call Scripts\activate.bat
)

@REM 設定ファイル削除
del YakunyakuKonjac_Public\src\config\setting.json 2>nul