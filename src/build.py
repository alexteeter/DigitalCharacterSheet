import Character as dnd
import PySimpleGUI as sg
import character_tools
from options import options
import sys
import os
import json
import images
import logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

opt = options.Options()

sg.theme(opt.theme)


def get_character():
    logging.info('Getting Character...')
    layout = [[sg.Text('Open a Saved Character or Create New',key='-DISPLAY-')],
            [sg.Button('Load Character'), sg.Button('New Character')]]
    window = sg.Window('Digital Character Sheet 2020', layout, icon = images.dragon)
    
    while True:
        event, values = window.read()
        if event is None:
            quit()
            break
        if event == 'Load Character':
            try:
                character = open_character()
                if character == None:
                    character = get_character()
                break
            except:
                pass
            #character = open_character()
            #if character != None:
            #    break

        if event == 'New Character':
            character =  create_character()
            break
    window.close()
    return character
    
def open_character():
    logging.info('Opening Character...')
    #character = dnd.load_character(sg.popup_get_file('Open Character'))
    try:
        character = dnd.load_character(get_save(get_savelist()))
    except:
        logging.error('Failed to open characer!')
        sg.PopupError('Failed to Open Character!')
        return None
    logging.info(character.name + ' loaded!')
    return character

def display_character(ch):
    logging.info('Displaying Character...')
    #############################################
    menu_def = [['File', ['Open', 'Save', 'New', 'Delete...']],
                ['Edit', ['Change Stats', 'Options']],
                ['Help']]
    hitDice_frame = [[sg.T(ch.currentHitDice, key='-currentHitDice-'), sg.T(' / ' + ch.hitDice, key = '-hit_dice-'), sg.T(ch.hit_die, key = '-hit_die-')],
                    [sg.Button('Use Hit Die'), sg.Button('Replenish')]]
    name_frame = [[sg.T('Level: ' + ch.level,key='-level-'),sg.T(ch.charClass,key='-charClass-'),sg.T('Race: ' + ch.race,key='-race-'), sg.Button('Languages...')],
                [sg.Frame('Armor Class',[[sg.T(ch.armorClass, key='-armorClass-')]]),sg.Frame('Proficiency Bonus',[[sg.T(ch.prof,key='-prof-')]]),sg.Frame('HP',[[sg.T('0' + ch.hpCurrent, key='-hpCurrent-'), sg.T(' / '), sg.T(ch.hpMax, key='-hpMax-')],
                                                                                                                                [sg.B('Damage'),sg.B('Heal')]]),sg.Frame('Hit Dice',hitDice_frame)],
                ]

    if opt.mod_size == 'Big':
        stat_frame = [[sg.Frame('Strength',[[sg.T(ch.get_str_mod(),font='Any 22',key='-strMod-')],
                    [sg.T(ch.strength,key='-STR-')]])],
                    [sg.Frame('Dexterity',[[sg.T(ch.get_dex_mod(),font='Any 22',key='-dexMod-')],
                    [sg.T(ch.dex,key='-DEX-')]])],
                    [sg.Frame('Constitution',[[sg.T(ch.get_con_mod(),font='Any 22',key='-conMod-')],
                    [sg.T(ch.con,key='-CON-')]])],
                    [sg.Frame('Intelligence',[[sg.T(ch.get_int_mod(),font='Any 22',key='-intMod-')],
                    [sg.T(ch.intelligence,key='-INT-')]])],
                    [sg.Frame('Wisdom',[[sg.T(ch.get_wis_mod(),font='Any 22',key='-wisMod-')],
                    [sg.T(ch.wisdom,key='-WIS-')]])],
                    [sg.Frame('Charisma',[[sg.T(ch.get_cha_mod(),font='Any 22',key='-chaMod-')],
                    [sg.T(ch.charisma,key='-CHA-')]])],
                    ]
    if opt.mod_size == 'Small':
        stat_frame = [[sg.Frame('Strength',[[sg.T(ch.strength,font='Any 22',key='-STR-')],
                    [sg.T(ch.get_str_mod(),key='-strMod-')]])],
                    [sg.Frame('Dexterity',[[sg.T(ch.dex,font='Any 22',key='-DEX-')],
                    [sg.T(ch.get_dex_mod(),key='-dexMod-')]])],
                    [sg.Frame('Constitution',[[sg.T(ch.con,font='Any 22',key='-CON-')],
                    [sg.T(ch.get_con_mod(),key='-conMod-')]])],
                    [sg.Frame('Intelligence',[[sg.T(ch.intelligence,font='Any 22',key='-INT-')],
                    [sg.T(ch.get_int_mod(),key='-intMod-')]])],
                    [sg.Frame('Wisdom',[[sg.T(ch.wisdom,font='Any 22',key='-WIS-')],
                    [sg.T(ch.get_wis_mod(),key='-wisMod-')]])],
                    [sg.Frame('Charisma',[[sg.T(ch.charisma,font='Any 22',key='-CHA-')],
                    [sg.T(ch.get_cha_mod(),key='-chaMod-')]])],
                    ]

    savingThrows_frame = [[sg.Frame('Strength',[[sg.T(ch.get_str_save(),key='-strSave-')]])],
                        [sg.Frame('Dexterity',[[sg.T(ch.get_dex_save(),key='-dexSave-')]])],
                        [sg.Frame('Constitution',[[sg.T(ch.get_con_save(),key='-conSave-')]])],
                        [sg.Frame('Intelligence',[[sg.T(ch.get_int_save(),key='-intSave-')]])],
                        [sg.Frame('Wisdom',[[sg.T(ch.get_wis_save(),key='-wisSave-')]])],
                        [sg.Frame('Charisma',[[sg.T(ch.get_cha_save(),key='-chaSave-')]])]
                        ]
    skills_frame = [
                    [sg.T('Acrobatics: '+str(ch.get_acrobatics()),key='-acro-')],
                    [sg.T('Animal Handling: '+str(ch.get_animal_handling()),key='-animal-')],
                    [sg.T('Arcana: '+str(ch.get_arcana()),key='-arcana-')],
                    [sg.T('Athletics: '+str(ch.get_athletics()),key='-ath-')],
                    [sg.T('Deception: '+str(ch.get_deception()),key='-deception-')],
                    [sg.T('History: '+str(ch.get_history()),key='-history-')],
                    [sg.T('Insight: '+str(ch.get_insight()),key='-insight-')],
                    [sg.T('Intimidation: '+str(ch.get_intimidation()),key='-intimidation-')],
                    [sg.T('Investigation: '+str(ch.get_investigation()),key='-investigation-')],
                    [sg.T('Medicine: '+str(ch.get_medicine()),key='-medicine-')],
                    [sg.T('Nature: '+str(ch.get_nature()),key='-nature-')],
                    [sg.T('Perception: '+str(ch.get_perception()),key='-perception-')],
                    [sg.T('Performance: '+str(ch.get_performance()),key='-performance-')],
                    [sg.T('Persuasion: '+str(ch.get_persuasion()),key='-persuasion-')],
                    [sg.T('Religion: '+str(ch.get_religion()),key='-religion-')],
                    [sg.T('Sleight of Hand: '+str(ch.get_sleight_of_hand()),key='-sleight-')],
                    [sg.T('Stealth: '+str(ch.get_stealth()),key='-stealth-')],
                    [sg.T('Survival: '+str(ch.get_survival()),key='-survival-')]
                    ]
    
    weapons_frame = []
    for weapon in ch.weapons:
        try:
            name = weapon['name']
            dmg = weapon['dmg']
            weapons_frame += [[sg.Frame(name,[[sg.T('Damage: ' + dmg)]])]]
        except:
            pass
    weapons_frame += [[sg.Button('Add Weapon...'), sg.Button('Remove Weapon...')]]
    
    equipment_frame = []
    
    spells_frame = []
    
    col1 = [[sg.Frame('',stat_frame)],
            [sg.Frame('Passive Perception',[[sg.T(ch.get_passive_perception(),key='-passive-')]])],
            ]
    col2 = [[sg.Frame('Is '+ch.name+' Down?',[[sg.T(ch.isDown, key='-isDown-')]])],
            [sg.Frame('Inspiration',[[sg.T(ch.inspiration, key='-insp-')],
                                    [sg.Button('Use'), sg.Button('Give')]])],
            [sg.Frame('Saving Throws',savingThrows_frame)],
            [sg.Frame('Gold',[[sg.T('000' + ch.gold, key='-GOLD-')],
                            [sg.Button('Spend'), sg.Button('Add')]])]
            ]
    col3 = [
            [sg.Frame('Initiative',[[sg.Text(ch.get_initiative(), key = '-init-')]])],
            [sg.Frame('Skills',skills_frame)]
            ]
    col4 = [
            [sg.Frame('Weapons',weapons_frame)],
            [sg.Button('Spells...'), sg.Button('Actions...'), sg.Button('Feats...')],
            [sg.Button('Equipment...'), sg.Button('Pools...')]
            ]
    layout = [[sg.Menu(menu_def)],
            [sg.Frame(ch.name, name_frame,key='-name-', font=('Any', 30, 'italic'))],
            [sg.Column(col1, justification='left'), sg.Column(col2, justification='left'), sg.Column(col3, justification='left'), sg.Column(col4)]
            ]
    logging.info('Opening Window...')
    window = sg.Window('Digital Character Sheet 2020', layout, grab_anywhere=True, resizable=True, icon = images.dragon)
    changed = False
    while True:
        event, values = window.read()
        window['-GOLD-'].update(ch.gold)
        if event is (None):
            if changed:
                saveLayout = [[sg.T('Would you like to save the current character?')],
                            [sg.Button('Save'), sg.Button('Nah')]]
                saveWindow = sg.Window('Save Character?', saveLayout, icon = images.dragon)
                while True:
                    event, values = saveWindow.read()
                    if event is None:
                        break
                    if event == 'Save':
                        save_character(ch)
                        break
                    if event == 'Nah':
                        break
            quit()
            break
        if event == 'Damage':
            try:
                ch.damage(sg.popup_get_text('Enter damage: ', icon = images.dragon))
                logging.info('Damaged ' + ch.name)
                window['-hpCurrent-'].update(ch.hpCurrent)
                if ch.isDown:
                    sg.Popup(ch.name + ' is down!', icon = images.dragon)
                    logging.info(ch.name + ' is Down!')
                    window['-isDown-'].update(ch.isDown)
            except:
                pass
        if event == 'Use Hit Die':
            if ch.currentHitDice != 0:
                ch.set_current_hit_dice(int(ch.currentHitDice) - 1)
            if ch.currentHitDice == 0:
                sg.Popup('Out of Hit Dice!', icon = images.dragon)
            window['-currentHitDice-'].update(ch.currentHitDice)
        if event == 'Replenish':
            if int(ch.currentHitDice) < int(ch.hitDice):
                ch.set_current_hit_dice(int(ch.currentHitDice) + 1)
                window['-currentHitDice-'].update(ch.currentHitDice)
            if int(ch.currentHitDice) >= int(ch.hitDice):
                ch.currentHitDice = ch.hitDice
                sg.Popup('Hit Dice Full!', icon = images.dragon)
        if event == 'Heal':
            try:
                ch.heal(sg.popup_get_text('Amount healed: ', icon = images.dragon))
                window['-hpCurrent-'].update(ch.hpCurrent)
                window['-isDown-'].update(ch.isDown)
            except:
                pass
        if event == 'Spend':
            try:
                ch.spend_gold(sg.popup_get_text('Enter amount spent: ', icon = images.dragon))
                window['-GOLD-'].update(ch.gold)
            except:
                pass
        if event == 'Add':
            try:
                ch.add_gold(sg.popup_get_text('Enter amount to add: ', icon = images.dragon))
                window['-GOLD-'].update(ch.gold)
            except:
                pass
        if event == 'Use':
            ch.inspiration = False
            window['-insp-'].update(ch.inspiration)
        if event == 'Give':
            ch.inspiration = True
            window['-insp-'].update(ch.inspiration)
        ###
        if event == 'Languages...':
            character_tools.languages.display_lang(ch)
        if event == 'Actions...':
            character_tools.actions.display_actions(ch)
        if event == 'Spells...':
            character_tools.spells.display_spells(ch)
        if event == 'Feats...':
            character_tools.feats.display_feats(ch)
        if event == 'Equipment...':
            character_tools.equipment.display_equipment(ch)
        ###
        if event == 'Save':
            save_character(ch)
            changed = False
        if event == 'Open':
            openLayout = [[sg.T('Would you like to save the current character?')],
                    [sg.Button('Save'), sg.Button('Nah')]]
            openWindow = sg.Window('Save Character?', openLayout, icon = images.dragon)
            while True:
                event, values = openWindow.read()
                if event is None:
                    open = False
                    break
                if event == 'Save':
                    save_character(ch)
                    open = True
                    break
                if event == 'Nah':
                    open = True
                    break
            if open:
                try:
                    ch = open_character()
                    openWindow.close()
                    window.close()
                    display_character(ch)
                except:
                    pass
            else:
                openWindow.close()
        if event == 'New':
            openLayout = [[sg.T('Would you like to save the current character?')],
                    [sg.Button('Save'), sg.Button('Nah')]]
            openWindow = sg.Window('Save Character?', openLayout, icon = images.dragon)
            while True:
                event, values = openWindow.read()
                if event is None:
                    open = False
                    break
                if event == 'Save':
                    save_character(ch)
                    open = True
                    break
                if event == 'Nah':
                    open = True
                    break
            if open:
                try:
                    openWindow.close()
                    window.close()
                    ch = create_character()
                    display_character(ch)
                except:
                    pass
            else:
                openWindow.close()
        if event == 'Delete...':
            del_prompt()
        if event == 'Change Stats':
            try:
                character_tools.stats.change_stats(window, ch)
            except:
                sg.PopupError('Failed to Set Stat!', icon = images.dragon)
        if event == 'Options':
            opt.change_options()
            window.close()
            display_character(ch)
        ###
        if event == 'Pools...':
            character_tools.pool.show_pools(ch)
        if event == 'Add Weapon...':
            ch.add_weapon(character_tools.weapons.add_weapon(ch))
            window.close()
            display_character(ch)
        if event == 'Remove Weapon...':
            character_tools.weapons.del_weapon(ch)
            window.close()
            display_character(ch)
        if event != None and event != 'Save':
            logging.info('Event selected')
            changed = True

