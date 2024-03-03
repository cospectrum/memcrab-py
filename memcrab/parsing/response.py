from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import Enum

from .utils import U8


class ResponseKind(Enum):
    Pong = 128
    Ok = 129
    Value = 130
    KeyNotFound = 131
    Error = 255

    @classmethod
    def from_val(cls, val: int) -> ResponseKind:
        match val:
            case cls.Pong.value:
                return cls.Pong
            case cls.Ok.value:
                return cls.Ok
            case cls.Value.value:
                return cls.Value
            case cls.KeyNotFound.value:
                return cls.KeyNotFound
            case cls.Error.value:
                return cls.Error
            case _:
                raise ValueError

    def flag(self) -> U8:
        return U8(self.value)


class Response(ABC):
    pass


class Pong(Response):
    pass


class Ok(Response):
    pass


@dataclass
class Value(Response):
    inner: bytes


class KeyNotFound(Response):
    pass


@dataclass
class Error(Response):
    msg: str
