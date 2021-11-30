from typing import List, NamedTuple
from abc import ABC, abstractmethod
from construct import Struct, Int8ul
from solana.transaction import TransactionInstruction, AccountMeta
from solana.sysvar import SYSVAR_CLOCK_PUBKEY
from solana.publickey import PublicKey
from sdk.constants import ManagePositionOptionalAccounts


class InstructionCore(ABC):
    layout: Struct = None

    def to_dict(self):
        instance_dict = self.__dict__
        for key, val in instance_dict.items():
            if type(val) == tuple and len(val) == 1:
                instance_dict[key] = val[0]
            elif type(val) == PublicKey:
                instance_dict[key] = val.__str__()
            elif type(val) == ManagePositionOptionalAccounts:
                instance_dict[key] = {
                    'discount_token': val.discount_token,
                    'referrer': val.referrer
                }
        return instance_dict

    def build(self) -> bytes:
        if self.layout == Struct():
            bytes_data = bytes(0)
        else:
            instruction_dict = self.to_dict()
            bytes_data = self.layout.build(instruction_dict)
        ones = [5 for i in range(100)]
        # bytes_data = Int8ul[100].build(ones)
        return bytes_data

    @abstractmethod
    def get_instruction(self, *args, **kwargs) -> TransactionInstruction:
        pass

