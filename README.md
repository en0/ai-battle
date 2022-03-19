# AI Battle Game

Create an AI to battle other AIs

## Quick Start

Install airena

```
pip install git+https://github.com/en0/ai-battle.git@master
```

Create a bot: `./bot1.py`

```
from airena.components.ai_base import AiBase


class Bot1(AiBase):

    color = (255, 0, 255)

    def initialize(self):
        ...

    def think(self):
        ...
```

Run the bot

```
python -m airena ./bot1.py
```

## Notes

Bigger screen
Needs a way to determin if we are done turning to focus
