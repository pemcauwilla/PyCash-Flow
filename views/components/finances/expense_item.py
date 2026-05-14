import qtawesome as qta
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame, 
    QLabel, 
    QPushButton
)

from ..shared import CleanHBoxLayout
from assets.theme import Colors
from core.constants import ExpenseCategories

class ExpenseItem(QFrame):
    edit_requested = Signal(dict)
    delete_requested = Signal(int)

    def __init__(self, data : dict):
        super().__init__()
        self.data = data
        
        self._setup_ui(data)
        self._setup_layouts()
        self._connect_signals()

    def _setup_ui(self, data : dict) -> None:
        self.setProperty("class", "expense_item")
        self.setFixedHeight(64)

        title = data["name"]
        color_hex = ExpenseCategories.get_color(data["category"])
        amount = data["amount"] / 100.0

        self.edit_btn = QPushButton()
        self.edit_btn.setIcon(qta.icon("fa5s.pen", color=Colors.ICON_PRIMARY, color_active=Colors.ACCENT_CYAN))
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setProperty("class", "exp_edit_btn")

        self.color_dot = QFrame()
        self.color_dot.setFixedSize(10, 10) 
        self.color_dot.setStyleSheet(f"background-color: {color_hex};")
        self.color_dot.setProperty("class", "exp_color_dot")
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setProperty("class", "exp_title_lbl")

        self.amount_lbl = QLabel(f"R$ {amount:.2f}")
        self.amount_lbl.setProperty("class", "exp_amount_lbl")

        self.delete_btn = QPushButton()
        self.delete_btn.setIcon(qta.icon("fa5s.trash", color=Colors.ICON_PRIMARY, color_active=Colors.ACCENT_PINK)) 
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setProperty("class", "exp_delete_btn")

    def _setup_layouts(self):
        main_layout = CleanHBoxLayout()
        main_layout.setContentsMargins(8, 8 , 8, 8)

        main_layout.addWidget(self.edit_btn)
        main_layout.addSpacing(8)
        main_layout.addWidget(self.color_dot)
        main_layout.addSpacing(8)
        main_layout.addWidget(self.title_lbl)
        main_layout.addStretch()
        main_layout.addWidget(self.amount_lbl)
        main_layout.addSpacing(16)
        main_layout.addWidget(self.delete_btn)

        self.setLayout(main_layout)

    def _connect_signals(self):
        self.edit_btn.clicked.connect(self._emit_edit)
        self.delete_btn.clicked.connect(self._emit_delete)

    def _emit_edit(self):
        self.edit_requested.emit(self.data)

    def _emit_delete(self):
        self.delete_requested.emit(self.data["id"])