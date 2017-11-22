# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import datetime

from neopixel import *

import argparse
import signal
import sys
def signal_handler(signal, frame):
    colorWipe(strip, Color(0,0,0))
    sys.exit(0)

def opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 256      # Number of LED pixels: 8x32
LED_PIN        = 21      # GPIO pin connected to the pixels (18 uses PWM!, 21 uses PCM).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 10      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# LED strip position in matrix form
# [x][y] => x forms the lines beginning with 0 at the top
#        => y forms the columns beggining with 0 at the left
matrix_pos = [
    [255, 254, 253, 252, 251, 250, 249, 248, 191, 190, 189, 188, 187, 186, 185, 184, 127, 126, 125, 124, 123, 122, 121, 120, 63, 62, 61, 60, 59, 58, 57, 56],
    [247, 246, 245, 244, 243, 242, 241, 240, 183, 182, 181, 180, 179, 178, 177, 176, 119, 118, 117, 116, 115, 114, 113, 112, 55, 54, 53, 52, 51, 50, 49, 48],
    [239, 238, 237, 236, 235, 234, 233, 232, 175, 174, 173, 172, 171, 170, 169, 168, 111, 110, 109, 108, 107, 106, 105, 104, 47, 46, 45, 44, 43, 42, 41, 40],
    [231, 230, 229, 228, 227, 226, 225, 224, 167, 166, 165, 164, 163, 162, 161, 160, 103, 102, 101, 100, 99,  98,  97,  96,  39, 38, 37, 36, 35, 34, 33, 32],
    [223, 222, 221, 220, 219, 218, 217, 216, 159, 158, 157, 156, 155, 154, 153, 152, 95,  94,  93,  92,  91,  90,  89,  88,  31, 30, 29, 28, 27, 26, 25, 24],
    [215, 214, 213, 212, 211, 210, 209, 208, 151, 150, 149, 148, 147, 146, 145, 144, 87,  86,  85,  84,  83,  82,  81,  80,  23, 22, 21, 20, 19, 18, 17, 16],
    [207, 206, 205, 204, 203, 202, 201, 200, 143, 142, 141, 140, 139, 138, 137, 136, 79,  78,  77,  76,  75,  74,  73,  72,  15, 14, 13, 12, 11, 10, 9,  8],
    [199, 198, 197, 196, 195, 194, 193, 192, 135, 134, 133, 132, 131, 130, 129, 128, 71,  70,  69,  68,  67,  66,  65,  64,  7,  6,  5,  4,  3,  2,  1,  0] 
]

