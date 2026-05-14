from PySide6.QtWidgets import (
    QDialog, QLineEdit, QComboBox, QDateEdit, 
    QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

from .components.shared import CleanVBoxLayout, CleanHBoxLayout 
from core.constants import ExpenseCategories

class AddExpenseDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_layouts()
        self._connect_signals()

        self.expense_id = None

        if data:
            self._load_existing_data(data)
            self._modify_ui()


    def _setup_ui(self):
        self.setWindowTitle("Nova Despesa")
        self.setModal(True) 
        self.setFixedSize(350, 450)
        
        self.setProperty("class", "dialog_bg") 

        self.title_lbl = QLabel("Adicionar Despesa")

        # --- NAME ---
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Título (ex: Supermercado)")

        # --- DESCRIPTION ---
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Descrição (opcional)")

        # --- VALUE ---
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Valor (ex: 150.00)")
        # Validation 
        regex = QRegularExpression(r"^[0-9]+([.,][0-9]{1,2})?$")
        validator = QRegularExpressionValidator(regex)
        self.amount_input.setValidator(validator)
        
        # --- DATE ---
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate()) 
        self.date_input.setCalendarPopup(True) 
        
        # --- CATEGORY ---
        self.category_cb = QComboBox()
        self.category_cb.addItems(ExpenseCategories.get_all_names())

        # --- BUTTONS ---
        self.save_btn = QPushButton("Salvar")
        self.save_btn.setProperty("class", "save_btn") 
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setProperty("class", "cancel_btn")

    def _setup_layouts(self):
        main_layout = CleanVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        main_layout.addWidget(self.title_lbl)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.desc_input)
        main_layout.addWidget(self.amount_input)
        main_layout.addWidget(self.date_input)
        main_layout.addWidget(self.category_cb)

        main_layout.addStretch() 

        btn_layout = CleanHBoxLayout()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addSpacing(16)
        btn_layout.addWidget(self.save_btn)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def _connect_signals(self) -> None:
        self.save_btn.clicked.connect(self.validate_and_accept)
        self.cancel_btn.clicked.connect(self.reject)

    def validate_and_accept(self):
        """Checks empty inputs and accepts event"""
        if not self.name_input.text().strip() or not self.amount_input.text().strip():
            answer = QMessageBox.warning(
                self,
                "Atenção!!",
                "O campo de valores não pode estar vazio!",
                QMessageBox.StandardButton.Ok
            )
            return 
        
        self.accept()

    def get_data(self) -> dict:
        """Read inputs and formats them to save in the DB"""
        
        raw_amount = self.amount_input.text().replace(',', '.')
        try:
            amount_cents = int(round(float(raw_amount) * 100))
        except ValueError:
            amount_cents = 0 

        return {
            "name": self.name_input.text().strip(),
            "description": self.desc_input.text().strip(),
            "amount": amount_cents,
            "date": self.date_input.date().toString("yyyy-MM-dd"), 
            "category": self.category_cb.currentText()
        }
    
    def _load_existing_data(self, data):
        self.name_input.setText(data["name"])
        self.desc_input.setText(data["description"])
        self.amount_input.setText(str(data["amount"] / 100.0))

        converted_date = QDate.fromString(data["date"], Qt.ISODate)
        self.date_input.setDate(converted_date)
        
        self.category_cb.setCurrentIndex(ExpenseCategories.get_all_names().index(data["category"]))
        self.expense_id = data["id"]

    def _modify_ui(self):
        self.setWindowTitle("Atualizar Despesa")
        self.title_lbl.setText("Atualizar Despesa")

