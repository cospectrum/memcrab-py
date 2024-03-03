from .response import Error, KeyNotFound, Ok, Pong, Response, ResponseKind, Value
from .request import Clear, Delete, Get, Ping, Request, RequestKind, Set
from .utils import U64, U8
from .aliases import KeyLen, Expiration

MsgKind = RequestKind | ResponseKind
Msg = Request | Response


HEADER_SIZE = U8.sizeof() + U64.sizeof()


def kind_from_flag(flag: int) -> MsgKind:
    if flag < 128:
        return RequestKind.from_val(flag)
    return ResponseKind.from_val(flag)


class Parser:
    def decode_header(self, chunk: bytes) -> tuple[MsgKind, int]:
        assert len(chunk) == HEADER_SIZE
        kind = kind_from_flag(chunk[0])
        payload_len = int.from_bytes(chunk[1:])
        return kind, payload_len

    def encode(self, msg: Msg) -> bytes:
        flag = msg.kind().flag().be()
        payload = msg.payload()
        payload_len = U64(len(payload)).be()
        return flag + payload_len + payload

    def decode(self, kind: MsgKind, payload: bytes) -> Msg:
        if isinstance(kind, RequestKind):
            return self.decode_request(kind, payload)
        return self.decode_response(kind, payload)

    def decode_request(self, kind: RequestKind, payload: bytes) -> Request:
        Kind = RequestKind

        def split_at(slice: bytes, at: int) -> tuple[bytes, bytes]:
            return slice[:at], slice[at:]

        match kind:
            case Kind.Ping: return Ping()
            case Kind.Get: return Get(payload.decode())
            case Kind.Set:
                klen_bytes, tail = split_at(payload, KeyLen.sizeof())
                exp_bytes, tail = split_at(tail, Expiration.sizeof())

                klen = KeyLen.from_be(klen_bytes)
                expiration = Expiration.from_be(exp_bytes)
                key, val = split_at(tail, klen.inner)
                return Set(key=key.decode(), val=val, expiration=expiration.inner)

            case Kind.Clear: return Clear()
            case Kind.Delete: return Delete(payload.decode())

    def decode_response(self, kind: ResponseKind, payload: bytes) -> Response:
        Kind = ResponseKind
        match kind:
            case Kind.Ok: return Ok()
            case Kind.Pong: return Pong()
            case Kind.KeyNotFound: return KeyNotFound()
            case Kind.Value: return Value(payload)
            case Kind.Error: return Error(msg=payload.decode())
