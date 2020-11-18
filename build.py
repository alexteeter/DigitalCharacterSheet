import Character as dnd
import PySimpleGUI as sg
import sys
import os
import json
import images

sg.theme('DarkGrey')

def get_character():
    print('Getting Character...')
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
    print('Opening Character...')
    #character = dnd.load_character(sg.popup_get_file('Open Character'))
    try:
        character = dnd.load_character(get_save(get_savelist()))
    except:
        print('Failed to open characer!')
        sg.PopupError('Failed to Open Character!')
        return None
    print(character.name + ' loaded!')
    return character

def display_character(ch):
    print('Displaying Character...')
    #############################################
    menu_def = [['File', ['Open', 'Save', 'New', 'Delete...']],
                ['Edit', ['Change Stats']],
                ['Help']]
    hitDice_frame = [[sg.T(ch.currentHitDice, key='-currentHitDice-'), sg.T(' / ' + ch.hitDice)],
                    [sg.Button('Use Hit Die'), sg.Button('Replenish')]]
    name_frame = [[sg.T('Level: ' + ch.level,key='-level-'),sg.T(ch.charClass,key='-charClass-'),sg.T('Race: ' + ch.race,key='-race-')],
                [sg.Frame('Armor Class',[[sg.T(ch.armorClass, key='-armorClass-')]]),sg.Frame('Proficiency Bonus',[[sg.T(ch.prof,key='-prof-')]]),sg.Frame('HP',[[sg.T('0' + ch.hpCurrent, key='-hpCurrent-'), sg.T(' / '), sg.T(ch.hpMax, key='-hpMax-')],
                                                                                                                                [sg.B('Damage'),sg.B('Heal')]]),sg.Frame('Hit Dice',hitDice_frame)],
                ]

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
    print('Opening Window...')
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
                print('Damaged ' + ch.name)
                window['-hpCurrent-'].update(ch.hpCurrent)
                if ch.isDown:
                    sg.Popup(ch.name + ' is down!', icon = images.dragon)
                    print(ch.name + ' is Down!')
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
        if event == 'Actions...':
            display_actions(ch)
        if event == 'Spells...':
            display_spells(ch)
        if event == 'Feats...':
            display_feats(ch)
        if event == 'Equipment...':
            display_equipment(ch)
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
                changeStats(window, ch)
            except:
                sg.PopupError('Failed to Set Stat!', icon = images.dragon)
        if event == 'Pools...':
            show_pools(ch)
        if event == 'Add Weapon...':
            ch.add_weapon(add_weapon(ch))
            window.close()
            display_character(ch)
        if event == 'Remove Weapon...':
            del_weapon(ch)
            window.close()
            display_character(ch)
        if event != None and event != 'Save':
            print('Event selected')
            changed = True

def save_character(ch):
    print('Attempting to save Character...')
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
        print('Saving Character...')
        ch.save_character(filename)
        print(ch.name + ' Saved!')
        add_save(ch.name, filename)
        print('Save Added!')

def add_save(name, filename):
    print('Adding save to saves.json...')
    saves = str(dnd.path) + '/characters/saves.json'
    savelist = get_savelist()
    savelist[name] = filename
    with open(saves, 'w') as json_file:
        json.dump(savelist, json_file)
    
def get_savelist():
    print('Getting Save List from saves.json...')
    saves = str(dnd.path) + '/characters/saves.json'
    if os.path.isfile(saves):
        with open(saves) as j:
            return json.load(j)
    else:
        return {}

