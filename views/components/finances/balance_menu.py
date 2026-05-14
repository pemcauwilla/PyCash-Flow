from PySide6.QtWidgets import (
    QFrame,
)

from ..shared.clean_horizontal_layout import CleanHBoxLayout
from .balance_card import BalanceCard

class BalanceMenu(QFrame):
    """Top menu containing all balances"""
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_layouts()
        
    def _setup_ui(self) -> None:
        self.setObjectName("top_menu")

        self.monthly_card = BalanceCard("Saldo Mensal", "fa5s.calendar-alt")
        self.remaining_card = BalanceCard("Saldo Restante", "fa5s.wallet")
        self.total_card = BalanceCard("Saldo Total", "fa5s.piggy-bank")

    def _setup_layouts(self) -> None:
        layout = CleanHBoxLayout()
        layout.setContentsMargins(16,16,16,16)
        layout.setSpacing(32)
        layout.addWidget(self.monthly_card)
        layout.addWidget(self.remaining_card)
        layout.addWidget(self.total_card)
        self.setLayout(layout)

    def _connect_signals(self):
        pass

    def format_currency(self, cents: int) -> str:
        """Receive cents (int) and formats it to Real (R$)"""
        if not cents:  
            cents = 0
            
        real_value = cents / 100.0
        return f"R$ {real_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def update_values(self, summary_data : dict):
        monthly_txt = self.format_currency(summary_data.get("monthly", 0))
        remaining_txt = self.format_currency(summary_data.get("remaining", 0))
        total_txt = self.format_currency(summary_data.get("total", 0))

        self.monthly_card.value_lbl.setText(monthly_txt)
        self.remaining_card.value_lbl.setText(remaining_txt)
        self.total_card.value_lbl.setText(total_txt)
