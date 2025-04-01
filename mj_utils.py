import subprocess
import os

board_map = {
    "esp8266": "esp8266:esp8266:nodemcu",
    "esp32": "esp32:esp32:devkitC",
    "nano": "arduino:avr:nano",
    "uno": "arduino:avr:uno"
}

def print_yellow(text):
    print(f"\033[33m{text}\033[0m")  # yellow color

def print_green(text):
    print(f"\033[32m{text}\033[0m")  # green color

def print_red(text):
    print(f"\033[31m{text}\033[0m")  # red color

def compile_project(board_name: str, project_path: str) -> bool:
    try:
        command = ["arduino-cli", "compile", "--fqbn", board_map[board_name], project_path, "--output-dir", f"/tmp/arduino/"]
        print_yellow(f"Running command: {' '.join(command)}")
        print("-------------------------------------------")
        subprocess.run(command, check=True)
        print("-------------------------------------------")
        print_green("Compilation successful!")
        print("-------------------------------------------")
        return True
    except subprocess.CalledProcessError:
        print("-------------------------------------------")
        print_red("Compilation failed!")
        print("-------------------------------------------")
        return False

def upload_project(board_name: str, project_path: str, port_num: int, use_esptool: bool) -> bool:
    project_name = os.path.basename(project_path)
    try:
        if use_esptool:
            command = ["esptool.py", "--chip", f"{board_name}", "--port", f"/dev/ttyUSB{port_num}", "--baud", "921600", "write_flash", "0x00000", f"/tmp/arduino/{project_name}.bin"]
        else:
            command = ["arduino-cli", "upload", "-p", f"/dev/ttyUSB{port_num}", "--fqbn", board_name, project_path, "--input-file", f"/tmp/arduino/{project_name}.bin"]
        
        print_yellow(f"Running command: {' '.join(command)}")
        print("-------------------------------------------")
        subprocess.run(command, check=True)
        print("-------------------------------------------")
        print_green("Upload successful!")
        print("-------------------------------------------")
        return True
    except subprocess.CalledProcessError:
        print("-------------------------------------------")
        print_red("Upload failed!")
        print("-------------------------------------------")
        return False

def open_tty(port_num: int) -> bool:
    try:
        command = ["screen", f"/dev/ttyUSB{port_num}", "115200"]
        print_yellow(f"Running command: {' '.join(command)}")
        print("-------------------------------------------")
        subprocess.run(command, check=True)
        print("-------------------------------------------")
        print_green("TTY opened successfully!")
        print("-------------------------------------------")
        return True
    except subprocess.CalledProcessError:
        print("-------------------------------------------")
        print_red("Failed to open tty!")
        print("-------------------------------------------")
        return False

def compile_and_upload(board_name: str, project_path: str, port_num: int, use_esptool: bool) -> bool:
    if compile_project(board_name, project_path):
        return upload_project(board_name, project_path, port_num, use_esptool)
    return False

def upload_and_open_tty(board_name: str, project_path: str, port_num: int, use_esptool: bool) -> bool:
    if upload_project(board_name, project_path, port_num, use_esptool):
        return open_tty(port_num)
    return False

def compile_upload_and_open_tty(board_name: str, project_path: str, port_num: int, use_esptool: bool) -> bool:
    if compile_project(board_name, project_path):
        if upload_project(board_name, project_path, port_num, use_esptool):
            return open_tty(port_num)
    return False

