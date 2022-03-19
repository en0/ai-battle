# AI Battle Game

Create an AI to battle other AIs

## Quick Start

Install airena

```
pip install git+https://github.com/en0/ai-battle.git@master
```

Create a bot: `./my_bot.py`

```
from airena.components.ai_base import AiBase


class MyBot(AiBase):

    color = (0, 0, 255)

    def update(self):
        self.fire()
```

Run the bot

```
python -m airena ./my_bot.py
```

