# dc.py
# -----------------------------------------------
# A minimal DM‑spammer bot for Discord
# -----------------------------------------------
# 1. Replace the placeholders below with your own data
# 2. Run: python dc.py
# 3. The bot will start sending the message to the target user
# 4. Stop the bot with Ctrl + C
# -----------------------------------------------

import discord
import asyncio

# ---------- USER SETTINGS ----------
TOKEN = ""          # <-- Put your bot token here
TARGET_USER_ID = 1500573732345872568    # <-- Replace with the numeric user ID to DM
MESSAGE = "Podi Aunty"  # <-- Custom message to send
DELAY = 0.0                            # <-- Seconds between messages (0.1 = ~10 msgs/sec)

# ---------- BOT CLASS ----------
class DMSpammerBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        # The correct super call: no placeholders, just forward args
        super().__init__(intents=intents)
        self.target_user = None
        self.spamming_task = None

    async def on_ready(self):
        print(f"[+] Bot logged in as {self.user} (ID: {self.user.id})")
        try:
            self.target_user = await self.fetch_user(TARGET_USER_ID)
        except Exception as e:
            print(f"[-] Failed to fetch user {TARGET_USER_ID}: {e}")
            await self.close()
            return

        print(f"[+] Target user fetched: {self.target_user} (ID: {self.target_user.id})")
        # Start the spam loop
        self.spamming_task = asyncio.create_task(self.send_spam())

    async def send_spam(self):
        while True:
            try:
                await self.target_user.send(MESSAGE)
                print(f"[+] Sent message to {self.target_user.name}")
            except discord.HTTPException as e:
                print(f"[-] HTTPException while sending DM: {e}")
            except Exception as e:
                print(f"[-] Unexpected error: {e}")

            # Wait before sending the next message
            await asyncio.sleep(DELAY)

    async def on_disconnect(self):
        print("[*] Bot disconnected")

    async def on_error(self, event, *args, **kwargs):
        print(f"[!] Error in event {event}: {args}")

# ---------- RUNNING THE BOT ----------
if __name__ == "__main__":
    # Enable all intents (required for DM fetching)
    intents = discord.Intents.default()
    intents.message_content = True  # Needed if you ever want to read message content

    bot = DMSpammerBot(intents=intents)
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print("\n[*] Keyboard interrupt received – shutting down")
    except Exception as e:
        print(f"[-] Unexpected exception: {e}")