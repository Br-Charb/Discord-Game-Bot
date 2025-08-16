# Imports
import random
import json
import os
from dotenv import load_dotenv
import discord
from discord.ui import Button, View

load_dotenv()

# Initiate bot with API token
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Create test.json if it doesn't exist
def ensureJsonFileExists():
    if not os.path.exists("test.json"):
        initial_data = {"users": []}
        with open("test.json", "w") as f:
            json.dump(initial_data, f, indent=4)
        print("Created new test.json file")

def createNewAccount(name):
    print(f"Looking for JSON at: {os.path.abspath('test.json')}")
    with open("test.json", "r") as f:
        data = json.load(f)
    
    ids = [x["id"] for x in data["users"]]
    if name not in ids:
        data["users"].append({"id": name, "balance": 1000})

    with open("test.json", "w") as f:
        json.dump(data, f, indent=4)    

def getInfo(name):
    with open("test.json", "r") as f:
        data = json.load(f)
    
    for i in data["users"]:
        if i["id"] == name:
            return i

def balanceChange(name, wager, result): 
    balance = getInfo(name)["balance"]
    if result == "w":
        balance += wager
    elif result == "l":
        balance -= wager
    elif result == "d":
        pass
    with open("test.json", "r") as f:
        data = json.load(f)
    for i in data["users"]:
        if i["id"] == name:
            i["balance"] = balance
    with open("test.json", "w") as f:
        json.dump(data, f, indent=4)

# On ready
@client.event
async def on_ready():
    ensureJsonFileExists()
    print("The bot is online as {0.user}".format(client))

# BLACKJACK
def blackjackSetup(author, dealerCard1, playerCard1, playerCard2, dealerTotal, playerTotal):
    global bjEmbed
    global name
    global Author
    global DealerCard1
    global PlayerCard1
    global PlayerCard2
    global DealerTotal
    global PlayerTotal
    Author = author
    DealerCard1 = dealerCard1
    PlayerCard1 = playerCard1
    PlayerCard2 = playerCard2
    DealerTotal = dealerTotal
    PlayerTotal = playerTotal
    name = str(author).split('#')[0]
    bjEmbed = discord.Embed()
    bjEmbed = bjEmbed.set_author(name=f"{name}'s Blackjack Game", icon_url=author.avatar)
    bjEmbed.add_field(
        name=f"Namron's Worst Nightmare (Dealer)",
        value=f"Cards: `{dealerCard1}` ` ? `\nTotal: `{dealerTotal}`",
        inline=False)
    bjEmbed.add_field(
        name=f"{name} (Player)",
        value=f"Cards: `{playerCard1}` `{playerCard2}`\nTotal: `{playerTotal}`",
        inline=False)


