import qtawesome as qta
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QGridLayout
)

from ..shared import CleanVBoxLayout, CleanHBoxLayout 
from ..shared.custom_piechart import CustomPieChart
from .chart_legend import ChartLegend
from core.constants import ExpenseCategories
from assets.theme import Colors

class ChartPanel(QFrame):
    """Panel containing the current expenses graph"""
    def __init__(self):
        super().__init__()
        self.categories = ExpenseCategories.get_all_names()
        self._setup_ui()
        self._setup_layout()
        
    def _setup_ui(self):
        #self.setProperty("class", "glass_card")
        
        self.switch_view_btn = QPushButton()
        self.switch_view_btn.setIcon(qta.icon('fa5s.chart-bar', color=Colors.ICON_PRIMARY))
        self.switch_view_btn.setToolTip("Ver Gráfico Anual (Barras)")
        self.switch_view_btn.setCursor(Qt.CursorShape.PointingHandCursor) 
        self.switch_view_btn.setProperty("class", "ghost_btn") 

        self.pie_chart = CustomPieChart()
        self.pie_chart.setStyleSheet("background-color: lightgray; text-align: center;")
        
    def _setup_layout(self):
        layout = CleanVBoxLayout()
        # Header
        header_layout = CleanHBoxLayout()
        header_layout.addStretch() 
        header_layout.addWidget(self.switch_view_btn)
        layout.addLayout(header_layout)

        # Pie Chart
        layout.addWidget(self.pie_chart, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(16)

        # Chart legend
        legend_container = QFrame()        
        legend_layout = QGridLayout()
        legend_layout.setContentsMargins(0,0,0,0)
        legend_layout.setSpacing(16)
        
        for i, cat in enumerate(self.categories):
            legend_layout.addWidget(ChartLegend(ExpenseCategories.get_color(cat), cat), int(i / 3), i % 3)
        
        legend_container.setLayout(legend_layout)

        layout.addWidget(legend_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

        self.setLayout(layout)
