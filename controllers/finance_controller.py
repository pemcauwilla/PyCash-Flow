class FinanceController:
    def __init__(self, model):
        self.model = model 

    def save_new_expense(self, expense_data: dict):
        self.model.add_expense(expense_data)

    def update_expense(self, expense_id : int, expense_data: dict):
        self.model.update_expense(expense_id, expense_data)

    def delete_expense(self, expense_id: int):
        self.model.delete_expense(expense_id)