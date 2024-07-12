import threading
import pystray
from PIL import Image
import subprocess


class TrayIcon:
    def __init__(self, observers, executor, icon_path, default_behavior):
        self.observers = observers
        self.executor = executor
        self.icon_path = icon_path
        self.default_behavior = default_behavior
        self.icon = None

    def create_image(self):
        image = Image.open(self.icon_path)
        return image

    def start(self):
        image = self.create_image()
        menu = pystray.Menu(
            pystray.MenuItem("Start Sync", self.start_sync),
            pystray.MenuItem("Stop Sync", self.stop_sync),
            pystray.MenuItem("Open Config UI", self.open_config_ui),
            pystray.MenuItem(
                "Set Behavior",
                pystray.Menu(
                    pystray.MenuItem(
                        "Symbolic Link",
                        self.set_symbolic,
                        checked=lambda item: self.default_behavior == "symbolic",
                    ),
                    pystray.MenuItem(
                        "Copy File",
                        self.set_copy,
                        checked=lambda item: self.default_behavior == "copy",
                    ),
                ),
            ),
            pystray.MenuItem("Exit", self.exit),
        )
        self.icon = pystray.Icon("File Watcher Service", image, "iCloudSync", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def start_sync(self, icon, item):
        for observer in self.observers:
            observer.start()
        self.icon.notify("iCloudSync", "Synchronization started.")

    def stop_sync(self, icon, item):
        for observer in self.observers:
            observer.stop()
        self.icon.notify("iCloudSync", "Synchronization stopped.")

    def open_config_ui(self, icon, item):
        subprocess.Popen(["python", "config_ui.py"])

    def set_symbolic(self, icon, item):
        self.default_behavior = "symbolic"
        self.icon.notify("iCloudSync", "Behavior set to create symbolic links.")

    def set_copy(self, icon, item):
        self.default_behavior = "copy"
        self.icon.notify("iCloudSync", "Behavior set to copy files.")

    def exit(self, icon, item):
        self.stop_sync(icon, item)
        self.executor.shutdown()
        self.icon.stop()
