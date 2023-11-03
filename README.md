# angr_eBirds

![Canada Goose](https://github.com/DanielTimbie/angr_eBirds/assets/44413655/8f6469e1-38ec-46e8-86f6-00fcf1953dbc)


This project started as python practice - it is essentially a clone of the popular phone game 
'Flappy Bird', but it gives the user the option to connect to Cornell Labs' eBird API to pull 
a list of the five most recent birds sighted in their area. These birds are then playable using 
a dropdown box in the main menu. The game is programmed in python, and has the default location 
set to Chicago. 

The importand files are:

• `app/main.py`

• `app/ebird_api.py`

• `graphics/.`

`main.py` is responsible for implementing the game functions. `ebird_api.py` does the API call for 
Cornell Labs' eBird. For now, the only functionality is to pull a list of recent bird sightings. 
Finally, `graphics` is a folder that contains all of the sprites used to run the game. 

!!! If using this code, please go to the `ebird_api.py` file and $change the API key$ !!!

To get started, run `main.py`. You will be greeted by the default start screen:

<img width="402" alt="Screen Shot 2023-11-03 at 12 28 27 AM" src="https://github.com/DanielTimbie/angr_eBirds/assets/44413655/895e28ec-beb3-4c0a-98a7-d83758671baa">

When a user clicks "Fetch Recent Birds", a list of five of the most recent birds spotted at the location code is returned. 
The default is Cook Country, IL. A user can then click the drop-down menu to choose which bird they wish to play as - 
I am currently working on building out the list of birds that have corresponding playable sprites. If a bird has a sprite
listed in `graphics/bird sprites`, it will take the place of the default bird, which will be the playable character if 
a user's choice does not have a corresponding sprite. 

The default bird when a sprite is unavailable is this little guy right here:

<img width="494" alt="Screen Shot 2023-11-03 at 12 41 56 AM" src="https://github.com/DanielTimbie/angr_eBirds/assets/44413655/c61d75b5-428e-4cbd-845c-9b41809f95b5">

I'm not sure what kind of bird he's supposed to be.

Here's a screenshot from the game while it's running - I'm playing as a Northern Shoveler, and I'm using the forest background. That can be toggled
with a button on the bottom left hand side of the screen.

<img width="327" alt="Screen Shot 2023-11-03 at 12 45 42 AM" src="https://github.com/DanielTimbie/angr_eBirds/assets/44413655/8219d84b-7b38-441e-aac4-6d47ff2b1a7e">

After you get going, it's pretty self explanatory. Press the space bar to keep your bird from hitting the obstacles. Good luck!

~Daniel

![Canada Goose](https://github.com/DanielTimbie/angr_eBirds/assets/44413655/7ab4ec6b-6733-4ae5-b8c6-76da5a59f217)