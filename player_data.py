import json
import os
from typing import Dict, Optional
from dataclasses import dataclass, asdict

@dataclass
class PlayerStats:
    user_id: str
    username: str
    balance: int
    games_played: int
    games_won: int
    games_lost: int
    total_bet: int
    total_won: int
    
    def win_rate(self) -> float:
        if self.games_played == 0:
            return 0.0
        return (self.games_won / self.games_played) * 100

class PlayerDataManager:
    def __init__(self, data_file: str = "players.json"):
        self.data_file = data_file
        self.players: Dict[str, PlayerStats] = {}
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for user_id, stats in data.items():
                        self.players[user_id] = PlayerStats(**stats)
            except Exception as e:
                print(f"Error loading data: {e}")
                self.players = {}
        else:
            self.players = {}
    
    def save_data(self):
        try:
            data = {user_id: asdict(stats) for user_id, stats in self.players.items()}
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get_player(self, user_id: str, username: str) -> PlayerStats:
        if user_id not in self.players:
            self.players[user_id] = PlayerStats(
                user_id=user_id,
                username=username,
                balance=1000,
                games_played=0,
                games_won=0,
                games_lost=0,
                total_bet=0,
                total_won=0
            )
            self.save_data()
        else:
            self.players[user_id].username = username
        
        return self.players[user_id]
    
    def update_balance(self, user_id: str, amount: int):
        if user_id in self.players:
            self.players[user_id].balance += amount
            self.save_data()
    
    def record_game(self, user_id: str, bet: int, payout: int):
        if user_id in self.players:
            player = self.players[user_id]
            player.games_played += 1
            player.total_bet += bet
            
            if payout > 0:
                player.games_won += 1
                player.total_won += payout
            elif payout < 0:
                player.games_lost += 1
            
            player.balance += payout
            self.save_data()
    
    def has_sufficient_balance(self, user_id: str, amount: int) -> bool:
        if user_id in self.players:
            return self.players[user_id].balance >= amount
        return False
    
    def get_balance(self, user_id: str) -> int:
        if user_id in self.players:
            return self.players[user_id].balance
        return 0
    
    def get_leaderboard(self, limit: int = 10) -> list:
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: p.balance,
            reverse=True
        )
        return sorted_players[:limit]
