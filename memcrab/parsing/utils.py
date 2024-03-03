from __future__ import annotations


class U8:
    inner: int

    def __init__(self, val: int) -> None:
        assert 0 <= val <= U8.max()
        self.inner = val

    @staticmethod
    def max() -> int:
        return 255

    def be(self) -> bytes:
        return self.inner.to_bytes(self.sizeof(), "big")

    @staticmethod
    def from_be(slice: bytes) -> U8:
        return U8(int.from_bytes(slice))

    @classmethod
    def sizeof(cls) -> int:
        return 1


class U32:
    inner: int

    def __init__(self, val: int) -> None:
        assert 0 <= val <= U64.max()
        self.inner = val

    @staticmethod
    def max() -> int:
        return 2**32 - 1

    def be(self) -> bytes:
        return self.inner.to_bytes(self.sizeof(), "big")

    @staticmethod
    def from_be(slice: bytes) -> U32:
        return U32(int.from_bytes(slice))

    @classmethod
    def sizeof(cls) -> int:
        return 32 // 8


class U64:
    inner: int

    def __init__(self, val: int) -> None:
        assert 0 <= val <= U64.max()
        self.inner = val

    @staticmethod
    def max() -> int:
        return 2**64 - 1

    def be(self) -> bytes:
        return self.inner.to_bytes(self.sizeof(), "big")

    @staticmethod
    def from_be(slice: bytes) -> U64:
        return U64(int.from_bytes(slice))

    @classmethod
    def sizeof(cls) -> int:
        return 64 // 8
