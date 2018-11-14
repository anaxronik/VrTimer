from tkinter import *
import time
import shelve


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


# Пытаемся получить значение переменной из файла если не находим то заменяем его значением по умолчанию
with shelve.open(settings_file) as var1:
    first_start = var1.get("first_start", first_start)
    font_label = var1.get("font_label", font_label)
    timer_start = var1.get("timer_start", timer_start)
    font_size = var1.get("font_size", font_size)
    seconds = var1.get("seconds", seconds)
    target_time = var1.get('target_time', target_time)


def set_target_time():
    global target_time
    target_time = varP.get()*60
    print('Выбранно целевое время', target_time, 'секунд.   ', time.strftime('%H:%M:%S', time.gmtime(target_time)))
    remain_label.configure(text=remain_label.configure(text=time.strftime('%H:%M:%S', time.gmtime(target_time))))
    with shelve.open(settings_file) as var:
        var['target_time'] = target_time


def plus_button_press():
    global font_size
    font_size += 1
    print(font_size)
    label1.configure(font=(font_label, font_size))
    remain_label.configure(font=(font_label, font_size))
    with shelve.open(settings_file) as var:
        var['font_size'] = font_size


def minus_button_press():
    global font_size
    font_size -= 1
    print(font_size)
    label1.configure(font=(font_label, font_size))
    remain_label.configure(font=(font_label, font_size))
    with shelve.open(settings_file) as var:
        var['font_size'] = font_size


def clear_button():
    btn_start.pack_forget()
    btn_pause.pack_forget()
    btn_continue.pack_forget()
    btn_close.pack_forget()
    btn_reset.pack_forget()


def tick():
    global seconds, after_id, target_time
    after_id = root.after(1000, tick)
    label1.configure(text=time.strftime('%H:%M:%S', time.gmtime(seconds)))
    if target_time == 0:
        remain_label.configure(text='ВЫБЕРИ ВРЕМЯ')
    else:
        if target_time - seconds < 0:
            remain_label.configure(text='ВРЕМЯ ВЫШЛО')
            remain_label.configure(bg='red')

        else:
            remain_label.configure(text=time.strftime('%H:%M:%S', time.gmtime(target_time - seconds)))
            remain_label.configure(bg='black')
    seconds += 1
    '''
    with shelve.open(settings_file) as var2:
        var2['seconds'] = seconds
    '''


def start_sw():
    global timer_start
    if not timer_start:
        tick()
        clear_button()
        btn_pause.pack(fill=BOTH, expand=1)
        btn_close.pack(fill=BOTH)
        btn_reset.pack(fill=BOTH, expand=1)
        label1.configure(bg='Black')
        remain_label.configure(bg='Black')
        timer_start = True


def pause_sw():
    global timer_start
    if timer_start:
        root.after_cancel(after_id)  # Остановить таймер
        clear_button()
        btn_continue.pack(fill=BOTH, expand=1)
        btn_close.pack(fill=BOTH)
        btn_reset.pack(fill=BOTH, expand=1)
        label1.configure(bg='green')
        remain_label.configure(bg='green')
        timer_start = False


def continue_sw():
    global timer_start
    if not timer_start:
        tick()
        clear_button()
        btn_pause.pack(fill=BOTH, expand=1)
        btn_close.pack(fill=BOTH)
        btn_reset.pack(fill=BOTH, expand=1)
        label1.configure(bg='Black')
        remain_label.configure(bg='Black')
        timer_start = True


def reset_sw():
    global after_id
    global seconds
    global timer_start
    pause_sw()
    after_id = root.after(1000, tick)
    root.after_cancel(after_id)  # Остановить таймер
    seconds = 0
    label1.configure(text='00:00:00')
    clear_button()
    btn_start.pack(fill=BOTH, expand=1)
    btn_close.pack(fill=BOTH)
    btn_reset.pack(fill=BOTH, expand=1)
    label1.configure(bg='green')
    remain_label.configure(bg='green')
    timer_start = False
    with shelve.open(settings_file) as var:
        var['seconds'] = 0


def close_program():
    with shelve.open(settings_file) as var2:
        var2['seconds'] = seconds

    sys.exit()


def hide_time_changer():
    print('def hide_time_changer():')
    global show_time_control

    if not show_time_control:
        print('Показываю панель добавления времени.')
        btn_hour_plus.pack(side=LEFT, fill=BOTH, expand=1)
        lbl_hour.pack(side=LEFT, fill=BOTH, expand=1)
        btn_hour_minus.pack(side=LEFT, fill=BOTH, expand=1)
        btn_min_plus.pack(side=LEFT, fill=BOTH, expand=1)
        lbl_min.pack(side=LEFT, fill=BOTH, expand=1)
        btn_min_minus.pack(side=LEFT, fill=BOTH, expand=1)
        btn_sec_plus.pack(side=LEFT, fill=BOTH, expand=1)
        lbl_sec.pack(side=LEFT, fill=BOTH, expand=1)
        btn_sec_minus.pack(side=LEFT, fill=BOTH, expand=1)
        show_time_control = True

    else:
        print('Скрываю панель добавления времени.')
        btn_hour_plus.forget()
        lbl_hour.forget()
        btn_hour_minus.forget()
        btn_min_plus.forget()
        lbl_min.forget()
        btn_min_minus.forget()
        btn_sec_plus.forget()
        lbl_sec.forget()
        btn_sec_minus.forget()
        show_time_control = False


