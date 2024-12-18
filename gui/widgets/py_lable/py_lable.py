from qt_core import *

style = '''
QLabel {{
    color: {_color};
}}
'''

class PyLabel(QLabel):
    def __init__(
        self, 
        text="",
        color="#FFF"
    ):
        super().__init__()

        self.setText(text)
        
        self.set_stylesheet(
            color
        )

    def set_stylesheet(
        self,
        color
    ):
        style_format = style.format(
            _color=color
        )
        self.setStyleSheet(style_format)