class HitButton(Button):
    global bjEmbed

    def __init__(self, author):
        super().__init__(label="Hit", style=discord.ButtonStyle.blurple)
        self.author = author

    global dealer_cards
    dealer_cards = []

    async def callback(self, interaction):
        def hitCard():
            global bjEmbed
            global card_sum
            global bjCount
            global bjView
            global bjOutcome
            # Third player card
            if card_sum <= 22 and bjCount == 0:
                # draw player card 3
                global PlayerCard3
                PlayerCard3 = card()
                # Edit embed
                bjEmbed = discord.Embed()
                bjEmbed = bjEmbed.set_author(name=f"{name}'s Blackjack Game", icon_url=Author.avatar)
                bjEmbed.add_field(
                    name=f"Namron's Worst Nightmare (Dealer)",
                    value=
                    f"Cards: `{DealerCard1}` ` ? `\nTotal: `{dealer_card_sum}`",
                    inline=False)
                bjEmbed.add_field(
                    name=f"{name} (Player)",
                    value=
                    f"Cards: `{PlayerCard1}` `{PlayerCard2}` `{PlayerCard3}`\nTotal: `{card_sum}`",
                    inline=False)
                bjCount += 1
                # make a new button
                bjView = View()
                hit1 = HitButton(self.author)
                stand1 = StandButton(self.author)
                bjView.add_item(hit1)
                bjView.add_item(stand1)
            #Fourth player card
            elif card_sum <= 22 and bjCount == 1:
                global PlayerCard4
                PlayerCard4 = card()
                bjEmbed = discord.Embed()
                bjEmbed = bjEmbed.set_author(name=f"{name}'s Blackjack Game", icon_url=Author.avatar)
                bjEmbed.add_field(
                    name=f"Namron's Worst Nightmare (Dealer)",
                    value=
                    f"Cards: `{DealerCard1}` ` ? `\nTotal: `{dealer_card_sum}`",
                    inline=False)
                bjEmbed.add_field(
                    name=f"{name} (Player)",
                    value=
                    f"Cards: `{PlayerCard1}` `{PlayerCard2}` `{PlayerCard3}` `{PlayerCard4}`\nTotal: `{card_sum}`",
                    inline=False)
                bjCount += 1
                bjView = View()
                hit2 = HitButton(self.author)
                stand2 = StandButton(self.author)
                bjView.add_item(hit2)
                bjView.add_item(stand2)
            # Fifth player card (win)
            elif card_sum <= 22 and bjCount == 2:
                global PlayerCard5
                PlayerCard5 = card()
                bjEmbed = discord.Embed()
                bjEmbed = bjEmbed.set_author(name=f"{name}'s Blackjack Game", icon_url=Author.avatar)
                bjEmbed.add_field(
                    name=f"Namron's Worst Nightmare (Dealer)",
                    value=
                    f"Cards: `{DealerCard1}` ` ? `\nTotal: `{dealer_card_sum}`",
                    inline=False)
                bjEmbed.add_field(
                    name=f"{name} (Player)",
                    value=
                    f"Cards: `{PlayerCard1}` `{PlayerCard2}` `{PlayerCard3}` `{PlayerCard4}` `{PlayerCard5}`\nTotal: `{card_sum}`",
                    inline=False)
                bjCount += 1
                if card_sum <= 22:
                    bjView = View()
                    bjOutcome = f"You won ${wager}, you had five cards and went under 21"
                    result = "w"
                    balanceChange(trueName, wager, result)
                    bjEmbed.remove_field(0)
                    bjEmbed.insert_field_at(0,
                                            name=f"Result",
                                            value=f'{bjOutcome}')
                    bjEmbed.insert_field_at(
                        1,
                        name=f"Namron's Worst Nightmare (Dealer)",
                        value=
                        f"Cards: `{DealerCard1}` `{dealer_card()}`\nTotal: `{dealer_card_sum}`",
                        inline=False)
            if card_sum >= 22:
                bjOutcome = f"You lost ${wager}, you busted and went over 21."
                result = "l"
                balanceChange(trueName, wager, result)
                bjEmbed.remove_field(0)
                bjEmbed.insert_field_at(0,
                                        name=f"Result",
                                        value=f'{bjOutcome}')
                bjEmbed.insert_field_at(
                    1,
                    name=f"Namron's Worst Nightmare (Dealer)",
                    value=
                    f"Cards: `{DealerCard1}` `{dealer_card()}`\nTotal: `{dealer_card_sum}`",
                    inline=False)
                bjView = View()

        if interaction.user == Author:
            hitCard()
            try:
                await interaction.response.edit_message(embed=bjEmbed, view=bjView)
            except:
                pass


