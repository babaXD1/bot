# Highrise Blackjack Casino Bot

**Project Type**: Highrise Game Bot
**Language**: Python 3.11
**Framework**: Highrise Bot SDK

## 📋 Project Summary

A fully-featured blackjack casino bot for Highrise with gold betting system. Players can play blackjack via chat commands, place bets, withdraw winnings, and view statistics.

## 🎯 Main Features

- Gold betting system (10-10,000 gold range)
- Classic blackjack rules
- House edge mechanics (push = house wins)
- Gold withdrawal to Highrise
- Player statistics and leaderboard
- Welcome message with rules on join
- Moderator teleport command
- JSON-based data storage

## 🏗️ Architecture

### File Structure
```
.
├── bot.py              # Main bot file (Highrise integration)
├── blackjack.py        # Blackjack game logic
├── player_data.py      # Player data management
├── run.py              # Bot launcher
├── players.json        # Player data (auto-created)
├── .env                # Environment variables (SECRET)
└── README.md           # User documentation
```

### Components

1. **BlackjackBot (bot.py)**
   - Extends Highrise BaseBot
   - Handles chat commands
   - Manages game state

2. **BlackjackGame (blackjack.py)**
   - Game logic
   - Card dealing and scoring
   - Dealer AI

3. **PlayerDataManager (player_data.py)**
   - Player balance management
   - Statistics tracking
   - JSON data storage

## 🔧 Required Configuration

Before running the bot, set these environment variables:

- `HIGHRISE_ROOM_ID`: Highrise room ID
- `HIGHRISE_API_TOKEN`: Bot API token

These credentials can be obtained from [Highrise Create Portal](https://create.highrise.game).

## 🎮 Game Mechanics

### Betting System
- Minimum: 10 gold
- Maximum: 10,000 gold
- Starting balance: 1000 gold

### House Edge
- Push (tie) = House wins
- Dealer blackjack pays 1.5x
- Player blackjack pays 1.5x

### Dealer Rules
- Stands on 17 or higher
- Hits on 16 or lower

## 📊 Data Management

Player data is stored in `players.json`:
- Balance
- Games played
- Win/loss counts
- Total bets and winnings

## 🚀 Workflow

Bot runs with `python run.py` command. Establishes Highrise WebSocket connection and becomes active in the room.

## 📝 Recent Changes

**Date**: October 18, 2025

- Initial version created
- Core blackjack logic implemented
- Gold betting system integrated
- Player data management added
- Highrise SDK integration completed
- All text translated to English
- Changed !blackjack to !bet command
- Added gold withdrawal feature
- Added welcome message on user join
- Added moderator teleport command

## 🎯 Future Features

- Double down feature
- Split feature  
- Insurance
- Multi-player support
- Tournament system
