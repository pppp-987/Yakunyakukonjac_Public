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

@REM 履歴の削除
del /Q YakunyakuKonjac_Public\src\history\image_after\*.png 2>nul
del /Q YakunyakuKonjac_Public\src\history\image_before\*.png 2>nul

@REM 設定ファイル削除
del YakunyakuKonjac_Public\src\config\setting.json 2>nul

@REM キャッシュの削除
rmdir /s /q YakunyakuKonjac_Public\src\__pycache__ 2>nul
rmdir /s /q YakunyakuKonjac_Public\src\package\__pycache__ 2>nul
rmdir /s /q YakunyakuKonjac_Public\src\package\translation\__pycache__ 2>nul
rmdir /s /q YakunyakuKonjac_Public\src\package\window\__pycache__ 2>nul
rmdir /s /q YakunyakuKonjac_Public\src\package\thread\__pycache__ 2>nul

@REM エラーログファイルを空にする(アプリケーション実行中は失敗)
copy nul YakunyakuKonjac_Public\log\error_detailed.log >nul 2>&1
copy nul YakunyakuKonjac_Public\log\error_simple.log >nul 2>&1

@REM AWSの認証情報や設定ファイルの削除
rmdir /s /q .aws 2>nul

@REM EasyOCRモデルの削除
rmdir /s /q .EasyOCR 2>nul