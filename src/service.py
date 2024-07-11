import threading
import pystray
from PIL import Image, ImageDraw


class TrayIcon:
    def __init__(self, observer, executor):
        self.observer = observer
        self.executor = executor
        self.icon = None

    def create_image(self):
        # Load the image
        return Image.open("iCloudSync_icon.png")

    def start(self):
        image = self.create_image()
        menu = pystray.Menu(
            pystray.MenuItem("Start Sync", self.start_sync),
            pystray.MenuItem("Stop Sync", self.stop_sync),
            pystray.MenuItem("Exit", self.exit),
        )
        self.icon = pystray.Icon("File Watcher Service", image, "iCloudSync", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def start_sync(self, icon, item):
        self.observer.start()
        self.icon.notify("iCloudSync", "Synchronization started.")

    def stop_sync(self, icon, item):
        self.observer.stop()
        self.icon.notify("iCloudSync", "Synchronization stopped.")

    def exit(self, icon, item):
        self.stop_sync(icon, item)
        self.executor.shutdown()
        self.icon.stop()
