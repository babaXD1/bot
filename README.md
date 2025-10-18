# 🎰 Highrise Blackjack Casino Bot

A fully-featured blackjack casino bot for Highrise with gold betting system.

## 📋 Features

- **Gold Betting System**: Minimum 10, maximum 10,000 gold bets
- **Classic Blackjack Rules**: Dealer stands on 17
- **House Edge**: Push (tie) = House wins, Blackjack pays 1.5x
- **Player Statistics**: Balance, win/loss ratio, total winnings
- **Leaderboard**: Top 10 richest players
- **Gold Withdrawal**: Withdraw your winnings to Highrise
- **Auto-save**: JSON-based player data storage
- **Welcome Message**: Rules displayed when players join

## 🎮 Commands

### Player Commands
- `!bet [amount]` - Start a game (e.g., !bet 100)
- `!hit` - Draw a card
- `!stand` - Hold (dealer plays)
- `!balance` - Check your balance
- `!stats` - View your statistics
- `!leaderboard` - See top 10 richest players
- `!withdraw [amount]` - Withdraw gold to Highrise (min: 100)
- `!help` - Show help message with rules

### Moderator Commands
- `!tp [username]` - Teleport user to you (moderators only)

## 🚀 Setup

### 1. Highrise Bot and Room Setup

1. Login to [Highrise Create Portal](https://create.highrise.game)
2. Dashboard → Bots & API Keys → Create Bot
3. Copy your API Token
4. Create a room or enter an existing room
5. Copy Room ID (Dashboard → Creations → Three Dots → Copy Room ID)

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and enter your credentials:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
HIGHRISE_ROOM_ID=your_room_id_here
HIGHRISE_API_TOKEN=your_api_token_here
```

### 3. Run the Bot

```bash
python run.py
```

## 🎲 Game Rules

- Players play against the dealer
- Dealer stands on 17 or higher
- Blackjack (Ace + 10) pays 1.5x
- Push (tie) = House wins (house edge)
- Every player starts with 1,000 gold
- Minimum bet: 10 gold
- Maximum bet: 10,000 gold
- Minimum withdrawal: 100 gold

## 📊 Technical Details

### File Structure

- `bot.py` - Main bot file (Highrise SDK integration)
- `blackjack.py` - Blackjack game logic
- `player_data.py` - Player data management
- `run.py` - Bot launcher script
- `players.json` - Player data (auto-created)

### Requirements

- Python 3.11+
- highrise-bot-sdk

## 🔧 Future Features

This project is open for development. Potential features:

- Double down (double your bet)
- Split (split matching cards)
- Insurance (when dealer shows Ace)
- Multi-player support
- Daily/weekly tournaments

## 📝 License

This project is for educational purposes.
