import PySimpleGUI as sg
import character_tools
import logging
import sys
import images

sg.theme('DarkGrey')

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def display_equipment(ch):
    logging.info('Displaying equipment...')
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
            logging.info(event + ' removed from equipment list!')
            sg.Popup(event + ' removed!', icon = images.dragon)
            remove_window.close()
            remove_item(ch)
    remove_window.close()