def save_character(ch):
    logging.info('Attempting to save Character...')
    overwrite = False
    write = False
    filepath = str(dnd.path) + '/characters/'
    filename = filepath + str(ch.name) + '.ini'
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    except OSError:
        sg.PopupError('Failed to make directory!', icon = images.dragon)
    try:
        with open(filename) as f:
            f.readline()
            overwrite = True
    except IOError:
        sg.Popup(str(ch.name)+' save file not found, creating new save.', icon = images.dragon)
        write = True
    if overwrite:
        layout = [[sg.Text('A Save File for ' + str(ch.name) + ' already exisits! \nOverwrite?')],
                    [sg.Button('Overwrite', bind_return_key=True), sg.Button('Cancel')]]
        window = sg.Window('Overwrite '+str(ch.name)+'?', layout, icon = images.dragon)
        while True:
            event, values = window.read()
            if event is None:
                break
            if event == 'Overwrite':
                write = True
                break
            if event == 'Cancel':
                break
        window.close() 
    if write:
        logging.info('Saving Character...')
        ch.save_character(filename)
        logging.info(ch.name + ' Saved!')
        add_save(ch.name, filename)
        logging.info('Save Added!')

def add_save(name, filename):
    logging.info('Adding save to saves.json...')
    saves = str(dnd.path) + '/characters/saves.json'
    savelist = get_savelist()
    savelist[name] = filename
    with open(saves, 'w') as json_file:
        json.dump(savelist, json_file)
    
