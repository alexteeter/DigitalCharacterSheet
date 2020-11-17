# DigitalCharacterSheet
A digital character sheet for Dungeons and Dragons Fifth Edtion

## Overview
A simple Python-based program that tracks all (most) of the stats and numbers needed for D&D, that's homebrew-agnostic, and pretty editable. This is a work in progress, but can get most characters through any campaign.
Using user-input, the program can create, save, load, and import characters. Save data for each cahracter is stored locally in a human-editable .ini file for easy access.

## Requirements
Windows, for now.
### If running from .py or .bat
Program will require Python 3 or higher (available from the [Python site](https://www.python.org/downloads/) or the Microsoft Store).
Also you will need to install PySimpleGUI, which can be done using the Pip installer in the command prompt or PowerShell.
> pip install PySimpleGUI
### If running from .exe
Only Windows is needed.

## Use
Upon first use, you will need to create (or import a character). The program will prompt the user for basic character stats (e.g. Name, Class, Ability Scores, etc.).
#### Note:
When entering proficiencies, the program expects a comma seperated list- i.e. "Wisdom, Charisma, Athletics, Intimidation".
Other items such as Feats/Actions/Spells, etc. can be added/removed in the "Stats" drop down menu.
