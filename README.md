Make user to apply any changes to this file to README_RAW.rst as well!

![todo-telegram-bot Logo](https://github.com/SurajMeena/todo-telegram-bot/blob/master/img/todogroup_bot.png)

We have made you a bot you can't refuse

Join our community for discussions, feature requests and reporting bugs for todo bot through our [Telegram group](https://telegram.me/pythontelegrambotgroup). Join us!

*Stay tuned for feature updates and bug fixes on our* [Telegram Channel](https://telegram.me/todogroup_bot).

![Supported Python versions](https://img.shields.io/badge/Python-3.7+-yellow.svg?logo=python)
![Supported Pyrogram versions](https://img.shields.io/badge/Pyrogram-orange.svg?logo=pyrogram)
![MIT License](https://img.shields.io/badge/License-MIT-blue.svg?logo=MIT)
![Bot](https://img.shields.io/badge/Telegram-Bot-green.svg?logo=telegram)
![Bot Help Channel](https://img.shields.io/badge/Telegram-Channel-blue.svg?logo=telegram)
![Bot Help Group](https://img.shields.io/badge/Telegram-Group-red.svg?logo=telegram)
![Bot Working Video](https://img.shields.io/badge/Working-Video-Purple.svg?logo=telegram)

## Table of contents

- [Introduction](#introduction)
- [How to Deploy](#how-to-deploy)
   - [Pre-requisites](#pre-requisites)
   - [On Terminal or VPS](#on-terminal-or-vps)
- [Getting help](#getting-help)
- [Contribution and Contributors](#contribution-and-contributors)

## Introduction

`todo-telegram-bot` as name suggests is a todo list management bot for groups and personal chats. You can create several lists automatically and manage them efficiently. The bot is based on adding items to list based on hashtags present in messages. All you need to do is tell the about about hashtags that needs to be tracked for getting added in a list. As of now, users can create one separate list independent of any hashtag.

## How to Deploy

### Pre-requisites

- Firebase Key
   - Open [Firebase](https://firebase.google.com) and Sign in using a google account
   - Click on Go to Console option followed by clicking on adding a project
   - Follow appropriate dialogs to create a new project
   - In your project, go to realtime database and create a new databaset there
   - Now Go to Project Settings and create a new private key under service accounts.
   - Store downloaded key in todo-telegram-bot folder
- Telegram API ID and API Hash
- Bot Token from Botfather

### On Terminal or VPS

1. Clone the repository in your home directory or anywhere you want it to and then cd into the repository folder

    ```shell
    $ git clone https://github.com/SurajMeena/todo-telegram-bot.git
    $ cd todo-telegram-bot
    ```

2. Create a virtual environment and activate it

    ```shell
    $ python -m venv venv_name
    $ source venv_name/bin/activate
    ```

3. Install python packages for successful working of bot

    ```shell
    $ pip install -r requirements.txt --nodeps
    ```

4. Copy and Rename sample_config.ini to todogroup_bot.ini and configure its content accordingly

5. Replace sample_firebase_key.json with key file obtained from following prerequisites

6. Copy and Rename sample.env to .env and configure its content accordingly

7. Run bot

    ```shell
    $ python -m bot
    ```

## Getting help

You can get help in several ways:

1. We have a todogroup_bot Channel and Group for relaying updates and discussions

    [![Bot Help Channel](https://img.shields.io/badge/Telegram-Group-blue.svg?logo=telegram)](https://telegram.me/help_todogroup_bot)
    [![Bot Help Group](https://img.shields.io/badge/Telegram-Group-red.svg?logo=telegram)](https://telegram.me/help_todogroup_chat)

    Join us!

2. Report bugs, request new features or ask questions through our group or you can also contact us through our support bot.

    [![Support Bot](https://img.shields.io/badge/Support-Bot-blue.svg?logo=telegram)](https://telegram.me/messtotelebot)

## Contribution and Contributors

Contributions of all sizes are welcome. You can also help us by [reporting bugs on our Telegram Group](https://telegram.me/help_todogroup_chat) and [Support Bot](https://telegram.me/messtotelebot).

Huge Thanks to [Vikram Singh](https://github.com/vpsinghg) for his valuable contribution in this project.