class StandButton(Button):
    global bjEmbed

    def __init__(self, author):
        super().__init__(label="Stand", style=discord.ButtonStyle.blurple)
        self.author = author

    global dealer_cards
    dealer_cards = []

    async def callback(self, interaction):
        def standCard():
            # Draws dealer's cards
            while dealer_card_sum <= 16:
                dealer_cards.append(dealer_card())
            # Check win/loss/draw condition
            if dealer_card_sum >= 22 and card_sum < 22:
                bjOutcome = f"You won ${wager}, dealer bust and went over 21."
                result = "w"
                balanceChange(trueName, wager, result)
            elif dealer_card_sum > card_sum:
                bjOutcome = f"You lost ${wager}, dealer stood with a higher score of `{str(dealer_card_sum)}`."
                result = "l"
                balanceChange(trueName, wager, result)
            elif dealer_card_sum == card_sum:
                bjOutcome = f"Drew, both you and the dealer stood with the same score of `{str(card_sum)}`."
                result = "d"
                balanceChange(trueName, wager, result)
            elif dealer_card_sum < card_sum:
                bjOutcome = f"You won ${wager}, you stood with a higher score of `{str(card_sum)}`"
                result = "w"
                balanceChange(trueName, wager, result)
            # Edit embed
            if len(dealer_cards) == 1:
                bjEmbed.remove_field(0)
                bjEmbed.insert_field_at(0, name=f"Result", value=f'{bjOutcome}')
                bjEmbed.insert_field_at(
                    1,
                    name=f"Namron's Worst Nightmare (Dealer)",
                    value=
                    f"Cards: `{DealerCard1}` `{dealer_cards[0]}`\nTotal: `{dealer_card_sum}`",
                    inline=False)
            elif len(dealer_cards) == 2:
                bjEmbed.remove_field(0)
                bjEmbed.insert_field_at(0,
                                        name=f"Result",
                                        value=f'{bjOutcome}')
                bjEmbed.insert_field_at(
                    1,
                    name=f"Namron's Worst Nightmare (Dealer)",
                    value=
                    f"Cards: `{DealerCard1}` `{dealer_cards[0]}` `{dealer_cards[1]}`\nTotal: `{dealer_card_sum}`",
                    inline=False)
            elif len(dealer_cards) == 3:
                bjEmbed.remove_field(0)
                bjEmbed.insert_field_at(0,
                                        name=f"Result",
                                        value=f'{bjOutcome}')
                bjEmbed.insert_field_at(
                    1,
                    name=f"Namron's Worst Nightmare (Dealer)",
                    value=
                    f"Cards: `{DealerCard1}` `{dealer_cards[0]}` `{dealer_cards[1]}` `{dealer_cards[2]}`\nTotal: `{dealer_card_sum}`",
                    inline=False)
            if len(dealer_cards) == 4:
                bjOutcome = f"You lost ${wager}, dealer had five cards and went under 21"
                result = "l"
                balanceChange(trueName, wager, result)
                bjEmbed.remove_field(0)
                bjEmbed.insert_field_at(0,
                                        name=f"Result",
                                        value=f'{bjOutcome}')
                bjEmbed.insert_field_at(
                    1,
                    name=f"Namron's Worst Nightmare (Dealer)",
                    value=
                    f"Cards: `{DealerCard1}` `{dealer_cards[0]}` `{dealer_cards[1]}` `{dealer_cards[2]}` `{dealer_cards[3]}`\nTotal: `{dealer_card_sum}`",
                    inline=False)

        if interaction.user == Author:
            standCard()
            try:
                await interaction.response.edit_message(embed=bjEmbed,
                                                        view=None)
            except:
                pass
#HELP COMMAND
class BackHelpPage(Button):
    def __init__(self, author):
        super().__init__(label="Back Page", style=discord.ButtonStyle.blurple)
        self.author = author

    async def callback(self, interaction):
        if interaction.user == self.author:
            global helpEmbed
            helpEmbed = discord.Embed(title="Help Information", color=0xFFA500)
            helpEmbed.add_field(name="$help", value="This command pulls up this help menu.", inline=False)
            helpEmbed.add_field(name="$rps", value="Plays rock paper scissors against the bot.", inline=False)
            helpEmbed.add_field(name="$8ball", value="Ask the magic 8ball any of your questions.", inline=False)
            helpEmbed.add_field(name="$blackjack", value="Plays blackjack against the bot")
            helpEmbed.set_footer(text="Page 1/2")
            view = View()
            view.add_item(NextHelpPage(self.author))
        try:
            await interaction.response.edit_message(embed=helpEmbed, view=view)
        except:
            pass

