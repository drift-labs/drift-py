"""This module contains common utilities for Structs and general parsing."""
from typing import List, Dict
from hashlib import sha256
from construct import (
    Struct, Int8ul, Int16ul, Int32ul, Int64ul, Int64sl, Bytes, Flag, Padding, Container, ListContainer, BytesInteger,
    Adapter
)
from solana.publickey import PublicKey


class InstructionIdentifier(Adapter):
    """Class for parsing and building instruction identifiers."""
    subcon = Bytes(8)

    def __init__(self) -> None:
        super().__init__(self.subcon)

    def _encode(self, obj, context, path):
        formatted_string = f'global:{obj}'
        bytes_data = sha256(formatted_string.encode()).digest()[:8]
        return bytes_data

    def _decode(self, obj, context, path):
        raise ValueError('Cannot reverse a SigHash.')


class Base58EncodingLayout(Adapter):
    """Easy parsing and building of PublicKey objects."""

    def __init__(self, length: int) -> None:
        self.subcon = Bytes(length)
        super().__init__(self.subcon)

    def _decode(self, obj, context, path):
        return PublicKey(self.subcon.parse(obj))

    def _encode(self, obj, context, path):
        if type(obj) == PublicKey:
            return obj.__bytes__()
        elif type(obj) == str:
            return PublicKey(obj).__bytes__()
        else:
            raise Exception('Invalid object.')

INSTRUCTION_NAME_LAYOUT = InstructionIdentifier()

PUBLIC_KEY_LAYOUT = Base58EncodingLayout(32)

ORACLE_SOURCE_LAYOUT = Int8ul

Int128ul = BytesInteger(
    length=16,
    signed=False,
    swapped=True
)
Int128sl = BytesInteger(
    length=16,
    signed=True,
    swapped=True
)

POSITION_DIRECTION_LAYOUT = Int8ul

MANAGE_POSITION_OPTIONAL_ACCOUNTS_LAYOUT = Struct(
    'discount_token' / Flag,
    'referrer' / Flag
)