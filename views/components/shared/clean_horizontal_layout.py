from PySide6.QtWidgets import (
    QHBoxLayout
)

class CleanHBoxLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        