from tkinter import *
import tkinter.ttk as ttk
import shelve
import os
import socket
from tkinter import filedialog


class ControlButton:
    def __init__(self):
        self.settings_folder = 'users' + '//' + socket.gethostname()
        self.settings_file = self.settings_folder + '//' + "games_data"

        if os.path.exists(self.settings_folder):
            print('Фаил со списком игр найден')
        else:
            print('Фаил с настройками не найден. Создаю папку для его хранения')
            os.makedirs(self.settings_folder)

        self.default_games = \
            {
                'Игра 1': {'path': 'D:\py\shelve', 'process': 'steam', 'count': 0},
                'Игра 2': {'path': 'D:\py\shelve', 'process': 'steam', 'count': 0},
                'Игра 3': {'path': 'D:\py\shelve', 'process': 'steam', 'count': 0},
                'Игра 4': {'path': 'D:\py\shelve', 'process': 'steam', 'count': 0},
            }
        with shelve.open(self.settings_file) as var1:
            self.games = var1.get('games', self.default_games)

        self.root = Tk()
        self.root.overrideredirect(1)  # Убрать кнопку крестик итд и из панели задач
        self.root.geometry('+0+200')
        self.root.wm_attributes('-topmost', 1)  # Окно поверх всех окон
        self.root.resizable(False, False)
        self.show_button = Button(self.root, text='>\n>\n>', command=self.command_window)
        self.show_button.grid(rowspan=100, sticky='news')
        self.hide_button = Button(self.root, text='<\n<\n<', command=self.hide_window)

        self.button2 = Button(self.root, text='Steam', command=self.start_steam)
        self.button3 = Button(self.root, text='X', bg='#E81123', command=self.kill_steam)

        self.button5 = Button(self.root, text='Steam VR', command=self.start_steamvr)
        self.button6 = Button(self.root, text='X', bg='#E81123', command=self.kill_steamvr)

        self.but_opt = Button(self.root, text='↓↓↓ ИГРЫ ↓↓↓', command=self.game_list)
        self.button8 = Button(self.root, text='ЗАПУСТИТЬ', bg='#4B6EAF', command=self.start_program)
        self.chose_box = ttk.Combobox(self.root, values=list(self.games))
        self.button10 = Button(self.root, text='X', bg='#E81123', command=self.kill_process)

        self.root.mainloop()
        self.update_combobox

    def command_window(self):
        print('def command_window(self):')

        self.show_button.grid_forget()
        self.hide_button.grid(rowspan=100, sticky='nesw', )

        self.button2.grid(row=0, column=1, columnspan=2, sticky='nesw')
        self.button3.grid(row=0, column=3, sticky='nesw')

        self.button5.grid(row=1, column=1, columnspan=2, sticky='nesw')
        self.button6.grid(row=1, column=3, sticky='nesw')

        self.but_opt.grid(row=2, column=1, columnspan=3, sticky='news')
        self.chose_box.grid(row=3, column=1, columnspan=3, sticky='nesw')
        self.button8.grid(row=4, column=1, columnspan=2, sticky='nesw')
        self.button10.grid(row=4, column=3, sticky='nesw')

    def hide_window(self):
        self.hide_button.grid_forget()
        self.button2.grid_forget()
        self.button3.grid_forget()
        self.button5.grid_forget()
        self.button6.grid_forget()
        self.button8.grid_forget()
        self.chose_box.grid_forget()
        self.button10.grid_forget()
        self.but_opt.grid_forget()

        self.show_button.grid(rowspan=100, sticky='news')

    def game_list(self):
        self.game_list_window = Tk()
        self.game_list_window.geometry('740x200+200+200')
        self.game_list_window.title('Список запускаемых игр')
        self.game_list_window.resizable(False, False)


        self.selected_game = StringVar()
        self.chose_game = ttk.Combobox(self.game_list_window, textvariable=self.selected_game, values=list(self.games), postcommand=self.postcommand)
        self.chose_game.bind("<<ComboboxSelected>>", self.combo_box_command)
        self.chose_game.grid(row=0, column=0, columnspan=2, sticky='news', padx=5, pady=10)
        self.button_add = Button(self.game_list_window, text='Добавить', command=self.add_game).grid(row=0, column=2,
                                                                                                     sticky='news',
                                                                                                     padx=5, pady=10)
        self.button_delete = Button(self.game_list_window, text='Удалить', command=self.delete_game).grid(row=0, column=3, sticky='news', padx=5, pady=10)
        Label(self.game_list_window, text='Название').grid(row=1, column=0, sticky='news', padx=5, pady=0)
        Button(self.game_list_window, text='Путь к .EXE', command=self.insert_file_name).grid(row=2, column=0, sticky='news', padx=5, pady=0)
        Label(self.game_list_window, text='Имя процесса').grid(row=3, column=0, sticky='news', padx=5, pady=0)
        Label(self.game_list_window, text='Счетчик запусков').grid(row=4, column=0, sticky='news', padx=5, pady=0)

        self.name_entry = Entry(self.game_list_window, width=100)
        self.name_entry.grid(row=1, column=1, sticky='news', padx=5, pady=5, columnspan=100)

        self.exe_entry = Entry(self.game_list_window)
        self.exe_entry.grid(row=2, column=1, sticky='news', padx=5, pady=5, columnspan=100)

        self.process_entry = Entry(self.game_list_window)
        self.process_entry.grid(row=3, column=1, sticky='news', padx=5, pady=5, columnspan=100)

        self.run_count_entry = Entry(self.game_list_window)
        self.run_count_entry.grid(row=4, column=1, sticky='news', padx=5, pady=5, columnspan=100)

        self.button_save = Button(self.game_list_window, text='Сохранить', command=self.save_games)
        self.button_save.grid(row=5, column=0, columnspan=100, sticky='news', padx=5, pady=10)

    def add_game(self):
        print('def add_game(self):')
        self.games.update({('Игра ' + str(len(self.games) + 1)): {'path': r'C:\Program Files (x86)\Steam\steamapps\common\SteamVR\bin\win64\vrstartup.exe', 'process': 'steam', 'count': 0}})
        print('Добавленна ', list(self.games)[len(self.games)-1])

        self.update_combobox()  # Обновление комбобоксов
        self.update_games_file()
        self.chose_game.set('Игра ' + str(len(self.games)))
        self.update_entres()

    def delete_game(self):
        print('def delete_game(self):')
        del self.games[self.chose_game.get()]
        self.name_entry.delete(0, END)
        self.exe_entry.delete(0, END)
        self.process_entry.delete(0, END)
        self.run_count_entry.delete(0, END)

        self.update_combobox()  # Обновление комбобоксов
        self.update_games_file()

        self.chose_game.set('')

    def save_games(self):
        print('\ndef save_games(self):')

        self.games.update({self.name_entry.get(): {'path': self.exe_entry.get(), 'process': self.process_entry.get(), 'count': self.run_count_entry.get()}})

        self.update_combobox()# Обновление комбобоксов

        self.update_games_file()

    def postcommand(self):
        print('def postcommand(self):    Метод выполняемый при клике на комбобокс')
        self.update_combobox()  # Обновление комбобоксов

    def update_entres(self):
        self.name_entry.delete(0, END)
        self.name_entry.insert(0, self.chose_game.get())

        self.exe_entry.delete(0, END)
        self.exe_entry.insert(0, self.games[self.chose_game.get()]['path'])

        self.process_entry.delete(0, END)
        self.process_entry.insert(0, self.games[self.chose_game.get()]['process'])

        self.run_count_entry.delete(0, END)
        self.run_count_entry.insert(0, self.games[self.chose_game.get()]['count'])

    def combo_box_command(self, event):
        print('def combo_box_command(self, event):   метод выполняемый если в комбобоксе что-то выбрано')
        print('В комбобоксе выбранно ', self.chose_game.get())  # Выводим в консоль что было выбрано
        self.update_entres()

    def update_combobox(self):
        sorted_games_list = list(self.games.keys())
        sorted_games_list.sort()
        self.chose_game['values'] = sorted_games_list
        self.chose_box['values'] = sorted_games_list

    def update_games_file(self):
        sorted(self.games)
        with shelve.open(self.settings_file) as var:
            var['games'] = self.games

    def start_program(self):
        print('def start_program(self):')
        process = self.games[self.chose_box.get()]['path']
        os.startfile(process)

    def insert_file_name(self):
        game_file_name = filedialog.askopenfilename()
        print(game_file_name)
        self.exe_entry.delete(0, END)
        self.exe_entry.insert(0, game_file_name)

    def kill_process(self):
        print('\ndef kill_process(self):')
        process = self.games[self.chose_box.get()]['process']
        result = re.findall(r'[^,]+', process)
        print(result)

        for i in result:
            command = r'taskkill /f /im ' + '"' + i + '"'
            print(command)
            os.system(command)

    def start_steam(self):
        print('def start_steam(self):')
        process = 'C:\Program Files (x86)\Steam\Steam.exe'
        os.startfile(process)

    def start_steamvr(self):
        print('def start_steamvr(self):')
        print('def start_steam(self):')
        process = r'C:\Program Files (x86)\Steam\steamapps\common\SteamVR\bin\win64\vrstartup.exe'
        os.startfile(process)

    def kill_steam(self):
        print('def kill_steam(self):')
        os.system(r'taskkill /f /im ' + '"' + 'Steam.exe' + '"')

    def kill_steamvr(self):
        print('def kill_steamvr(self):')
        os.system(r'taskkill /f /im ' + '"' + 'vrcompositor.exe' + '"')
        os.system(r'taskkill /f /im ' + '"' + 'vrmonitor.exe' + '"')
        os.system(r'taskkill /f /im ' + '"' + 'vrserver.exe' + '"')
        os.system(r'taskkill /f /im ' + '"' + 'vrdashboar.exe' + '"')


if __name__ == '__main__':
    print('Программа запущенна')
    ControlButton()
