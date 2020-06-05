# A basic queue cog for discord.py

# Getting Started

## This is built for my [discord-bot](https://github.com/stroupbslayen/discord-bot) framework.

- To install, copy the folders into the `bot` directory

# Commands

## add

- Everyone - `True`
- Aliases - `null`
- Usage - `<prefix>addApproved`
- Example - `!addApproved`
- Description - Add yourself to the queue!

## clear

- Everyone - `False`
- Aliases - `null`
- Usage - `<prefix>clear`
- Example - `!clear`
- Description - Clears the queue

## next

- Everyone - `False`
- Aliases - `null`
- Usage - `<prefix>next`
- Example - `!next`
- Description - Call the next member in the queue

## position

- Everyone - `True`
- Aliases - `null`
- Usage - `<prefix>position`
- Example - `!position`
- Description - Check your position in the queue

## queue

- Everyone - `True`
- Aliases - `null`
- Usage - `<prefix>queue`
- Example - `!queue`
- Description - See who's up next!

## remove

- Everyone - `True`
- Aliases - `null`
- Usage - `<prefix>remove`
- Example - `!remove`
- Description - Remove yourself from the queue

## toggleq

- Everyone - `False`
- Aliases - `None`
- Usage - `<prefix>toggle`
- Example - `!toggle`
- Description - Toggles the queue to open or closed

# Notes

- Python 3.6+ is required
- Add role names or ids to the `APPROVED_ROLES` variable in the script
