from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QMainWindow, QWidget, 
    QLabel, QStackedWidget,
    QMessageBox
)

from core.observer import Observer
from helpers.utils import format_month_year
from .components.finances import BalanceMenu, ExpensesPanel, ChartPanel, SideMenu
from .components.shared import CleanVBoxLayout, CleanHBoxLayout
from .add_expense_dialog import AddExpenseDialog

class FinancesWindow(QMainWindow, Observer):
    """Main Finance Window class"""
    def __init__(self, controller, model):
        super().__init__()

        self.current_display_date = QDate.currentDate()
        self.controller = controller
        self.model = model

        self._setup_ui()
        self._setup_layouts()
        self._connect_signals()
      
    def _setup_ui(self) -> None:
        """Create all UI elements and sets window parameters"""
        self.setWindowTitle("Life Manager - Finances")
        self.setMinimumSize(1024, 768)
        self.resize(1280, 720)

        self.top_menu = BalanceMenu()

        self.side_menu = SideMenu()

        self.expenses_panel = ExpensesPanel()
        self.chart_panel = ChartPanel()

        self.chart_page_placeholder = QLabel("[TELA COM OS 12 GRÁFICOS]")
        self.chart_page_placeholder.setStyleSheet("background-color: lightblue; font-size:20px;")

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setProperty("class", "main_stacked_widget")

    def _setup_layouts(self) -> None:
        """Create and set up all layouts"""
        # --- Main Page (Expenses + Chart )
        default_exp_page_view = QWidget()
        default_exp_layout = CleanHBoxLayout()
        default_exp_layout.setContentsMargins(16,16,16,16)
        default_exp_layout.setSpacing(16)
        default_exp_layout.addWidget(self.expenses_panel, stretch=1)
        default_exp_layout.addWidget(self.chart_panel, stretch=1)
        default_exp_page_view.setLayout(default_exp_layout)
        # -----

        # --- StackedWidget ---
        self.stacked_widget.addWidget(default_exp_page_view)
        self.stacked_widget.addWidget(self.chart_page_placeholder)
        # -----

        # --- Actual Content (Top Menu + StackedWidget)
        content_layout = CleanVBoxLayout()
        content_layout.setContentsMargins(0,4,0,4)
        content_layout.addWidget(self.top_menu)
        content_layout.addWidget(self.stacked_widget)
        # -----

        # --- Final assembly --- 
        main_layout = CleanHBoxLayout()
        main_layout.addWidget(self.side_menu)
        main_layout.addLayout(content_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        central_widget.setObjectName("main_window_central_widget")
        self.setCentralWidget(central_widget)
        # -----

    def _connect_signals(self) -> None:
        """Connect all signals and events"""
        self.expenses_panel.add_btn.clicked.connect(self._open_add_dialog)

        self.expenses_panel.edit_requested.connect(self._open_edit_dialog)
        self.expenses_panel.delete_requested.connect(self._delete_expense)

        self.expenses_panel.prev_month_btn.clicked.connect(self._go_to_prev_month)
        self.expenses_panel.next_month_btn.clicked.connect(self._go_to_next_month)

    def update(self, data=None):
        """Method called when there's a change in the model"""
        if data in ["ADD_NEW_EXPENSE", "UPDATED_DATA", "INIT_SCREEN"]:
            self.refresh_all_data()

    def refresh_all_data(self):
        year_month_db = self.current_display_date.toString("yyyy-MM")
        month_text = self.current_display_date.toString("MM/yyyy")
        self.expenses_panel.month_lbl.setText(month_text)

        expenses = self.model.get_all_expenses(year_month_db)
        summary = self.model.get_balance_summary(year_month_db)
        category_totals = self.model.get_expenses_by_category(year_month_db)

        formatted_month_text = format_month_year(self.current_display_date)
        self.expenses_panel.update_month_title(formatted_month_text)

        self.expenses_panel.update_items(expenses)
        self.top_menu.update_values(summary)
        self.chart_panel.pie_chart.update_pie_chart(category_totals)

    def _open_add_dialog(self):
        dialog = AddExpenseDialog(self)
        
        if dialog.exec():
            expense_data = dialog.get_data()
            self.controller.save_new_expense(expense_data)

    def _open_edit_dialog(self, data_dict : dict):
        dialog = AddExpenseDialog(self, data=data_dict) 
        if dialog.exec():
            expense_data = dialog.get_data()
            
            answer = QMessageBox.question(
                self,
                "Confirmar Alteração",
                "Deseja salvar as alterações feitas nesta despesa?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save
            )
            
            if answer == QMessageBox.StandardButton.Save:
                self.controller.update_expense(data_dict["id"], expense_data)

    def _delete_expense(self, expense_id : int):
        answer = QMessageBox.question(
            self, 
            "Confirmar Exclusão", 
            "Tem certeza que deseja excluir essa despesa?\nEssa ação não pode ser desfeita.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No 
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.controller.delete_expense(expense_id)
            
    def _go_to_prev_month(self):
        self.current_display_date = self.current_display_date.addMonths(-1)
        self.refresh_all_data() 

    def _go_to_next_month(self):
        self.current_display_date = self.current_display_date.addMonths(1)
        self.refresh_all_data()        
    