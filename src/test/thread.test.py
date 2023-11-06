
import PySimpleGUI as sg
import time
import threading


# My function that takes a long time to do...
class Thread_cls:
    def my_long_operation(id, window):
        time.sleep(10)
        print("処理終了")
        # ウィンドウが閉じられているかどうか取得
        print(window.was_closed())
        # ウィンドウが閉じられていないなら
        if not window.was_closed():
            window.write_event_value("-end-", id)
        else:
            print("ウィンドウ終了")


class Win1:
    def main():
        layout = [
            [sg.Text("My Window")],
            [sg.Input(key="-IN-")],
            [sg.Text(key="-OUT-")],
            [sg.Button("Threaded"), sg.Button("cancel")],
        ]

        window = sg.Window("Window Title", layout)

        thread_dict = {}
        thread_count = 0
        ignore_thread_events = False
        while True:  # Event Loop
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                if thread_dict:  # There are still running threads
                    ignore_thread_events = True  # Set the flag to ignore thread events
                break

            if event == "Threaded":
                # Let PySimpleGUI do the threading for you...
                id = thread_count
                # thread = threading.Thread(target=lambda: my_long_operation(id))
                # スレッド作成
                thread = threading.Thread(
                    target=Thread_cls.my_long_operation,
                    args=(id, window),
                    daemon=True,
                )
                # スレッド開始
                thread.start()
                # スレッドの辞書作成
                thread_dict[id] = thread
                print(id, "スレッド開始")
                print(thread_dict)
                thread_count += 1
            elif event == "-end-":
                id = values["-end-"]
                thread_dict.pop(id)
                print(id, "スレッド停止")
                print(thread_dict)
            elif event == "cancel":
                # print(list(thread_dict.values()))
                for thread in thread_dict.values():
                    print(thread)
                break

        window.close()


class Win2:
    def main():
        layout = [
            [sg.Text("test")],
        ]

        window = sg.Window("Window2", layout)

        while True:  # Event Loop
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break


if __name__ == "__main__":
    Win1.main()
    Win2.main()
