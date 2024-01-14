import inquirer
from inquirer import Text
from network import Tracker, Peer, CHUNK_SIZE
import models
import asyncio
import sys
import os
import hashlib
from typing import List
from transfer import Download


def get_tracker_info():
    questions = [
        inquirer.List(
            "option",
            message="What would you like to do?",
            choices=["Assign a tracker", "Join as tracker"],
        ),
    ]

    option = inquirer.prompt(questions)["option"]
    if option == "Join as tracker":
        asyncio.create_task(Tracker.start_server())
    elif option == "Assign a tracker":
        question = [
            Text(name="ip", message="Give the Tracker IP"),
        ]
        response = inquirer.prompt(question)
        Tracker.TRACKER_IP = response["ip"]
        print(f"Tracker assigned: {Tracker.TRACKER_IP}")


def download_select_file(file_names):
    file_names.append("Go back")
    questions = [
        inquirer.List(
            "option",
            message="Which file would you like to download?",
            choices=file_names,
        ),
    ]

    option = inquirer.prompt(questions)
    return option["option"]


def upload_select_file():
    file_names = os.listdir("./files")
    file_names.append("Go back")
    questions = [
        inquirer.List(
            "option",
            message="Which file would you like to upload?",
            choices=file_names,
        ),
    ]

    option = inquirer.prompt(questions)
    return option["option"]


def get_input():
    questions = [
        inquirer.List(
            "option",
            message="What would you like to do?",
            choices=[
                "Download a file",
                "Upload a file",
                "See current status",
                "Exit the program",
            ],
        ),
    ]

    option = inquirer.prompt(questions)
    return option["option"]


def create_hash_values(filebase: models.FileBase) -> List[str]:
    """
    Creates hash for each chunk and returns a list.
    """
    f = open(f"./files/{filebase.name}", "rb")
    hashes = []
    for i in range(filebase.size // CHUNK_SIZE):
        data = f.read(CHUNK_SIZE)
        md5 = hashlib.md5(data)
        hashes.append(md5.hexdigest())
    if filebase.size % CHUNK_SIZE != 0:
        data = f.read(filebase.size % CHUNK_SIZE)
        md5 = hashlib.md5(data)
        hashes.append(md5.hexdigest())
    return hashes


async def main():
    """
    User interface
    """
    print("Welcome Onboard to Bittorrentpy")

    get_tracker_info()

    asyncio.create_task(Peer.start_server())
    while True:
        option = await asyncio.get_event_loop().run_in_executor(None, get_input)
        if option == "Download a file":
            files = await Tracker.get_files()
            file_names = [
                f"{ind}: {fi.name}({round(fi.size / 10 ** 6, 3)}MB)"
                for ind, fi in enumerate(files.files)
            ]
            selected = download_select_file(file_names)
            if selected == "Go back":
                continue

            file = await Tracker.get_file_peers(
                files.files[int(selected[: selected.find(":")])]
            )
            asyncio.create_task(Download.create_download(file))

        elif option == "Upload a file":
            selected = upload_select_file()
            if selected == "Go back":
                continue
            size = os.path.getsize(f"./files/{selected}")
            file = models.FileBase(name=selected, size=size)
            hashes = await asyncio.get_event_loop().run_in_executor(
                None, create_hash_values, file
            )
            await Tracker.register_file(file, hashes)
            status = {"file": file, "finished": 1.0}
            Download.active_files.append(status)

        elif option == "See current status":
            print(f"Local files: {Download.active_files}")

        elif option == "Exit the program":
            sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        Peer.VERBOSE = True
    asyncio.run(main())
