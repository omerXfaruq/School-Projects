import asyncio
from asyncio import StreamReader, StreamWriter
import socket
import models
import json
from typing import List

CHUNK_SIZE = 10**6


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class Peer:
    PORT = 1234
    VERBOSE = False

    @staticmethod
    async def request_chunk(ip, filename: str, chunk_id: int, size):
        reader, writer = await asyncio.open_connection(ip, Peer.PORT)

        message = {"filename": filename, "chunk_id": chunk_id}
        if Peer.VERBOSE:
            print(f"Requesting: {message!r} from {ip}")
        writer.write(json.dumps(message).encode())
        await writer.drain()

        data = await reader.readexactly(size)
        writer.close()
        await writer.wait_closed()
        return data

    @staticmethod
    async def handle_message(reader: StreamReader, writer: StreamWriter):
        """
        Reads and sends a chunk.
        """
        data = await reader.read(CHUNK_SIZE)
        jsondata = json.loads(data)
        file = jsondata["filename"]
        chunk = jsondata["chunk_id"]
        f = open(f"./files/{file}", "rb")
        f.seek(chunk * CHUNK_SIZE)
        data = f.read(CHUNK_SIZE)
        writer.write(data)
        await writer.drain()

        writer.close()
        await writer.wait_closed()

    @staticmethod
    async def start_server():
        server = await asyncio.start_server(
            Peer.handle_message, get_ip_address(), Peer.PORT
        )

        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving Peer on {addrs}")

        async with server:
            await server.serve_forever()


class Tracker:
    PORT = 1233
    TRACKER_IP = None
    FILES: List[models.File] = []

    @staticmethod
    async def get_files() -> models.Files:
        """
        Requests available files from the Tracker.
        """
        reader, writer = await asyncio.open_connection(Tracker.TRACKER_IP, Tracker.PORT)
        writer.write(
            models.Message(type=models.MessageTypes.GET_FILE_LIST)
            .model_dump_json()
            .encode()
        )
        await writer.drain()

        data = await reader.read(50)
        size = int(data.decode())
        data = await reader.readexactly(size)
        files = models.Files(**json.loads(data))
        return files

    @staticmethod
    async def get_file_peers(file: models.FileBase) -> models.File | None:
        """
        Requests the list of peers from the tracker.
        """
        reader, writer = await asyncio.open_connection(Tracker.TRACKER_IP, Tracker.PORT)
        writer.write(
            models.Message(
                type=models.MessageTypes.GET_CHUNK_LOCATIONS, payload=file.model_dump()
            )
            .model_dump_json()
            .encode()
        )
        await writer.drain()
        data = await reader.read(50)
        size = int(data.decode())
        if size == -1:
            return None
        data = await reader.readexactly(size)
        file = models.File(**json.loads(data))
        return file

    @staticmethod
    async def register_file(file: models.FileBase, hashes: List[str]):
        """
        Registers a file to the Tracker.
        """
        reader, writer = await asyncio.open_connection(Tracker.TRACKER_IP, Tracker.PORT)

        body = {
            "file": file.model_dump(),
            "hashes": hashes,
        }
        data = json.dumps(body).encode()

        message = (
            models.Message(
                type=models.MessageTypes.FILE_REGISTER, payload={"size": f"{len(data)}"}
            )
            .model_dump_json()
            .encode()
        )

        writer.write(message)
        await writer.drain()
        await asyncio.sleep(0.01)
        writer.write(data)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    @staticmethod
    async def register_chunk(file: models.FileBase, chunk: int):
        """
        Registers a chunk to the tracker.
        """
        reader, writer = await asyncio.open_connection(Tracker.TRACKER_IP, Tracker.PORT)
        writer.write(
            models.Message(
                type=models.MessageTypes.CHUNK_REGISTER,
                payload={"file": file.model_dump(), "chunk": chunk},
            )
            .model_dump_json()
            .encode()
        )
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    @staticmethod
    async def handle_message(reader: StreamReader, writer: StreamWriter):
        """
        Tracker server, handles all types of messages from the peers.
        """
        data = await reader.read(100)
        data = json.loads(data)
        message = models.Message(**data)

        addr = writer.get_extra_info("peername")

        if message.type == models.MessageTypes.GET_FILE_LIST:
            di = {"files": [fi.file.model_dump() for fi in Tracker.FILES]}
            data = json.dumps(di).encode()
            size = len(data)
            writer.write(f"{size}".encode())
            await writer.drain()
            await asyncio.sleep(0.1)
            writer.write(data)
            await writer.drain()

        elif message.type == models.MessageTypes.GET_CHUNK_LOCATIONS:
            file = next(
                (
                    fi
                    for fi in Tracker.FILES
                    if fi.file == models.FileBase(**message.payload)
                ),
                None,
            )
            if file is None:
                writer.write(f"{-1}".encode())
                await writer.drain()
            else:
                data = json.dumps(file.model_dump()).encode()
                size = len(data)
                writer.write(f"{size}".encode())
                await writer.drain()
                await asyncio.sleep(0.01)
                writer.write(data)
                await writer.drain()

        elif message.type == models.MessageTypes.FILE_REGISTER:
            size = int(message.payload["size"])
            data = await reader.readexactly(size)
            data = json.loads(data)

            filebase = models.FileBase(**data["file"])
            hashes = data["hashes"]

            chunks = [([addr[0]], has) for has in hashes]
            file = models.File(
                file=filebase,
                chunks=chunks,
            )
            Tracker.FILES.append(file)

        elif message.type == models.MessageTypes.CHUNK_REGISTER:
            chunk = message.payload["chunk"]
            filebase = message.payload["file"]
            file = next(
                (fi for fi in Tracker.FILES if fi.file == models.FileBase(**filebase)),
                None,
            )

            file.chunks[chunk][0].append(addr[0])

        writer.close()
        await writer.wait_closed()

    @staticmethod
    async def start_server():
        Tracker.TRACKER_IP = get_ip_address()
        server = await asyncio.start_server(
            Tracker.handle_message, Tracker.TRACKER_IP, Tracker.PORT
        )
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)

        print(f"Serving Tracker on {addrs}\n")

        async with server:
            await server.serve_forever()
