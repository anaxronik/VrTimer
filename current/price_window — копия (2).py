from tkinter import *
import tkinter.ttk as ttk

# Задаем начальные переменные
first_start = True
font_label = 'Impact'
timer_start = False
font_size = 100
seconds = 0
settings_file = "Vr_timer_data"
after_id = ''
target_time = 0
show_time_control = False
time_interval = 5*60 # Период расчета цены в секудах

# Задаем начальные цены
# Интервал 10 минут
# Первая строчка цены для одного игрока
# вторая строчка цены для одного игрока
# Третья строчка цены для одного игрока
# Четвертая строчка цены для одного игрока
#                [0ми, 10м, 20м, 30м, 60м]
default_price = [[200, 200, 400, 500, 900],
                 [300, 300, 600, 800, 600],
                 [400, 400, 800, 1000, 400],
                 [400, 400, 800, 1000, 400],
                 ]


def calculate_price():
    print(default_price[0][1])
    print('Колличество игроков выбранно ', number_of_players.get()+1)
    print('Цены для этого колличества игроков ', default_price[number_of_players.get()])
    current_time_interval = seconds // time_interval
    print('Текущий отрезок времени ', current_time_interval)
    print('Текущий размер скидки', discount.get(), '%')
    price_with_discount = int(default_price[number_of_players.get()][current_time_interval]*((100-discount.get())/100))
    print('Сумма с учетом скидки ', price_with_discount)
    price_label.configure(text=(price_with_discount, 'р'))


def reset_calculate_button():
    number_of_players.set(0)
    discount.set(0)
    calculate_price()


price_window = Tk()
price_window.wm_attributes('-topmost', 1)  # Окно поверх всех окон
price_window.overrideredirect(1)  # Убрать кнопку крестик итд и из панели задач
price_window.geometry("+%d+0" % (price_window.winfo_screenwidth() // 2 - price_window.winfo_reqwidth() // 2))

number_of_players = IntVar()
number_of_players.set(0)

plr_rdb1 = Radiobutton(price_window, text="1", variable=number_of_players, value=0, command=calculate_price)
plr_rdb2 = Radiobutton(price_window, text="2", variable=number_of_players, value=1, command=calculate_price)
plr_rdb3 = Radiobutton(price_window, text="3", variable=number_of_players, value=2, command=calculate_price)
plr_rdb4 = Radiobutton(price_window, text="4", variable=number_of_players, value=3, command=calculate_price)

price_label = Label(price_window,
                    font=(font_label, font_size),
                    text='200 р',
                    bg='black',
                    fg='white')

label_discount = Label(text='Скидка')
label_percent = Label(text='%')

discount = IntVar()
discount.set(0)
discount_pole = ttk.Combobox(price_window, textvariable=discount,
                             values=['0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65',
                                     '70', '75', '80', '85', '90', '95', '100'])

calculate_button = Button(text='Расчитать', command=calculate_price)
reset_calculate_button = Button(text='o', command=reset_calculate_button)

plr_rdb1.grid(row=0, column=0)
plr_rdb2.grid(row=1, column=0)
plr_rdb3.grid(row=2, column=0)
plr_rdb4.grid(row=3, column=0)

price_label.grid(row=0, column=1, rowspan=4, columnspan=4, sticky=N + S + W + E)

label_discount.grid(row=4, column=1, sticky=EW)
discount_pole.grid(row=4, column=2, sticky=W)
label_percent.grid(row=4, column=3, sticky=W)
calculate_button.grid(row=4, column=4, sticky=N + S + W + E)
reset_calculate_button.grid(row=4, column=0, sticky=N + S + W + E)

price_window.mainloop()
