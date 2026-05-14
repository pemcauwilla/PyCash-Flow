import qtawesome as qta
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QGraphicsDropShadowEffect
)

from ..shared import CleanHBoxLayout, CleanVBoxLayout
from assets.theme import Colors

class BalanceCard(QFrame):
    """Individual card that shows one title, one icon and one value"""
    def __init__(self, title_text : str, icon_name : str):
        super().__init__()
        self._setup_ui(title_text=title_text, icon_name=icon_name)
        self._setup_layouts()

    def _setup_ui(self, title_text :str, icon_name : str) -> None:
        self.setProperty("class", "glass_card")

        icon = qta.icon(icon_name, color=Colors.ICON_PRIMARY)
        self.icon_lbl = QLabel()
        self.icon_lbl.setProperty("class", "icon_lbl")
        self.icon_lbl.setPixmap(icon.pixmap(32,32))
        
        self.title_lbl = QLabel(title_text)
        self.title_lbl.setProperty("class", "card_title")

        self.value_lbl = QLabel("0.00")
        self.value_lbl.setProperty("class", "card_value")

        # ---- DropShadow Effect ----- 
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25) 
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(5, 10, 20, 150))
        self.setGraphicsEffect(shadow)

    def _setup_layouts(self)-> None: 
        # --- Main layout ---
        main_layout = CleanVBoxLayout()
        main_layout.setContentsMargins(24,24,24,24)
        main_layout.setSpacing(12)
        # -----
        # --- Card Header ---
        header_layout = CleanHBoxLayout()
        header_layout.setSpacing(8)
        header_layout.addWidget(self.icon_lbl)  
        header_layout.addWidget(self.title_lbl)
        header_layout.addStretch() 
        # -----

        # --- Assembly both layouts
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.value_lbl)

        self.setLayout(main_layout)
        # -----

    def _connect_signals(self) -> None:
        pass

    def set_value(self, value : float, currency : str = "R$") -> None:
        """Update only this cards value"""
        self.value_lbl.setText(f"{currency} {value:.2f}")
