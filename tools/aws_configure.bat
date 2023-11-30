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

@REM AWSの設定の保存先の指定
set AWS_SHARED_CREDENTIALS_FILE=.aws\credentials
@REM AWSの認証情報の保存先の指定
set AWS_CONFIG_FILE=.aws\config

echo AWS設定画面
echo 中断する場合、Ctrl + Zを押してください。

@REM AWSの設定
aws configure