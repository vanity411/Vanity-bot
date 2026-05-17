import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID = 1505196263023317182
KEYWORD = "/balkan"


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


async def check_member(member: discord.Member):
    role = member.guild.get_role(ROLE_ID)
    if not role:
        return

    has_keyword = False

    # Check custom status
    for activity in member.activities:
        if isinstance(activity, discord.CustomActivity):
            if activity.name and KEYWORD in activity.name.lower():
                has_keyword = True

    # Find reps channel
    channel = discord.utils.get(member.guild.text_channels, name="reps")

    try:
        if has_keyword:
            if role not in member.roles:
                await member.add_roles(role)

                # 🔥 ANNOUNCEMENT MESSAGE
                if channel:
                    await channel.send(
                        f"Tssm 4 Repping us, {member.mention} ⁈"
                    )

        else:
            if role in member.roles:
                await member.remove_roles(role)

    except discord.Forbidden:
        print("Missing permissions to manage roles.")


@bot.event
async def on_member_join(member):
    await check_member(member)


@bot.event
async def on_member_update(before, after):
    await check_member(after)


@bot.event
async def on_presence_update(before, after):
    await check_member(after)


bot.run("MTUwNTIxNDgyNjQ1OTE3MzAwNQ.GLQ0i1.UBCat0jGVH5KlWHpo_ckLJ_hjVhzXNJv7O7ETs")
