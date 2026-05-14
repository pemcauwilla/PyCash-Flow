from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRectF, Qt

from assets.theme import Colors
from core.constants import ExpenseCategories

class CustomPieChart(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(300, 300)
        
        self.colors = []
        self.data_percentages = []
        self.total_text= ""
        
    def set_data(self, percentages: list, colors: list, total_text: str):
        """Update the chart with new data"""
        self.data_percentages = percentages
        self.total_text = total_text
        self.colors = colors

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        total_width = self.width()
        total_height = self.height()
        taille_cercle = min(total_width , total_height, 300) - 20 
        
        x = (total_width - taille_cercle) / 2
        y = (total_height - taille_cercle) / 2

        rect = QRectF(x, y, taille_cercle, taille_cercle)
        start_angle = 0 

        for color, percentage in zip(self.colors, self.data_percentages):
            painter.setBrush(QColor(color))
            span_angle = int((percentage / 100.0) * 360 * 16)
            painter.drawPie(rect, start_angle, span_angle)
            start_angle += span_angle

        taille_trou = taille_cercle * 0.65
        trou_x = x + (taille_cercle - taille_trou) / 2
        trou_y = y + (taille_cercle - taille_trou) / 2
        rect_trou = QRectF(trou_x, trou_y, taille_trou, taille_trou)

        painter.setBrush(QColor(Colors.BG_GRAD_END)) 
        painter.drawEllipse(rect_trou)

        painter.setPen(QColor(Colors.ICON_PRIMARY)) 
        font = painter.font()
        font.setBold(True)
        font.setPointSize(16)
        painter.setFont(font)
        painter.drawText(rect_trou, Qt.AlignmentFlag.AlignCenter, self.total_text)

    def update_pie_chart(self, category_totals: dict):
        """Update the PieChart's slices"""
        if not category_totals:
            self.set_data(
                percentages=[100], 
                colors=[Colors.CHART_GRAY], 
                total_text="R$ 0.00"
            )
            return
        
        all_total_cents = sum(category_totals.values())
        total_real = all_total_cents / 100.0
        total_text = f"R$ {total_real:.2f}"
  
        new_percentages = []
        new_colors = []

        for category, amount_cents in category_totals.items():
            percentage = (amount_cents / all_total_cents) * 100
            
            new_percentages.append(percentage)

            slice_color = ExpenseCategories.get_color(category)
            new_colors.append(slice_color)

        self.set_data(
            percentages=new_percentages, 
            colors=new_colors, 
            total_text=total_text
        )

        self.update()