class NextHelpPage(Button):
    def __init__(self, author):
        super().__init__(label="Next Page", style=discord.ButtonStyle.blurple)
        self.author = author

    async def callback(self, interaction):
        if interaction.user == self.author:
            global helpEmbed
            helpEmbed = discord.Embed(title="Help Information", color=0xFFA500)
            helpEmbed.add_field(name="OOPS!", value="It appears that this page is empty, sorry for the inconvenience.")
            helpEmbed.set_footer(text="Page 2/2")
            view = View()
            view.add_item(BackHelpPage(self.author))
        try:
            await interaction.response.edit_message(embed=helpEmbed, view=view)
        except:
            pass

# Rubik's cube scramble generator
def generateScramble():
    moves = ["R", "U", "L", "D", "B", "F"]
    moves2 = [x + "\'" for x in moves] + [x + "2" for x in moves]
    moves += moves2
    scramble = []
    while len(scramble) <= 15:
        move = random.choice(moves)
        if len(scramble) == 0:
            scramble.append(move)
        else:
            if move[0] != scramble[len(scramble)-1][0]:
                scramble.append(move)
    return ' '.join(scramble)

@client.event
async def on_message(message):
    # Variables
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')
    # Prevents infinite loop
    if message.author == client.user:
        return

    # CLEAR COMMAND
    elif user_message.lower().split(' ')[0] == "$clear":
        try:
            await message.channel.purge(limit=int(user_message.lower().split(' ')[1]))
            await message.channel.send(f"{user_message.lower().split(' ')[1]} messages cleared."); return
        except:
            await message.channel.send("Please enter how many messages you want to clear."); return
    
    elif user_message.lower().split(' ')[0] == "$balance":
        createNewAccount(message.author.id)
        with open("test.json", "r") as f:
            data = json.load(f)
        for i in data["users"]:
            if i["id"] == message.author.id:
                await message.channel.send("Your balance is: $" + str(i["balance"]))

    # 8BALL COMMAND
    elif user_message.lower().split(' ')[0] == "$8ball":
        chance = random.randrange(0, 7)
        messages = {
            0: "Of course.",
            1: "No chance.",
            2: "Maybe.",
            3: "Of course not.",
            4: "Most definitely.",
            5: "No.",
            6: "Yes."
        }
        await message.channel.send(messages[chance]); return

