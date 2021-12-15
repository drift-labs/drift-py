"""Core functionality for modelling drift Solana accounts."""
import json
from typing import Union
from abc import ABC, abstractmethod
from construct import Struct, Container

class ElementCore(ABC):
    """Core functionality for modelling drift solana accounts."""
    layout: Struct = None

    @classmethod
    @abstractmethod
    def from_container(cls, container: Container):
        """Create an object from a container."""
        pass

    @classmethod
    def parse(cls, bytes_data: bytes):
        """Create an object from bytes."""
        container = cls.layout.parse(bytes_data)
        obj = cls.from_container(container=container)
        return obj

    @abstractmethod
    def to_dict(self) -> Union[dict, list]:
        """For pretty printing."""
        pass

    def __str__(self):
        my_dict = self.to_dict()
        return json.dumps(
            obj=my_dict,
            sort_keys=False,
            indent=4
        )
