import sys


try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    print(
        "Error: tkinter is not installed. Please install it to use the configuration UI."
    )
    print("On Debian-based systems, use: sudo apt-get install python3-tk")
    print("On Red Hat-based systems, use: sudo yum install python3-tkinter")
    print(
        "On macOS, ensure you have installed Python from python.org or use Homebrew to install it with tkinter support."
    )
    sys.exit(1)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Config
from config import ConfigLoader


class ConfigUI:
    def __init__(self, root):
        self.root = root
        self.root.title("iCloudSync Configuration")

        self.config_loader = ConfigLoader()

        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.folder_to_watch_label = tk.Label(self.frame, text="Folder to Watch:")
        self.folder_to_watch_label.grid(row=0, column=0, sticky="w")
        self.folder_to_watch_entry = tk.Entry(self.frame, width=50)
        self.folder_to_watch_entry.grid(row=0, column=1)

        self.destination_folder_label = tk.Label(self.frame, text="Destination Folder:")
        self.destination_folder_label.grid(row=1, column=0, sticky="w")
        self.destination_folder_entry = tk.Entry(self.frame, width=50)
        self.destination_folder_entry.grid(row=1, column=1)

        self.icon_path_label = tk.Label(self.frame, text="Icon Path:")
        self.icon_path_label.grid(row=2, column=0, sticky="w")
        self.icon_path_entry = tk.Entry(self.frame, width=50)
        self.icon_path_entry.grid(row=2, column=1)

        self.icon_size_label = tk.Label(self.frame, text="Icon Size:")
        self.icon_size_label.grid(row=3, column=0, sticky="w")
        self.icon_size_entry = tk.Entry(self.frame, width=50)
        self.icon_size_entry.grid(row=3, column=1)

        self.default_behavior_label = tk.Label(self.frame, text="Default Behavior:")
        self.default_behavior_label.grid(row=4, column=0, sticky="w")
        self.default_behavior_var = tk.StringVar(value="symbolic")
        self.default_behavior_symbolic = tk.Radiobutton(
            self.frame,
            text="Symbolic Link",
            variable=self.default_behavior_var,
            value="symbolic",
        )
        self.default_behavior_symbolic.grid(row=4, column=1, sticky="w")
        self.default_behavior_copy = tk.Radiobutton(
            self.frame,
            text="Copy File",
            variable=self.default_behavior_var,
            value="copy",
        )
        self.default_behavior_copy.grid(row=4, column=1, sticky="e")

        self.save_button = tk.Button(self.frame, text="Save", command=self.save_config)
        self.save_button.grid(row=5, column=1, sticky="e")

    def load_config(self):
        self.folder_to_watch_entry.insert(
            0, self.config_loader.get_config("folder_to_watch")
        )
        self.destination_folder_entry.insert(
            0, self.config_loader.get_config("destination_folder")
        )
        self.icon_path_entry.insert(0, self.config_loader.get_config("icon_path"))
        self.icon_size_entry.insert(0, self.config_loader.get_config("icon_size"))
        self.default_behavior_var.set(self.config_loader.get_config("default_behavior"))

    def save_config(self):
        self.config_loader.set_config(
            "folder_to_watch", self.folder_to_watch_entry.get()
        )
        self.config_loader.set_config(
            "destination_folder", self.destination_folder_entry.get()
        )
        self.config_loader.set_config("icon_path", self.icon_path_entry.get())
        self.config_loader.set_config("icon_size", self.icon_size_entry.get())
        self.config_loader.set_config(
            "default_behavior", self.default_behavior_var.get()
        )

        messagebox.showinfo("Success", "Configuration saved successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigUI(root)
    root.mainloop()
