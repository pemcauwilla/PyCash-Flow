if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    from views.finances_window import FinancesWindow 
    from models.database import DatabaseManager
    from controllers.finance_controller import FinanceController
    from assets.theme import load_styles

    app = QApplication(sys.argv)
    app.setStyleSheet(load_styles())

    db_model = DatabaseManager()
    controller = FinanceController(db_model)

    window = FinancesWindow(controller, db_model)
    window.update("INIT_SCREEN")
    window.show()

    db_model.attach(window)
    
    sys.exit(app.exec())