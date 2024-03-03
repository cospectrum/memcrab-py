from __future__ import annotations

from abc import ABC, abstractmethod
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
    @abstractmethod
    def kind(self) -> ResponseKind:
        raise TypeError

    @abstractmethod
    def payload(self) -> bytes:
        raise TypeError


class Pong(Response):
    def kind(self) -> ResponseKind:
        return ResponseKind.Pong

    def payload(self) -> bytes:
        return bytes()


class Ok(Response):
    def kind(self) -> ResponseKind:
        return ResponseKind.Ok

    def payload(self) -> bytes:
        return bytes()


@dataclass
class Value(Response):
    inner: bytes

    def kind(self) -> ResponseKind:
        return ResponseKind.Value

    def payload(self) -> bytes:
        return self.inner


class KeyNotFound(Response):
    def kind(self) -> ResponseKind:
        return ResponseKind.KeyNotFound

    def payload(self) -> bytes:
        return bytes()


@dataclass
class Error(Response):
    msg: str

    def kind(self) -> ResponseKind:
        return ResponseKind.Error

    def payload(self) -> bytes:
        return self.msg.encode()
