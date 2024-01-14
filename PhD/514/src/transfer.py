import asyncio
from typing import List
import models
from network import CHUNK_SIZE, Peer, Tracker
import random
import hashlib
import math

CONCURRENCY_LIMIT = 10
LOCK = asyncio.Lock()

class Download:
    active_files = []
    current_chunks = [None] * CONCURRENCY_LIMIT

    @staticmethod
    async def create_download(file: models.File):
        """
        Creates a file, and downloads the data from peers.

        Args:
            file:

        Returns:

        """
        status = {"file": file.file, "finished": 0}
        Download.active_files.append(status)
        f = open(f"./files/{file.file.name}", "wb")
        f.seek(file.file.size - 1)
        f.write(b"\0")
        f.close()

        rarest_indexes = [
            i[0] for i in sorted(enumerate(file.chunks), key=lambda x: x[1][0])
        ]
        chunk_count = len(file.chunks)
        size = file.file.size
        for i in range(math.ceil(chunk_count / CONCURRENCY_LIMIT)):
            await asyncio.gather(
                *[
                    Download.download_chunk(
                        file.file,
                        file.chunks[i][0],
                        file.chunks[i][1],
                        i,
                        chunk_count,
                        size,
                    )
                    for i in rarest_indexes[
                        i * CONCURRENCY_LIMIT : (i + 1) * CONCURRENCY_LIMIT
                    ]
                ]
            )
            status["finished"] = round(i * CONCURRENCY_LIMIT / len(file.chunks), 2)

        status["finished"] = 1.0
        print(f"Finished Downloading {file.file.name}")

    @staticmethod
    async def download_chunk(
        filebase: models.FileBase,
        peers: List[str],
        mhash: str,
        chunk_id: int,
        chunk_count: int,
        filesize: int,
    ):
        """
        Downloads a chunk from available peers. Retries until it gets the correct chunk.
        """
        if chunk_count - 1 == chunk_id and filesize % CHUNK_SIZE != 0:
            size = filesize % CHUNK_SIZE
        else:
            size = CHUNK_SIZE

        data = await Peer.request_chunk(
            random.choice(peers), filebase.name, chunk_id, size
        )
        md5 = hashlib.md5(data).hexdigest()
        if md5 != mhash:
            print(
                f"Incorrect chunk received, chunk: {chunk_id} downloading it from another peer, calc hash: {md5}, original hash: {mhash}"
            )
            await Download.download_chunk(
                filebase, peers, mhash, chunk_id, chunk_count, filesize
            )
        async with LOCK:
            with open(f"./files/{filebase.name}", "r+b") as f:
                f.seek(chunk_id * CHUNK_SIZE)
                f.write(data)

        await Tracker.register_chunk(filebase, chunk_id)
