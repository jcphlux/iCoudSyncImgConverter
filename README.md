# iCoudSyncImgConverter

iCloudSync is a tool designed to monitor a folders for changes, convert HEIC files to JPG, and either create symbolic links or copy other files to a destination folder. It includes a configuration UI for easy management of settings.

## Features

- Monitor a specified folder for changes
- Convert HEIC files to JPG format
- Create symbolic links or copy files to a destination folder
- Configuration settings stored in a SQLite database
- System tray icon for easy control
- Configuration UI for managing settings

## Requirements

- Python 3.x
- `tkinter` (for configuration UI)
- `watchdog`
- `sqlalchemy`
- `pillow`
- `pillow-heif`
- `pystray`
- `cairosvg`

## Installation

### Install Python and Required Packages

Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

### Install Required Python Packages

```sh
pip install watchdog sqlalchemy pillow pillow-heif pystray cairosvg


1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/iCloudSync.git
    ```




## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3. See the [LICENSE](LICENSE) file for more information.

## Contact

For any questions or inquiries, please contact us at [email protected]
