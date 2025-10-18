import random
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Card:
    suit: str
    rank: str
    
    def value(self) -> int:
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
    
    def __str__(self) -> str:
        suit_symbols = {'Hearts': '♥️', 'Diamonds': '♦️', 'Clubs': '♣️', 'Spades': '♠️'}
        return f"{self.rank}{suit_symbols.get(self.suit, self.suit)}"

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()
    
    def reset(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
    
    def draw(self) -> Card:
        if len(self.cards) < 10:
            self.reset()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards: List[Card] = []
    
    def add_card(self, card: Card):
        self.cards.append(card)
    
    def get_value(self) -> int:
        value = sum(card.value() for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_busted(self) -> bool:
        return self.get_value() > 21
    
    def __str__(self) -> str:
        return ' '.join(str(card) for card in self.cards)

class BlackjackGame:
    MIN_BET = 10
    MAX_BET = 10000
    
    def __init__(self):
        self.deck = Deck()
        self.player_hand: Optional[Hand] = None
        self.dealer_hand: Optional[Hand] = None
        self.bet: int = 0
        self.game_active: bool = False
    
    def start_game(self, bet: int) -> Tuple[bool, str, Optional[int]]:
        if bet < self.MIN_BET:
            return False, f"❌ Minimum bet is {self.MIN_BET} gold!", None
        if bet > self.MAX_BET:
            return False, f"❌ Maximum bet is {self.MAX_BET} gold!", None
        
        self.bet = bet
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        
        self.game_active = True
        
        game_state = self._format_game_state(hide_dealer_card=True)
        
        if self.player_hand.is_blackjack():
            if self.dealer_hand.is_blackjack():
                result = "🤝 Both Blackjack! Push - House wins!"
                payout = -self.bet
                self.game_active = False
                return True, f"{game_state}\n\n{result}\n💰 Loss: -{self.bet} gold", payout
            else:
                result = "🎉 BLACKJACK! You won!"
                payout = int(self.bet * 1.5)
                self.game_active = False
                return True, f"{game_state}\n\n{result}\n💰 Win: +{payout} gold", payout
        
        return True, f"{game_state}\n\n✅ Game started! Type !hit or !stand", None
    
    def hit(self) -> Tuple[bool, str, Optional[int]]:
        if not self.game_active or self.player_hand is None:
            return False, "❌ No active game! Start with !bet [amount]", None
        
        self.player_hand.add_card(self.deck.draw())
        
        if self.player_hand.is_busted():
            game_state = self._format_game_state(hide_dealer_card=False)
            self.game_active = False
            return True, f"{game_state}\n\n💥 Busted! Dealer wins.\n💰 Loss: -{self.bet} gold", -self.bet
        
        game_state = self._format_game_state(hide_dealer_card=True)
        return True, f"{game_state}\n\n✅ Card dealt! Type !hit or !stand", None
    
    def stand(self) -> Tuple[bool, str, int]:
        if not self.game_active or self.player_hand is None or self.dealer_hand is None:
            return False, "❌ No active game! Start with !bet [amount]", 0
        
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.draw())
        
        game_state = self._format_game_state(hide_dealer_card=False)
        
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        self.game_active = False
        
        if self.dealer_hand.is_busted():
            return True, f"{game_state}\n\n🎉 Dealer busted! You won!\n💰 Win: +{self.bet} gold", self.bet
        
        if player_value > dealer_value:
            return True, f"{game_state}\n\n🎉 You won!\n💰 Win: +{self.bet} gold", self.bet
        elif player_value < dealer_value:
            return True, f"{game_state}\n\n😔 Dealer wins!\n💰 Loss: -{self.bet} gold", -self.bet
        else:
            return True, f"{game_state}\n\n🤝 Push! House wins.\n💰 Loss: -{self.bet} gold", -self.bet
    
    def _format_game_state(self, hide_dealer_card: bool = False) -> str:
        if self.player_hand is None or self.dealer_hand is None:
            return ""
        
        dealer_cards = str(self.dealer_hand.cards[0]) + " 🎴" if hide_dealer_card else str(self.dealer_hand)
        dealer_value = self.dealer_hand.cards[0].value() if hide_dealer_card else self.dealer_hand.get_value()
        
        state = f"🎰 BLACKJACK (Bet: {self.bet} gold)\n\n"
        state += f"🎴 Dealer: {dealer_cards}"
        if not hide_dealer_card:
            state += f" ({dealer_value})"
        state += f"\n👤 You: {self.player_hand} ({self.player_hand.get_value()})"
        
        return state
    
    def get_bet(self) -> int:
        return self.bet
