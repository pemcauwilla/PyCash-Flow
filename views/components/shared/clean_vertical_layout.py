from PySide6.QtWidgets import (
    QVBoxLayout
)

class CleanVBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)