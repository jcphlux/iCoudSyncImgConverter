from database import get_session
from models import FolderConfig, UniversalConfig


class ConfigLoader:
    def __init__(self):
        self.session = get_session()

    def get_all_folder_configs(self):
        return self.session.query(FolderConfig).all()

    def get_universal_config(self):
        return self.session.query(UniversalConfig).first()

    def add_folder_config(self, source_folder, destination_folder):
        if (
            self.session.query(FolderConfig)
            .filter(
                (FolderConfig.source_folder == source_folder)
                | (FolderConfig.destination_folder == destination_folder)
            )
            .first()
        ):
            raise ValueError("Source or destination folder is already in use.")
        folder_config = FolderConfig(
            source_folder=source_folder, destination_folder=destination_folder
        )
        self.session.add(folder_config)
        self.session.commit()

    def update_universal_config(self, icon_path, default_behavior):
        config = self.get_universal_config()
        if config:
            config.icon_path = icon_path
            config.default_behavior = default_behavior
            self.session.commit()
        else:
            raise ValueError("Universal config not found.")
