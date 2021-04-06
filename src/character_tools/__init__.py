import Character
import PySimpleGUI as sg
import logging
import sys
import images
from character_tools import feats
from character_tools import actions
from character_tools import spells
from character_tools import stats
from character_tools import languages
from character_tools import pool
from character_tools import weapons
from character_tools import equipment
from character_tools import hit_boxes

def edit_item(item):
    layout = [[]]
    col1 = [[sg.T('Name')],
            [sg.T('Description')]
            ]
    col2 = [[sg.Input(default_text=item['name'], key = '-name-')],
            [sg.Multiline(default_text=item['description'], key = '-description-')]
            ]
    layout = [[sg.Column(col1, element_justification='l'), sg.Column(col2, element_justification='l')],
                [sg.Button('Save'), sg.Button('Back')]
                ]
    window = sg.Window('Edit Item', layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            window.close()
            logging.info('Item Edit cancelled')
            return
        if event == 'Save':
            break
    item['name'] = values['-name-']
    item['description'] = values['-description-']
    logging.info('Item edited!')
    window.close()