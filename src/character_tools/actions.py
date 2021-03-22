import PySimpleGUI as sg
import character_tools
import logging
import sys
import images

sg.theme('DarkGrey')

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def display_actions(ch):
    logging.info('Displaying actions...')
    layout = [[sg.Text('Actions', font='Any 20')]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for action in ch.actions:
        if index%2 == 0:
            col1 += [[sg.Frame(action['name'], [[sg.Multiline(action['description'])], [sg.Button('Edit', key = action['name'])]])]]
        else:
            col2 += [[sg.Frame(action['name'], [[sg.Multiline(action['description'])], [sg.Button('Edit', key = action['name'])]])]]
        index += 1
    layout += [[sg.Column(col1), sg.Column(col2)],
                [sg.Button('Add Action...'), sg.Button('Remove Action...')]]
    window = sg.Window('Actions',layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            break
        elif event == 'Add Action...':
            add_action(ch)
            window.close()
            display_actions(ch)
        elif event == 'Remove Action...':
            remove_action(ch)
            window.close()
            display_actions(ch)
        elif event != None:
            action = next(action for action in ch.actions if action['name'] == event)
            character_tools.edit_item(action)
            window.close()
            display_actions(ch)
        window.close()

def add_action(ch): 
    logging.info('Adding action...')
    name = sg.popup_get_text('Enter Name:', icon = images.dragon)
    if name is None or name == '':
        logging.info('Cancelling Add Action')
        return
    try:
        if next(action for action in ch.actions if action['name'] == name):
            sg.PopupError('Action already exists! Please use a different name.')
            logging.error('Action name already exists! Cancelling Add Action')
            return
    except:
        pass
    descript = sg.popup_get_text('Enter Description:', icon = images.dragon)
    if descript is None:
        logging.info('Cancelling Add Action')
        return
    ch.add_action(ch.Action(name, description = descript))
    logging.info('Action added!')

def remove_action(ch):
    logging.info('Removing Action...')
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
            logging.info(event + 'removed!')
            sg.Popup(event + ' removed!', icon = images.dragon)
            remove_window.close()
            remove_action(ch)
    remove_window.close()
