import PySimpleGUI as sg
import character_tools
import logging
import sys
import images

sg.theme('DarkGrey')

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def display_lang(ch):
    logging.info('Displaying Languages...')
    layout = [[sg.Text(ch.name + '\'s Tongues',font='Any 20')]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for item in ch.languages:
        if index%2 == 0:
            col1 += [[sg.Text('• ' + item)]]
        else:
            col2 += [[sg.Text('• ' + item)]]
        index += 1
    layout += [[sg.Column(col1),sg.Column(col2)],
                [sg.Button('Add Language...'), sg.Button('Remove Language...'), sg.Button('Back')]]
    window = sg.Window('Languages', layout, icon = images.dragon)
    while True:
        event, values = window.read()
        if event == None or event == 'Back':
            break
        if event == 'Add Language...':
            add_lang(ch)
            window.close()
            display_lang(ch)
        if event == 'Remove Language...':
            remove_lang(ch)
            window.close()
            display_lang(ch)
    window.close()

def remove_lang(ch):
    remove_layout = [[]]
    col1 = [[]]
    col2 = [[]]
    index = 0
    for item in ch.languages:
        if index%2 == 0:
            col1 += [[sg.Button(item)]]
        else:
            col2 += [[sg.Button(item)]]
        index += 1
    remove_layout = [[sg.Text('Choose Language to Remove')],
                    [sg.Column(col1), sg.Column(col2)],
                    [sg.Button('Back')]]
    remove_window = sg.Window('Remove Language', remove_layout, icon = images.dragon)
    while True:
        event, values = remove_window.read()
        if event == None or event == 'Back':
            break
        if event != None:
            ch.languages.remove(event)
            logging.info(event + ' removed from language list!')
            sg.Popup(event + ' removed!', icon = images.dragon)
            remove_window.close()
            remove_lang(ch)
    remove_window.close()

def add_lang(ch):
    ch.languages.append(sg.popup_get_text('Enter Language: ', icon = images.dragon))
