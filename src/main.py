import os
import sys
from concurrent.futures import ThreadPoolExecutor
from watchdog.observers import Observer
from config import ConfigLoader
from database import get_engine, initialize_db, get_session
from file_processor import HEICtoJPGHandler, FileDeletionHandler
from utils import TrayIcon


def main():
    config_loader = ConfigLoader()

    folder_to_watch = config_loader.get_config("folder_to_watch")
    destination_folder = config_loader.get_config("destination_folder")

    if not os.path.exists(folder_to_watch):
        print(f"Error: The folder to watch '{folder_to_watch}' does not exist.")
        sys.exit(1)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    engine = get_engine("sqlite:///icloud_sync.db")
    initialize_db(engine)
    session = get_session(engine)

    executor = ThreadPoolExecutor(max_workers=4)
    event_handler = HEICtoJPGHandler(session)
    delete_handler = FileDeletionHandler(folder_to_watch, destination_folder, session)

    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)
    observer.schedule(delete_handler, path=folder_to_watch, recursive=False)
    observer.schedule(delete_handler, path=destination_folder, recursive=False)

    tray_icon = TrayIcon(observer, executor)
    tray_icon.start()

    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    executor.shutdown()


if __name__ == "__main__":
    main()
