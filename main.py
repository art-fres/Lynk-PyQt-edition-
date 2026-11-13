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
from styles.dark import DARK_THEME
from styles.light import LIGHT_THEME

#Работа с темами приложения

THEMES = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME
}

NOTIFY_DAYS = 3

def load_theme(name):
    return THEMES.get(name)


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
                            title TEXT UNIQUE NOT NULL, 
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

"""Обновление данных"""
def get_subscription_by_id(sub_id):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT id, title, end_date, cost, category_id 
                          FROM subscriptions WHERE id = ?""", (sub_id,))
        return cursor.fetchone()


def update_subscription(sub_id, title, end_date, cost, cat_id):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE subscriptions 
                          SET title=?, end_date=?, cost=?, category_id=? 
                          WHERE id=?""",
                       (title, end_date, cost, cat_id, sub_id))
        conn.commit()


def \
        delete_subscription_by_id(sub_id):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
        conn.commit()
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

def get_ex_subs(days):
    today = dt.date.today()
    limit = today + dt.timedelta(days=days)

    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT id, title, end_date, cost FROM subscriptions
         WHERE end_date BETWEEN ? AND ?""", (today.isoformat(), limit.isoformat()))

        return cursor.fetchall()
"""Основная логика"""
#1. Диалоговое окно
#2. Основное окно


class DialogWindow(QDialog):
    def __init__(self, parent=None, new_data = None): #new_data - кортеж новых данных, если он пустой то это создание новой записи:
        super().__init__(parent)
        f = io.StringIO(dialog_template)
        uic.loadUi(f, self)

        validator = QRegularExpression(r"^\d*[.,]?\d*$") #можно вводить только int или float
        self.inputCost.setValidator(QRegularExpressionValidator(validator, self))

        self.inputDate.setMinimumDate(QDate.currentDate())
        self.inputDate.setDate(QDate.currentDate().addDays(30))

        self.btnSave.clicked.connect(self.save)
        self.btnCancel.clicked.connect(self.reject)

        self.load_categories()

        self.new_data = new_data

        if self.new_data:
            self.update_sub()

    def load_categories(self):
        for id, name in get_categories():
            self.comboCategory.addItem(name, id)

    def update_sub(self):
        sub_id, title, end_date, cost, cat_id = self.new_data
        self.inputName.setText(title)
        self.inputCost.setText(f"{cost:.2f}")


        date = QDate.fromString(end_date, "yyyy-MM-dd")
        if date.isValid():
            self.inputDate.setDate(date)



        index = self.comboCategory.findData(cat_id)
        if index != -1:
            self.comboCategory.setCurrentIndex(index)

        self.setWindowTitle("Редактирование подписки")
        self.btnSave.setText("СОХРАНИТЬ")


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
            if self.new_data:
                sub_id = self.new_data[0]
                update_subscription(sub_id, name, date, cost, id_category)
            else:
                add_subscription(name, date, cost, id_category)
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "ОШИБКА БД", "Скорее всего подписка с таким именем уже существует")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка БД", f"Подробнее: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(main_template)
        uic.loadUi(f, self)

        #доп настройка таблицы
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tableWidget.setSelectionBehavior(
            self.tableWidget.SelectionBehavior.SelectRows
        )
        self.tableWidget.setSelectionMode(
            self.tableWidget.SelectionMode.ExtendedSelection
        )
        self.tableWidget.cellDoubleClicked.connect(self.on_row_double_click)

        """Применение темы"""
        self.cur_theme = "dark"
        qss = load_theme(self.cur_theme)
        if qss:
            QApplication.instance().setStyleSheet(qss)


        self.btnTheme.clicked.connect(self.change_theme)
        self.btnAdd.clicked.connect(self.open_dialog)
        self.btnDelete.clicked.connect(self.delete_sub)
        self.load_data()
        self.notifications()




    def open_dialog(self):
        dialog = DialogWindow(self)
        if dialog.exec():
            self.load_data()


    def load_data (self):
        self.tableWidget.setRowCount(0) #чтобы не было наслоения

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, header.ResizeMode.ResizeToContents)
        for i in range(1, 4):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)

        date_today = dt.datetime.now().date()

        for row, (id_, title, end_date, cost, name) in enumerate(get_all_sub()):
            self.tableWidget.insertRow(row)

            date = dt.datetime.strptime(end_date, "%Y-%m-%d").date()

            """Получаем все данные для каждой записи в бд"""
            item_title = QTableWidgetItem(title)
            item_date = QTableWidgetItem(date.strftime("%d.%m.%Y"))
            item_cost = QTableWidgetItem(f"{cost:.2f} руб.")
            item_cat = QTableWidgetItem(name)

            item_title.setData(Qt.ItemDataRole.UserRole, id_)
            """Выравнивание"""
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_cost.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            item_cat.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if date < date_today:
                item_title.setForeground(QColor("red"))
                item_date.setForeground(QColor("red"))
            elif (date - date_today).days <= 3:
                item_title.setForeground(QColor("orange"))
                item_date.setForeground(QColor("orange"))


            self.tableWidget.setItem(row, 0, item_title)
            self.tableWidget.setItem(row, 1, item_date)
            self.tableWidget.setItem(row, 2, item_cost)
            self.tableWidget.setItem(row, 3, item_cat)

    def change_theme(self):
        if self.cur_theme == "dark":
            self.cur_theme = "light"
            qss = load_theme(self.cur_theme)
            if qss:
                QApplication.instance().setStyleSheet(qss)
        else:
            self.cur_theme = "dark"
            qss = load_theme(self.cur_theme)
            if qss:
                QApplication.instance().setStyleSheet(qss)


    def notifications(self):
        today = dt.date.today().isoformat()
        subs = []

        for id_, title, end_date, cost in get_ex_subs(NOTIFY_DAYS):
            if was_notified_today(id_, today):
                continue

            log_notification(id_, today)
            days = (dt.date.fromisoformat(end_date) - dt.date.fromisoformat(today)).days

            print(days)

            if days == 0:
                when = "сегодня"
            elif days == 1:
                when = "завтра"
            else:
                when = f"через {days} дн."
            subs.append(f"{title} - {when} ({cost:.2f} руб.)")


        if subs:
            QMessageBox.information(self, "Подписки истекают", "\n".join(subs))

    def on_row_double_click(self, row, column):
        item = self.tableWidget.item(row, 0)
        if not item:
            return

        sub_id = item.data(Qt.ItemDataRole.UserRole)
        if sub_id is None:
            return


        new_data = get_subscription_by_id(sub_id)
        if not new_data:
            QMessageBox.warning(self, "Ошибка", "Подписка не найдена в БД!")
            return
        dialog = DialogWindow(self, new_data)
        if dialog.exec():
            self.load_data()

    def delete_sub(self):
        selection = self.tableWidget.selectionModel()
        rows = sorted({idx.row() for idx in selection.selectedRows()})


        if not rows:
            current_row = self.tableWidget.currentRow()
            if current_row == -1:
                QMessageBox.warning(self, "Внимание", "Выберите подписку для удаления!")
                return
            rows = [current_row]

        subs = []
        for row in rows:
            item = self.tableWidget.item(row, 0)
            if item and item.data(Qt.ItemDataRole.UserRole) is not None:
                subs.append((item.data(Qt.ItemDataRole.UserRole), item.text()))

        if not subs:
            return

        if len(subs) == 1:
            text = f"Удалить подписку «{subs[0][1]}»?"
        else:
            preview = "\n".join(f"• {title}" for _, title in subs[:10])
            if len(subs) > 10:
                preview += f"\n… и ещё {len(subs) - 10}"
            text = f"Удалить {len(subs)} подписок?\n\n{preview}"

        reply = QMessageBox.question(
            self, "Подтверждение", text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            for sub_id, _ in subs:
                delete_subscription_by_id(sub_id)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось удалить:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_db()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())