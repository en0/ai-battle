from typing import Dict, Any

from ..game_component import GameComponent


class Meta(GameComponent):
    type: str
    props: Dict[str, Any]