def get_save(savelist):
    print('Getting save from Save List...')
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
    print('Attempting to Creat Character...')
    col1 = [
            [sg.T('Enter Details and Stats')],
            [sg.T('Name: ')],
            [sg.T('Race: ')],
            [sg.T('Subrace: ')],
            [sg.T('Languages: ')],
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
            [sg.T('Hit Dice: ')],
            [sg.T('Proficiencies: ')],
            [sg.T('Gold: ')]
            ]
    col2 = [
            [sg.T('')],
            [sg.In(key='-name-')],
            [sg.In(key='-race-')],
            [sg.In(key='-subrace-')],
            [sg.In(key='-languages-')],
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
            [sg.In(key='-hitDice-')],
            [sg.In(key='-proficiencies-')],
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
    languages = values['-languages-']
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
    profRaw = values['-proficiencies-']
    proficiencies = profRaw.split(', ')
    [string.casefold() for string in proficiencies]
    gold = values['-gold-']
    #equipmentRaw = values['-equipment-']
    #equipment = equipmentRaw.split(', ')
    #weaponsRaw = values['-weapons-']
    #weapons = weaponsRaw.split(', ')
    try:
        print('Creating Character...')
        character = dnd.Character(level, proficiency, armorClass, strength, dex, constitution, intelligence, wisdom, charisma, hpMax, gold, name = name, race = race, subrace = subrace, languages = languages, charClass = charClass, hitDice = hitDice)
        character.proficiencies = proficiencies
        #character.equipment = equipment
        #character.weapons = weapons
        character.inspiration = False
        print('Character Created!')
    except:
        print('Character creation failed!')
        sg.PopupError('Failed to Create Character!', icon = images.dragon)
        return None
    return character

def del_prompt():
    print('Selecting who to delete...')
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
            print('Removing ' + name + ' from saves list...')
            savelist = get_savelist()
            savefile = savelist[name]
            del savelist[name]
            saves = str(dnd.path) + '/characters/saves.json'
            with open(saves, 'w') as json_file:
                json.dump(savelist, json_file)
            
            print('Deleting ' + name + '...')
            os.remove(savefile)
            print('Deleted ' + name + '!')
            sg.Popup('Deleted ' + name + '!', icon = images.dragon)
            break
        if event == None or event == 'No':
            break
    window.close()

def changeStats(window, ch):
    print('Changing stats...')
    col1 = [
            [sg.Button('Strength')],
            [sg.Button('Dexterity')],
            [sg.Button('Constitution')],
            [sg.Button('Intelligence')],
            [sg.Button('Wisdom')],
            [sg.Button('Charisma')],
            [sg.Button('Spell Slots')]
            ]
    
    col2 = [
            [sg.Button('Name')],
            [sg.Button('Class')],
            [sg.Button('Proficiency Bonus')],
            [sg.Button('Initiative Bonus')],
            [sg.Button('Max HP')],
            [sg.Button('Armor Class')],
            [sg.Button('Race?')]
            ]
    
    layout = [
            [sg.Column(col1), sg.Column(col2)]
            ]
    changeWindow = sg.Window('Change Stats/Info', layout, icon = images.dragon)
    while True:
        event, values = changeWindow.read()
        if event is None:
            break
        if event == 'Strength':
            try:
                ch.set_strength(sg.popup_get_text('Enter new Strength:', icon = images.dragon))
                window['-STR-'].update(ch.strength)
                window['-strMod-'].update(ch.get_str_mod())
                window['-ath-'].update('Athletics: '+str(ch.get_athletics()))
                window['-strSave-'].update(ch.get_str_save())
            except:
                sg.PopupError('Failed to set Strength!', icon = images.dragon)
        if event == 'Dexterity':
            try:
                ch.set_dex(sg.popup_get_text('Enter new Dexterity:', icon = images.dragon))
                window['-DEX-'].update(ch.dex)
                window['-dexMod-'].update(ch.get_dex_mod())
                window['-acro-'].update('Acrobatics: '+str(ch.get_acrobatics()))
                window['-sleight-'].update('Sleight of Hand: '+str(ch.get_sleight_of_hand()))
                window['-dexSave-'].update(ch.get_dex_save())
            except:
                sg.PopupError('Failed to set Dexterity!', icon = images.dragon)
        if event == 'Constitution':
            try:
                ch.set_con(sg.popup_get_text('Enter new Constitution:', icon = images.dragon))
                window['-CON-'].update(ch.con)
                window['-conMod-'].update(ch.get_con_mod())
                window['-conSave-'].update(ch.get_con_save())
            except:
                sg.PopupError('Failed to set Constitution!', icon = images.dragon)
        if event == 'Intelligence':
            try:
                ch.set_intelligence(sg.popup_get_text('Enter new Intelligence:', icon = images.dragon))
                window['-INT-'].update(ch.intelligence)
                window['-intMod-'].update(ch.get_int_mod())
                window['-arcana-'].update('Arcana: '+str(ch.get_arcana()))
                window['-history-'].update('History: '+str(ch.get_history()))
                window['-investigation-'].update('Investigation: '+str(ch.get_investigation()))
                window['-nature-'].update('Nature: '+str(ch.get_nature()))
                window['-religion-'].update('Religion: '+str(ch.get_religion()))
                window['-intSave-'].update(ch.get_int_save())
            except:
                sg.PopupError('Failed to set Intelligence!', icon = images.dragon)
        if event == 'Wisdom':
            try:
                ch.set_wisdom(sg.popup_get_text('Enter new Wisdom:', icon = images.dragon))
                window['-WIS-'].update(ch.wisdom)
                window['-wisMod-'].update(ch.get_wis_mod())
                window['-animal-'].update('Animal Handling: '+str(ch.get_animal_handling()))
                window['-insight-'].update('Insight: '+str(ch.get_insight()))
                window['-medicine-'].update('Medicine: '+str(ch.get_medicine()))
                window['-perception-'].update('Perception: '+str(ch.get_perception()))
                window['-survival-'].update('Survival: '+str(ch.get_survival()))
                window['-passive-'].update(ch.get_passive_perception())
                window['-wisSave-'].update(ch.get_wis_save())
            except:
                sg.PopupError('Failed to set Wisdom!', icon = images.dragon)
        if event == 'Charisma':
            try:
                ch.set_charisma(sg.popup_get_text('Enter new Charisma:', icon = images.dragon))
                window['-CHA-'].update(ch.charisma)
                window['-deception-'].update('Deception: '+str(ch.get_deception()))
                window['-intimidation-'].update('Intimidation: '+str(ch.get_intimidation()))
                window['-performance-'].update('Performance: '+str(ch.get_performance()))
                window['-persuasion-'].update('Persuasion: '+str(ch.get_persuasion()))
                window['-wisSave-'].update(ch.get_cha_save())
            except:
                sg.PopupError('Failed to set Charisma!', icon = images.dragon)
        ##
        if event == 'Name':
            try:
                ch.set_name(sg.popup_get_text('Enter new Name:', icon = images.dragon))
                window['-name-'].update(ch.name) 
            except:
                sg.PopupError('Failed to set Name!', icon = images.dragon)
        if event == 'Class':
            ch.set_charClass(sg.popup_get_text('Enter new Class', icon = images.dragon))
            window['-charClass-'].update(ch.charClass)
        if event == 'Initiative Bonus':
            try:
                ch.set_initiative_bonus(sg.popup_get_text('Enter New Initiative Bonus:', icon = images.dragon))
                window['-init-'].update(ch.get_initiative())
            except:
                sg.PopupError('Did not set stat!', icon = images.dragon)
        if event == 'Proficiency Bonus':
            ch.set_prof(sg.popup_get_text('Enter New Proficiency Bonus:', icon = images.dragon))
            window['-passive-'].update(ch.get_passive_perception())
            window['-prof-'].update(ch.prof)
            if 'strength' in ch.proficiencies:
                window['-strSave-'].update(ch.get_str_save())
            if 'dexterity' in ch.proficiencies:
                window['-dexSave-'].update(ch.get_dex_save())
                window['-dexMod-'].update(ch.get_dex_mod())
            if 'constitution' in ch.proficiencies:
                window['-conSave-'].update(ch.get_con_save())
                window['-conMod-'].update(ch.get_con_mod())
            if 'intelligence' in ch.proficiencies:
                window['-intSave-'].update(ch.get_int_save())
                window['-intSave-'].update(ch.get_int_save())
            if 'wisdom' in ch.proficiencies:
                window['-wisSave-'].update(ch.get_wis_save())
            if 'charisma' in ch.proficiencies:
                window['-chaSave-'].update(ch.get_cha_save())
            
            if 'acrobatics' in ch.proficiencies:
                window['-acro-'].update(ch.get_acrobatics())
            if 'animal handling' in ch.proficiencies:
                window['-animal-'].update(ch.get_animal_handling())
            if 'arcana' in ch.proficiencies:
                window['-arcnana-'].update(ch.get_arcana())
            if 'athletics' in ch.proficiencies:
                window['-athletics-'].update(ch.get_athletics())
            if 'deception' in ch.proficiencies:
                window['-deception-'].update('Deception: '+str(ch.get_deception()))
            if 'history' in ch.proficiencies:
                window['-history-'].update('History: '+str(ch.get_history()))
            if 'insight' in ch.proficiencies:
                window['-insight-'].update('Insight: '+str(ch.get_insight()))
            if 'intimidation' in ch.proficiencies:
                window['-intimidation-'].update('Intimidation: '+str(ch.get_intimidation()))
            if 'investigation' in ch.proficiencies:
                window['-investigation-'].update('Investigation: '+str(ch.get_investigation()))
            if 'medicine' in ch.proficiencies:
                window['-medicine-'].update('Medicine: '+str(ch.get_medicine()))
            if 'nature' in ch.proficiencies:
                window['-nature-'].update('Nature: '+str(ch.get_nature()))
            if 'perception' in ch.proficiencies:
                window['-perception-'].update('Perception: '+str(ch.get_perception()))
            if 'performance' in ch.proficiencies:
                window['-performance-'].update('Performance: '+str(ch.get_performance()))
            if 'persuasion' in ch.proficiencies:
                window['-persuasion-'].update('Persuasion: '+str(ch.get_persuasion()))
            if 'religion' in ch.proficiencies:
                window['-religion-'].update('Religion: '+str(ch.get_religion()))
            if 'sleight of hand' in ch.proficiencies:
                window['-sleight-'].update('Sleight of Hand: '+str(ch.get_sleight_of_hand()))
            if 'stealth' in ch.proficiencies:
                window['-stealth-'].update('Stealth: '+str(ch.get_stealth()))
            if 'survival' in ch.proficiencies:
                window['-survival-'].update('Survival: '+str(ch.get_survival()))
        if event == 'Max HP':
            ch.set_hpMax(sg.popup_get_text('Enter new Max HP:', icon = images.dragon))
            window['-hpMax-'].update(ch.hpMax)
        if event == 'Armor Class':
            ch.set_armorClass(sg.popup_get_text('Enter new Armor Class:', icon = images.dragon))
            window['-armorClass-'].update(ch.armorClass)
        if event == 'Race?':
            ch.set_race(sg.popup_get_text('An unusual request...', icon = images.dragon))
            window['-race-'].update('Dolezal')
        if event == 'Spell Slots':
            #try:
            edit_spell_slots(ch)
            #except:
            #    sg.PopupError('Failed to set Spell Slot!')
    changeWindow.close()
    
def display_actions(ch):
    print('Displaying actions...')
    layout = [[sg.Text('Actions', font='Any 20')]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for action in ch.actions:
        if index%2 == 0:
            col1 += [[sg.Frame(action['name'], [[sg.Multiline(action['description'])]])]]
        else:
            col2 += [[sg.Frame(action['name'], [[sg.Multiline(action['description'])]])]]
        index += 1
    layout += [[sg.Column(col1), sg.Column(col2)],
                [sg.Button('Add Action...'), sg.Button('Remove Action...')]]
    window = sg.Window('Actions',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            break
        if event == 'Add Action...':
            add_action(ch)
            window.close()
            display_actions(ch)
        if event == 'Remove Action...':
            remove_action(ch)
            window.close()
            display_actions(ch)
        window.close()

def add_action(ch): 
    print('Adding action...')
    name = sg.popup_get_text('Enter Name:', icon = images.dragon)
    descript = sg.popup_get_text('Enter Description:', icon = images.dragon)
    ch.add_action(ch.Action(name, description = descript))

def remove_action(ch):
    print('Removing Action...')
    remove_layout = [[]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for action in ch.actions:
        if index%2 == 0:
            col1 += [[sg.Button(action['name'])]]
        else:
            col2 += [[sg.Button(action['name'])]]
        index += 1
    remove_layout = [[sg.Text('Choose Item to Remove')],
                    [sg.Column(col1), sg.Column(col2)],
                    [sg.Button('Back')]]
    remove_window = sg.Window('Remove Action', remove_layout, icon = images.dragon)
    while True:
        event, values = remove_window.read()
        if event == None or event == 'Back':
            break
        if event != None:
            action = next(action for action in ch.actions if action['name'] == event)
            ch.del_action(action)
            print(event + 'removed!')
            sg.Popup(event + ' removed!', icon = images.dragon)
            remove_window.close()
            remove_action(ch)
    remove_window.close()

def display_feats(ch):
    print('Displaying Feats...')
    layout = [[sg.Text('Feats', font='Any 20')]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for feat in ch.feats:
        if index%2 == 0:
            col1 += [[sg.Frame(feat['name'], [[sg.Multiline(feat['description'])]])]]
        else:
            col2 += [[sg.Frame(feat['name'], [[sg.Multiline(feat['description'])]])]]
        index += 1
    layout += [[sg.Column(col1), sg.Column(col2)],
                [sg.Button('Add Feat...'), sg.Button('Remove Feat...')]]
    window = sg.Window('Feats',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            break
        if event == 'Add Feat...':
            
            add_feat(ch)
            window.close()
            display_feats(ch)
        if event == 'Remove Feat...':
            remove_feat(ch)
            window.close()
            display_feats(ch)
        window.close()
        
def add_feat(ch): 
    print('Adding Feat...')
    name = sg.popup_get_text('Enter Name:', icon = images.dragon)
    descript = sg.popup_get_text('Enter Description:', icon = images.dragon)
    ch.add_feat(ch.Feat(name, description = descript))
    print(name + ' added!')

def remove_feat(ch):
    print('Removing Feat...')
    remove_layout = [[]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for feat in ch.feats:
        if index%2 == 0:
            col1 += [[sg.Button(feat['name'])]]
        else:
            col2 += [[sg.Button(feat['name'])]]
        index += 1
    remove_layout = [[sg.Text('Choose Feat to Remove')],
                    [sg.Column(col1), sg.Column(col2)],
                    [sg.Button('Back')]]
    remove_window = sg.Window('Remove Feat', remove_layout, icon = images.dragon)
    while True:
        event, values = remove_window.read()
        if event == None or event == 'Back':
            break
        if event != None:
            feat = next(feat for feat in ch.feats if feat['name'] == event)
            ch.del_feat(feat)
            print(event + ' removed!')
            sg.Popup(event + ' removed!', icon = images.dragon)
            remove_window.close()
            remove_feat(ch)
    remove_window.close()

def display_spells(ch):
    print('Displaying Spells...')
    layout = [[sg.Text('Spells', font='Any 20')]]
    col0 = [[sg.Frame('Slots', show_spell_slots(ch))]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for spell in ch.spells:
        if index%2 == 0:
            col1 += [[sg.Frame(spell['name'], [[sg.Text('Level ' + spell['level']), sg.Button('Cast...', key=spell['name'])],
                                                [sg.Multiline(spell['description'])]])]]
        else:
            col2 += [[sg.Frame(spell['name'], [[sg.Text('Level ' + spell['level']), sg.Button('Cast...', key=spell['name'])],
                                                [sg.Multiline(spell['description'])]])]]
        index += 1
    layout += [[sg.Column(col0), sg.Column(col1), sg.Column(col2)],
                [sg.Button('Add Spell...'), sg.Button('Remove Spell...')]]
    window = sg.Window('Spells',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            break
        if event == 'Add Spell...':
            add_spell(ch)
            window.close()
            display_spells(ch)
        if event == 'Remove Spell...':
            remove_spell(ch)
            window.close()
            display_spells(ch)
        if event == 'Replenish':
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
    level = sg.popup_get_text('Spell Level:', icon = images.dragon)
    descript = sg.popup_get_text('Enter Description:', icon = images.dragon)
    ch.add_spell(ch.Spell(name, level, description = descript))
    print(name + ' added to spell list!')

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
            print(event + ' removed from spell list!')
            sg.Popup(event + ' removed!', icon = images.dragon)
            remove_window.close()
            remove_spell(ch)
    remove_window.close()

def cast_spell(ch):
    print('Casting spell...')
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
        if event != None:
            ch.use_spell_slot(event)
            print('Used spell slot!')
            break
    window.close()
    #except:
    #    sg.Popup('Did not cast spell!')

def show_spell_slots(ch):   
    print('Showing spell slots...')
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
    print('Editing spell slots...')
    ch.set_spell_slot(int(sg.popup_get_text('Enter Slot Level', icon = images.dragon)), int(sg.popup_get_text('Enter Number of Total Slots', icon = images.dragon)))

def display_equipment(ch):
    print('Displaying equipment...')
    layout = [[sg.Text(ch.name + '\'s Equipment',font='Any 20')]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for item in ch.equipment:
        if index%2 == 0:
            col1 += [[sg.Text('• ' + item)]]
        else:
            col2 += [[sg.Text('• ' + item)]]
        index += 1
    layout += [[sg.Column(col1),sg.Column(col2)],
                [sg.Button('Add Item...'), sg.Button('Remove Item...'), sg.Button('Back')]]
    equipment_window = sg.Window('Equipment', layout, icon = images.dragon)
    while True:
        event, values = equipment_window.read()
        if event == None or event == 'Back':
            break
        if event == 'Add Item...':
            ch.equipment.append(sg.popup_get_text('Enter Item: ', icon = images.dragon))
            equipment_window.close()
            display_equipment(ch)
        if event == 'Remove Item...':
            remove_item(ch)
            equipment_window.close()
            display_equipment(ch)
    equipment_window.close()

def remove_item(ch):
    remove_layout = [[]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for item in ch.equipment:
        if index%2 == 0:
            col1 += [[sg.Button(item)]]
        else:
            col2 += [[sg.Button(item)]]
        index += 1
    remove_layout = [[sg.Text('Choose Item to Remove')],
                    [sg.Column(col1), sg.Column(col2)],
                    [sg.Button('Back')]]
    remove_window = sg.Window('Remove Item', remove_layout, icon = images.dragon)
    while True:
        event, values = remove_window.read()
        if event == None or event == 'Back':
            break
        if event != None:
            ch.equipment.remove(event)
            print(event + ' removed from equipment list!')
            sg.Popup(event + ' removed!', icon = images.dragon)
            remove_window.close()
            remove_item(ch)
    remove_window.close()

def add_weapon(ch):
    name = sg.popup_get_text('Enter Name:', icon = images.dragon)
    damage= sg.popup_get_text('Enter Damage:', icon = images.dragon)
    descript = sg.popup_get_text('Enter Description:', icon = images.dragon)
    print('Adding ' + name + ' to Weapon list...')
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
            print(weapon['name'] + ' removed from Weapon list!')
            weapon_window.close()
            del_weapon(ch)
    weapon_window.close()

def show_pools(ch):
    print('Showing Pools...')
    pool_layout = []
    for pool in ch.pools:
        #try:
        name = pool.name
        max = pool.max
        current = pool.get_current()
        pool_layout += [[sg.Frame(name, [[sg.Text(str(current) + '/' + str(max))]])]]
        #except:
        #    pass
    pool_layout += [[sg.Button('Use...'), sg.Button('Replenish...'), sg.Button('Replenish All')],
                    [sg.Button('Add Pool...'), sg.Button('Remove Pool...'), sg.Button('Back')]]
    window = sg.Window('Pools', pool_layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event is None or event == 'Back':
            break
        if event == 'Use...':
            use_pool(ch)
        if event == 'Replenish...':
            replenish_pool(ch)
        if event == 'Replenish All':
            for pool in ch.pools:
                pool.current = pool.max
        if event == 'Add Pool...':
            ch.add_pool(add_pool(ch))
        if event == 'Remove Pool...':
            del_pool(ch)
        if event != None or 'Back':
            window.close()
            show_pools(ch)
    window.close()
        
 
def add_pool(ch):
    print('Adding Pool...')
    col1 = [
            [sg.Text('Name:')],
            [sg.Text('Max Amount:')]
            ]
    col2 = [
            [sg.In(key = '-name-')],
            [sg.In(key = '-max-')]
            ]
    
    layout = [
            [sg.Column(col1), sg.Column(col2)],
            [sg.Button('Save', bind_return_key = True)]
            ]
    window = sg.Window('New Pool', layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event is None:
            window.close()
            break
        if event == 'Save':
            name = values['-name-']
            max = values['-max-']
            window.close()
            print(name + ' added to Pools!')
            return ch.Pool(name, max)
            break

def del_pool(ch):
    col1 = [[]]
    col2 = [[]]
    i = 0
    for pool in ch.pools:
        if i%2 == 0:
            col1 += [[sg.Button(pool.name)]]
        else:
            col2 += [[sg.Button(pool.name)]]
        i += 1
    
    layout = [[sg.Column(col1), sg.Column(col2)],
                [sg.Button('Back')]]
    window = sg.Window('Remove Pool', layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            break
        else:
            pool = next(pool for pool in ch.pools if pool.name == event)
            ch.del_pool(pool)
            print(pool.name + ' removed from Pools!')
            window.close()
            del_pool(ch)
        window.close()

def use_pool(ch):
    col1 = [[]]
    col2 = [[]]
    i = 0
    for pool in ch.pools:
        if i%2 == 0:
            col1 += [[sg.Button(pool.name)]]
        else:
            col2 += [[sg.Button(pool.name)]]
        i += 1
    
    pool_layout = [[sg.Column(col1), sg.Column(col2)],
                [sg.Button('Back')]]
    pool_window = sg.Window('Use Pool', pool_layout, icon = images.dragon)
    while True:
        event, values = pool_window.read()
        if event == None or event == 'Back':
            break
        if event != None:
            pool = next(pool for pool in ch.pools if pool.name == event)
            pool.use(sg.popup_get_text('Enter Amount Used:', icon = images.dragon))
            print('Used ' + pool.name + '!')
            if pool.current == 0:
                sg.Popup(pool.name + ' is empty!', icon = images.dragon)
                print(pool.name + ' is empty!')
        pool_window.close()
def replenish_pool(ch):
    col1 = [[]]
    col2 = [[]]
    i = 0
    for pool in ch.pools:
        if i%2 == 0:
            col1 += [[sg.Button(pool.name)]]
        else:
            col2 += [[sg.Button(pool.name)]]
        i += 1
    
    pool_layout = [[sg.Column(col1), sg.Column(col2)],
                [sg.Button('Back')]]
    pool_window = sg.Window('Use Pool', pool_layout, icon = images.dragon)
    while True:
        event, values = pool_window.read()
        if event == None or event == 'Back':
            break
        if event != None:
            pool = next(pool for pool in ch.pools if pool.name == event)
            pool.replenish(sg.popup_get_text('Enter Amount Used:', icon = images.dragon))
            if pool.current == pool.max:
                print(pool.name + ' is fully replenished!')
                sg.Popup(pool.name + ' is fully replenished!', icon = images.dragon)
        pool_window.close()