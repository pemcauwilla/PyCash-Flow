import os
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class ColorTokens:
    # Background and borders
    BG_GRAD_START: str = "#0A0F1E"  
    BG_GRAD_MID: str = "#1A1528"   
    BG_GRAD_END: str = "#112230"

    GLASS_BG: str = "rgba(100, 150, 255, 0.03)" 
    GLASS_BORDER: str = "rgba(255, 255, 255, 0.08)" 
    GLASS_HOVER: str = "rgba(255, 255, 255, 0.07)"
    GLASS_BORDER_HOVER: str = "rgba(255, 255, 255, 0.15)" 

    # Text
    ACCENT_CYAN: str = "#048D9C"    
    ACCENT_PINK: str = "#FF007F"    
    ACCENT_PURPLE: str = "#B388FF"  
    TEXT_PRIMARY: str = "rgba(255, 255, 255, 0.9)"
    TEXT_SECONDARY: str = "rgba(255, 255, 255, 0.5)"
    TEXT_BLACK: str = "#0A0F1E"

    #Icons
    ICON_PRIMARY: str="#E0E0E0"

    # Buttons
    BTN_HOVER_GLASS: str = "rgba(255, 255, 255, 0.08)"
    BTN_PRESSED_GLASS: str = "rgba(255, 255, 255, 0.05)"
    BTN_PRESSED_CYAN: str= "#00717E"
    
    BTN_ACCENT_CYAN_PRESSED: str="#00B3CC"
    BTN_ACCENT_CYAN_HOVER: str="#6ED2DD"

    BTN_CANCEL_HOVER_BORDER: str="rgba(255, 255, 255, 0.2)"
    BTN_CANCEL_HOVER_BG: str="rgba(255, 255, 255, 0.05)"
    BTN_CANCEL_PRESSED_BG: str="rgba(255, 255, 255, 0.02)"

    # Input and menus 
    INPUT_BG: str = "rgba(0, 0, 0, 0.2)"
    INPUT_BG_FOCUS: str = "rgba(0, 0, 0, 0.3)"
    SIDE_MENU_BORDER: str = "rgba(255, 255, 255, 0.05)"

    # ScrollBar
    SBAR_HANDLE_VERTICAL : str = "rgba(255, 255, 255, 0.15)"
    HOVER_SBAR_HANDLE_VERTICAL : str = "rgba(255, 255, 255, 0.3)"

    # Chart
    CHART_LIGHT_PURPLE : str = "#BB86FC"
    CHART_LIGHT_GREEN : str = "#03DAC6"
    CHAR_DARK_PURPLE : str = "#3700B3"
    CHART_LIGHT_RED : str = "#CF6679"
    CHART_DARK_GREEN : str = "#018786"
    CHART_LIGHT_ORANGE : str = "#FFB86C"
    CHART_CYAN : str = "#8BE9FD"
    CHART_GRAY : str = "#888888"

# ----- 
Colors = ColorTokens()
# -----

def load_styles() -> str : 
    """Read all the qss files while injecting all the custom variables, concatenating them all together at the end"""

    # The file's order matters here 
    qss_files = [ 
        "assets/global_styles.qss",
        "assets/card_styles.qss",
        "assets/balance_menu.qss",
        "assets/expenses_menu.qss",
        "assets/side_menu.qss",
        "assets/expense_item.qss",
        "assets/add_dialog.qss"
    ]

    combined_qss = ""

    for file_path in qss_files:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f: 
                combined_qss += f.read() + "\n"
        else:
            print(f"ATTENTION!!! Missing file -> {file_path}")

    combined_qss = _replace_qss(Colors, combined_qss)
    

    return combined_qss

def _replace_qss(x_class: dataclass, qss_file : str) -> str:
    for key, value in asdict(x_class).items():
        qss_file = qss_file.replace(f"@{key}", str(value))

    return qss_file