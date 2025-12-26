# GET BEST PLAYER 🥇

This is a python script that gets you the player with the highest rating for a specific round of the __Africa cup of nations 2025 tournament__ 🏆

## How to use it ?

1. Firstly, you run the script  `python run`
1. then, you login or register
1. lastly, you choose which round is your target (the last one is the default)

## Authentication
1. all users are stored in `users.json` file
1. the system ensures that usernames and emails are unique and valid
1. passwords are stored as __hashes (Argon2)__ 

## But how it works ?
Basically, the script calls a free API over the internet, get all the data it needs (which matches were in a specific round, all the players data), process that then show the results. 