from typing import Dict, Any

from ..game_component import GameComponent
from ..typing import IMessageService


class Meta(GameComponent):

    type: str
    props: Dict[str, Any]

    def startup(self):
        self.props = self.props or {}
        for key, value in self.props.items():
            self._send(key, value, "insert")

    def __setitem__(self, key: str, value: Any):
        if key not in self:
            self.props[key] = value
            self._send(key, value, "insert")

        elif key in self and self.props[key] != value:
            self.props[key] = value
            self._send(key, value, "update")

    def __getitem__(self, key: str) -> Any:
        return self.props[key]

    def __contains__(self, key: str) -> bool:
        return key in self.props

    def _send(self, key, value, op):
            self.broadcast(
                f"Meta:{key}",
                owner=self.game_object,
                op=op,
                value=value)
