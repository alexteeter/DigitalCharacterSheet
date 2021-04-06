import PySimpleGUI as sg
import character_tools
import logging
import sys
import images

def display_spells(ch):
    logging.info('Displaying Spells...')
    layout = [[sg.Text('Spells', font='Any 20')]]
    col0 = [[sg.Frame('Slots', show_spell_slots(ch))],
            [sg.Frame('Spell Attack Mod',character_tools.hit_boxes.spell_attack(ch.get_spell_mod(), ch.prof))],
            [sg.Frame('Spell Save DC',character_tools.hit_boxes.spell_dc(ch.get_spell_mod(), ch.prof))]
            ]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for spell in ch.spells:
        if index%2 == 0:
            col1 += [[sg.Frame(spell['name'], [[sg.Text('Level ' + spell['level']), sg.Button('Cast...', key=spell['name'])],
                                                [sg.Multiline(spell['description'])]])]]
        else:
            col2 += [[sg.Frame(spell['name'], [[sg.Text('Level ' + spell['level']), sg.Button('Cast...')],
                                                [sg.Multiline(spell['description'])]])]]
        index += 1
    layout += [[sg.Column(col0), sg.Column(col1), sg.Column(col2)],
                [sg.Button('Add Spell...'), sg.Button('Remove Spell...'), sg.Button('Edit Spell...')]
                ]
    window = sg.Window('Spells',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            break
        elif event == 'Add Spell...':
            add_spell(ch)
            window.close()
            display_spells(ch)
        elif event == 'Remove Spell...':
            remove_spell(ch)
            window.close()
            display_spells(ch)
        elif event == 'Edit Spell...':
            edit_spell(get_spell_to_edit(ch))
            #except:
            #    logging.error('Failed to edit Spell!')
            window.close()
            display_spells(ch)
        elif event == 'Replenish':
            ch.replenish_spell_slots()
            window.close()
            display_spells(ch)
        elif event != None:
            cast_spell(ch)
            window.close()
            display_spells(ch)
        window.close()

def add_spell(ch):
    name = sg.popup_get_text('Enter Name:', icon = images.dragon)
    if name is None:
        return
    level = sg.popup_get_text('Spell Level:', icon = images.dragon)
    if level is None:
        return
    descript = sg.popup_get_text('Enter Description:', icon = images.dragon)
    ch.add_spell(ch.Spell(name, level, description = descript))
    logging.info(name + ' added to spell list!')

def remove_spell(ch):
    remove_layout = [[]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for spell in ch.spells:
        if index%2 == 0:
            col1 += [[sg.Button(spell['name'])]]
        else:
            col2 += [[sg.Button(spell['name'])]]
        index += 1
    remove_layout = [[sg.Text('Choose Spell to Remove')],
                    [sg.Column(col1), sg.Column(col2)],
                    [sg.Button('Back')]]
    remove_window = sg.Window('Remove Spell', remove_layout, icon = images.dragon)
    while True:
        event, values = remove_window.read()
        if event == None or event == 'Back':
            break
        if event != None:
            spell = next(spell for spell in ch.spells if spell['name'] == event)
            ch.del_spell(spell)
            logging.info(event + ' removed from spell list!')
            sg.Popup(event + ' removed!', icon = images.dragon)
            remove_window.close()
            remove_spell(ch)
    remove_window.close()

def get_spell_to_edit(ch):
    edit_layout = [[]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for spell in ch.spells:
        if index%2 == 0:
            col1 += [[sg.Button(spell['name'])]]
        else:
            col2 += [[sg.Button(spell['name'])]]
        index += 1
    edit_layout = [[sg.Text('Choose Spell to Edit')],
                    [sg.Column(col1), sg.Column(col2)],
                    [sg.Button('Back')]]
    edit_window = sg.Window('Edit Spell', edit_layout, icon = images.dragon)
    while True:
        event, values = edit_window.read()
        if event == None or event == 'Back':
            break
        if event != None:
            spell = next(spell for spell in ch.spells if spell['name'] == event)
            edit_window.close()
            return spell
    edit_window.close()
def edit_spell(spell):
    layout = [[]]
    col1 = [[sg.T('Name')],
            [sg.T('Level')],
            [sg.T('Description')]
            ]
    col2 = [[sg.Input(default_text=spell['name'], key = '-name-')],
            [sg.Input(default_text=spell['level'], key = '-level-')],
            [sg.Multiline(default_text=spell['description'], key = '-description-')]
            ]
    layout = [[sg.Column(col1, element_justification='l'), sg.Column(col2, element_justification='l')],
                [sg.Button('Save'), sg.Button('Back')]
                ]
    window = sg.Window('Edit Spell', layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            window.close()
            logging.info('Spell Edit cancelled')
            return
        if event == 'Save':
            break
    spell['name'] = values['-name-']
    spell['level'] = values['-level-']
    spell['description'] = values['-description-']
    logging.info('Spell edited!')
    window.close()
        
def cast_spell(ch):
    logging.info('Casting spell...')
    #try:
    col1 = [[]]
    col2 = [[]]
    col3 = [[]]
    for spell_slot in ch.spell_slots.keys():
        if spell_slot%2 == 0:
            col2 += [[sg.Button(spell_slot, key = spell_slot)]]
        elif spell_slot%3 == 0:
            col3 += [[sg.Button(spell_slot, key = spell_slot)]]
        else:
            col1 += [[sg.Button(spell_slot, key = spell_slot)]]
    layout = [[sg.Column(col1), sg.Column(col2), sg.Column(col3)],
                [sg.Button('Back')]]
    window = sg.Window('Level to cast at', layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            break
        elif event != None:
            if ch.current_spell_slots[event] == 0:
                sg.Popup('No Spell Slots left!', icon = images.dragon)
                break
            ch.use_spell_slot(event)
            logging.info('Used spell slot!')
            break
    window.close()
    #except:
    #    sg.Popup('Did not cast spell!')

def show_spell_slots(ch):   
    logging.info('Showing spell slots...')
    layout = [[]]
    i = 1
    for slot in ch.spell_slots:
        line = 'Level ' + str(i) + ' slots:\n'
        for x in range(0, ch.spell_slots.get(int(slot))):
            if x < ch.current_spell_slots[i]:
                line += '⚫'
                #line += [[sg.Button('', image_data=images.circle_full,
                #                button_color=(sg.theme_background_color(),sg.theme_background_color()),
                #                border_width=0)]]
            else:
                line += '⚪'
                #line += [[sg.Button('', image_data=images.circle_empty,
                #                button_color=(sg.theme_background_color(),sg.theme_background_color()),
                #                border_width=0)]]
        layout.append([sg.Text(line)])
        i += 1
    layout.append([sg.Button('Replenish')])
    return layout

def edit_spell_slots(ch):
    logging.info('Editing spell slots...')
    ch.set_spell_slot(int(sg.popup_get_text('Enter Slot Level', icon = images.dragon)), int(sg.popup_get_text('Enter Number of Total Slots', icon = images.dragon)))
