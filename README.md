
# Welcome Bot

WelcomeBot is a feature-rich Discord bot designed to enhance your server's welcome experience. It greets new members, assigns roles automatically, and allows server administrators to customize welcome messages with buttons and embeds.

## Features

- **Welcome Messages:** Send personalized welcome messages to new members.
- **Auto Role Assignment:** Automatically assign roles to new members and bots.
- **Custom Buttons:** Add up to 3 custom buttons to the welcome message.
- **Invite Tracking:** Track who invited new members to your server.

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/your-username/WelcomeBot.git
    ```
2. Navigate to the project directory:
    ```sh
    cd WelcomeBot
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `config.json` file in the root directory with your bot token:
    ```json
    {
        "token": "YOUR_DISCORD_BOT_TOKEN"
    }
    ```
2. Run the bot:
    ```sh
    python bot.py
    ```

## Commands

### `/set_channel`

Set the welcome channel for the server.

**Usage:**
```sh
/set_channel <channel>
```

### `/set_roles`

Set the auto roles for bots and members.

**Usage:**
```sh
/set_roles <bot_role> <member_role>
```

### `/add_button`

Add a custom button to the welcome message.

**Usage:**
```sh
/add_button <label> <url> <emoji>
```

## Example Usage

### Setting the Welcome Channel

![Set Channel Example](path/to/set_channel_example.png)

### Setting Roles

![Set Roles Example](path/to/set_roles_example.png)

### Adding a Custom Button

![Add Button Example](path/to/add_button_example.png)

### Welcome Message

![Welcome Message Example](path/to/welcome_message_example.png)

## Code Explanation

The bot is built using `discord.py` and includes various commands to set up and manage welcome messages. Here are the main components:

- **Command Registration:** Regular and premium commands are registered and their statuses are tracked.
- **Welcome Message:** When a new member joins, the bot sends a welcome message with the member's avatar and details.
- **Invite Tracking:** The bot tracks who invited the new member and includes this information in the welcome message.
- **Custom Buttons:** Server administrators can add custom buttons to the welcome message.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, join our [Discord Server](https://discord.gg/DzjuTABN6E).
