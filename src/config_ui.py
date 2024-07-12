import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QHBoxLayout,
    QMessageBox,
)
from config import ConfigLoader


class ConfigUI(QWidget):
    def __init__(self):
        super().__init__()
        self.config_loader = ConfigLoader()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Source folder selection
        self.source_folder_label = QLabel("Source Folder: Not Selected", self)
        self.layout.addWidget(self.source_folder_label)
        self.source_folder_button = QPushButton("Select Source Folder", self)
        self.source_folder_button.clicked.connect(self.select_source_folder)
        self.layout.addWidget(self.source_folder_button)

        # Destination folder selection
        self.destination_folder_label = QLabel("Destination Folder: Not Selected", self)
        self.layout.addWidget(self.destination_folder_label)
        self.destination_folder_button = QPushButton("Select Destination Folder", self)
        self.destination_folder_button.clicked.connect(self.select_destination_folder)
        self.layout.addWidget(self.destination_folder_button)

        # Add folder config button
        self.add_button = QPushButton("Add Folder Config", self)
        self.add_button.clicked.connect(self.add_folder_config)
        self.layout.addWidget(self.add_button)

        # Icon path selection
        self.icon_path_label = QLabel("Icon Path: Not Selected", self)
        self.layout.addWidget(self.icon_path_label)
        self.icon_path_button = QPushButton("Select Icon Path", self)
        self.icon_path_button.clicked.connect(self.select_icon_path)
        self.layout.addWidget(self.icon_path_button)

        # Default behavior selection
        self.default_behavior_label = QLabel("Default Behavior:", self)
        self.layout.addWidget(self.default_behavior_label)
        self.default_behavior_symbolic = QRadioButton("Symbolic Link", self)
        self.default_behavior_copy = QRadioButton("Copy File", self)
        behavior_layout = QHBoxLayout()
        behavior_layout.addWidget(self.default_behavior_symbolic)
        behavior_layout.addWidget(self.default_behavior_copy)
        self.layout.addLayout(behavior_layout)

        # Save universal config button
        self.save_button = QPushButton("Save Universal Config", self)
        self.save_button.clicked.connect(self.save_universal_config)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)
        self.setWindowTitle("Config UI")
        self.load_config()
        self.show()

    def select_source_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_folder_label.setText(f"Source Folder: {folder}")

    def select_destination_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.destination_folder_label.setText(f"Destination Folder: {folder}")

    def select_icon_path(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select Icon File", "", "Images (*.png *.xpm *.jpg)"
        )
        if file:
            self.icon_path_label.setText(f"Icon Path: {file}")

    def add_folder_config(self):
        source_folder = self.source_folder_label.text().replace("Source Folder: ", "")
        destination_folder = self.destination_folder_label.text().replace(
            "Destination Folder: ", ""
        )

        try:
            self.config_loader.add_folder_config(source_folder, destination_folder)
            QMessageBox.information(
                self, "Success", "Folder configuration added successfully!"
            )
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_universal_config(self):
        icon_path = self.icon_path_label.text().replace("Icon Path: ", "")
        default_behavior = (
            "symbolic" if self.default_behavior_symbolic.isChecked() else "copy"
        )

        try:
            self.config_loader.update_universal_config(icon_path, default_behavior)
            QMessageBox.information(
                self, "Success", "Universal configuration saved successfully!"
            )
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_config(self):
        folder_configs = self.config_loader.get_all_folder_configs()
        if folder_configs:
            self.source_folder_label.setText(
                f"Source Folder: {folder_configs[0].source_folder}"
            )
            self.destination_folder_label.setText(
                f"Destination Folder: {folder_configs[0].destination_folder}"
            )

        universal_config = self.config_loader.get_universal_config()
        if universal_config:
            self.icon_path_label.setText(f"Icon Path: {universal_config.icon_path}")
            if universal_config.default_behavior == "symbolic":
                self.default_behavior_symbolic.setChecked(True)
            else:
                self.default_behavior_copy.setChecked(True)


def launch_config_ui():
    app = QApplication(sys.argv)
    ex = ConfigUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch_config_ui()
