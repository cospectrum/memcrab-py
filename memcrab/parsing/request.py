from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .utils import U32, U64, U8


class RequestKind(Enum):
    Ping = 0
    Get = 1
    Set = 2
    Delete = 3
    Clear = 4

    @classmethod
    def from_val(cls, val: int) -> RequestKind:
        match val:
            case cls.Ping.value: return cls.Ping
            case cls.Get.value: return cls.Get
            case cls.Set.value: return cls.Set
            case cls.Delete.value: return cls.Delete
            case cls.Clear.value: return cls.Clear
            case _:
                raise ValueError

    def flag(self) -> U8:
        return U8(self.value)


class Request(ABC):
    @abstractmethod
    def payload(self) -> bytes:
        raise TypeError
    @abstractmethod
    def kind(self) -> RequestKind:
        raise TypeError

class Ping(Request):
    def kind(self) -> RequestKind:
        return RequestKind.Ping
    def payload(self) -> bytes:
        return bytes()

@dataclass
class Get(Request):
    key: str
    def kind(self) -> RequestKind:
        return RequestKind.Get
    def payload(self) -> bytes:
        return self.key.encode()


@dataclass
class Set(Request):
    key: str
    val: bytes
    expiration: int = 0
    def kind(self) -> RequestKind:
        return RequestKind.Set
    def payload(self) -> bytes:
        key = self.key.encode()
        klen = U64(len(key)).be()
        exp = U32(self.expiration).be()
        return klen + exp + key + self.val


@dataclass
class Delete(Request):
    key: str
    def kind(self) -> RequestKind:
        return RequestKind.Delete
    def payload(self) -> bytes:
        return self.key.encode()


class Clear(Request):
    def kind(self) -> RequestKind:
        return RequestKind.Clear
    def payload(self) -> bytes:
        return bytes()
