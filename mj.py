#!/usr/bin/python3

import argparse
import os
import json
import argcomplete
from mj_utils import *

BOARD_NAME = "esp8266"
PORT_NUM = 0
PROJECT_PATH = "unknown"
PROJECT_NAME = "unknown"
USE_ESPTOOL = False


parser = argparse.ArgumentParser(description="Board manager")
subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

commands = {
    "compile": "Compile sketch",
    "upload": "Upload sketch to the board",
    "open-tty": "Open tty of board",
    "1": "Compile and upload sketch",
    "2": "Upload sketch and open tty",
    "3": "Compile, upload, and open tty"
}

for cmd, desc in commands.items():
    subparser = subparsers.add_parser(cmd, help=desc)
    subparser.add_argument("-b", "--board", type=str, default=BOARD_NAME ,choices=["esp8266", "esp32", "arduino"], help="Board name")
    subparser.add_argument("-p", "--port", type=int, default=PORT_NUM, help="Number of /dev/ttyUSB<i>")
    subparser.add_argument("-P", "--project", type=str, default=PROJECT_PATH, help="Path to project .ino")
    subparser.add_argument("-c", "--conf", type=str, help="Path to configuration")
    subparser.add_argument("-e", "--use-esptool", type=bool, default=USE_ESPTOOL, help="Use esptool instead of arduino-cli")

argcomplete.autocomplete(parser)
args = parser.parse_args()


print("-------------------------------------------")
print("---------------BOARD-MANAGER---------------")

if args.conf :
    if not os.path.exists(args.conf):
        print("-------------------------------------------")
        print_red(f"Config does not exist: {args.conf}")
        print("-------------------------------------------")
        print_red("Fail :(")
        print("-------------------------------------------")
        exit(-1)
    with open(args.conf, "r") as config_file:
        config_data = json.load(config_file)
    BOARD_NAME = config_data.get("board", BOARD_NAME)
    PORT_NUM = config_data.get("port", PORT_NUM)
    PROJECT_PATH = config_data.get("project", PROJECT_PATH)
    USE_ESPTOOL = config_data.get("use-esptool", USE_ESPTOOL)

else:
    BOARD_NAME = args.board
    PORT_NUM = args.port
    PROJECT_PATH = args.project
    USE_ESPTOOL = args.use_esptool

PROJECT_NAME = os.path.basename(PROJECT_PATH)

if not os.path.exists(PROJECT_PATH):
        print("-------------------------------------------")
        print_red(f"Project does not exist: {PROJECT_PATH}")
        print("-------------------------------------------")
        print_red("Fail :(")
        print("-------------------------------------------")
        exit(-1)

print("-------------------------------------------")
if args.conf:
    print_yellow(f"--- Conf read from: {args.conf}")
    print("-------------------------------------------")
print(f"Board: {BOARD_NAME}")
print(f"Port: {PORT_NUM}")
print(f"Project: {PROJECT_PATH}")
print(f"Use esptool: {USE_ESPTOOL}")
print("-------------------------------------------")
print_green("Successfully get configuration :)")
print("-------------------------------------------")


if args.command == "compile":
    compile_project(BOARD_NAME, PROJECT_PATH)

elif args.command == "upload":
    upload_project(BOARD_NAME, PROJECT_PATH, PORT_NUM, USE_ESPTOOL)

elif args.command == "open-tty":
    open_tty(PORT_NUM)

elif args.command == "1":
    compile_and_upload(BOARD_NAME, PROJECT_PATH, PORT_NUM, USE_ESPTOOL)

elif args.command == "2":
    upload_and_open_tty(BOARD_NAME, PROJECT_PATH, PORT_NUM, USE_ESPTOOL)

elif args.command == "3":
    compile_upload_and_open_tty(BOARD_NAME, PROJECT_PATH, PORT_NUM, USE_ESPTOOL)

