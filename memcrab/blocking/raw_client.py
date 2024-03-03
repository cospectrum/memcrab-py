from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar
from memcrab.parsing import Request, Response
from memcrab.parsing.request import Get, Set
from memcrab.parsing.response import Error, KeyNotFound, Ok, Value

from .connections import Tcp


class Rpc(Protocol):
    def call(self, request: Request) -> Response:
        ...


C = TypeVar('C', bound=Rpc)


@dataclass
class RawClient(Generic[C]):
    conn: C

    @staticmethod
    def tcp(addr: str) -> RawClient[Tcp]:
        conn = Tcp.connect(addr)
        return RawClient(conn)

    def get(self, key: str) -> bytes | None:
        resp = self.conn.call(Get(key))
        match resp:
            case Value(val):
                return val
            case KeyNotFound():
                return None
            case msg:
                hint = f'unexpected msg: {msg}'
                raise TypeError(hint)

    def set(self, key: str, val: bytes) -> None | Error:
        resp = self.conn.call(Set(key=key, val=val))
        match resp:
            case Ok():
                return None
            case Error():
                return resp
            case msg:
                hint = f'unexpected msg: {msg}'
                raise TypeError(hint)
