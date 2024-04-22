from pathlib import Path
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer
from time import sleep

src_dir = Path(r"C:\Users\sebastian\Downloads")

# folder map for respective file extensions
folder_names = {
    "Audio": {'aif', 'cda', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wav', 'wma'},
    "Compressed": {'7z', 'deb', 'pkg', 'rar', 'rpm', 'gz', 'z', 'zip', 'bz2', 'xz', 'gzip'},
    'Code': {'js', 'jsp', 'html', 'ipynb', 'py', 'java', 'css'},
    'Documents': {'ppt', 'pptx', 'pdf', 'xls', 'xlsx', 'doc', 'docx', 'txt', 'tex', 'epub', 'csv'},
    'Images': {'bmp', 'gif', 'ico', 'jpeg', 'jpg', 'png', 'jfif', 'svg', 'tif', 'tiff'},
    'Softwares': {'apk', 'bat', 'bin', 'exe', 'jar', 'msi', 'py'},
    'Videos': {'3gp', 'avi', 'flv', 'h264', 'mkv', 'mov', 'mp4', 'mpg', 'mpeg', 'wmv'},
}

# check whether the necessary folders are present if not make those directories
[src_dir.joinpath(folder_name).mkdir(parents=True, exist_ok=True) for folder_name in folder_names.keys()]


# get new name for the file if the file already exists
def unique_name(name: Path):
    counter = 1
    while name.exists():
        name = name.parent / f'{name.stem.rstrip(f' ({counter-1})')} ({counter}){name.suffix}'
        counter += 1
    return name


# move files to destination folder
def move_file(dst_folder: Path, curr_file_path: Path) -> None:
    curr_file_path.replace(unique_name(dst_folder / curr_file_path.name))


# event handler to check and move files to the respective folders
class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event: FileSystemEvent) -> None:
        file_set = {file for file in src_dir.glob('*') if file.is_file() } #and file.suffix != '.tmp'

        for folder, extensions in folder_names.items():
            if file_set:
                dst_folder = src_dir / folder
                [move_file(dst_folder, file) for file in file_set if file.suffix[1:].lower() in extensions]


if __name__ == '__main__':
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, str(src_dir), recursive=False)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()
