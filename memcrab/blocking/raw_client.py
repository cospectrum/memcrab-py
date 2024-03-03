from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Never, Protocol, TypeVar
from memcrab.parsing import Request, Response
from memcrab.parsing.request import Clear, Delete, Get, Ping, Set
from memcrab.parsing.response import KeyNotFound, Ok, Pong, Value

from .connections import Tcp


class Rpc(Protocol):
    def call(self, request: Request) -> Response: ...


C = TypeVar("C", bound=Rpc)


@dataclass
class RawClient(Generic[C]):
    conn: C

    @staticmethod
    def tcp(addr: tuple[str, int]) -> RawClient[Tcp]:
        conn = Tcp.connect(addr)
        return RawClient(conn)

    def ping(self) -> None:
        match self.conn.call(Ping()):
            case Pong():
                return None
            case _:
                raise ValueError("ping failed")

    def get(self, key: str) -> bytes | None:
        match self.conn.call(Get(key)):
            case Value(val):
                return val
            case KeyNotFound():
                return None
            case resp:
                invalid_resp(resp)

    def set(self, key: str, val: bytes) -> None:
        match self.conn.call(Set(key, val)):
            case Ok():
                return None
            case resp:
                invalid_resp(resp)

    def delete(self, key: str) -> None:
        match self.conn.call(Delete(key)):
            case Ok():
                return None
            case KeyNotFound():
                raise ValueError(f"{key=} not found")
            case resp:
                invalid_resp(resp)

    def clear(self) -> None:
        match self.conn.call(Clear()):
            case Ok():
                return None
            case resp:
                invalid_resp(resp)


def invalid_resp(resp: Response) -> Never:
    raise TypeError(f"unexpected response: {resp}")
