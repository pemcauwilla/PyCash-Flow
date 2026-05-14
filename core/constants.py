from dataclasses import dataclass

from assets.theme import Colors

@dataclass(frozen=True)
class ConfigKeys:
    MONTHLY_INCOME: str = "monthly_income"
    TOTAL_BALANCE: str = "total_balance"

@dataclass(frozen=True)
class CategoryTheme:
    name: str
    color: str

class ExpenseCategories:
    """Categories names and colors all centralized in this class"""
    
    ALIMENTACAO = CategoryTheme("Alimentação", Colors.CHART_LIGHT_PURPLE) 
    TRANSPORTE = CategoryTheme("Transporte", Colors.CHART_LIGHT_GREEN)  
    MORADIA = CategoryTheme("Moradia", Colors.CHAR_DARK_PURPLE)     
    LAZER = CategoryTheme("Lazer", Colors.CHART_LIGHT_RED)         
    SAUDE = CategoryTheme("Saúde", Colors.CHART_DARK_GREEN)         
    EDUCACAO = CategoryTheme("Educação", Colors.CHART_LIGHT_ORANGE)    
    OUTROS = CategoryTheme("Outros", Colors.CHART_CYAN)       
    
    @classmethod
    def get_all_names(cls) -> list[str]:
        """Return all the names to fill a ComboBox"""
        return [
            cls.ALIMENTACAO.name, cls.TRANSPORTE.name, cls.MORADIA.name,
            cls.LAZER.name, cls.SAUDE.name, cls.EDUCACAO.name, cls.OUTROS.name
        ]

    @classmethod
    def get_color(cls, category_name: str) -> str:
        """Search for the category color, else return gray"""
        for key, cat_theme in cls.__dict__.items():
            if isinstance(cat_theme, CategoryTheme) and cat_theme.name == category_name:
                return cat_theme.color
        return Colors.CHART_GRAY 

Keys = ConfigKeys()
