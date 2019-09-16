import PySimpleGUI as sg
from MatrixDriver import LedMatrix
from pyfirmata import ArduinoMega

PORT = '/dev/cu.usbmodem144101'
RATE = 57600
PIN_DATA_IN = 12
PIN_LOAD = 11
PIN_CLOCK = 10

LED_ON = 'Images/red-led-on.png'
LED_OFF = 'Images/red-led-off.png'

ON = 1
OFF = 0


class Matrix(LedMatrix):

    def __init__(self):
        self.logicMatrix = []
        self.initialize_matrix()
        self.board = ArduinoMega(PORT, baudrate=RATE)
        super().__init__(self.board, PIN_DATA_IN, PIN_LOAD, PIN_CLOCK)
        self.clear()
        self.layout = []
        self.build_layout()

    def initialize_matrix(self):
        self.logicMatrix = [[0 for i in range(0, 8)] for j in range(0, 8)]

    def reset_matrix(self, window):
        self.initialize_matrix()
        for i in range(0, 8):
            for j in range(0, 8):
                button = window.FindElement(key=(i, j))
                button.Update(image_filename=LED_OFF)
        self.clear()

    # TODO: Redesign the GUI to include actual columns
    def build_layout(self, rows=8, cols=8):
        self.layout = [[sg.T('   ')] + [sg.T('{}'.format(str(i)), pad=(13, 0), font='Any 13') for i in range(8)]]
        for i in range(rows):
            gui_row = [sg.T(str(i) + '   ', font='Any 13')]
            for j in range(cols):
                gui_row.append(self.render_led_button((i, j)))
            gui_row.append(sg.Button(str(i), key=(i, 8), pad=(5, 5), size=(5, 3)))
            self.layout.append(gui_row)
        last_row = [sg.Button(str(i), key=(8, i), pad=(5, 5), size=(5, 3)) for i in range(0, 8)]
        last_row.insert(0, sg.T('   '))
        self.layout.append(last_row)
        command_row = [sg.T('   ')] + [sg.Button('Clear', size=(20, 3), pad=(5, 3))]
        self.layout.append(command_row)

    @staticmethod
    def render_led_button(key, state=OFF):
        if state == ON:
            image = LED_ON
        else:
            image = LED_OFF
        return sg.RButton('', image_filename=image, size=(1, 1), pad=(5, 5), key=key)

    def set_led(self, row, col, window, state):
        button = window.FindElement(key=(row, col))
        if state == ON:
            self.logicMatrix[row][col] = ON
            button.Update(image_filename=LED_ON)
            self.draw_matrix(self.logicMatrix)
        else:
            self.logicMatrix[row][col] = OFF
            button.Update(image_filename=LED_OFF)
            self.draw_matrix(self.logicMatrix)

    def set_row(self, row, window, state):
        if state == ON:
            image = LED_ON
        else:
            image = LED_OFF
        for i in range(0, 8):
            self.logicMatrix[row][i] = state
            button = window.FindElement(key=(row, i))
            button.Update(image_filename=image)
        self.draw_matrix(self.logicMatrix)

    def set_col(self, col, window, state):
        if state == ON:
            image = LED_ON
        else:
            image = LED_OFF
        for i in range(0, 8):
            self.logicMatrix[i][col] = state
            button = window.FindElement(key=(i, col))
            button.Update(image_filename=image)
        self.draw_matrix(self.logicMatrix)

    def change_col(self, col, window):
        if self.logicMatrix[0][col] == OFF:
            self.set_col(col, window, ON)
        else:
            self.set_col(col, window, OFF)

    def change_row(self, row, window):
        if self.logicMatrix[row][0] == OFF:
            self.set_row(row, window, ON)
        else:
            self.set_row(row, window, OFF)

    def change_led(self, row, col, window):
        if self.logicMatrix[row][col] == OFF:
            self.set_row(row, col, window, ON)
        else:
            self.set_row(row, col, window, OFF)


def gui_loop(window, matrix):
    while True:
        event, values = window.read()
        if event == 'Clear':
            matrix.reset_matrix(window)
        if event in (None, 'Cancel'):  # if user closes window or clicks cancel
            break
        if type(event) is tuple:
            row, col = event
            if col == 8:
                matrix.change_row(row, window)
            elif row == 8:
                matrix.change_col(col, window)
            else:
                if matrix.logicMatrix[row][col] == 0:
                    matrix.set_led(row, col, window, ON)
                else:
                    matrix.set_led(row, col, window, OFF)
    window.close()


if __name__ == '__main__':
    myMatrix = Matrix()
    matrix_window = sg.Window('Matrix 0.1', myMatrix.layout)
    gui_loop(matrix_window, myMatrix)
