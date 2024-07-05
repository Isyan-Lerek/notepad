from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout


import json

notes = []
app = QApplication([])


#App interface
#app window parameters
notes_win = QWidget()
notes_win.setWindowTitle('Simple Notes')
notes_win.resize(900, 700)


#app window widgets
list_notes = QListWidget()
list_notes_label = QLabel('Daftar Catatan')


button_note_create = QPushButton('Buat Catatan') #a window with field "Enter note name" appears
button_note_del = QPushButton('Hapus catatan')
button_note_save = QPushButton('Simpan catatan')


field_tag = QLineEdit('')
field_tag.setPlaceholderText('Masukan tag...')
field_text = QTextEdit()
button_tag_add = QPushButton('Tambahkan Tag')
button_tag_del = QPushButton('Hapus tag catatan')
button_tag_search = QPushButton('Cari catatan dengan tag')
list_tags = QListWidget()
list_tags_label = QLabel('Daftar Tags')


#arrangement of widgets by layouts
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


#App functionality


#Working with note text
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Add note", "Note name: ")
    if ok and note_name != "":
        note = list()
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note[0])
        list_tags.addItems(note[2])
        print(notes)
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0]+'\n')


def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                with open(str(index)+".txt", "w") as file:
                    file.write(note[0]+'\n')
                    file.write(note[1]+'\n')
                    for tag in note[2]:
                        file.write(tag+' ')
                    file.write('\n')
            index += 1
        print(notes)
    else:
        print("Note to save is not selected!")



def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text() #note yang dipilih
        for note in notes:
            if note[0] == key:
                list_tags.clear()
                field_tag.clear()
                #masukan list yg sudah diperbarui
                list_notes.takeItem(list_notes.currentRow())
                notes.remove(note)
        #notes=> note=["A", "aloheuvue", ["asal"]]
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0]+'\n')
        print(notes)
    else:
        print("Please select a note!")


#Working with note tags
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        for note in notes:
            if note[0] == key and note[2] != tag:
                note[2] = tag
                list_tags.addItem(tag)
                field_tag.clear()
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0]+'\n')
        print(notes)
    else:
        print("Please select a note!")


def del_tag():
    #cek dulu, apakah kita pilih note A / note B /dll
    if list_notes.selectedItems():
        #cari tau judul note yg kita pilih
        key = list_notes.selectedItems()[0].text()
        #cari tau tag dari note yg kita pilih
        tag = list_tags.selectedItems()[0].text()
        #setelah tau, baru remove
        for note in notes:
            if note[0] == key and note[2] == tag:
                list_notes.clear()
                field_tag.clear()
                list_tags.takeItem(list_tags.currentRow())
                notes.remove(note)
        #kita simpen ke dalam json file
        #json file berisikan semua data
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0]+'\n')
        print(notes)
    else:
        print("note yang tag nya mau di delete, belum dipilih")


def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Search notes by tag" and tag:
        print(tag)
        notes_filtered = {} #notes with the highlighted tag will be here
        for note in notes:
            if tag in notes[note]["tags"]: 
                notes_filtered[note]=notes[note]
        button_tag_search.setText("Reset search")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == "Reset search":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Search notes by tag")
        print(button_tag_search.text())
    else:
        pass
    
#App startup
#attaching event handling
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)


#app startup 
notes_win.show()
app.exec_()