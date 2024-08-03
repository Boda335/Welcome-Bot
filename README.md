# Welcome-Bot

## Overview

This Discord bot is designed to enhance server management with features such as setting welcome channels, managing roles, and adding custom buttons to welcome messages. It also includes functionality to overlay user avatars on images and send personalized welcome messages.

## Features

- **Welcome Channel Setup**: Configure a welcome channel for new members.
- **Role Assignment**: Automatically assign roles to new members and bots.
- **Custom Buttons**: Add up to 3 custom buttons to welcome messages.
- **Avatar Overlay**: Overlay user avatars on a background image.
- **Personalized Welcome Messages**: Send customized welcome messages with embed and buttons.

## Requirements

- Python 3.8 or higher
- `discord.py` library
- `Pillow` library
- `requests` library

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo-url.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd your-repo-directory
   ```

3. **Install Dependencies**:

   ```bash
   pip install discord.py pillow requests
   ```

4. **Configure Your Bot**:

   - Replace `"Token Here"` in `client.run("Token Here")` with your bot's token.
   - Ensure that `guild_data.json` and `bg/welcome_image.png` are in the correct paths.

## Usage

1. **Run the Bot**:

   ```bash
   python your_bot_file.py
   ```

2. **Commands**:

   - `/set_channel <channel>`: Set the welcome channel for the server.
   - `/set_roles <bot_role> <member_role>`: Set roles for bots and members.
   - `/add_button <label> <url> <emoji>`: Add a custom button to the welcome message.

   Ensure you have administrative permissions to use these commands.

## How It Works

- **`on_ready` Event**: Logs bot's status and refreshes application commands.
- **`on_member_join` Event**: Sends a personalized welcome message to new members, including their avatar overlaid on a background image, and assigns roles based on their type (bot or member).

## File Structure

- `your_bot_file.py`: Main bot script.
- `guild_data.json`: Stores guild-specific settings.
- `bg/welcome_image.png`: Background image for overlaying avatars.

## Support

For any issues or questions, please reach out via [Discord Server](https://discord.gg/DzjuTABN6E).

## Credits

- **Bot Coder**: boda3350
- **GitHub Repository**: [Your GitHub Repository](https://github.com/your-repo-url)
- **Discord Server**: [Join Us](https://discord.gg/DzjuTABN6E)
