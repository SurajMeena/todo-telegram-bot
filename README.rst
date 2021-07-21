..
    Make user to apply any changes to this file to README_RAW.rst as well!

.. image:: https://github.com/img/todogroup_bot.png
   :align: center
   :target: https://telegram.me/todogroup_bot
   :alt: todo-telegram-bot Logo

We have made you a bot you can't refuse

Join our community for discussions, feature requests and reporting bugs for todo bot through our `Telegram group <https://telegram.me/pythontelegrambotgroup>`_. Join us!

*Stay tuned for feature updates and bug fixes on our* `Telegram Channel <https://telegram.me/todogroup_bot>`_.

.. image:: https://img.shields.io/badge/Python-3.7+-yellow.svg?logo=python
   :target: https://telegram.me/todogroup_bot
   :alt: Supported Python versions

.. image:: https://img.shields.io/badge/Pyrogram-orange.svg?logo=pyrogram
   :target: https://core.telegram.org/bots/api-changelog
   :alt: Supported Bot API versions

.. image:: https://img.shields.io/badge/License-MIT-blue.svg?logo=MIT
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: MIT License

.. image:: https://img.shields.io/badge/Telegram-Bot-green.svg?logo=telegram
   :target: https://telegram.me/todogroup_bot
   :alt: Bot

.. image:: https://img.shields.io/badge/Telegram-Channel-blue.svg?logo=telegram
   :target: https://telegram.me/help_todogroup_bot
   :alt: Bot Help Channel

.. image:: https://img.shields.io/badge/Telegram-Group-red.svg?logo=telegram
   :target: https://telegram.me/help_todogroup_chat
   :alt: Bot Help Group

.. image:: https://img.shields.io/badge/Working-Video-Purple.svg?logo=telegram
   :target: https://t.me/help_todogroup_bot/5
   :alt: Bot Working Video

=================
Table of contents
=================

- `Introduction`_

- `How to Deploy`_

  #. `Pre-requisites`_

  #. `On Terminal or VPS`_

- `Getting help`_

- `Contribution and Contributors`_

============
Introduction
============
``todo-telegram-bot`` as name suggests is a todo list management bot for groups and personal chats. You can create several lists automatically and manage them efficiently. The bot is based on adding items to list based on hashtags present in messages. All you need to do is tell the about about hashtags that needs to be tracked for getting added in a list. As of now, users can create one separate list independent of any hashtag.

=============
How to Deploy
=============

---------------
Pre-requisites
---------------
* Firebase Key

   1. Open `Firebase <https://firebase.google.com>`_ and Sign in using a google account
   2. Click on Go to Console option followed by clicking on adding a project
   3. Follow appropriate dialogs to create a new project
   4. In your project, go to realtime database and create a new databaset there
   5. Now Go to Project Settings and create a new private key under service accounts.
   6. Store downloaded key in todo-telegram-bot folder
* Telegram API ID and API Hash
* Bot Token from Botfather

-------------------
On Terminal or VPS
-------------------

1. Clone the repository in your home directory or anywhere you want it to and then cd into the repository folder

.. code:: shell

   $ git clone https://github.com/SurajMeena/todo-telegram-bot.git
   $ cd todo-telegram-bot

2. Create a virtual environment and activate it

.. code:: shell

   $ python -m venv venv_name
   $ source venv_name/bin/activate

3. Install python packages for successful working of bot

.. code:: shell

   $ pip install -r requirements.txt

4. Copy and Rename sample_config.ini to todogroup_bot.ini and configure it's content accordingly

5. Replace sample_firebase_key.json with key file obtained from following prerequisites

6. Copy and Rename sample.env to .env and configure it's content accordingly

7. Run bot

.. code:: shell

   $ python -m bot

============
Getting help
============

You can get help in several ways:

1. We have a todogroup_bot Channel and Group for relaying updates and discussions

.. image:: https://img.shields.io/badge/Telegram-Group-blue.svg?logo=telegram
   :target: https://telegram.me/help_todogroup_bot
   :alt: Bot Help Channel

.. image:: https://img.shields.io/badge/Telegram-Group-red.svg?logo=telegram
   :target: https://telegram.me/help_todogroup_chat
   :alt: Bot Help Group

Join us!

2. Report bugs, request new features or ask questions through our group or you can also contact us through our support bot.

.. image:: https://img.shields.io/badge/Support-Bot-blue.svg?logo=telegram
   :target: https://telegram.me/messtotelebot
   :alt: Support Bot
   
==============================
Contribution and Contributors
==============================

Contributions of all sizes are welcome. You can also help us by `reporting bugs on our Telegram Group <https://telegram.me/help_todogroup_chat>`_ and `Support Bot <https://telegram.me/messtotelebot>`_.

Huge Thanks to `Vikram Singh <https://github.com/vpsinghg>`_ for his valuable contribution in this project.