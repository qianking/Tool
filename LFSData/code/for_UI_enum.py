from enum import Enum
from PySide6.QtCore import Qt

class Text_Color(Enum):
    black = Qt.black
    darkYellow = Qt.darkYellow
    red = Qt.red
    blue = Qt.blue
    darkGreen = Qt.darkGreen


print(Qt.red)

print(Text_Color.red.value)