import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure


class AboutDialog(QDialog):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("About / אודות")
        self.setFixedSize(420, 260)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        card = QFrame()
        card.setObjectName("about_card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)

        # כותרת האפליקציה
        title_label = QLabel("📊 אפליקציית ניתוח נתונים (Ice Cream App)")
        title_label.setObjectName("about_title")
        card_layout.addWidget(title_label)

        # פרטי היוצר / הסטודנט (התאם לפי הצורך)
        info_label = QLabel(
            "פותח ע\"י: ליאל אליהו\n"
            "קורס: מכטרוניקה | תרגיל 2\n"
            "תיאור: אפליקציית שולחן עבודה לטעינה והצגה גרפית של נתונים."
        )
        info_label.setObjectName("about_info")
        card_layout.addWidget(info_label)

        # קישור לחיץ למאגר GitHub
        github_link = QLabel(
            '<a href="https://github.com/your-username/your-repository"'
            ' style="color: #2563eb; text-decoration: none; font-weight: bold;">'
            '🔗 מאגר ה-GitHub שלי</a>'
        )
        github_link.setObjectName("about_link")
        github_link.setTextFormat(Qt.TextFormat.RichText)
        github_link.setOpenExternalLinks(True)
        card_layout.addWidget(github_link)

        layout.addWidget(card)

        # כפתור סגירה
        close_btn = QPushButton("סגור")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("אפליקציית ניתוח נתונים - PySide6 & Matplotlib")
        self.resize(850, 650)

        self.temperatures = []
        self.revenues = []

        # וידג'ט מרכזי ופריסה ראשית
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # 1. סרגל עליון (כפתור בחירת קובץ, תצוגת נתיב וכפתור אודות)
        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("toolbar_frame")
        top_layout = QHBoxLayout(toolbar_frame)
        top_layout.setContentsMargins(8, 8, 8, 8)
        top_layout.setSpacing(10)

        self.btn_select_csv = QPushButton("📂 בחר קובץ CSV")
        self.btn_select_csv.clicked.connect(self.select_csv_file)
        top_layout.addWidget(self.btn_select_csv)

        self.lbl_file_path = QLabel("טרם נבחר קובץ...")
        self.lbl_file_path.setObjectName("file_path_label")
        top_layout.addWidget(self.lbl_file_path, stretch=1)

        self.btn_about = QPushButton("ℹ️ About")
        self.btn_about.setObjectName("about_button")
        self.btn_about.clicked.connect(self.show_about_dialog)
        top_layout.addWidget(self.btn_about)

        main_layout.addWidget(toolbar_frame)

        # 2. אזור גרף מוטמע של Matplotlib וסרגל כלים
        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas, stretch=1)

        # ציור גרף דוגמה ראשוני
        self.plot_graph()

    def select_csv_file(self) -> None:
        """
        פותח חלון בחירת קובץ CSV ומציג את הנתיב שנבחר.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "בחר קובץ CSV",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )

        if file_path:
            self.lbl_file_path.setText(f"קובץ שנבחר: {file_path}")
            # איפוס הרשימות למקרה שטוענים קובץ חדש
            self.temperatures = []
            self.revenues = []
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                # מדלגים על שורת הכותרות (שורה 0)
                for line in lines[1:]:
                    parts = line.strip().split(',')
                    self.temperatures.append(float(parts[0]))
                    self.revenues.append(float(parts[1]))

            self.plot_graph()

    def plot_graph(self) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # ציור גרף נקודות (scatter) עם גודל נקודה 1
        ax.scatter(self.temperatures, self.revenues, s=1)

        # כותרות לצירים ולגרף
        ax.set_title("Ice Cream Revenue vs. Temperature")
        ax.set_xlabel("Temperature")
        ax.set_ylabel("Revenue ($)")

        # העפת הקו העליון והימני של המסגרת
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        self.canvas.draw()

    def show_about_dialog(self) -> None:
        """פותח את חלון ה-About הנפרד."""
        dialog = AboutDialog(self)
        dialog.exec()


def load_stylesheet(app: QApplication) -> None:
    """טוען את קובץ העיצוב style.qss ומחיל אותו על האפליקציה."""
    try:
        with open("style.qss", "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        pass


def main() -> None:
    app = QApplication(sys.argv)
    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
