from typing import List, Dict
from construct import (Struct, Int8ul, Int16ul, Int32ul, Int64ul, Int64sl, Bytes, Flag, Padding, Container,
                       ListContainer, BytesInteger)
from solana.publickey import PublicKey


PUBLIC_KEY_LAYOUT = Bytes(32)

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