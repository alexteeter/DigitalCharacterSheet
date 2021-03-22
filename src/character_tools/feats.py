import PySimpleGUI as sg
import character_tools
import logging
import sys
import images

sg.theme('DarkGrey')

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def display_feats(ch):
    logging.info('Displaying Feats...')
    layout = [[sg.Text('Feats', font='Any 20')]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for feat in ch.feats:
        if index%2 == 0:
            col1 += [[sg.Frame(feat['name'], [[sg.Multiline(feat['description'])], [sg.Button('Edit', key = feat['name'])]])]]
        else:
            col2 += [[sg.Frame(feat['name'], [[sg.Multiline(feat['description'])], [sg.Button('Edit', key = feat['name'])]])]]
        index += 1
    layout += [[sg.Column(col1), sg.Column(col2)],
                [sg.Button('Add Feat...'), sg.Button('Remove Feat...')]]
    window = sg.Window('Feats',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            break
        elif event == 'Add Feat...':
            add_feat(ch)
            window.close()
            display_feats(ch)
        elif event == 'Remove Feat...':
            remove_feat(ch)
            window.close()
            display_feats(ch)
        elif event != None:
            feat = next(feat for feat in ch.feats if feat['name'] == event)
            character_tools.edit_item(feat)
            window.close()
            display_feats(ch)
        window.close()

def add_feat(ch): 
    logging.info('Adding Feat...')
    name = sg.popup_get_text('Enter Name:', icon = images.dragon)
    if name is None or name == '':
        logging.info('Cancelling Add Feat')
        return
    try:
        if next(feat for feat in ch.feats if feat['name'] == name):
            sg.PopupError('Feat already exists! Please use a different name.')
            logging.error('Feat ' + name + 'already exists! Cancelling Add Action')
            return
    except:
        pass
    descript = sg.popup_get_text('Enter Description:', icon = images.dragon)
    if descript is None:
        logging.info('Cancelling Add Feat')
        return
    ch.add_feat(ch.Feat(name, description = descript))
    logging.info(name + ' added!')

def remove_feat(ch):
    logging.info('Removing Feat...')
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
            logging.info(event + ' removed!')
            sg.Popup(event + ' removed!', icon = images.dragon)
            remove_window.close()
            remove_feat(ch)
    remove_window.close()
