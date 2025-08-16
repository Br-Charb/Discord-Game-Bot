![Discord-bot-preview](https://github.com/user-attachments/assets/e33b4826-52bf-4194-a34d-6640e24bef34)
<br />
![PYTHON](https://img.shields.io/badge/python-0000CC?style=for-the-badge&logo=Python&logoColor=white)

# Discord Minigame Bot

Discord bot which provides games such as blackjack and rock-paper-scissors, as well as a magic 8-ball and currency system. Players start with $1000 and can wager money on games.

## Features
- **Blackjack** with betting system
- **Rock Paper Scissors**
- **Magic 8-Ball** responses
- **Currency system** with persistent balance tracking
- **Coinflip** betting game
- User balance management with JSON storage

## Commands
- `$blackjack [amount]` or `$bj [amount]` - Play blackjack with optional wager
- `$rps` - Rock Paper Scissors game
- `$8ball [question]` - Magic 8-ball responses
- `$balance` - Check your current balance
- `$coinflip [amount]` - Bet on coinflip

## Setup

### Prerequisites
- Python 3.8+
- Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/discord-minigame-bot.git
cd discord-minigame-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```
TOKEN=your_discord_bot_token_here
```

4. Copy the template user data file:
```bash
cp user_data_template.json test.json
```

5. Run the bot:
```bash
python DiscordBot.py
```

## Getting a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Add Bot"
5. Copy the token and paste it in your `.env` file
6. Under "Privileged Gateway Intents", enable "Message Content Intent"

## File Structure
```
├── bot.py                # Main bot file
├── test.json             # User data (auto-created)
├── requirements.txt      # Dependencies
├── .gitignore            # Files to ignore in git
├── LICENSE               # MIT License
├── .env                  # Bot token (not included)
└── README.md             # This file
```

## License
This project is licensed under the MIT License.


