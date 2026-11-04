import os
os.environ['QT_OPENGL'] = 'software'

import io
import datetime as dt
from PyQt6 import uic
import sqlite3
import sys
from PyQt6.QtCore import QRegularExpression, Qt, QTimer, QDate
from PyQt6.QtGui import QRegularExpressionValidator, QColor
from PyQt6.QtWidgets import QDialog, QMessageBox, QMainWindow, QTableWidgetItem, QApplication
from ui.main_window import main_template
from ui.dialog_window import dialog_template

#Работа с темами приложения
THEMES = {
    "dark": os.path.join("styles", "dark.qss"),
    "light": os.path.join("styles", "light.qss")
}


def load_theme(name):
    path = THEMES.get(name)

    if path and os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as theme:
            return theme.read()

    return ""


"""Работа с базами данных"""
#1. БД для подписок
# 2. БД для уведомлений

connection = sqlite3.connect("lynk.db")
def init_db():
    with connection as conn:
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            name TEXT UNIQUE NOT NULL)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS subscriptions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            title TEXT NOT NULL, 
                            end_date TEXT NOT NULL, 
                            cost REAL, 
                            category_id INTEGER NOT NULL,
                            FOREIGN KEY(category_id) REFERENCES categories(id))""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS notifications_log (
                            subscription_id INTEGER, 
                            notify_date TEXT,
                            PRIMARY KEY (subscription_id, notify_date))""")

        def_categories = ["Банк", "Кино", "Музыка", "Другое", "Связь", "Софт", "Игры"]
        for c in def_categories:
            cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (c,))

#БД для подписок
def get_categories():
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT id, name FROM categories ORDER BY name""")
        rez = cursor.fetchall()
    return rez


def add_subscription(title, end_date, cost, cat_id):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO subscriptions (title, end_date, cost, category_id) VALUES (?, ?, ?, ?)""",
                       (title, end_date, cost, cat_id))
        conn.commit()

def get_all_sub():
    with connection as conn:
        cursor = conn.cursor()

        cursor.execute("""SELECT s.id, s.title, s.end_date, s.cost, c.name
        FROM subscriptions s
        JOIN categories c ON s.category_id = c.id
        ORDER BY s.end_date ASC""")
    return cursor.fetchall()

#БД для уведомлений

def log_notification(sub_id, date):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO notifications_log (subscription_id, notify_date) VALUES (?, ?)""",
                    (sub_id, date))
        conn.commit()


def was_notified_today(sub_id, date):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT 1 FROM notifications_log WHERE subscription_id=? AND notify_date=?""",
                       (sub_id, date))
        rez = cursor.fetchone()
    return rez is not None


"""Основная логика"""
#1. Диалоговое окно
#2. Основное окно


class DialogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        f = io.StringIO(dialog_template)
        uic.loadUi(f, self)

        validator = QRegularExpression(r"^\d*[.,]?\d*$") #можно вводить только int или float

        self.inputCost.setValidator(QRegularExpressionValidator(validator, self))
        self.btnSave.clicked.connect(self.save)
        self.btnCancel.clicked.connect(self.reject)

        self.load_categories()

    def load_categories(self):
        for id, name in get_categories():
            self.comboCategory.addItem(name, id)


    def save (self):
        name = self.inputName.text().strip()
        cost = self.inputCost.text().strip().replace(",", ".")


        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название подписки!".capitalize())
            return
        if not cost:
            QMessageBox.warning(self, "Ошибка", "Введите стоимость подписки!".capitalize())
            return


        try:
            cost = float(cost)
        except ValueError:
            QMessageBox.warning(self, "ОШИБКА",f"НЕКОРРЕКТНАЯ СТОИМОСТЬ!")
            return

        if cost <= 0:
            QMessageBox.warning(self, "ОШИБКА", "Стоимость должна быть больше нуля!".capitalize())
            return

        date = self.inputDate.date().toString("yyyy-MM-dd")
        id_category = self.comboCategory.currentData() #currentData = id

        try:
            add_subscription(name, date, cost, id_category)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "ОШИБКА БД", f"Подробнее: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(main_template)
        uic.loadUi(f, self)
        self.tableWidget.verticalHeader().setVisible(False)
        self.cur_theme = "dark"

        self.btnAdd.clicked.connect(self.open_dialog)
        self.load_data()
        # self.notifications()
        # self.tray()


    def load_data (self):
        self.tableWidget.setRowCount(0) #чтобы не было наслоения

        date_today = dt.datetime.now().date()

        for row, (id_, title, end_date, cost, name) in enumerate(get_all_sub()):
            self.tableWidget.insertRow(row)

            date = dt.datetime.strptime(end_date, "%Y-%m-%d").date()

            """Получаем все данные для каждой записи в бд"""
            item_title = QTableWidgetItem(title)
            item_date = QTableWidgetItem(date.strftime("%d.%m.%Y"))
            item_cost = QTableWidgetItem(f"{cost:.2f} руб.")
            item_cat = QTableWidgetItem(name)

            """Выравнивание"""
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_cost.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            item_cat.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if date < date_today:
                item_title.setForeground(QColor("red"))
                item_date.setForeground(QColor("red"))
            elif (date - date_today).days <= 3:
                item_title.setForeground(QColor("orange"))


            self.tableWidget.setItem(row, 0, item_title)
            self.tableWidget.setItem(row, 1, item_date)
            self.tableWidget.setItem(row, 2, item_cost)
            self.tableWidget.setItem(row, 3, item_cat)

    def open_dialog(self):
        dialog = DialogWindow(self)
        if dialog.exec():
            self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    init_db()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())