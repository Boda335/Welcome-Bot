# Welcome Wizard

Welcome Wizard is a Discord bot designed to enhance server management by welcoming new members, setting up channels, and adding interactive elements like custom buttons. It includes features for handling member roles, tracking invites, and overlaying user avatars on welcome images.

## Features

- **Custom Welcome Messages**: Automatically sends a customized welcome message with an overlayed avatar image when a new member joins.
- **Channel Management**: Set a welcome channel where new member greetings are posted.
- **Role Assignment**: Automatically assigns roles to new members based on their status (bot or regular member).
- **Interactive Buttons**: Add up to 3 custom buttons to the welcome message for enhanced interaction.
- **Invite Tracking**: Tracks invites to identify who invited the new member and includes this information in the welcome message.

## Commands

### `/set_channel`
Sets the welcome channel for the server.
- **Parameters**: `channel` (TextChannel)

### `/set_roles`
Sets the auto roles for bots and members.
- **Parameters**: `bot_role` (Role), `member_role` (Role)

### `/add_button`
Adds a custom button to the welcome message.
- **Parameters**: `label` (string), `url` (string), `emoji` (string)

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/welcome-wizard.git
    ```

2. Install the required packages:
    ```bash
    pip install discord.py pillow requests
    ```

3. Update the `Token Here` placeholder in the script with your bot's token.

4. Run the bot:
    ```bash
    python bot.py
    ```

## Configuration

- **`guild_data.json`**: This file stores server-specific settings such as channel IDs, role IDs, and button configurations.
- **`bg/welcome_image.png`**: This is the background image used for overlaying user avatars.

## Contributing

Feel free to fork this repository and submit pull requests. Contributions and suggestions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please join our [Discord Server](https://discord.gg/DzjuTABN6E).

---

_Coded by boda3350_
