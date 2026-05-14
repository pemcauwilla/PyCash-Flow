import qtawesome as qta
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt, QSize

from ..shared import CleanVBoxLayout
from assets.theme import Colors

class SideMenu(QFrame):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_layouts()

    def _setup_ui(self) -> None:
        self.setProperty("class", "side_menu")
        self.setFixedWidth(70)

        self.app_logo = QLabel()
        icon = qta.icon('fa5s.chart-pie', color=Colors.ICON_PRIMARY)
        self.app_logo.setPixmap(icon.pixmap(32,32))
        self.app_logo.setProperty("class", "app_logo")
      
        self.separator = QFrame()
        self.separator.setFixedHeight(1)
        self.separator.setProperty("class", "side_menu_separator")

        self.expenses_btn = QPushButton()
        self.expenses_btn.setIcon(qta.icon("fa5s.wallet"))
        self.expenses_btn.setIconSize(QSize(28,28))
        self.expenses_btn.setToolTip("Despesas")
        self.expenses_btn.setProperty("class", "side_menu_icon_btn")

    def _setup_layouts(self) -> None:
        main_layout = CleanVBoxLayout()

        main_layout.addSpacing(16)
        main_layout.addWidget(self.app_logo, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        main_layout.addSpacing(16)

        main_layout.addWidget(self.separator)

        main_layout.addSpacing(16)

        main_layout.addWidget(self.expenses_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

    
        