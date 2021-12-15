"""Core functionality for modelling history accounts."""
from construct import Container

from sdk.state.core import ElementCore


class HistoryCore(ElementCore):
    """Object containing core functionality for modelling history accounts."""

    @classmethod
    def from_container(cls, container: Container):
        """Create a history-account object from a container."""
        pass

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'head': self.head,
            'records': [record.to_dict() for record in self.records]
        }
        return my_dict
