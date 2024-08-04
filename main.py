import discord
from discord.ext import commands
from discord.ui import Button, View
from PIL import Image, ImageDraw
import io
import json
import requests

intents = discord.Intents.default()
intents.members = True
intents.invites = True

client = commands.Bot(command_prefix="!", intents=intents)

def load_json(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def load_config(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
config = load_config('config.json')
token = config.get("token")
def save_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
regular_commands_status = []
premium_commands_status = []
def register_command_status(name, status, premium=False):
    if premium:
        premium_commands_status.append({"name": name, "status": status})
    else:
        regular_commands_status.append({"name": name, "status": status})
guild_data = load_json('guild_data.json')
regular_commands_status = []
premium_commands_status = []
def register_command_status(name, status, premium=False):
    if premium:
        premium_commands_status.append({"name": name, "status": status})
    else:
        regular_commands_status.append({"name": name, "status": status})
        
def overlay_avatar_on_image(background_path, avatar_url, avatar_size=100, position=None):
    background = Image.open(background_path).convert("RGBA")
    response = requests.get(avatar_url)
    avatar = Image.open(io.BytesIO(response.content)).convert("RGBA")
    avatar = avatar.resize((avatar_size, avatar_size), Image.LANCZOS)
    mask = Image.new('L', avatar.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    avatar.putalpha(mask)
    if position is None:
        position = ((background.size[0] - avatar_size) // 2, (background.size[1] - avatar_size) // 2)
    background.paste(avatar, position, avatar)
    return background

def check_admin_permissions(interaction: discord.Interaction):
    return any(role.permissions.administrator for role in interaction.user.roles)
def premium_command(func):
    func.is_premium = True
    register_command_status(func.__name__, "✔️", premium=True)  # تسجيل الأمر كبريميوم
    return func

# ديكوريتور لتحديد الأوامر العادية وتسجيلها
def regular_command(func):
    func.is_premium = False
    register_command_status(func.__name__, "✔️")  # تسجيل الأمر كعادي
    return func

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print("Started refreshing application (/) commands.")
    print("Successfully reloaded application (/) commands.")
    print("┌───────────────────────────────┬────────────┐")
    print("│ Command Name                  │   Status   │")
    print("├───────────────────────────────┼────────────┤")
    for command in regular_commands_status:
        print(f"│ {command['name']:<29} │     {command['status']}      │")
    print("└───────────────────────────────┴────────────┘")
    print("coded by boda3350")
    print("https://discord.gg/DzjuTABN6E")

    await client.tree.sync()

@client.tree.command(name="set_channel", description="Set the welcome channel for the server.")
@regular_command
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    if not check_admin_permissions(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    if guild_id not in guild_data:
        guild_data[guild_id] = {}
    guild_data[guild_id]['welcome_channel_id'] = channel.id
    save_json('guild_data.json', guild_data)
    await interaction.response.send_message(f"Welcome channel set to {channel.mention}", ephemeral=True)
guild_data = load_json('guild_data.json')

@client.tree.command(name="set_roles", description="Set the auto roles for bots and members.") 
@regular_command
async def set_roles(interaction: discord.Interaction, bot_role: discord.Role, member_role: discord.Role):
    if not check_admin_permissions(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    if guild_id not in guild_data:
        await interaction.response.send_message("Please set the welcome channel first using /set_channel", ephemeral=True)
        return
    
    guild_data[guild_id]['bot_role_id'] = bot_role.id
    guild_data[guild_id]['member_role_id'] = member_role.id
    save_json('guild_data.json', guild_data)
    await interaction.response.send_message(f"Roles set: Bot Role - {bot_role.mention}, Member Role - {member_role.mention}", ephemeral=True)

@client.tree.command(name="add_button", description="Add a custom button to the welcome message.")
@regular_command
async def add_button(interaction: discord.Interaction, label: str, url: str, emoji: str):
    if not check_admin_permissions(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    if guild_id not in guild_data:
        await interaction.response.send_message("Please set the welcome channel first using /set_channel", ephemeral=True)
        return
    
    if 'buttons' not in guild_data[guild_id]:
        guild_data[guild_id]['buttons'] = []

    if len(guild_data[guild_id]['buttons']) >= 3:
        await interaction.response.send_message("You can only add up to 3 buttons.", ephemeral=True)
        return

    guild_data[guild_id]['buttons'].append({"label": label, "url": url, "emoji": emoji})
    save_json('guild_data.json', guild_data)
    await interaction.response.send_message(f"Button added: {label}", ephemeral=True)

@client.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id not in guild_data:
        return
    
    welcome_channel_id = guild_data[guild_id].get('welcome_channel_id')
    bot_role_id = guild_data[guild_id].get('bot_role_id')
    member_role_id = guild_data[guild_id].get('member_role_id')

    if welcome_channel_id:
        welcome_channel = member.guild.get_channel(welcome_channel_id)
        if welcome_channel:
            role = member.guild.get_role(bot_role_id) if member.bot else member.guild.get_role(member_role_id)
            if role:
                await member.add_roles(role)
            
            # Fetch the current invites
            new_invites = await member.guild.invites()
            used_invite = None
            for invite in new_invites:
                prev_uses = guild_data[guild_id].get('invites', {}).get(invite.code, 0)
                if invite.uses > prev_uses:
                    used_invite = invite
                    break

            inviter_mention = "Unknown"
            invite_code = used_invite.code if used_invite else "N/A"
            if used_invite and used_invite.inviter:
                inviter_mention = f"<@{used_invite.inviter.id}>"

            thumbnail_url = member.guild.icon.url if member.guild.icon else None
            user_image_url = member.avatar.url
            background_path = './bg/welcome_image.png'
            avatar_size = 450
            position = (685, 280)
            final_image = overlay_avatar_on_image(background_path, user_image_url, avatar_size, position)
            
            with io.BytesIO() as output:
                final_image.save(output, format="PNG")
                output.seek(0)
                image_url = discord.File(fp=output, filename="welcome_image.png")

            welcome_embed = discord.Embed(
                color=0xedab55,
                title="Welcome to the Server!",
                description=f"Hello {member}, welcome to **{member.guild.name}**! Enjoy your stay.",
                timestamp=discord.utils.utcnow()
            ).add_field(name="Username", value=member.name, inline=True) \
             .add_field(name="Invited By", value=inviter_mention, inline=True) \
             .add_field(name="Invite Code", value=f"||{invite_code}||", inline=True) \
             .add_field(name="Total Members", value=str(member.guild.member_count), inline=True) \
             .set_thumbnail(url=thumbnail_url) \
             .set_image(url="attachment://welcome_image.png")

            view = View()
            if 'buttons' in guild_data[guild_id]:
                for button in guild_data[guild_id]['buttons']:
                    view.add_item(Button(style=discord.ButtonStyle.link, url=button['url'], label=button['label'], emoji=button['emoji']))

            # Send the embed to the welcome channel
            await welcome_channel.send(content=f"{member.mention}", embeds=[welcome_embed], view=view, files=[image_url])

            # Send the embed to the new member via DM
            try:
                await member.send(embed=welcome_embed, view=view, files=[image_url])
            except discord.Forbidden:
                print(f"Could not send DM to {member}")
                
if __name__ == "__main__":
    client.run(token)
