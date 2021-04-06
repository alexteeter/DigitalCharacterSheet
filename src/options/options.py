import Character as dnd
import PySimpleGUI as sg
import logging
import sys
import images
import configparser

class Options:
    def __init__(self):
        self.config = configparser.ConfigParser()
        try:
            self.load_options()
        except:
            logging.error('Failed to load preferences!')
            self.mod_size = 'Big'
            self.theme = 'DarkGrey'
            self.save_options()
        sg.theme(self.theme)
    
    def get_options_file(self):
        filename = str(dnd.path) + '\preferences.ini'
        return filename

    def save_options(self):
        self.config['options'] = {'mod_size':self.mod_size,
                                'theme':self.theme}
        filename = self.get_options_file()
        with open(filename, 'w') as configfile:
                self.config.write(configfile)
        logging.info('Options Saved')
        
    def load_options(self):
        self.config.read(self.get_options_file())
        self.mod_size = self.config['options']['mod_size']
        self.theme = self.config['options']['theme']
            
    def change_options(self):
        col1 = [[sg.T('Mod Size')],
                [sg.T('Theme')]
                ]
        col2 = [[sg.Combo(values = ['Big', 'Small'], default_value = self.mod_size, key = 'mod_size')],
                [sg.Combo(values = sg.theme_list(), default_value = self.theme, key = 'theme')]
                ]
        layout = [[sg.Column(col1, element_justification = 'l'), sg.Column(col2, element_justification = 'l')],
                    [sg.Button('Save')]
                    ]
        window = sg.Window('Options', layout, grab_anywhere=True, resizable=True, icon = images.dragon)
        while True:
            event, values = window.read()
            if event is None:
                break
            if event == 'Save':
                self.mod_size = values['mod_size']
                self.theme = values['theme']
                sg.theme(self.theme)
                self.save_options()
                sg.Popup('Options Saved', icon = images.dragon)
                break
        window.close()