from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel
)

from ..shared import CleanHBoxLayout
from assets.theme import Colors

class ChartLegend(QFrame):
    def __init__(self, color_hex : str=Colors.ACCENT_CYAN, text : str=""):
        super().__init__()
        self._setup_ui(color_hex=color_hex, text=text)
        self._setup_layouts()

    def _setup_ui(self, color_hex : str, text: str):
        self.color_box = QFrame()
        self.color_box.setFixedSize(12, 12)
        self.color_box.setStyleSheet(f""" 
            background-color: {color_hex};                              
        """)
        self.color_box.setProperty("class", "legend_color_box")

        self.label = QLabel(text)

    def _setup_layouts(self):
        main_layout = CleanHBoxLayout()
        main_layout.setSpacing(8)

        main_layout.addWidget(self.color_box, alignment=Qt.AlignmentFlag.AlignVCenter)
        main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(main_layout)