def get_savelist():
    logging.info('Getting Save List from saves.json...')
    saves = str(dnd.path) + '/characters/saves.json'
    if os.path.isfile(saves):
        with open(saves) as j:
            return json.load(j)
    else:
        return {}

def get_save(savelist):
    logging.info('Getting save from Save List...')
    layout = [[sg.Text('Select Character:', font='Any 20')]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for save in savelist.keys():
        if index%2 == 0:
            col1 += [[sg.Button(save)]]
        else:
            col2 += [[sg.Button(save)]]
        index += 1
    layout += [[sg.Column(col1), sg.Column(col2)],
                [sg.Button('Import...')]]
    #if index == 0:
    #    sg.Popup('No Saves Found!')
    #    return None
    window = sg.Window('Open Character',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event is None:
            window.close()
            return None
        if event == 'Import...':
            window.close()
            return sg.popup_get_file('Open Character', icon = images.dragon)
        else:
            window.close()
            return savelist[event]
    
def create_character():
    logging.info('Attempting to Create Character...')
    col1 = [
            [sg.T('Enter Details and Stats')],
            [sg.T('Name: ')],
            [sg.T('Race: ')],
            [sg.T('Subrace: ')],
            [sg.T('Class: ')],
            [sg.T('Level: ')],
            [sg.T('Proficiency Bonus: ')],
            [sg.T('Armor Class: ')],
            [sg.T('Strength: ')],
            [sg.T('Dexterity: ')],
            [sg.T('Constitution: ')],
            [sg.T('Intelligence: ')],
            [sg.T('Wisdom: ')],
            [sg.T('Charisma: ')],
            [sg.T('Max HP: ')],
            [sg.T('Hit Die: ')],
            [sg.T('Hit Dice: ')],
            [sg.T('Gold: ')]
            ]
    col2 = [
            [sg.T('')],
            [sg.In(key='-name-')],
            [sg.In(key='-race-')],
            [sg.In(key='-subrace-')],
            [sg.In(key='-charClass-')],
            [sg.In(key='-level-')],
            [sg.In(key='-prof-')],
            [sg.In(key='-armorClass-')],
            [sg.In(key='-strength-')],
            [sg.In(key='-dex-')],
            [sg.In(key='-constitution-')],
            [sg.In(key='-intelligence-')],
            [sg.In(key='-wisdom-')],
            [sg.In(key='-charisma-')],
            [sg.In(key='-hpMax-')],
            [sg.In(key='-hit_die-')],
            [sg.In(key='-hitDice-')],
            [sg.In(key='-gold-')]
            ]
    layout = [[sg.Column(col1), sg.Column(col2, element_justification='r')],
             [sg.Button('Save', bind_return_key=True)]]
    window = sg.Window('Digital Character Sheet 2020',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == 'Save':
            break
        if event is None:
            quit()
    window.close()
    name = values['-name-']
    race = values['-race-']
    subrace = values['-subrace-']
    charClass = values['-charClass-']
    level = values['-level-']
    proficiency = values['-prof-']
    armorClass = values['-armorClass-']
    strength = values['-strength-']
    dex = values['-dex-']
    constitution = values['-constitution-']
    intelligence = values['-intelligence-']
    wisdom = values['-wisdom-']
    charisma = values['-charisma-']
    hpMax = values['-hpMax-']
    hitDice = values['-hitDice-']
    hit_die = values['-hit_die-']
    #profRaw = values['-proficiencies-']
    #proficiencies = profRaw.split(', ')
    #[string.casefold() for string in proficiencies]
    gold = values['-gold-']
    #equipmentRaw = values['-equipment-']
    #equipment = equipmentRaw.split(', ')
    #weaponsRaw = values['-weapons-']
    #weapons = weaponsRaw.split(', ')
    #Proficiencies Window
    proficiencies = character_tools.stats.set_proficiencies()
    #try:
    logging.info('Creating Character...')
    character = dnd.Character(level, proficiency, armorClass, strength, dex, constitution, intelligence, wisdom, charisma, hpMax, gold, name = name, race = race, subrace = subrace,charClass = charClass, hitDice = hitDice, hit_die = hit_die)
    #character.languages = languages
    character.proficiencies = proficiencies
    #character.equipment = equipment
    #character.weapons = weapons
    character.inspiration = False
    logging.info('Character Created!')
    #except:
    #    logging.error('Character creation failed!')
    #    sg.PopupError('Failed to Create Character!', icon = images.dragon)
    #    return None
    return character

def del_prompt():
    logging.info('Selecting who to delete...')
    layout = [[sg.Text('Delete Character:', font = 'Any 20')]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    savelist = get_savelist()
    for save in savelist.keys():
        if index%2 == 0:
            col1 += [[sg.Button(save)]]
        else:
            col2 += [[sg.Button(save)]]
        index += 1
    layout += [[sg.Column(col1), sg.Column(col2)]]
    window = sg.Window('Open Character',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event is None:
            break
        else:
            del_character(event)
            break
    window.close()
    
def del_character(name):
    layout = [[sg.Text('Are you sure you want to delete ' + name + '?')],
                [sg.Button('Yes'), sg.Button('No')]]
    window = sg.Window('Delete Character', layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == 'Yes':
            logging.info('Removing ' + name + ' from saves list...')
            savelist = get_savelist()
            savefile = savelist[name]
            del savelist[name]
            saves = str(dnd.path) + '/characters/saves.json'
            with open(saves, 'w') as json_file:
                json.dump(savelist, json_file)
            
            logging.info('Deleting ' + name + '...')
            os.remove(savefile)
            logging.info('Deleted ' + name + '!')
            sg.Popup('Deleted ' + name + '!', icon = images.dragon)
            break
        if event == None or event == 'No':
            break
    window.close()