# BLACKJACK COMMAND
    elif "$blackjack" in user_message.lower() or "$bj" in user_message.lower():
        global trueName
        trueName = message.author.id
        createNewAccount(trueName)
        try: 
            global wager
            wager = int(user_message.lower().split(' ')[1])
        except: await message.channel.send("Please enter a valid wager."); return
        balance = getInfo(message.author.id)["balance"]
        if balance < wager:
            await message.channel.send("You don't have enough money!"); return
        global card_sum
        global ace_count
        global dealer_card_sum
        global dealer_ace_count
        global bjCount
        global bjOutcome
        global dealer_cards
        bjCount = 0
        card_sum = 0
        ace_count = 0
        dealer_card_sum = 0
        dealer_ace_count = 0
        bjOutcome = ""
        dealer_cards = []
        # GENERATES PLAYER CARD
        global card
        def card():
            global card_sum
            global ace_count
            global player_total
            card_suit = ["♥", "♣", "♦", "♠"]
            card_face = ["10", "J", "Q", "K"]
            card_num = random.randint(2, 11)
            card_name = card_num
            if card_num == 10:
                card_name = random.choice(card_face)
            if card_num == 11:
                card_name = "A"
                ace_count += 1
            card_sum = card_sum + card_num
            if ace_count >= 1 and card_sum >= 22:
                card_sum = card_sum - 10
                ace_count -= 1
            return f"{random.choice(card_suit)} {card_name}"

        # GENERATES DEALER CARD
        global dealer_card

        def dealer_card():
            global dealer_card_sum
            global dealer_ace_count
            card_suit = ["♥", "♣", "♦", "♠"]
            card_face = ["10", "J", "Q", "K"]
            card_num = random.randint(2, 11)
            card_name = card_num
            if card_num == 10:
                card_name = random.choice(card_face)
            if card_num == 11:
                card_name = "A"
                dealer_ace_count += 1
            dealer_card_sum = dealer_card_sum + card_num
            if dealer_ace_count >= 1 and dealer_card_sum >= 22:
                dealer_card_sum = dealer_card_sum - 10
                dealer_ace_count -= 1
            return f"{random.choice(card_suit)} {card_name}"

        blackjackSetup(message.author, dealer_card(), card(), card(), dealer_card_sum, card_sum)
        view = View()
        hit = HitButton(message.author)
        stand = StandButton(
            message.author
        )  #; playagain = PlayAgainButton(message.author); quit = QuitButton(message.author)
        view.add_item(hit)
        view.add_item(stand)
        await message.channel.send(embed=bjEmbed, view=view)
        return

    elif "$test" in user_message.lower():
        button = Button(label="TESTING", style=discord.ButtonStyle.green)
        button2 = Button(label="BUTTON2", style=discord.ButtonStyle.danger)
        async def button_callback2(interaction):
            await interaction.response.edit_message(view=None)
        async def button_callback(interaction):
            view = View()
            view.add_item(button2)
            await interaction.response.edit_message(view=view)
        button.callback = button_callback2
        button2.callback = button_callback
        view = View()
        view.add_item(button)
        view.add_item(button2)
        await message.channel.send("TESTING", view=view); return

    elif user_message.lower().split(' ')[0] == "$coinflip":
        try: wager = int(user_message.lower().split(' ')[1])
        except: await message.channel.send("Please enter a wager."); return
        headsButton = Button(label="Heads", style=discord.ButtonStyle.blurple)
        tailsButton = Button(label="Tails", style=discord.ButtonStyle.blurple)
        embed = discord.Embed(title="Coinflip")
        coinflipOutcome = random.choice(["Heads", "Tails"])
        async def headsButtonCallback(interaction):
            if message.author == interaction.user:
                if coinflipOutcome == "Heads":
                    embed = discord.Embed(title="Coinflip", color=0x00FF00)
                    embed.add_field(name="Result", value=f"You won {wager*2} coins.")
                    balanceChange(message.author.id, wager, "w")
                else:
                    embed = discord.Embed(title="Coinflip", color=0xFF0000)
                    embed.add_field(name="Result", value=f"You lost {wager} coins. :(")
                    balanceChange(message.author.id, wager, "l")
                await interaction.response.edit_message(embed=embed, view=None); return
        async def tailsButtonCallback(interaction):
            if message.author == interaction.user:
                if coinflipOutcome == "Tails":
                    embed = discord.Embed(title="Coinflip", color=0x00FF00)
                    embed.add_field(name="Result", value=f"You won {wager*2} coins.")
                    balanceChange(message.author.id, wager, "w")
                else:
                    embed = discord.Embed(title="Coinflip", color=0xFF0000)
                    embed.add_field(name="Result", value=f"You lost {wager} coins. :(")   
                    balanceChange(message.author.id, wager, "l")   
                await interaction.response.edit_message(embed=embed, view=None); return
        headsButton.callback = headsButtonCallback
        tailsButton.callback = tailsButtonCallback
        view = View()
        view.add_item(headsButton)
        view.add_item(tailsButton)
        await message.channel.send(embed=embed, view=view); return
client.run(token)