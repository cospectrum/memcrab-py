from memcrab.parsing.aliases import PayloadLen
from .response import Error, KeyNotFound, Ok, Pong, Response, ResponseKind, Value
from .request import Request
from .utils import U64, U8


HEADER_SIZE = U8.sizeof() + U64.sizeof()


class Parser:
    def encode_request(self, req: Request) -> bytes:
        flag = req.kind().flag().be()
        payload = req.payload()
        header = flag + PayloadLen(len(payload)).be()
        return header + payload

    def decode_header(self, chunk: bytes) -> tuple[ResponseKind, int]:
        assert len(chunk) == HEADER_SIZE
        kind = ResponseKind.from_val(chunk[0])
        return kind, PayloadLen.from_be(chunk[1:]).inner

    def decode_response(self, kind: ResponseKind, payload: bytes) -> Response:
        Kind = ResponseKind
        match kind:
            case Kind.Ok:
                return Ok()
            case Kind.Pong:
                return Pong()
            case Kind.KeyNotFound:
                return KeyNotFound()
            case Kind.Value:
                return Value(payload)
            case Kind.Error:
                return Error(msg=payload.decode())
