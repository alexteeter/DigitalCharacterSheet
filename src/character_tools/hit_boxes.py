import Character as dnd
import PySimpleGUI as sg
import character_tools
import logging
import sys
import images

def spell_attack(mod, prof):
    if mod == '':
        return [[sg.T('Please select a Spell Modifier!')]]
    else:
        return [[sg.T('Add ' + str(prof) + ' + ' + str(mod))]]

def spell_dc(mod, prof):
    if mod == '':
        return [[sg.T('Please select a Spell Modifier!')]]
    else:
        return [[sg.T('Add 8 + ' + str(prof) + ' + ' + str(mod))]]

def get_spell_mod():
    layout = [[sg.T('Select Spell Mod: '), sg.Combo(values = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'], default_value = 'INT', key = 'spell_mod')],
                [sg.B('Save'), sg.B('Cancel')]]
    window = sg.Window('Select Spell Mod', layout, grab_anywhere=True, resizable=True, icon = images.dragon)
    while True:
        event, values = window.read()
        if event is None or event == 'Cancel':
            window.close()
            return None
            break
        if event == 'Save':
            mod = values['spell_mod']
            window.close()
            return mod  
            break
    window.close()
def weapon_attack(mod, prof):
    return
    
def weapon_damage(prof):
    return