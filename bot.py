from highrise import BaseBot, User, Position
from blackjack import BlackjackGame
from player_data import PlayerDataManager
import os

class BlackjackBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.games = {}
        self.player_data = PlayerDataManager()
        self.moderators = set()
        self.user_positions = {}
    
    async def on_start(self, session_metadata):
        print("🎰 Blackjack Bot started!")
        await self.load_moderators()
        await self.highrise.chat("🎰 Blackjack Casino is now OPEN! Type !help for commands and rules")
    
    async def load_moderators(self):
        try:
            room_users = await self.highrise.get_room_users()
            for user, position in room_users.content:
                try:
                    privileges = await self.highrise.get_room_privilege(user.id)
                    if privileges.moderator or privileges.designer:
                        self.moderators.add(user.id)
                except:
                    pass
            print(f"✅ {len(self.moderators)} moderators loaded")
        except Exception as e:
            print(f"⚠️ Could not load moderators: {e}")
    
    async def on_user_join(self, user: User, position: Position):
        self.user_positions[user.id] = position
        
        welcome_msg = f"""🎰 Welcome @{user.username} to Blackjack Casino!

📜 RULES:
• Minimum bet: 10 gold | Maximum bet: 10,000 gold
• Dealer stands on 17
• Blackjack pays 1.5x
• Push (tie) = House wins
• Starting balance: 1,000 gold

Type !help for all commands. Good luck! 🍀"""
        
        await self.highrise.chat(welcome_msg)
    
    async def on_user_move(self, user: User, position: Position):
        self.user_positions[user.id] = position
    
    async def on_chat(self, user: User, message: str):
        user_id = user.id
        username = user.username
        
        if not message.startswith("!"):
            return
        
        parts = message.split()
        command = parts[0].lower()
        
        if command == "!help":
            await self.send_help(user)
        
        elif command == "!bet":
            if len(parts) < 2:
                await self.highrise.chat(f"@{username} ❌ Usage: !bet [amount] (min: 10, max: 10000)")
                return
            
            try:
                bet = int(parts[1])
            except ValueError:
                await self.highrise.chat(f"@{username} ❌ Please enter a valid amount!")
                return
            
            await self.start_blackjack(user, bet)
        
        elif command == "!hit":
            await self.hit(user)
        
        elif command == "!stand":
            await self.stand(user)
        
        elif command == "!balance":
            await self.show_balance(user)
        
        elif command == "!stats":
            await self.show_stats(user)
        
        elif command == "!leaderboard" or command == "!top":
            await self.show_leaderboard()
        
        elif command == "!withdraw":
            if len(parts) < 2:
                await self.highrise.chat(f"@{username} ❌ Usage: !withdraw [amount]")
                return
            
            try:
                amount = int(parts[1])
            except ValueError:
                await self.highrise.chat(f"@{username} ❌ Please enter a valid amount!")
                return
            
            await self.withdraw_gold(user, amount)
        
        elif command == "!tp":
            if len(parts) < 2:
                await self.highrise.chat(f"@{username} ❌ Usage: !tp [username]")
                return
            
            target_username = parts[1].lstrip('@')
            await self.teleport_user(user, target_username)
    
    async def send_help(self, user: User):
        help_text = """🎰 BLACKJACK CASINO COMMANDS

💰 GAME COMMANDS:
!bet [amount] - Start game (min: 10, max: 10000)
!hit - Draw a card
!stand - Hold (dealer plays)
!balance - Check your balance
!stats - View your statistics
!leaderboard - See top 10 richest players
!withdraw [amount] - Withdraw gold to Highrise
!help - Show this help message

📜 GAME RULES:
• Dealer stands on 17
• Blackjack pays 1.5x your bet
• Push (tie) = House wins
• Starting balance: 1,000 gold
• Minimum bet: 10 gold
• Maximum bet: 10,000 gold

👮 MODERATOR COMMANDS:
!tp [username] - Teleport user to you"""
        
        await self.highrise.chat(f"@{user.username}\n{help_text}")
    
    async def start_blackjack(self, user: User, bet: int):
        user_id = user.id
        username = user.username
        
        player = self.player_data.get_player(user_id, username)
        
        if not self.player_data.has_sufficient_balance(user_id, bet):
            await self.highrise.chat(
                f"@{username} ❌ Insufficient balance! Your balance: {player.balance} gold"
            )
            return
        
        if user_id in self.games:
            await self.highrise.chat(f"@{username} ⚠️ You already have an active game! Type !hit or !stand")
            return
        
        game = BlackjackGame()
        success, result, payout = game.start_game(bet)
        
        if not success:
            await self.highrise.chat(f"@{username} {result}")
            return
        
        self.games[user_id] = game
        
        if not game.game_active and payout is not None:
            self.player_data.record_game(user_id, bet, payout)
            if user_id in self.games:
                del self.games[user_id]
        
        await self.highrise.chat(f"@{username}\n{result}")
    
    async def hit(self, user: User):
        user_id = user.id
        username = user.username
        
        if user_id not in self.games:
            await self.highrise.chat(f"@{username} ❌ No active game! Start with !bet [amount]")
            return
        
        game = self.games[user_id]
        success, result, payout = game.hit()
        
        if not success:
            await self.highrise.chat(f"@{username} {result}")
            return
        
        if payout is not None:
            self.player_data.record_game(user_id, game.get_bet(), payout)
            del self.games[user_id]
        
        await self.highrise.chat(f"@{username}\n{result}")
    
    async def stand(self, user: User):
        user_id = user.id
        username = user.username
        
        if user_id not in self.games:
            await self.highrise.chat(f"@{username} ❌ No active game! Start with !bet [amount]")
            return
        
        game = self.games[user_id]
        success, result, payout = game.stand()
        
        if success:
            self.player_data.record_game(user_id, game.get_bet(), payout)
            del self.games[user_id]
        
        await self.highrise.chat(f"@{username}\n{result}")
    
    async def show_balance(self, user: User):
        player = self.player_data.get_player(user.id, user.username)
        await self.highrise.chat(
            f"@{user.username} 💰 Your balance: {player.balance} gold"
        )
    
    async def show_stats(self, user: User):
        player = self.player_data.get_player(user.id, user.username)
        
        stats_text = f"""📊 STATISTICS - {player.username}

💰 Balance: {player.balance} gold
🎮 Games Played: {player.games_played}
✅ Wins: {player.games_won}
❌ Losses: {player.games_lost}
📈 Win Rate: {player.win_rate():.1f}%
💵 Total Bet: {player.total_bet} gold
🏆 Total Won: {player.total_won} gold
📊 Net Profit: {player.balance - 1000:+d} gold"""
        
        await self.highrise.chat(f"@{user.username}\n{stats_text}")
    
    async def show_leaderboard(self):
        leaderboard = self.player_data.get_leaderboard(10)
        
        if not leaderboard:
            await self.highrise.chat("📊 No one on the leaderboard yet!")
            return
        
        text = "🏆 LEADERBOARD - Top 10 Richest\n\n"
        for i, player in enumerate(leaderboard, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {player.username}: {player.balance} gold\n"
        
        await self.highrise.chat(text)
    
    async def withdraw_gold(self, user: User, amount: int):
        user_id = user.id
        username = user.username
        
        player = self.player_data.get_player(user_id, username)
        
        if amount < 100:
            await self.highrise.chat(f"@{username} ❌ Minimum withdrawal is 100 gold!")
            return
        
        if not self.player_data.has_sufficient_balance(user_id, amount):
            await self.highrise.chat(
                f"@{username} ❌ Insufficient balance! Your balance: {player.balance} gold"
            )
            return
        
        try:
            item_id = "gold_bar_1" if amount == 1 else f"gold_bar_{min(amount, 10000)}"
            
            await self.highrise.tip_user(user_id, item_id)
            
            self.player_data.update_balance(user_id, -amount)
            
            new_balance = self.player_data.get_balance(user_id)
            
            await self.highrise.chat(
                f"@{username} ✅ Successfully withdrew {amount} gold to your Highrise account!\n💰 Remaining balance: {new_balance} gold"
            )
            
        except Exception as e:
            print(f"Withdrawal error: {e}")
            await self.highrise.chat(
                f"@{username} ❌ Withdrawal failed: {str(e)}\nNote: Gold bars must be available in the room inventory."
            )
    
    async def teleport_user(self, moderator: User, target_username: str):
        if moderator.id not in self.moderators:
            await self.highrise.chat(f"@{moderator.username} ❌ Only moderators can use this command!")
            return
        
        if moderator.id not in self.user_positions:
            await self.highrise.chat(f"@{moderator.username} ❌ Could not detect your position!")
            return
        
        try:
            room_users = await self.highrise.get_room_users()
            target_user = None
            
            for user, position in room_users.content:
                if user.username.lower() == target_username.lower():
                    target_user = user
                    break
            
            if not target_user:
                await self.highrise.chat(f"@{moderator.username} ❌ User not found: {target_username}")
                return
            
            moderator_pos = self.user_positions[moderator.id]
            
            await self.highrise.teleport(target_user.id, moderator_pos)
            await self.highrise.chat(f"✅ @{target_user.username} teleported!")
            
        except Exception as e:
            print(f"Teleport error: {e}")
            await self.highrise.chat(f"@{moderator.username} ❌ Teleport failed: {str(e)}")
