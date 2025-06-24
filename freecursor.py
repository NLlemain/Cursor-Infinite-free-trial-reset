import os
import shutil
import ctypes
import winreg
 
def secure_delete(file_path, passes=3):
    try:
        long_path = f"\\\\?\\{file_path}"
        if os.path.isfile(long_path):
            with open(long_path, 'ba+', buffering=0) as f:
                length = f.tell()
                for _ in range(passes):
                    f.seek(0)
                    f.write(os.urandom(length))
            os.remove(long_path)
            print(f"Securely deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")
 
def delete_directory(directory_path):
    try:
        long_path = f"\\\\?\\{directory_path}"
        if os.path.exists(long_path):
            shutil.rmtree(long_path, ignore_errors=True)
            print(f"Deleted directory: {directory_path}")
    except Exception as e:
        print(f"Error deleting {directory_path}: {e}")
 
def delete_registry_key(root, path):
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_ALL_ACCESS) as key:
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                subkey = winreg.EnumKey(key, 0)
                delete_registry_key(root, f"{path}\\{subkey}")
            winreg.DeleteKey(root, path)
            print(f"Deleted registry key: {path}")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error deleting registry key {path}: {e}")
 
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
 
def wipe_cursor_traces():
    cursor_paths = [
        os.path.expandvars(r"%APPDATA%\Cursor"),
        os.path.expandvars(r"%LOCALAPPDATA%\Cursor"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Cursor"),
        os.path.expandvars(r"%TEMP%\Cursor"),
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Cursor"),
        os.path.expandvars(r"%USERPROFILE%\.cursor"),  # hidden folder
        os.path.expandvars(r"%PROGRAMDATA%\Cursor"),
        os.path.expandvars(r"%LOCALAPPDATA%\CursorInstaller"),
        os.path.expandvars(r"%APPDATA%\Roaming\Cursor"),
        os.path.expandvars(r"%APPDATA%\CursorData"),
    ]
 
    for path in cursor_paths:
        if os.path.isdir(path):
            delete_directory(path)
        elif os.path.isfile(path):
            secure_delete(path)
 
    # Remove possible registry keys
    registry_keys = [
        r"Software\Cursor",
        r"Software\Classes\Cursor",
        r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Cursor",
    ]
 
    for key_path in registry_keys:
        delete_registry_key(winreg.HKEY_CURRENT_USER, key_path)
        delete_registry_key(winreg.HKEY_LOCAL_MACHINE, key_path)
 
def main():
    if not is_admin():
        print("This script requires administrative privileges to run.")
        return
 
    print("Wiping Cursor app traces...")
    wipe_cursor_traces()
    print("Done.")
 
if __name__ == "__main__":
    main()
 
 