font5x3 = [
	[0x00,0x00,0x00], # ' '	
	[0x00,0x1D,0x00], # '!'
	[0x18,0x00,0x18], # '"'
	[0x1F,0x0A,0x1F], # '#'
	[0x0A,0x1F,0x14], # '$'
	[0x13,0x04,0x19], # '%'
	[0x0A,0x15,0x0B], # '&'
	[0x00,0x18,0x00], # '''
	[0x00,0x0E,0x11], # '('
	[0x11,0x0E,0x00], # ')'
	[0x15,0x0E,0x15], # '*'
	[0x04,0x0E,0x04], # '+'
	[0x01,0x02,0x00], # ','
	[0x04,0x04,0x04], # '-'
	[0x00,0x03,0x00], # '.'
	[0x01,0x0E,0x10], # '/'
	[0x1F,0x11,0x1F], # '0'
	[0x09,0x1F,0x01], # '1'
	[0x17,0x15,0x1D], # '2'
	[0x11,0x15,0x1F], # '3'
	[0x1C,0x04,0x1F], # '4'
	[0x1D,0x15,0x17], # '5'
	[0x1F,0x15,0x17], # '6'
	[0x10,0x10,0x1F], # '7'
	[0x1F,0x15,0x1F], # '8'
	[0x1D,0x15,0x1F], # '9'
	[0x00,0x0A,0x00], # ':'
	[0x01,0x0A,0x00], # ';'
	[0x04,0x0A,0x11], # '<'
	[0x0A,0x0A,0x0A], # '='
	[0x11,0x0A,0x04], # '>'
	[0x10,0x15,0x18], # '?'
	[0x0E,0x15,0x0D], # '@'
	[0x0F,0x14,0x0F], # 'A'
	[0x1F,0x15,0x0A], # 'B'
	[0x0E,0x11,0x11], # 'C'
	[0x1F,0x11,0x0E], # 'D'
	[0x1F,0x15,0x15], # 'E'
	[0x1F,0x14,0x14], # 'F'
	[0x0E,0x15,0x17], # 'G'
	[0x1F,0x04,0x1F], # 'H'
	[0x11,0x1F,0x11], # 'I'
	[0x02,0x01,0x1E], # 'J'
	[0x1F,0x04,0x1B], # 'K'
	[0x1F,0x01,0x01], # 'L'
	[0x1F,0x08,0x1F], # 'M'
	[0x1F,0x0E,0x1F], # 'N'
	[0x0E,0x11,0x0E], # 'O'
	[0x1F,0x14,0x08], # 'P'
	[0x0E,0x13,0x0F], # 'Q'
	[0x1F,0x16,0x0D], # 'R'
	[0x09,0x15,0x12], # 'S'
	[0x10,0x1F,0x10], # 'T'
	[0x1E,0x01,0x1F], # 'U'
	[0x1e,0x01,0x1e], # 'V'
	[0x1F,0x06,0x1F], # 'W'
	[0x1B,0x04,0x1B], # 'X'
	[0x18,0x07,0x18], # 'Y'
	[0x13,0x15,0x19], # 'Z'
	[0x1F,0x11,0x00], # '['
	[0x18,0x04,0x03], # '\'
	[0x00,0x11,0x1F], # ']'
	[0x08,0x10,0x08], # '^'
	[0x01,0x01,0x01], # '_'
	[0x10,0x08,0x00], # '`'
	[0x03,0x05,0x07], # 'a'
	[0x1F,0x05,0x02], # 'b'
	[0x02,0x05,0x05], # 'c'
	[0x02,0x05,0x1F], # 'd'
	[0x06,0x0B,0x0D], # 'e'
	[0x04,0x0F,0x14], # 'f'
	[0x05,0x0D,0x0E], # 'g'
	[0x1F,0x04,0x03], # 'h'
	[0x00,0x17,0x00], # 'i'
	[0x01,0x01,0x16], # 'j'
	[0x0F,0x02,0x05], # 'k'
	[0x11,0x1F,0x01], # 'l'
	[0x07,0x06,0x07], # 'm'
	[0x07,0x04,0x03], # 'n'
	[0x02,0x05,0x02], # 'o'
	[0x07,0x0A,0x04], # 'p'
	[0x04,0x0A,0x07], # 'q'
	[0x0F,0x04,0x04], # 'r'
	[0x05,0x0F,0x0A], # 's'
	[0x08,0x1F,0x08], # 't'
	[0x06,0x01,0x07], # 'u'
	[0x06,0x03,0x06], # 'v'
	[0x07,0x03,0x07], # 'w'
	[0x05,0x02,0x05], # 'x'
	[0x09,0x05,0x0E], # 'y'
	[0x0B,0x0F,0x0D], # 'z'
	[0x04,0x1B,0x11], # '['
	[0x00,0x1F,0x00], # '|'
	[0x11,0x1B,0x04], # ']'
	[0x08,0x18,0x10], # '~'
]

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def writeChar(c, pos_x, pos_y, fg_color, bg_color):
    for i in range(3):
        line = font5x3[ord(c) - 0x20][i]
        for j in range(5):
            if (line & 0x01) == 0x01:
                strip.setPixelColor(matrix_pos[pos_y + 5 - j][pos_x + i], fg_color)
            else:
                strip.setPixelColor(matrix_pos[pos_y + 5 - j][pos_x + i], fg_color)
            line >>= 1


def showTime(long_format):
    now = datetime.datetime.now()
    
    dhour = now.hour // 10
    hour = now.hour % 10
    dminute = now.minute // 10
    minute = now.minute % 10
    dsecond = now.second // 10
    second = now.second % 10
    
    dhour = chr(ord('0') + dhour)
    hour = chr(ord('0') + hour)
    dminute = chr(ord('0') + dminute)
    minute = chr(ord('0') + minute)
    dsecond = chr(ord('0') + dsecond)
    second = chr(ord('0') + second)
    
    fg = Color(255,255,255)
    bg = Color(0,0,0)
    
    if long_format:
        writeChar(dhour, 1, 1, fg, bg)
        writeChar(hour, 5, 1, fg, bg)
        writeChar(':', 8, 1, fg, bg)
        writeChar(dminute, 11, 1, fg, bg)
        writeChar(minute, 15, 1, fg, bg)
        writeChar(':', 18, 1, fg, bg)
        writeChar(dsecond, 21, 1, fg, bg)
        writeChar(second, 25, 1, fg, bg)
    else:
        writeChar(dhour, 11, 1, fg, bg)
        writeChar(hour, 15, 1, fg, bg)
        writeChar(':', 18, 1, fg, bg)
        writeChar(dminute, 21, 1, fg, bg)
        writeChar(minute, 25, 1, fg, bg)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    while True:
        showTime(True)
        strip.show()
        time.sleep(500.0/1000.0)
#        print ('Color wipe animations.')
#        colorWipe(strip, Color(255, 0, 0))  # Red wipe
#        colorWipe(strip, Color(0, 255, 0))  # Blue wipe
#        colorWipe(strip, Color(0, 0, 255))  # Green wipe
#        print ('Theater chase animations.')
#        theaterChase(strip, Color(127, 127, 127))  # White theater chase
#        theaterChase(strip, Color(127,   0,   0))  # Red theater chase
#        theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
#        print ('Rainbow animations.')
#        rainbow(strip)
#        rainbowCycle(strip)
#        theaterChaseRainbow(strip)
