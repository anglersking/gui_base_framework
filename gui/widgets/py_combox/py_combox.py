# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# STYLE
# ///////////////////////////////////////////////////////////////
combo_style = '''
QComboBox {{
    background-color: {_bg_color};
    border-radius: {_radius}px;
    border: {_border_size}px solid {_border_color};
    padding-left: 10px;
    padding-right: 30px;  /* Make space for the arrow */
    color: {_color};
    selection-background-color: {_context_color};
    min-width: 150px;  /* Ensure a minimum width for the dropdown */
}}
QComboBox:focus {{
    border: {_border_size}px solid {_context_color};
    background-color: {_bg_color_active};
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;  /* Set the width for the drop-down arrow */
    border-left-width: 1px;
    border-left-color: {_context_color};
    border-left-style: solid;
    background-color: {_bg_color_active};  /* Background color for the drop-down */
}}
QComboBox::down-arrow {{
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 6px solid {_arrow_color};
    margin-left: 5px;  /* Adjust spacing */
}}
'''

# PY COMBO BOX
# ///////////////////////////////////////////////////////////////
class PyComboBox(QComboBox):
    def __init__(
        self,
        items=None,
        place_holder_text="",
        radius=8,
        border_size=2,
        border_color="#555",  # Border color when not focused
        color="#FFF",
        selection_color="#FFF",
        bg_color="#333",
        bg_color_active="#222",
        context_color="#00ABE8",
        arrow_color="#00ABE8",  # Custom arrow color
        parent=None
    ):
        super().__init__(parent)

        # PARAMETERS
        if items:
            self.addItems(items)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)

        # SET STYLESHEET
        self.set_stylesheet(
            radius,
            border_size,
            border_color,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            context_color,
            arrow_color
        )

    # SET STYLESHEET
    def set_stylesheet(
        self,
        radius,
        border_size,
        border_color,
        color,
        selection_color,
        bg_color,
        bg_color_active,
        context_color,
        arrow_color
    ):
        # APPLY STYLESHEET
        style_format = combo_style.format(
            _radius=radius,
            _border_size=border_size,
            _border_color=border_color,
            _color=color,
            _selection_color=selection_color,
            _bg_color=bg_color,
            _bg_color_active=bg_color_active,
            _context_color=context_color,
            _arrow_color=arrow_color
        )
        self.setStyleSheet(style_format)

    def setPlaceholderText(self, text):
        self.setEditable(True)
        self.lineEdit().setPlaceholderText(text)
        self.lineEdit().setReadOnly(True)