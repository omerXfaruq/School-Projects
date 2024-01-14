from typing import Optional, List, Any, Tuple
from pydantic import BaseModel, Field
from enum import Enum


class MessageTypes(Enum):
    GET_FILE_LIST = 1
    GET_CHUNK_LOCATIONS = 2
    FILE_REGISTER = 3
    CHUNK_REGISTER = 4


class Message(BaseModel):
    type: MessageTypes
    payload: dict = {}


class FileBase(BaseModel):
    name: str
    size: int


class Files(BaseModel):
    files: List[FileBase]


class File(BaseModel):
    file: FileBase
    chunks: List[Tuple[List[str], str]]  # ip addresses and hash for each chunk


if __name__ == "__main__":
    Message(type=MessageTypes.GET_FILE_LIST)
