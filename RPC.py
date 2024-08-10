import discord
import random
from settings import DISCORD_API_SECRET  # Import the token from settings.py

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

games = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!rps'):
        args = message.content.lower().split()
        if len(args) != 2:
            await message.channel.send("Usage: !rps @opponent")
            return

        opponent = message.mentions[0] if message.mentions else None
        if not opponent or opponent.bot or opponent == message.author:
            await message.channel.send("You must mention a valid user to challenge.")
            return

        game_key = tuple(sorted([message.author.id, opponent.id]))
        if game_key in games:
            await message.channel.send("A game is already in progress between you two.")
            return

        games[game_key] = {message.author.id: None, opponent.id: None}
        await message.channel.send(f"{message.author.mention} has challenged {opponent.mention} to Rock-Paper-Scissors! Each player, type 'rock', 'paper', or 'scissors' to make your move.")

    elif message.content.lower() in ["rock", "paper", "scissors"]:
        for game_key, game in games.items():
            if message.author.id in game:
                game[message.author.id] = message.content.lower()
                opponent_id = game_key[0] if game_key[1] == message.author.id else game_key[1]

                if game[opponent_id]:
                    await determine_winner(game_key, message.channel)
                else:
                    await message.channel.send(f"{message.author.mention} has made their move. Waiting for the opponent.")
                return

async def determine_winner(game_key, channel):
    user1_id, user2_id = game_key
    user1_choice = games[game_key][user1_id]
    user2_choice = games[game_key][user2_id]

    if user1_choice == user2_choice:
        result = "It's a tie!"
    elif (user1_choice == "rock" and user2_choice == "scissors") or \
         (user1_choice == "paper" and user2_choice == "rock") or \
         (user1_choice == "scissors" and user2_choice == "paper"):
        result = f"<@{user1_id}> wins!"
    else:
        result = f"<@{user2_id}> wins!"

    response = (f'<@{user1_id}> chose: {user1_choice}\n'
                f'<@{user2_id}> chose: {user2_choice}\n'
                f'{result}')
    await channel.send(response)
    del games[game_key]

client.run(DISCORD_API_SECRET)  # Use the token from settings.py
