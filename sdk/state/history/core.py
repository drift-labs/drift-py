from construct import Container

from sdk.state.core import ElementCore


class HistoryCore(ElementCore):

    @classmethod
    def from_container(cls, container: Container):
        pass

    def to_dict(self) -> dict:
        my_dict = {
            'head': self.head,
            'records': [record.to_dict() for record in self.records]
        }
        return my_dict