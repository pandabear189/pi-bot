import discord
from src.discord.globals import SERVER_ID, CHANNEL_REPORTS, REPORT_IDS, CENSORED_WORDS, CENSORED_EMOJIS, EVENT_INFO, TAGS
from embed import assemble_embed
from src.sheets.censor import get_censor
from src.sheets.events import get_events
from src.sheets.sheets import get_tags

# Meant for Pi-Bot only
async def auto_report(bot, reason, color, message):
    """Allows Pi-Bot to generate a report by himself."""
    server = bot.get_guild(SERVER_ID)
    reports_channel = discord.utils.get(server.text_channels, name=CHANNEL_REPORTS)
    embed = assemble_embed(
        title=f"{reason} (message from Pi-Bot)",
        webcolor=color,
        fields = [{
            "name": "Message",
            "value": message,
            "inline": False
        }]
    )
    message = await reports_channel.send(embed=embed)
    REPORT_IDS.append(message.id)
    await message.add_reaction("\U00002705")
    await message.add_reaction("\U0000274C")

async def sanitize_mention(member):
    if member == False: return True
    if member == "@everyone" or member == "@here": return False
    if member[:3] == "<@&": return False
    return True

async def harvest_id(user):
    return user.replace("<@!", "").replace(">", "")
    
async def lookup_role(name):
    name = name.title()
    if name == "Al" or name == "Alabama": return "Alabama"
    elif name == "All" or name == "All States": return "All States"
    elif name == "Ak" or name == "Alaska": return "Alaska"
    elif name == "Ar" or name == "Arkansas": return "Arkansas"
    elif name == "Az" or name == "Arizona": return "Arizona"
    elif name == "Cas" or name == "Ca-S" or name == "California (South)" or name == "Socal" or name == "California South" or name == "california-north": return "California (South)"
    elif name == "Can" or name == "Ca-N" or name == "California (North)" or name == "Nocal" or name == "California North" or name == "california-south": return "California (North)"
    if name == "Co" or name == "Colorado": return "Colorado"
    elif name == "Ct" or name == "Connecticut": return "Connecticut"
    elif name == "Dc" or name == "District Of Columbia" or name == "district-of-columbia": return "District of Columbia"
    elif name == "De" or name == "Delaware": return "Delaware"
    elif name == "Fl" or name == "Florida": return "Florida"
    elif name == "Ga" or name == "Georgia": return "Georgia"
    elif name == "Hi" or name == "Hawaii": return "Hawaii"
    elif name == "Id" or name == "Idaho": return "Idaho"
    elif name == "Il" or name == "Illinois": return "Illinois"
    elif name == "In" or name == "Indiana": return "Indiana"
    elif name == "Ia" or name == "Iowa": return "Iowa"
    elif name == "Ks" or name == "Kansas": return "Kansas"
    elif name == "Ky" or name == "Kentucky": return "Kentucky"
    elif name == "La" or name == "Louisiana": return "Louisiana"
    elif name == "Me" or name == "Maine": return "Maine"
    elif name == "Md" or name == "Maryland": return "Maryland"
    elif name == "Ma" or name == "Massachusetts": return "Massachusetts"
    elif name == "Mi" or name == "Michigan": return "Michigan"
    elif name == "Mn" or name == "Minnesota": return "Minnesota"
    elif name == "Ms" or name == "Mississippi": return "Mississippi"
    elif name == "Mo" or name == "Missouri": return "Missouri"
    elif name == "Mt" or name == "Montana": return "Montana"
    elif name == "Ne" or name == "Nebraska": return "Nebraska"
    elif name == "Nv" or name == "Nevada": return "Nevada"
    elif name == "Nh" or name == "New Hampshire": return "New Hampshire"
    elif name == "Nj" or name == "New Jersey": return "New Jersey"
    elif name == "Nm" or name == "New Mexico": return "New Mexico"
    elif name == "Ny" or name == "New York": return "New York"
    elif name == "Nc" or name == "North Carolina": return "North Carolina"
    elif name == "Nd" or name == "North Dakota": return "North Dakota"
    elif name == "Oh" or name == "Ohio": return "Ohio"
    elif name == "Ok" or name == "Oklahoma": return "Oklahoma"
    elif name == "Or" or name == "Oregon": return "Oregon"
    elif name == "Pa" or name == "Pennsylvania": return "Pennsylvania"
    elif name == "Ri" or name == "Rhode Island": return "Rhode Island"
    elif name == "Sc" or name == "South Carolina": return "South Carolina"
    elif name == "Sd" or name == "South Dakota": return "South Dakota"
    elif name == "Tn" or name == "Tennessee": return "Tennessee"
    elif name == "Tx" or name == "Texas": return "Texas"
    elif name == "Ut" or name == "Utah": return "Utah"
    elif name == "Vt" or name == "Vermont": return "Vermont"
    elif name == "Va" or name == "Virginia": return "Virginia"
    elif name == "Wa" or name == "Washington": return "Washington"
    elif name == "Wv" or name == "West Virginia": return "West Virginia"
    elif name == "Wi" or name == "Wisconsin": return "Wisconsin"
    elif name == "Wy" or name == "Wyoming": return "Wyoming"
    return False
    
async def refresh_algorithm():
    """Pulls data from the administrative sheet."""
    try:
        global CENSORED_WORDS
        global CENSORED_EMOJIS
        censor = await get_censor()
        CENSORED_WORDS = censor[0]
        CENSORED_EMOJIS = censor[1]
    except Exception as e:
        print("Could not refresh censor in refresh_algorithm:")
        print(e)

    try:
        global EVENT_INFO
        EVENT_INFO = await get_events()
    except Exception as e:
        print("Could not refresh event list in refresh_algorithm:")
        print(e)

    try:
        global TAGS
        TAGS = await get_tags()
    except Exception as e:
        print("Could not refresh tags in refresh_algorithm:")
        print(e)
    
    print("Refreshed data from sheet.")
    return True
    
def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()