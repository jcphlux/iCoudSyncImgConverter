import os
import sys
from concurrent.futures import ThreadPoolExecutor
from watchdog.observers import Observer
from config import ConfigLoader
from database import initialize_db, is_db_initialized, get_session
from file_processor import HEICtoJPGHandler, FileDeletionHandler
from utils import TrayIcon
from config_ui import launch_config_ui


def main():
    # Check if the database and tables are initialized
    if not is_db_initialized():
        print("Database not initialized. Initializing now...")
        initialize_db()

    config_loader = ConfigLoader()

    folder_configs = config_loader.get_all_folder_configs()
    universal_config = config_loader.get_universal_config()
    if not folder_configs or not universal_config:
        print("No configuration found. Launching configuration UI...")
        launch_config_ui()
        folder_configs = config_loader.get_all_folder_configs()
        universal_config = config_loader.get_universal_config()
        if not folder_configs or not universal_config:
            print("Configuration is required. Exiting.")
            sys.exit(1)

    executor = ThreadPoolExecutor(max_workers=4)
    observers = []
    handlers = []

    for config in folder_configs:
        source_folder = os.path.expandvars(config.source_folder)
        destination_folder = os.path.expandvars(config.destination_folder)
        default_behavior = universal_config.default_behavior

        if not os.path.exists(source_folder):
            print(f"Error: The folder to watch '{source_folder}' does not exist.")
            continue

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        session = get_session()

        event_handler = HEICtoJPGHandler(
            source_folder, destination_folder, session, default_behavior
        )
        delete_handler = FileDeletionHandler(source_folder, destination_folder, session)

        observer = Observer()
        observer.schedule(event_handler, path=source_folder, recursive=False)
        observer.schedule(delete_handler, path=source_folder, recursive=False)
        observer.schedule(delete_handler, path=destination_folder, recursive=False)

        observers.append(observer)
        handlers.append((event_handler, delete_handler))

    tray_icon = TrayIcon(
        observers,
        executor,
        universal_config.icon_path,
        universal_config.default_behavior,
    )
    tray_icon.start()

    for observer in observers:
        observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
    for observer in observers:
        observer.join()
    executor.shutdown()


if __name__ == "__main__":
    main()
