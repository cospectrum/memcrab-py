from __future__ import annotations

import socket

from dataclasses import dataclass

from memcrab.parsing import Request, Response, ResponseKind, Parser, HEADER_SIZE


@dataclass
class Tcp:
    sock: socket.socket
    parser: Parser
    _closed: bool

    @staticmethod
    def connect(addr: str) -> Tcp:
        sock = socket.socket()
        sock.connect(addr)
        return Tcp(sock, _closed=True, parser=Parser())

    def call(self, request: Request) -> Response:
        send = self.parser.encode(request)
        self.sock.sendall(send)
        header_bytes = self.read_exact(HEADER_SIZE)
        kind, payload_len = self.parser.decode_header(header_bytes)
        assert isinstance(kind, ResponseKind)
        payload = self.read_exact(payload_len)
        return self.parser.decode_response(kind, payload)

    def read_exact(self, n: int) -> bytes:
        if n == 0:
            return bytes()
        with self.sock.makefile('rb') as f:
            bs = f.read(n)
        assert len(bs) == n
        return bs

    def close(self) -> None:
        if not self._closed:
            self.sock.close()
            self._closed = True

    def __del__(self) -> None:
        self.close()
