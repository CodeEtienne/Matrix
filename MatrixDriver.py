"""
Code for MAX7219 from Maxim
Converted from this code: http://playground.arduino.cc/LEDMatrix/Max7219

Python code from Sawyer McLane:
https://github.com/samclane/DiscordMatrix/blob/master/led_matrix.py
"""

from time import sleep
from pyfirmata import ArduinoMega

HIGH = 1
LOW = 0

max7219_reg_noop = 0x00
max7219_reg_digit0 = 0x01
max7219_reg_digit1 = 0x02
max7219_reg_digit2 = 0x03
max7219_reg_digit3 = 0x04
max7219_reg_digit4 = 0x05
max7219_reg_digit5 = 0x06
max7219_reg_digit6 = 0x07
max7219_reg_digit7 = 0x08
max7219_reg_decodeMode = 0x09
max7219_reg_intensity = 0x0a
max7219_reg_scanLimit = 0x0b
max7219_reg_shutdown = 0x0c
max7219_reg_displayTest = 0x0f


class LedMatrix:
    def __init__(self, board, dataIn, load, clock, maxInUse=1):
        self._board = board
        self.pins = dict()
        self.pins['dataIn'] = dataIn
        self.pins['load'] = load
        self.pins['clock'] = clock
        self.maxInUse = maxInUse

    def _digitalWrite(self, pin, val):
        self._board.digital[pin].write(val)

    def _putByte(self, data):
        for i in range(8, 0, -1):
            mask = 0x01 << (i - 1)
            self._digitalWrite(self.pins["clock"], LOW)
            if data & mask:
                self._digitalWrite(self.pins["dataIn"], HIGH)
            else:
                self._digitalWrite(self.pins["dataIn"], LOW)
            self._digitalWrite(self.pins["clock"], HIGH)

    def maxSingle(self, reg, col):
        self._digitalWrite(self.pins["load"], LOW)
        self._putByte(reg)
        self._putByte(col)
        self._digitalWrite(self.pins["load"], LOW)
        self._digitalWrite(self.pins["load"], HIGH)

    def maxAll(self, reg, col):
        self._digitalWrite(self.pins["load"], LOW)
        for _ in range(0, self.maxInUse):
            self._putByte(reg)
            self._putByte(col)
        self._digitalWrite(self.pins["load"], LOW)
        self._digitalWrite(self.pins["load"], HIGH)

    def maxOne(self, maxNr, reg, col):
        self._digitalWrite(self.pins["load"], LOW)

        for _ in range(self.maxInUse, maxNr, -1):
            self._putByte(0)
            self._putByte(0)

        self._putByte(reg)
        self._putByte(col)

        for _ in range(maxNr - 1, 0, -1):
            self._putByte(0)
            self._putByte(0)

        self._digitalWrite(self.pins["load"], LOW)
        self._digitalWrite(self.pins["load"], HIGH)

    def clear(self):
        for e in range(1, 9):
            self.maxAll(e, 0)

    def setup(self):
        print('Initializing _matrix...')
        self._digitalWrite(13, HIGH)
        self.maxAll(max7219_reg_scanLimit, 0x07)
        self.maxAll(max7219_reg_decodeMode, 0x00)
        self.maxAll(max7219_reg_shutdown, 0x01)
        self.maxAll(max7219_reg_displayTest, 0x00)
        self.clear()
        self.maxAll(max7219_reg_intensity, 0x01 & 0x0f)
        print('Done')

    def draw_matrix(self, point_matrix):
        for col, pointlist in enumerate(point_matrix):
            self.maxSingle(col + 1, int(''.join(str(int(v)) for v in pointlist), 2))



def loop(matrix):
    """ Verify that the functions work. """

    matrix.maxSingle(1, 1)
    matrix.maxSingle(2, 2)
    matrix.maxSingle(3, 4)
    matrix.maxSingle(4, 8)
    matrix.maxSingle(5, 16)
    matrix.maxSingle(6, 32)
    matrix.maxSingle(7, 64)
    matrix.maxSingle(8, 128)

    sleep(.25)
    matrix.clear()
    sleep(.25)

    matrix.maxAll(1, 1)
    matrix.maxAll(2, 3)
    matrix.maxAll(3, 7)
    matrix.maxAll(4, 15)
    matrix.maxAll(5, 31)
    matrix.maxAll(6, 63)
    matrix.maxAll(7, 127)
    matrix.maxAll(8, 255)

    sleep(.25)
    matrix.clear()
    sleep(.25)
    x = [[1, 0, 0, 0, 0, 0, 0, 1],
         [0, 1, 0, 0, 0, 0, 1, 0],
         [0, 0, 1, 0, 0, 1, 0, 0],
         [0, 0, 0, 1, 1, 0, 0, 0],
         [0, 0, 0, 1, 1, 0, 0, 0],
         [0, 0, 1, 0, 0, 1, 0, 0],
         [0, 1, 0, 0, 0, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 0, 1]]
    matrix.draw_matrix(x)
    sleep(.25)
    matrix.clear()
    sleep(.25)


if __name__ == "__main__":
    board = ArduinoMega('/dev/cu.usbmodem144101', baudrate=57600)
    matrix = LedMatrix(board, 12, 11, 10, 1)
    matrix.setup()
    while True:
        loop(matrix)