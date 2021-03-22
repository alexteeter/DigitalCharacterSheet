import PySimpleGUI as sg
import character_tools
import logging
import sys
import images

sg.theme('DarkGrey')

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def show_pools(ch):
    logging.info('Showing Pools...')
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
    logging.info('Adding Pool...')
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
            logging.info(name + ' added to Pools!')
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
            logging.info(pool.name + ' removed from Pools!')
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
            logging.info('Used ' + pool.name + '!')
            if pool.current == 0:
                sg.Popup(pool.name + ' is empty!', icon = images.dragon)
                logging.warning(pool.name + ' is empty!')
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
                logging.info(pool.name + ' is fully replenished!')
                sg.Popup(pool.name + ' is fully replenished!', icon = images.dragon)
        pool_window.close()
