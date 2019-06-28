import enum
import struct
from typing import Dict


class Endianness(enum.Enum):
    LITTLE_ENDIAN = 1
    BIG_ENDIAN = 2


class AccountStateBlobDeserializer():
    """AccountStateBlob Deserializer

    Value Encoding:
    +---------+---------+---------+---------+---------+---------+
    | 4 Bytes | N Bytes | 8 Bytes | 8 Bytes | 8 Bytes | 8 Bytes |
    +---------+---------+---------+---------+---------+---------+
        |         |         |         |         |         |
        |         |         |         |         |         + Sequence Number
        |         |         |         |         |
        |         |         |         |         + Sent Events Count
        |         |         |         |
        |         |         |         + Received Events Count
        |         |         |
        |         |         + Balance
        |         |
        |         + Authentication Key (Auth Key Length in bytes)
        |
        + Authentication Key Length

    """
    def __init__(self, blob: bytes) -> None:
        self._blob = blob

    def run(self) -> dict:
        deserializer = LibraDeserializer()
        btree = deserializer.decode_btreemap(self._blob)
        for _, v in btree.items():
            blob = bytearray(v)
            (authentication_key, remaining_blob) = deserializer.decode_variable_length_bytes(blob)
            (balance, remaining_blob) = deserializer.decode_uint64(remaining_blob)
            (received_events_count, remaining_blob) = deserializer.decode_uint64(remaining_blob)
            (sent_events_count, remaining_blob) = deserializer.decode_uint64(remaining_blob)
            (sequence_number,_) = deserializer.decode_uint64(remaining_blob)
            return {
                'authentication_key': authentication_key.hex(),
                'balance': float(balance) / 1000000,
                'received_events_count': received_events_count,
                'sent_events_count': sent_events_count,
                'sequence_number': sequence_number
            }
        return {}


class LibraDeserializer():
    """Libra types deserializer

    BTreeMap Binary Encoding:
    +----------------------------------+----------------------+-----+------------------------+-------+-------+
    | No. Of Key-Value Pairs (4 Bytes) | Key Length (4 Bytes) | Key | Value Length (4 Bytes) | Value | Cont. |
    +----------------------------------+----------------------+-----+------------------------+-------+-------+

    """
    def __init__(self, endianness: Endianness = Endianness.LITTLE_ENDIAN) -> None:
        self._endianness = endianness

    def _get_endianness_sign(self) -> str:
        if self._endianness == Endianness.LITTLE_ENDIAN:
            return '<'
        return '>'

    def decode_btreemap(self, blob: bytes) -> Dict[bytes, bytes]:
        (length, remainig_blob) = self.decode_uint32(blob)
        mapping = {}
        for _ in range(0, length):
            (key, remainig_blob) = self.decode_variable_length_bytes(remainig_blob)
            (value, remainig_blob) = self.decode_variable_length_bytes(remainig_blob)
            mapping[bytes(key)] = bytes(value)
        return mapping

    def decode_variable_length_bytes(self, blob: bytes) -> (bytes, bytes):
        (value_length, remainig_blob) = self.decode_uint32(blob)
        (value, remainig_blob) = self.decode_variable_length(remainig_blob, value_length)
        return (value, remainig_blob)

    def decode_variable_length(self, blob: bytes, length: int) -> (bytes, bytes):
        return self._decode_any(length, f'{length}s', blob)

    def decode_uint64(self, blob: bytes) -> (bytes, bytes):
        return self._decode_any(8, 'Q', blob)

    def decode_uint32(self, blob: bytes) -> (bytes, bytes):
        return self._decode_any(4, 'I', blob)

    def decode_uint8(self, blob: bytes) -> (bytes, bytes):
        return self._decode_any(2, 'H', blob)

    def _decode_any(self, size: int, size_format: str, blob: bytes) -> (bytes, bytes):
        endianness_sign = self._get_endianness_sign()
        (value,) = struct.unpack_from(f'{endianness_sign}{size_format}', blob)
        return (value, blob[size:])
