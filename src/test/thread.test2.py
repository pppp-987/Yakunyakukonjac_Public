import keyboard
import time
from threading import Thread

class KeyboardEventListener:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.last_event_time = time.time()
        self.listener = None
        self.monitor_thread = None
        self.running = False

    def _on_event(self, event):
        # キーボードイベントが発生するたびに呼び出されます。
        self.last_event_time = time.time()

    def _monitor_keyboard_events(self):
        # 最後のキーボードイベントから指定された時間が経過したか監視します。
        while self.running:
            if time.time() - self.last_event_time > self.timeout:
                self.stop_listener()
                break
            time.sleep(1)

    def start_listener(self):
        # キーボードイベントリスナーを開始します。
        self.running = True
        self.listener = keyboard.hook(self._on_event)
        self.monitor_thread = Thread(target=self._monitor_keyboard_events)
        self.monitor_thread.start()

    def stop_listener(self):
        # キーボードイベントリスナーを停止します。
        if self.listener:
            keyboard.unhook(self.listener)
        self.running = False

# 使用例
listener = KeyboardEventListener(timeout=5) # 5秒間キーボードイベントがなければ停止
listener.start_listener()

# この例では、リスナーを停止させるための追加のコードは書いていません。
# 必要に応じてリスナーを停止させるための条件を追加してください。
