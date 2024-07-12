
# iCloud Sync Imgage Converter

<img src="imgs/PhluxApps.svg" alt="iCloudSyncImgConverter Logo" height="120">

<img src="imgs/icsic_logo.svg" alt="iCloudSyncImgConverter Logo" height="275">

[iCloud Sync Imgage Converter](https://github.com/jcphlux/iCoudSyncImgConverter) is a Python-based application designed to synchronize and process images from iCloud Photos. The application monitors specified folders, converts HEIC/HEVC images to JPG format, and handles file synchronization between source and destination directories.

## Features

- Monitors multiple source directories for new and modified files.
- Converts HEIC/HEVC images to JPG format.
- Option to either copy files or create symbolic links for non-HEIC/HEVC files.
- Synchronizes deletions between source and destination directories.
- Provides a system tray icon for easy control and configuration access.
- Uses a SQLite database to keep track of processed files.

## Requirements

- Python 3.6 or higher
- PyQt5
- Pillow
- watchdog
- SQLAlchemy
- pillow_heif

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/jcphlux/iCoudSyncImgConverter.git
    cd iCoudSyncImgConverter
    ```

2. create environment:

    ```sh
    python -m venv .venv
    ```

3. Start environment:

    ```sh
    .venv\Scripts\activate
    ```

4. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```sh
    python main.py
    ```

2. The first time you run the application, the configuration UI will open. Set your source and destination folders, icon path, and default behavior.

3. The application will start monitoring the specified source folders and processing files according to your settings.

## Configuration

The configuration can be changed at any time by accessing the configuration UI from the system tray icon.

### Configuration UI

- **Source Folder**: The folder to monitor for new and modified files.
- **Destination Folder**: The folder where processed files will be saved.
- **Icon Path**: Path to the system tray icon.
- **Default Behavior**: Choose between creating symbolic links or copying files for non-HEIC/HEVC files.

## Folder Structure

- `main.py`: Entry point of the application.
- `config.py`: Configuration loader and saver.
- `config_ui.py`: Configuration UI using PyQt5.
- `database.py`: Database initialization and session management.
- `file_processor.py`: File processing and event handling.
- `models.py`: Database models.
- `utils.py`: Utility functions and system tray icon management.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3. See the [LICENSE](LICENSE) file for more information.

## Contact

For any questions or inquiries, please contact us at [email protected]
