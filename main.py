import discord
from discord.ext import commands
from discord.ui import Button, View, Select, Modal, TextInput
from PIL import Image, ImageDraw
import io
import json
import requests
import os
os.system('cls' if os.name == 'nt' else 'clear')


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
def load_json(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

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
    register_command_status(func.__name__, "✔️", premium=True)
    return func

def regular_command(func):
    func.is_premium = False
    register_command_status(func.__name__, "✔️")
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

    activity = discord.Activity(type=discord.ActivityType.watching, name="you join the server")
    await client.change_presence(status=discord.Status.idle, activity=activity)
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
    
    
    
class EditButtonModal(Modal):
    def __init__(self, button_data):
        super().__init__(title="Edit Button")
        self.old_label = button_data['label']
        self.old_emoji = button_data.get('emoji', '')
        self.old_url = button_data.get('url', '')

        self.label_input = TextInput(label="Button Name", placeholder="Enter new button name", default=self.old_label)
        self.add_item(self.label_input)

        self.emoji_input = TextInput(label="Emoji", placeholder="Enter new emoji", default=self.old_emoji)
        self.add_item(self.emoji_input)

        self.url_input = TextInput(label="URL", placeholder="Enter new URL", default=self.old_url)
        self.add_item(self.url_input)

    async def on_submit(self, interaction: discord.Interaction):
        new_label = self.label_input.value
        new_emoji = self.emoji_input.value
        new_url = self.url_input.value

        guild_id = str(interaction.guild_id)
        if guild_id in guild_data:
            # Remove old button data
            guild_data[guild_id]['buttons'] = [button for button in guild_data[guild_id].get('buttons', []) if button['label'] != self.old_label]
            
            # Add new button data
            guild_data[guild_id].setdefault('buttons', []).append({
                'label': new_label,
                'emoji': new_emoji,
                'url': new_url
            })
            
            save_json('guild_data.json', guild_data)
            # Respond to the interaction to confirm the update
            await interaction.response.send_message(f"Button '{self.old_label}' has been updated to '{new_label}'.", ephemeral=True)
        else:
            await interaction.response.send_message("Failed to update button. No data found.", ephemeral=True)

        # Use a follow-up message to confirm successful update
        await interaction.followup.send("Button updated successfully.", ephemeral=True)

@client.tree.command(name="manage_buttons", description="Manage buttons by selecting from a menu.")
async def manage_buttons(interaction: discord.Interaction):
    guild_id = str(interaction.guild_id)
    if guild_id not in guild_data or 'buttons' not in guild_data[guild_id]:
        await interaction.response.send_message("No buttons to manage.", ephemeral=True)
        return
    
    buttons = guild_data[guild_id]['buttons']

    seen_labels = set()
    options = []
    for button in buttons:
        label = button['label']
        emoji = button.get('emoji', '')
        if label not in seen_labels:
            option = discord.SelectOption(
                label=label,
                value=label,
                emoji=emoji if emoji else None  # Use emoji if present
            )
            options.append(option)
            seen_labels.add(label)

    select_menu = discord.ui.Select(placeholder="Choose a button to manage...", options=options, custom_id="manage_buttons_select")
    view = View()
    view.add_item(select_menu)
    
    await interaction.response.send_message("Select a button to manage:", view=view, ephemeral=True)



@client.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data['custom_id'] == 'manage_buttons_select':
            selected_label = interaction.data['values'][0]
            guild_id = str(interaction.guild_id)
            button_data = next((button for button in guild_data[guild_id].get('buttons', []) if button['label'] == selected_label), None)

            if button_data:
                view = View()
                
                # Button to delete the selected button
                delete_button = Button(label="Delete Button", style=discord.ButtonStyle.danger, custom_id=f"delete_button_{selected_label}")
                view.add_item(delete_button)

                # Button to edit the selected button
                edit_button = Button(label="Edit Button", style=discord.ButtonStyle.primary, custom_id=f"edit_button_{selected_label}")
                view.add_item(edit_button)

                await interaction.response.send_message("Choose an action:", view=view, ephemeral=True)

        elif interaction.data['custom_id'].startswith('delete_button_'):
            button_label = interaction.data['custom_id'].split('_', 2)[2]
            guild_id = str(interaction.guild_id)
            
            # Delete the selected button
            if guild_id in guild_data:
                guild_data[guild_id]['buttons'] = [btn for btn in guild_data[guild_id].get('buttons', []) if btn['label'] != button_label]
                save_json('guild_data.json', guild_data)
                await interaction.response.send_message(f"Button '{button_label}' has been deleted.", ephemeral=True)
            else:
                await interaction.response.send_message("Failed to delete button. No data found.", ephemeral=True)

        elif interaction.data['custom_id'].startswith('edit_button_'):
            button_label = interaction.data['custom_id'].split('_', 2)[2]
            # Open the modal to edit the button
            button_data = next((button for button in guild_data[str(interaction.guild_id)].get('buttons', []) if button['label'] == button_label), None)
            if button_data:
                modal = EditButtonModal(button_data)
                await interaction.response.send_modal(modal)


    

@client.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id not in guild_data:
        return
    
    welcome_channel_id = guild_data[guild_id].get('welcome_channel_id')
    bot_role_id = guild_data[guild_id].get('bot_role_id')
    member_role_id = guild_data[guild_id].get('member_role_id')

    # تحديث قائمة الدعوات قبل التحقق من الدعوة المستخدمة
    invites_before = guild_data[guild_id].get('invites', {})
    invites_after = await member.guild.invites()

    if welcome_channel_id:
        welcome_channel = member.guild.get_channel(welcome_channel_id)
        if welcome_channel:
            role = member.guild.get_role(bot_role_id) if member.bot else member.guild.get_role(member_role_id)
            if role:
                await member.add_roles(role)
            
            # العثور على الدعوة المستخدمة
            used_invite = None
            for invite in invites_after:
                if invite.uses > invites_before.get(invite.code, 0):
                    used_invite = invite
                    break

            inviter_mention = "Unknown"
            invite_code = used_invite.code if used_invite else "N/A"
            if used_invite and used_invite.inviter:
                inviter_mention = f"<@{used_invite.inviter.id}>"

            thumbnail_url = member.guild.icon.url if member.guild.icon else None
            
            # تحقق من صورة الأفاتار الخاصة بالعضو
            user_image_url = member.avatar.url if member.avatar else "https://cdn.discordapp.com/embed/avatars/0.png"
            
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
                    custom_button = Button(label=button['label'], url=button['url'], emoji=button['emoji'])
                    view.add_item(custom_button)

            # إرسال الـEmbed مع الأزرار إلى قناة الترحيب
            await welcome_channel.send(content=f"{member.mention}",embed=welcome_embed, file=image_url, view=view)

            try:
                # إرسال الـEmbed مع الأزرار إلى الرسائل الخاصة
                if member.dm_channel is None:
                    await member.create_dm()
                await member.dm_channel.send(embed=welcome_embed, file=image_url, view=view)
            except discord.Forbidden:
                print(f"Couldn't send a DM to {member.name} with id {member.id}.")

    # تحديث بيانات الدعوات بعد الاستخدام
    guild_data[guild_id]['invites'] = {invite.code: invite.uses for invite in invites_after}
    save_json('guild_data.json', guild_data)

@client.event
async def on_invite_create(invite):
    guild_id = str(invite.guild.id)
    if guild_id not in guild_data:
        guild_data[guild_id] = {}

    if 'invites' not in guild_data[guild_id]:
        guild_data[guild_id]['invites'] = {}

    guild_data[guild_id]['invites'][invite.code] = invite.uses
    save_json('guild_data.json', guild_data)

@client.event
async def on_invite_delete(invite):
    guild_id = str(invite.guild.id)
    if guild_id in guild_data and 'invites' in guild_data[guild_id]:
        guild_data[guild_id]['invites'].pop(invite.code, None)
        save_json('guild_data.json', guild_data)

client.run(token)
