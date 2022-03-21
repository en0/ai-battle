from typing import Dict, Tuple, List, Any
from .vector import Vector2
from .typing import IGameComponent


def bullet_preset(
    position: Vector2,
    rotation: float,
    vector: Vector2,
    speed: float,
    color: Tuple[int, int, int],
    props: Dict[str, Any] = None,
) -> Dict:
    props = props or {}
    props.setdefault("damage", 25)
    return {
        "Meta": {"type": "Bullet", "props": props},
        "Transform": {"position": position, "rotation": rotation},
        "Projectile": {"vector": vector, "speed": speed},
        "BulletSprite": {"color": color},
        "BoxCollider": {"size": (6, 6)},
    }

def tank_preset(
    controler: IGameComponent,
    position: Vector2,
    rotation: float,
    color: Tuple[int, int, int],
    props: Dict[str, Any] = None,
) -> Dict:

    props = props or {}
    props.setdefault("hat_rotation", rotation)
    props.setdefault("bullet_speed", 400)
    props.setdefault("fire_cooldown", 5000)
    props.setdefault("movement_speed", 100)
    props.setdefault("turn_speed", 2)
    props.setdefault("hat_radius", 10)
    props.setdefault("barrel_length", 3.5)
    props.setdefault("barrel_thinkness", 7)
    props.setdefault("body_length", 23)
    props.setdefault("body_width", 17)
    props.setdefault("body_thinkness", 3)
    props.setdefault("health", 100)

    return {
        "Meta": {"type": "Tank", "props": props},
        "Transform": {"position": position, "rotation": rotation},
        controler.__name__: None,
        "Tank": None,
        "TankSprite": {"color": color},
        "BoxCollider": {"size": (props["hat_radius"] * 2, props["hat_radius"] * 2)},
    }
