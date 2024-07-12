import os
import shutil
import hashlib
from PIL import Image
from pillow_heif import register_heif_opener
from watchdog.events import FileSystemEventHandler
from sqlalchemy.orm import Session
from models import ProcessedFile
from config import ConfigLoader

# Register HEIF opener to handle HEIC files
register_heif_opener()

config_loader = ConfigLoader()


def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()


def is_file_processed(session: Session, filename: str, filehash: str) -> bool:
    result = (
        session.query(ProcessedFile).filter_by(filename=filename, hash=filehash).first()
    )
    return result is not None


def log_processed_file(
    session: Session, filename: str, filehash: str, is_symbolic: bool
):
    processed_file = ProcessedFile(
        filename=filename, hash=filehash, is_symbolic=is_symbolic
    )
    session.merge(processed_file)
    session.commit()


def remove_processed_file(session: Session, filename: str):
    session.query(ProcessedFile).filter_by(filename=filename).delete()
    session.commit()


def copy_file(src_path, dst_path):
    try:
        shutil.copy2(src_path, dst_path)
        print(f"Copied file from {src_path} to {dst_path}")
    except Exception as e:
        print(f"Failed to copy file from {src_path} to {dst_path}: {e}")


def create_symbolic_link(src_path, dst_path):
    try:
        if not os.path.exists(dst_path):
            os.symlink(src_path, dst_path)
            print(f"Created symbolic link from {src_path} to {dst_path}")
    except Exception as e:
        print(f"Failed to create symbolic link from {src_path} to {dst_path}: {e}")


class HEICtoJPGHandler(FileSystemEventHandler):
    def __init__(
        self,
        source_folder: str,
        destination_folder: str,
        session: Session,
        default_behavior: str,
    ):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.session = session
        self.default_behavior = default_behavior
        self.process_all_files()

    def process_all_files(self):
        for root, _, files in os.walk(self.source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                self.process_file(file_path)

    def process_file(self, file_path):
        if file_path.lower().endswith((".heic", ".hevc")):
            self.process_heic_file(file_path)
        else:
            self.process_other_file(file_path)

    def process_heic_file(self, hevc_path):
        filename = os.path.basename(hevc_path)
        jpg_path = os.path.join(
            self.destination_folder, os.path.splitext(filename)[0] + ".jpg"
        )
        filehash = get_file_hash(hevc_path)

        if is_file_processed(self.session, filename, filehash):
            print(
                f"{filename} has already been processed with the same hash. Skipping."
            )
            return

        try:
            with Image.open(hevc_path) as img:
                img = img.convert("RGB")
                img.save(jpg_path, "JPEG")
            print(f"Successfully converted {hevc_path} to {jpg_path}")

            log_processed_file(self.session, filename, filehash, False)
        except Exception as e:
            print(f"Failed to convert {hevc_path}: {e}")

    def process_other_file(self, file_path):
        filename = os.path.basename(file_path)
        filehash = get_file_hash(file_path)
        destination_path = os.path.join(self.destination_folder, filename)

        if is_file_processed(self.session, filename, filehash):
            print(
                f"{filename} has already been processed with the same hash. Skipping."
            )
            return

        if os.path.exists(destination_path):
            os.remove(destination_path)
            print(f"Removed existing destination file: {destination_path}")

        if self.default_behavior == "symbolic":
            create_symbolic_link(file_path, destination_path)
            log_processed_file(self.session, filename, filehash, True)
        else:
            copy_file(file_path, destination_path)
            log_processed_file(self.session, filename, filehash, False)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        if event.is_directory:
            return
        self.process_file(event.src_path)


class FileDeletionHandler(FileSystemEventHandler):
    def __init__(self, source_folder: str, destination_folder: str, session: Session):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.session = session

    def on_deleted(self, event):
        if event.is_directory:
            return
        self.process(event)

    def process(self, event):
        filename = os.path.basename(event.src_path)
        source_path = os.path.join(self.source_folder, filename)
        destination_path = os.path.join(self.destination_folder, filename)

        if not os.path.exists(source_path) and os.path.exists(destination_path):
            os.remove(destination_path)
            print(f"Removed destination file: {destination_path}")
            remove_processed_file(self.session, filename)

        if not os.path.exists(destination_path) and os.path.exists(source_path):
            os.remove(source_path)
            print(f"Removed source file: {source_path}")
            remove_processed_file(self.session, filename)
