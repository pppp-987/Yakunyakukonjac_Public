import psutil
import os
import sys

def check_if_process_is_running(process_name):
    """
    システム上で指定された名前のプロセスが実行中かどうかをチェックする。
    """
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

if __name__ == "__main__":
    # 実行中の同名プロセスがあるかどうかをチェック
    if check_if_process_is_running(os.path.basename(__file__)):
        print(f"{__file__} はすでに実行中です。")
        sys.exit(1)

    print("実行開始")
    app_instance = App()  # メイン処理
