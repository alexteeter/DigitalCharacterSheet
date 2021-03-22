import PySimpleGUI as sg
import character_tools
import logging
import sys
import images

sg.theme('DarkGrey')

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def add_weapon(ch):
    name = sg.popup_get_text('Enter Name:', icon = images.dragon)
    damage= sg.popup_get_text('Enter Damage:', icon = images.dragon)
    descript = sg.popup_get_text('Enter Description:', icon = images.dragon)
    logging.info('Adding ' + name + ' to Weapon list...')
    return ch.Weapon(name, dmg = damage, description = descript)

def del_weapon(ch):
    col1 = [[]]
    col2 = [[]]
    i = 0
    for weapon in ch.weapons:
        if i%2 == 0:
            col1 += [[sg.Button(weapon['name'])]]
        else:
            col2 += [[sg.Button(weapon['name'])]]
        i += 1
    
    layout = [[sg.Column(col1), sg.Column(col2)],
                [sg.Button('Back')]]
    weapon_window = sg.Window('Remove Weapon', layout, icon = images.dragon)
    while True:
        event, values = weapon_window.read()
        if event == None or event == 'Back':
            break
        else:
            weapon = next(weapon for weapon in ch.weapons if weapon['name'] == event)
            ch.del_weapon(weapon)
            logging.info(weapon['name'] + ' removed from Weapon list!')
            weapon_window.close()
            del_weapon(ch)
    weapon_window.close()

