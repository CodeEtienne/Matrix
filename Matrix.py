import PySimpleGUI as sg


# All the stuff inside your window.


def render_square(key, location):
    if (location[0] + location[1]) % 2:
        color = '#B58863'
    else:
        color = '#F0D9B5'
    return sg.RButton('', image_filename='led-off-small.png', size=(1, 1), button_color=('white', color), pad=(0, 0),
                      key=key)


layout = [[sg.T('   ')] + [sg.T('{}'.format(str(i)), pad=(8, 0), font='Any 13') for i in range(8)]]

for i in range(8):
    row = [sg.T(str(i) + '   ', font='Any 13')]
    for j in range(8):
        row.append(render_square(key=(i, j), location=(i, j)))
    layout.append(row)
# Create the Window
window = sg.Window('Matrix 0.1', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    if event == 'Reset':
        window.FindElement('1-1').Update(False)

window.close()
