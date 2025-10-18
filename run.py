import os
import sys

room_id = os.getenv("HIGHRISE_ROOM_ID")
api_token = os.getenv("HIGHRISE_API_TOKEN")

if not room_id or not api_token:
    print("❌ Hata: HIGHRISE_ROOM_ID ve HIGHRISE_API_TOKEN çevre değişkenlerini ayarlayın!")
    print("\nKullanım:")
    print("export HIGHRISE_ROOM_ID='your_room_id'")
    print("export HIGHRISE_API_TOKEN='your_api_token'")
    sys.exit(1)

print(f"🎰 Blackjack Bot başlatılıyor...")
print(f"📍 Room ID: {room_id[:8]}...")
print(f"🔑 API Token: {api_token[:8]}...")

os.system(f"highrise bot:BlackjackBot {room_id} {api_token}")
