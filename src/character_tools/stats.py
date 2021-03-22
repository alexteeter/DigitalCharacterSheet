import PySimpleGUI as sg
import character_tools
import logging
import sys
import images

def change_stats(window, ch):
    logging.info('Changing stats...')
    col1 = [
            [sg.Button('Strength')],
            [sg.Button('Dexterity')],
            [sg.Button('Constitution')],
            [sg.Button('Intelligence')],
            [sg.Button('Wisdom')],
            [sg.Button('Charisma')],
            [sg.Button('Spell Slots')],
            [sg.Button('Level')],
            [sg.Button('Hit Dice')]
            ]
    
    col2 = [
            [sg.Button('Name')],
            [sg.Button('Class')],
            [sg.Button('Proficiency Bonus')],
            [sg.Button('Initiative Bonus')],
            [sg.Button('Max HP')],
            [sg.Button('Armor Class')],
            [sg.Button('Race?')],
            [sg.Button('Proficiencies')],
            [sg.Button('Hit Die')]
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
                window['-chaMod-'].update(ch.get_cha_mod())
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
            character_tools.spells.edit_spell_slots(ch)
            #except:
            #    sg.PopupError('Failed to set Spell Slot!')
        if event == 'Level':
            ch.set_level(sg.popup_get_text('Enter New Level:', icon = images.dragon))
            window['-level-'].update('Level: ' + ch.level)
        if event == 'Proficiencies':
            try:
                logging.info('Changing Proficiencies...')
                ch.proficiencies = set_proficiencies()
                logging.info('Proficiencies set!')
            except:
                logging.error('Failed to set Proficiencies!')
                sg.PopupError('Failed to set Proficiencies!')
            window['-passive-'].update(ch.get_passive_perception())
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
        if event == 'Hit Dice':
            ch.set_hitDice(sg.popup_get_text('Enter New Hit Dice:', icon = images.dragon))
            window['-hit_dice-'].update(' / ' + ch.hitDice)
        if event == 'Hit Die':
            logging.debug('Hit Die Button selected!')
            ch.set_hit_die(sg.popup_get_text('Enter Hit Die:', icon = images.dragon))
            window['-hit_die-'].update(ch.hit_die)
            logging.debug('Hit Die set to ' + ch.hit_die)
    changeWindow.close()
 
def set_proficiencies():
    logging.info('Getting Proficiencies...')
    prof = []
    col1 = [
            [sg.Checkbox('Strength', key='-str-')],
            [sg.Checkbox('Dexterity', key='-dex-')],
            [sg.Checkbox('Constitution', key='-con-')],
            [sg.Checkbox('Intelligence', key='-int-')],
            [sg.Checkbox('Wisdom', key='-wis-')],
            [sg.Checkbox('Charisma', key='-cha-')]
            ]
    col2 = [
            [sg.Checkbox('Acrobatics', key='-acro-')],
            [sg.Checkbox('Animal Handling', key='-animal-')],
            [sg.Checkbox('Arcana', key='-arca-')],
            [sg.Checkbox('Athletics', key='-ath-')],
            [sg.Checkbox('Deception', key='-dec-')],
            [sg.Checkbox('History', key='-hist-')],
            [sg.Checkbox('Insight', key='-ins-')],
            [sg.Checkbox('Intimidation', key='-intim-')],
            [sg.Checkbox('Investigation', key='-inv-')]
            ]
    col3 = [
            [sg.Checkbox('Medicine', key='-med-')],
            [sg.Checkbox('Nature', key='-nat-')],
            [sg.Checkbox('Perception', key='-per-')],
            [sg.Checkbox('Performance', key='-perf-')],
            [sg.Checkbox('Persuasion', key='-pers-')],
            [sg.Checkbox('Religion', key='-rel-')],
            [sg.Checkbox('Sleight of Hand', key='-soh-')],
            [sg.Checkbox('Stealth', key='-stealth-')],
            [sg.Checkbox('Survival', key='-surv-')]
            ]
    layout = [[sg.T('Select Proficiencies:')],
            [sg.Column(col1), sg.Column(col2, element_justification='l'), sg.Column(col3, element_justification='l')],
            [sg.Button('Save', bind_return_key=True)]]
    window = sg.Window('Digital Character Sheet 2020',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == 'Save':
            break
        if event is None:
            quit()
    window.close()
    #saving throws
    if values['-str-']:
        prof.append('strength')
    if values['-dex-']:
        prof.append('dexterity')
    if values['-con-']:
        prof.append('constitution')
    if values['-int-']:
        prof.append('intelligence')
    if values['-wis-']:
        prof.append('wisdom')
    if values['-cha-']:
        prof.append('charisma')
    #skill checks
    if values['-acro-']:
        prof.append('acrobatics')
    if values['-animal-']:
        prof.append('animal handling')
    if values['-arca-']:
        prof.append('arcana')
    if values['-ath-']:
        prof.append('athletics')
    if values['-dec-']:
        prof.append('deception')
    if values['-hist-']:
        prof.append('history')
    if values['-ins-']:
        prof.append('insight')
    if values['-intim-']:
        prof.append('intimidation')
    if values['-inv-']:
        prof.append('investigation')
    if values['-med-']:
        prof.append('medicine')
    if values['-nat-']:
        prof.append('nature')
    if values['-per-']:
        prof.append('perception')
    if values['-perf-']:
        prof.append('performance')
    if values['-pers-']:
        prof.append('persuasion')
    if values['-rel-']:
        prof.append('religion')
    if values['-soh-']:
        prof.append('sleight of hand')
    if values['-stealth-']:
        prof.append('stealth')
    if values['-surv-']:
        prof.append('survival')
    
    return prof
