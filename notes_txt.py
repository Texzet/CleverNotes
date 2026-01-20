#для начала скопируй сюда интерфейс "Умных заметок" и проверь его работу
#почни тут створювати додаток з розумними замітками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout

import json
import os
# --------- ДАНІ ЗАМІТОК ---------


# записуємо початкові замітки у файл JSON

app = QApplication([])

if os.path.exists("notes_data.json"):

    with open("notes_data.json", "r", encoding="utf-8") as file:
        notes = json.load(file)

else:
    notes = {

    "Ласкаво просимо!": {
        "текст": "Це найкращий додаток для заміток у світі!",
        "теги": ["добро", "інструкція"]
    }

}
    with open("notes_data.json", "w", encoding="utf-8") as file:
        json.dump(notes, file)


notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)


# віджети вікна програми
list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')


button_note_create = QPushButton('Створити замітку') # з'являється вікно з полем "Введіть ім'я замітки"
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')

field_text = QTextEdit()
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')


# розташування віджетів по лейаутах
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)


col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)


col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)


col_2.addLayout(row_3)
col_2.addLayout(row_4)


layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)

notes_win.setLayout(layout_notes)

def show_note():
    # отримуємо текст із замітки з виділеною назвою та відображаємо її в полі редагування
    key = list_notes.selectedItems()[0].text()
    
    field_text.setText( notes[key]["текст"] )
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки: ")
    if ok and note_name != "":

        notes[note_name] = {"текст" : "", "теги" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()

        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=2)
        print(notes)

    else:
        print("Замітка для збереження не вибрана!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()

        del notes[key]

        list_notes.clear()
        list_tags.clear()
        field_text.clear()

        list_notes.addItems(notes)

        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
        
    else:
        print("Замітка для видалення не вибрана!")

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()

        tag = field_tag.text()

        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)

            list_tags.addItem(tag)
            
            field_tag.clear()
        
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
        
    else:
        print("Замітка для додавання не вибрана!")

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()

        notes[key]["теги"].remove(tag)

        list_tags.clear()

        list_tags.addItems(notes[key]["теги"])

        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
        
    else:
        print("Тег не вибраний для видалення!")

def search_tag():
    tag = field_tag.text()

    if button_tag_search.text() == "Шукати замітки по тегу" and tag:
        
        notes_filtered = {}# тут будуть замітки з виділеним тегом
        
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]

        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        
    elif button_tag_search.text() == "Скинути пошук":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Шукати замітки по тегу")
        
    else:
        pass

# --------- ПОДІЇ ---------

# при кліку на замітку викликається функція show_note
list_notes.itemClicked.connect(show_note)

button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

# --------- ЗАВАНТАЖЕННЯ ДАНИХ З JSON ---------

# читаємо замітки з файлу
with open("notes_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# додаємо назви заміток у список
list_notes.addItems(data)


# запуск програми
notes_win.show()

app.exec_()

#затем запрограммируй демо-версию функционала
