from __future__ import annotations

import socket

from dataclasses import dataclass
from memcrab.parsing import Request, Response, ResponseKind, Parser, HEADER_SIZE


@dataclass
class Tcp:
    sock: socket.socket
    parser: Parser
    _closed: bool

    def call(self, request: Request) -> Response:
        send = self.parser.encode(request)
        self.sock.sendall(send)
        header_bytes = self.read_exact(HEADER_SIZE)
        kind, payload_len = self.parser.decode_header(header_bytes)
        assert isinstance(kind, ResponseKind)
        payload = self.read_exact(payload_len)
        return self.parser.decode_response(kind, payload)

    @staticmethod
    def connect(addr: tuple[str, int]) -> Tcp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(addr)
        return Tcp(sock, _closed=False, parser=Parser())

    def read_exact(self, size: int) -> bytes:
        buff = bytearray(size)
        pos = 0
        while pos < size:
            n = self.sock.recv_into(memoryview(buff)[pos:])
            if n == 0:
                raise EOFError
            pos += n
        return buff

    def close(self) -> None:
        if not self._closed:
            self.sock.close()
            self._closed = True

    def __del__(self) -> None:
        self.close()
