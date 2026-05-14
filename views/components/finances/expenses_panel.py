import qtawesome as qta
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QScrollArea,
    QLineEdit,
    QWidget
)

from ..shared import CleanHBoxLayout, CleanVBoxLayout
from .expense_item import ExpenseItem
from assets.theme import Colors

class ExpensesPanel(QFrame):
    """Panel containing all the expenses of the selected month"""
    edit_requested = Signal(dict)
    delete_requested = Signal(int)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_layouts()
        self._connect_signals()

    def _setup_ui(self) -> None:
        self.setProperty("class", "glass_card")

        self.prev_month_btn = QPushButton()
        self.prev_month_btn.setIcon(qta.icon('fa5s.chevron-left', color=Colors.ICON_PRIMARY))
        self.prev_month_btn.setCursor(Qt.CursorShape.PointingHandCursor) 
        self.prev_month_btn.setProperty("class", "ghost_btn")

        self.next_month_btn = QPushButton()
        self.next_month_btn.setIcon(qta.icon('fa5s.chevron-right', color=Colors.ICON_PRIMARY))
        self.next_month_btn.setCursor(Qt.CursorShape.PointingHandCursor) 
        self.next_month_btn.setProperty("class", "ghost_btn")

        self.month_lbl = QLabel("Maio 2026")
        self.month_lbl.setProperty("class", "month_title")
        self.month_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.expenses_scroll_area = QScrollArea()
        self.expenses_scroll_area.setWidgetResizable(True)
        self.expenses_scroll_area.setProperty("class", "expenses_scroll_area")
        self.scroll_content = QWidget()
        self.scroll_content.setProperty("class", "exp_scroll_widget")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Pesquisar despesa...")
        self.search_bar.setProperty("class", "search_input")

        self.add_btn = QPushButton()
        self.add_btn.setIcon(qta.icon('fa5s.plus', color=Colors.TEXT_BLACK))
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setProperty("class", "add_btn")

    def _setup_layouts(self) -> None:
        main_layout = CleanVBoxLayout() 
        main_layout.setContentsMargins(12,16,12,16)
        main_layout.setSpacing(16)

        # --- Month Header --- 
        month_layout = CleanHBoxLayout()
        month_layout.addWidget(self.prev_month_btn)
        month_layout.addWidget(self.month_lbl)
        month_layout.addWidget(self.next_month_btn)
        # -----
        # --- Search bar and add btn --- 
        search_add_layout = CleanHBoxLayout()
        search_add_layout.setSpacing(8)
        search_add_layout.addWidget(self.search_bar)
        search_add_layout.addWidget(self.add_btn)
        # -----

        # --- Expenses List ---
        self.scroll_layout = CleanVBoxLayout()
        self.scroll_layout.setContentsMargins(0,0,12,0)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_content.setLayout(self.scroll_layout)
        self.expenses_scroll_area.setWidget(self.scroll_content)
        # -----

        # --- Assemble everything ---
        main_layout.addLayout(month_layout)
        main_layout.addWidget(self.expenses_scroll_area)
        main_layout.addLayout(search_add_layout)
        # -----
        self.setLayout(main_layout)

    def _connect_signals(self) -> None:
        pass

    def clear_list(self):
        while(self.scroll_layout.count()):
            item = self.scroll_layout.takeAt(0)
            
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def add_expense_item(self, data : dict ):
        self.scroll_layout.addWidget(ExpenseItem(data))

    def update_items(self, expenses_list):
        self.clear_list() 
        
        for exp in expenses_list:
            item_widget = ExpenseItem(data=exp)
            
            item_widget.edit_requested.connect(self.edit_requested.emit)
            item_widget.delete_requested.connect(self.delete_requested.emit)
            
            self.scroll_layout.addWidget(item_widget)

    def update_month_title(self, title_text: str):
        self.month_lbl.setText(title_text)