def change_second(sec):
    print('def change_second():')
    print('Изменяю время на', sec, 'Секунд')
    global seconds
    if (seconds+sec) > 0:
        seconds = seconds + sec
        print('Время составляет ', seconds)
        label1.configure(text=time.strftime('%H:%M:%S', time.gmtime(seconds)))


#  Настройки главного окна
root = Tk()
root.wm_attributes('-topmost', 1)  # Окно поверх всех окон
root.overrideredirect(1)  # Убрать кнопку крестик итд и из панели задач
root.geometry('+0+0')


# Создание фрейма в котором будут располагаться кнопки
button_frame = Frame(root)
button_frame.pack(side=LEFT, fill=Y)


# Первичное Объявление кнопок кнопок
btn_start = Button(button_frame, text='▶', bg='#92A5E9', fg='white', command=start_sw)
btn_pause = Button(button_frame, text='||', bg='#92A5E9', fg='white', command=pause_sw)
btn_close = Button(button_frame, text='X', height=1, command=close_program)
btn_reset = Button(button_frame, text='⬛', bg='#E94B1B', fg='white', command=reset_sw)
btn_continue = Button(button_frame, text='▶', bg='#92A5E9', fg='white', command=continue_sw)

btn_sec_plus = Button(root, text='+', bg='green', command=lambda: change_second(1))
lbl_sec = Label(root, text='СЕК')
btn_sec_minus = Button(root, text='-', bg='#92A5E9', command=lambda: change_second(-1))
btn_min_plus = Button(root, text='+', bg='green', command=lambda: change_second(60))
lbl_min = Label(root, text='МИН')
btn_min_minus = Button(root, text='-', bg='#92A5E9', command=lambda: change_second(-60))
btn_hour_plus = Button(root, text='+', bg='green', command=lambda: change_second(3600))
lbl_hour = Label(root, text='ЧАС')
btn_hour_minus = Button(root, text='-', bg='#92A5E9', command=lambda: change_second(-3600))

# Первичное объявление циферблата

label1 = Label(root,
               font=(font_label, font_size),
               text=time.strftime('%H:%M:%S', time.gmtime(seconds)),
               bg='green',
               fg='white',
               anchor='w')


# Первичное расположение виджетов
btn_start.pack(fill=BOTH, expand=1)
btn_close.pack(fill=BOTH)
btn_reset.pack(fill=BOTH, expand=1)
label1.pack(side=TOP, fill='x')


#  Настройки  окна окна оставшегося времени
remain_window = Toplevel()
remain_window.wm_attributes('-topmost', 1)  # Окно поверх всех окон
remain_window.overrideredirect(1)  # Убрать кнопку крестик итд и из панели задач
remain_window.geometry('-0+0')


# Первичное объявление циферблата оставшегося времени
remain_label = Label(remain_window,
                     font=(font_label, font_size),
                     text='ВЫБЕРИ ВРЕМЯ',
                     bg='green',
                     fg='white',
                     anchor='w')


# Создание фрейма в котором будут располагаться кнопки
remain_button_frame = Frame(remain_window)


varP = IntVar()
varP.set(10)

# Первичное Объявление кнопок оставшегося времени

min_10 = Radiobutton(remain_button_frame, text="10", variable=varP, value=10, command=set_target_time)
min_20 = Radiobutton(remain_button_frame, text="20", variable=varP, value=20, command=set_target_time)
min_30 = Radiobutton(remain_button_frame, text="30", variable=varP, value=30, command=set_target_time)
min_60 = Radiobutton(remain_button_frame, text="60", variable=varP, value=60, command=set_target_time)
min_90 = Radiobutton(remain_button_frame, text="90", variable=varP, value=90, command=set_target_time)
min_120 = Radiobutton(remain_button_frame, text="120", variable=varP, value=120, command=set_target_time)


# Первичное расположение виджетов
remain_label.pack(fill='x')
remain_button_frame.pack()
min_10.pack(side=LEFT)
min_20.pack(side=LEFT)
min_30.pack(side=LEFT)
min_60.pack(side=LEFT)
min_90.pack(side=LEFT)
min_120.pack(side=LEFT)


# Задание горячих клавиш
root.bind('<Escape>', lambda event: close_program())
root.bind('<Return>', lambda event: start_sw())
root.bind('<BackSpace>', lambda event: reset_sw())
root.bind('<space>', lambda event: pause_sw())
root.bind('<+>', lambda event:  plus_button_press())
root.bind('<minus>', lambda event:  minus_button_press())
label1.bind("<Button-1>", lambda event:  hide_time_changer())


root.mainloop()
