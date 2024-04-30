import binascii
from cgitb import text
from ctypes.wintypes import HSTR
from uu import encode
import zlib
import sys

ASCIICHARS = ''.join(chr(i) for i in range(128))
ESCAPEHEX = rf"{ASCIICHARS[92]}"

FILEHEADER = [
    b"\x42\x4D"        , #BM | signature for a bitmap file
    b"\x36\x0C\x00\x00", #134 | size of file in bytes
    b"\x00\x00\x00\x00", #reserved bytes
    b"\x36\x00\x00\x00", #offset
]
INFOHEADER = [
    b"\x28\x00\x00\x00", #40
    b"\x20\x00\x00\x00", #32    | width
    b"\x20\x00\x00\x00", #32    | height 
    b"\x01\x00",         #1     | number of display plans
            b"\x18\x00", #24    | bits per pixel
    b"\x00\x00\x00\x00", #0     | type of compresion
    b"\x00\x0C\x00\x00", #80    | number of bytes in picture
    b"\x00\x00\x00\x00", #50190 | horizontal resolution
    b"\x00\x00\x00\x00", #50190 | vertical   resolution
    b"\x00\x00\x00\x00", #0     | number of colors
    b"\x00\x00\x00\x00", #0     | number of important colors
]


# Start at bottom left, then go right then up
# \x00 \x00 \x00
#   B    G    R
PIXELWIDTH = 32
PIXELHEIGHT = 32
pixels = [
    #row 1
    [
        "\x48\x45\x4C", #HEL
        "\x4C\x4F\x20", #LO[space]
        "\x57\x4F\x52", #WOR
        "\x4C\x44\x21", #LD!
        "\x00\x00\x00\x00", #nothing + padding
    ],
    #row 2
    [
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00\x00", #nothing + padding
    ],
    #row 3
    [
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00\x00", #nothing + padding
    ],
    #row 4
    [
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00\x00", #nothing + padding
    ],
    #row 5  
    [
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00", #nothing
        "\x00\x00\x00\x00", #nothing + padding
    ]
]

def MakeBMP(): #will write the full bitmap file
    with open("Showcase.bmp", "xb") as file:
        file.writelines(FILEHEADER)
        file.writelines(INFOHEADER)
        for row in pcBlock:
            for pixel in row:
                if pixel == "none":
                    file.write(b"\x20\x20\x20")
                else:
                    for pixelChar in pixel:
                        file.write(pixelChar.encode("us-ascii"))
            #file.write(b"\x20")

def str2pcs(text: str): #takes a string and gives an array of 3 char long strings
    pixels = [] #will hold the seperated character pairs or pixels
    for chars in range(0, len(text), 3): #takes groups of 3 chars to be turned into pixChars
        pixChars = "" #start the pixel string
        if chars + 3 > len(text): #we would overflow so go until the end
            pixChars = text[chars:len(text)]
            for extra in range(3 - len(pixChars)):
                pixChars += " "
        else: #no index worries
            pixChars = text[chars:chars+3]
        pixels.append(pixChars) #add current pixChar to the list of pixels
    return pixels #give back the pixels

def pcs2row(pcs: list): #takes in a list of pixels and returns a 2d list of pixel with the image width and height
    pixelX = 0 #horizontal position from left to right
    pixelY = 0 #vertical   position from bottom to top
    pixelBlock = [] #will hold the list for the rows
    while pixelY < PIXELHEIGHT: #we are not yet at the top
        pixelRow = [] #new row
        pixelX = 0
        while pixelX < PIXELWIDTH: #we have not reached the end of the row
            if (pixelY * PIXELWIDTH) + pixelX < len(pcs): #we still have pixels to add
                pixelRow.append(pcs[(pixelY * PIXELWIDTH) + pixelX])
            else: #no more pixels so fills the rest with "none"s
                pixelRow.append("none")
            pixelX += 1
        pixelBlock.append(pixelRow) #add the row to the block
        pixelY += 1
    return pixelBlock #give back the block of pixels

print()
strText = "\r\nThe frog jumps!" #input("Text: ") #get the string to be converted
#strText = "HELLO WORLD!" #input("Text: ") #get the string to be converted
print(len(strText)) #give the length of the text

#validation
#ans = "n"
#while ans == "n":
#    ans = input("do you want to use this string")

pix = str2pcs(strText) #get the string seperated into pixels
pcBlock = pcs2row(pix) #get the pixels blocked out

MakeBMP()