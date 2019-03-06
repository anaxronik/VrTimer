import time
import winsound
from win32api import GetSystemMetrics
from scripts.ControlButton import *
from threading import Thread
from scripts.ControlButton import ControlButton
import multiprocessing


class VrTimerTimer(object):
    def __init__(self):
        self.settings_folder = 'users'+'//'+socket.gethostname()
        self.settings_file = self.settings_folder+'//'+"Vr_timer_data"
        self.timer_start = False
        self.seconds = 0
        self.control_button_open = False
        self.font_size = 50
        self.font = 'Impact'
        self.timer_window_x = 0
        self.timer_window_y = 0
        self.remain_window_x = 500
        self.remain_window_y = 500
        self.price_window_x = 500
        self.price_window_y = 0
        self.max_screen_x = GetSystemMetrics(0)
        self.max_screen_y = GetSystemMetrics(1)

    def start(self):
        self.make_settings_file()
        self.load_variables()
        self.config_timer_window()
        self.draw_timer_window()
        self.bind_for_root_window()
        self.config_remain_window()
        self.draw_remain_window()
        self.bind_for_remain_window()
        self.config_price_window()
        self.draw_price_window()
        self.bind_for_price_window()
        self.set_background_color('green', self.root)
        self.set_background_color('green', self.price_window)
        self.set_background_color('green', self.remain_window)
        control_button = Thread(target=ControlButton())
        control_button.start()
        self.root.mainloop()  # Запуск главной петли графической оболочки. Должен быть последним.

    def save_variables(self):
        with shelve.open(self.settings_file) as var:
            var['font_size'] = self.font_size
            var['timer_window_x'] = re.split('\+', self.root.geometry())[1]
            var['timer_window_y'] = re.split('\+', self.root.geometry())[2]
            var['remain_window_x'] = re.split('\+', self.remain_window.geometry())[1]
            var['remain_window_y'] = re.split('\+', self.remain_window.geometry())[2]
            var['price_window_x'] = re.split('\+', self.price_window.geometry())[1]
            var['price_window_y'] = re.split('\+', self.price_window.geometry())[2]

    def load_variables(self):
        with shelve.open(self.settings_file) as var1:
            self.font_size = var1.get("font_size", 50)
            self.font = var1.get('font', 'Impact')
            self.timer_window_x = var1.get("timer_window_x", 0)
            self.timer_window_y = var1.get("timer_window_y", 0)
            self.remain_window_x = var1.get("remain_window_x", 1000)
            self.remain_window_y = var1.get("remain_window_y", 0)
            self.price_window_x = var1.get("price_window_x", 500)
            self.price_window_y = var1.get("price_window_y", 0)

    def make_settings_file(self):
        if not os.path.exists(self.settings_folder):
            os.makedirs(self.settings_folder)

    def config_timer_window(self):
        self.root = Tk()
        self.root.overrideredirect(1)  # Убрать кнопку крестик итд и из панели задач
        self.root.geometry('+%s+%s' % (self.timer_window_x, self.timer_window_y))
        self.root.wm_attributes('-topmost', 1)  # Окно поверх всех окон
        self.root.resizable(False, False)
        self.root.configure(background='black')

        self.close_button = Button(self.root, text='X', bg='red', fg='White', command=self.close_program)
        self.fonts_plus = Button(self.root, text='+', bg='green', fg='white', command=lambda: self.set_font_size(1))
        self.fonts_minus = Button(self.root, text='-', bg='#92A5E9', fg='white', command=lambda: self.set_font_size(-1))

        self.timer_label_sec = Label(self.root, text='00', bg='black', fg='white', font=(self.font, self.font_size))
        self.timer_label_min = Label(self.root, text='00', bg='black', fg='white', font=(self.font, self.font_size))
        self.timer_label_hours = Label(self.root, text='00', bg='black', fg='white', font=(self.font, self.font_size))
        self.label_points = Label(self.root, text=':', bg='black', fg='white', font=(self.font, self.font_size))
        self.label_points2 = Label(self.root, text=':', bg='black', fg='white', font=(self.font, self.font_size))

        self.start_button = Button(self.root, text='▶', bg='#92A5E9', fg='white', command=self.start_timer)
        self.stop_button = Button(self.root, text='⬛', bg='#E94B1B', fg='white', command=self.stop_timer)
        self.pause_button = Button(self.root, text='||', bg='green', fg='white', command=self.pause_timer)

        self.plus_1_hour_button = Button(self.root, text='+1', bg='green', fg='white', command=lambda: self.set_seconds(60*60))
        self.minus_1_hour_button = Button(self.root, text='-1', bg='#92A5E9', fg='white', command=lambda: self.set_seconds(-60*60))
        self.plus_10_min_button = Button(self.root, text='+10', bg='green', fg='white', command=lambda: self.set_seconds(600))
        self.minus_10_min_button = Button(self.root, text='-10', bg='#92A5E9', fg='white', command=lambda: self.set_seconds(-600))
        self.plus_1_min_button = Button(self.root, text='+1', bg='green', fg='white', command=lambda: self.set_seconds(60))
        self.minus_1_min_button = Button(self.root, text='-1', bg='#92A5E9', fg='white', command=lambda: self.set_seconds(-60))
        self.plus_10_sec_button = Button(self.root, text='+10', bg='green', fg='white', command=lambda: self.set_seconds(10))
        self.minus_10_sec_button = Button(self.root, text='-10', bg='#92A5E9', fg='white', command=lambda: self.set_seconds(-10))
        self.plus_1_sec_button = Button(self.root, text='+1', bg='green', fg='white', command=lambda: self.set_seconds(1))
        self.minus_1_sec_button = Button(self.root, text='-1', bg='#92A5E9', fg='white', command=lambda: self.set_seconds(-1))
        self.fonts_plus = Button(self.root, text='+', bg='green', fg='white', command=lambda: self.set_font_size(1))
        self.fonts_minus = Button(self.root, text='-', bg='#92A5E9', fg='white', command=lambda: self.set_font_size(-1))
        self.proshlo_label = Label(self.root, text='П\nР\nО\nШ\nЛ\nО', fg='white', font=('', self.font_size//9))

    def draw_timer_window(self):
        self.start_button.grid(row=0, column=0, rowspan=2, sticky=N + S + W + E)
        self.stop_button.grid(row=2, column=0, rowspan=2, sticky=N + S + W + E)
        self.timer_label_hours.grid(row=1, column=1, rowspan=2, columnspan=2, sticky=N + S + W + E)
        self.timer_label_min.grid(row=1, column=4, columnspan=2, rowspan=2,  sticky=N + S + W + E)
        self.timer_label_sec.grid(row=1, column=7, columnspan=2, rowspan=2,  sticky=N + S + W + E)
        self.label_points.grid(row=1, column=3, rowspan=2, sticky=N+S+W+E)
        self.label_points2.grid(row=1, column=6, rowspan=2, sticky=N+S+W+E)
        self.proshlo_label.grid(row=0, column=10, rowspan=10, sticky=N+S+W+E)

    def bind_for_root_window(self):
        self.root.bind('<Button-3>', self.right_mouse_on_root)
        self.root.bind('<+>', lambda event: self.set_font_size(1))
        self.root.bind('<minus>', lambda event: self.set_font_size(-1))
        self.root.bind('<1>', lambda event: self.on_mouse_press(event))
        self.root.bind('<B1-Motion>', lambda event: self.on_mouse_move(event, self.root))

    @staticmethod
    def close_program():
        sys.exit()

    def set_font_size(self, font_size):
        self.font_size += font_size
        self.timer_label_sec.configure(font=(self.font, self.font_size))
        self.timer_label_min.configure(font=(self.font, self.font_size))
        self.timer_label_hours.configure(font=(self.font, self.font_size))
        self.label_points.configure(font=(self.font, self.font_size))
        self.label_points2.configure(font=(self.font, self.font_size))
        self.save_variables()
        self.remain_label.configure(font=(self.font, self.font_size))
        self.price_label.configure(font=(self.font, self.font_size))
        self.proshlo_label.configure(font=('', self.font_size//9))

    def start_timer(self):
        if not self.timer_start:
            self.tick()
            self.timer_start = True
            self.start_button.grid_forget()
            self.pause_button.grid(row=0, column=0, rowspan=2, sticky=N+S+W+E)
            self.say_time('start')

            self.set_background_color('black', self.root)
            self.set_background_color('black', self.price_window)
            self.set_background_color('black', self.remain_window)

    def stop_timer(self):
        if self.timer_start:
            self.root.after_cancel(self.after_id)
            self.seconds = 0
            self.set_timer_text()
            self.pause_button.grid_forget()
            self.start_button.grid(row=0, column=0, rowspan=2, sticky=N + S + W + E)
            self.timer_start = False
            self.say_time('reset')
            self.set_background_color('green', self.root)
            self.set_background_color('green', self.price_window)
            self.set_background_color('green', self.remain_window)
            self.discount_box.set(value=0)

    def pause_timer(self):
        self.root.after_cancel(self.after_id)
        self.pause_button.grid_forget()
        self.start_button.grid(row=0, column=0, rowspan=2, sticky=N + S + W + E)
        self.timer_start = False
        self.say_time('pause')

        self.set_background_color('green', self.root)
        self.set_background_color('green', self.price_window)
        self.set_background_color('green', self.remain_window)

    @staticmethod
    def say_time(second):
        if second == 'start':
            winsound.PlaySound('sound/start.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 'pause':
            winsound.PlaySound('sound/pause.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 'reset':
            winsound.PlaySound('sound/reset.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 'continue':
            winsound.PlaySound('sound/continue.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 'finish':
            winsound.PlaySound('sound/finish.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 5 * 60:
            winsound.PlaySound('sound/5.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 10 * 60:
            winsound.PlaySound('sound/10.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 15 * 60:
            winsound.PlaySound('sound/15.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 20 * 60:
            winsound.PlaySound('sound/20.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 30 * 60:
            winsound.PlaySound('sound/30.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 40 * 60:
            winsound.PlaySound('sound/40.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 50 * 60:
            winsound.PlaySound('sound/50.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 60 * 60:
            winsound.PlaySound('sound/60.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 75 * 60:
            winsound.PlaySound('sound/75.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 90 * 60:
            winsound.PlaySound('sound/90.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 105 * 60:
            winsound.PlaySound('sound/105.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 120 * 60:
            winsound.PlaySound('sound/120.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 150 * 60:
            winsound.PlaySound('sound/150.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if second == 180 * 60:
            winsound.PlaySound('sound/180.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    def set_seconds(self, delta):
        self.seconds += delta
        if self.seconds <= 0:
            self.seconds = 0
        self.set_timer_text()

    def right_mouse(self, *args):
        if self.control_button_open:
            self.forget_timer_control_button()
            self.control_button_open = False
        else:
            self.draw_timer_control_button()
            self.control_button_open = True

    def tick(self):
        self.after_id = self.root.after(1000, self.tick)
        self.seconds += 1
        self.set_timer_text()
        self.calculate_remain_time()
        self.say_time(self.seconds)
        self.calculate_price()

    def set_timer_text(self):
        hours = time.strftime('%H', time.gmtime(self.seconds))
        minutes = time.strftime('%M', time.gmtime(self.seconds))
        seconds = time.strftime('%S', time.gmtime(self.seconds))
        self.timer_label_hours.configure(text=hours)
        self.timer_label_min.configure(text=minutes)
        self.timer_label_sec.configure(text=seconds)

    def change_bg_color(self):
        if self.timer_start:
            self.timer_label_hours.configure(bg='Black')
            self.timer_label_min.configure(bg='Black')
            self.timer_label_sec.configure(bg='Black')
            self.label_points.configure(bg='Black')
            self.label_points2.configure(bg='Black')
        else:
            self.timer_label_hours.configure(bg='Green')
            self.timer_label_min.configure(bg='Green')
            self.timer_label_sec.configure(bg='Green')
            self.label_points.configure(bg='Green')
            self.label_points2.configure(bg='Green')

    def on_mouse_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_move(self, event, window):
        window_size = re.split('\+', window.geometry())[0]
        window_x_y = re.split('x', window_size)
        rect = re.fullmatch(r'\d+x\d+\+(?P<x>-?\d+)\+(?P<y>-?\d+)', window.geometry())
        x = int(rect['x']) + (event.x - self.start_x)
        if x <= 0:
            x = 0
        if x >= self.max_screen_x - int(window_x_y[0]):
            x = self.max_screen_x - int(window_x_y[0])
        y = int(rect['y']) + (event.y - self.start_y)
        if y <= 0:
            y = 0
        if y >= self.max_screen_y - int(window_x_y[1]):
            y = self.max_screen_y - int(window_x_y[1])

        window.geometry(f'+{x}+{y}')
        self.save_variables()

    def right_mouse_on_root(self, *args):
        if self.control_button_open:
            self.forget_timer_control_button()
            self.control_button_open = False
        else:
            self.draw_timer_control_button()
            self.control_button_open = True

    def draw_timer_control_button(self):
        self.plus_1_hour_button.grid(row=0, column=1, columnspan=2, sticky=N + S + W + E)
        self.plus_10_min_button.grid(row=0, column=4, sticky=N + S + W + E)
        self.plus_1_min_button.grid(row=0, column=5, sticky=N + S + W + E)
        self.plus_10_sec_button.grid(row=0, column=7, sticky=N + S + W + E)
        self.plus_1_sec_button.grid(row=0, column=8, sticky=N + S + W + E)
        self.minus_1_hour_button.grid(row=3, column=1, columnspan=2, sticky=N + S + W + E)
        self.minus_10_min_button.grid(row=3, column=4, sticky=N + S + W + E)
        self.minus_1_min_button.grid(row=3, column=5, sticky=N + S + W + E)
        self.minus_10_sec_button.grid(row=3, column=7, sticky=N + S + W + E)
        self.minus_1_sec_button.grid(row=3, column=8, sticky=N + S + W + E)
        self.fonts_plus.grid(row=1, column=9, sticky=N + S + W + E)
        self.fonts_minus.grid(row=2, column=9, sticky=N + S + W + E)
        self.close_button.grid(row=0, column=9,sticky=N + S + W + E)

    def forget_timer_control_button(self):
        self.plus_1_hour_button.grid_forget()
        self.plus_10_min_button.grid_forget()
        self.plus_1_min_button.grid_forget()
        self.plus_10_sec_button.grid_forget()
        self.plus_1_sec_button.grid_forget()
        self.minus_1_hour_button.grid_forget()
        self.minus_10_min_button.grid_forget()
        self.minus_1_min_button.grid_forget()
        self.minus_10_sec_button.grid_forget()
        self.minus_1_sec_button.grid_forget()
        self.fonts_plus.grid_forget()
        self.fonts_minus.grid_forget()
        self.close_button.grid_forget()

    def config_remain_window(self):
        self.remain_window = Tk()
        self.remain_window.wm_attributes('-topmost', 1)  # Окно поверх всех окон
        self.remain_window.overrideredirect(1)  # Убрать кнопку крестик итд и из панели задач
        self.remain_window.geometry('+%s+%s' % (self.remain_window_x, self.remain_window_y))
        self.remain_window.resizable(False, False)
        self.remain_window.configure(background='black')
        self.remain_label = Label(self.remain_window, font=(self.font, self.font_size), text='00:00:00', fg='white')
        self.remain_time_box = ttk.Combobox(self.remain_window, width=2)
        self.remain_time_box.config(values=('', 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 90, 120, 150, 180))
        self.minutes_label = Label(self.remain_window, text='ОСТАЛОСЬ', bg='green', fg='white')

    def draw_remain_window(self):
        self.remain_label.grid(row=0, column=0, columnspan=2, sticky=N+S+W+E)
        self.remain_time_box.grid(row=1, column=0, sticky=N+S+W+E)
        self.minutes_label.grid(row=1, column=1, sticky=N+S+W+E)

    def bind_for_remain_window(self):
        self.remain_window.bind('<1>', lambda event: self.on_mouse_press(event))
        self.remain_window.bind('<B1-Motion>', lambda event: self.on_mouse_move(event, self.remain_window))
        #self.remain_window.bind('<3>', lambda event: self.update_font_size(event))

    def config_price_window(self):
        self.price_window = Tk()
        self.price_window.wm_attributes('-topmost', 1)  # Окно поверх всех окон
        self.price_window.overrideredirect(1)  # Убрать кнопку крестик итд и из панели задач
        self.price_window.geometry('+%s+%s' % (self.price_window_x, self.price_window_y))
        self.price_window.resizable(False, False)
        self.price_window.configure(background='black')

        self.price_label = Label(self.price_window, font=(self.font, self.font_size), text='0 р', bg='green', fg='white')
        self.players_box = ttk.Combobox(self.price_window, width=5, values=(1, 2, 3, 4))
        self.players_label = Label(self.price_window, text='ИГРОКОВ', bg='green', fg='white')

        self.discount_box = ttk.Combobox(self.price_window, width=5)
        self.discount_box.config(values=(0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 65, 70, 75, 80, 85, 90, 95, 100))
        self.discount_label = Label(self.price_window, text='%', bg='green', fg='white')

    def draw_price_window(self):
        self.price_label.grid(row=0, column=0, columnspan=4, sticky=N+S+W+E)
        self.players_box.grid(row=1, column=0, sticky=N+S+W+E)
        self.players_label.grid(row=1, column=1, sticky=N+S+W+E)
        self.discount_box.grid(row=1, column=2, sticky=N+S+W+E)
        self.discount_label.grid(row=1, column=3, sticky=N+S+W+E)
        self.players_box.set(value=1)
        self.discount_box.set(value=0)

    def bind_for_price_window(self):
        self.price_window.bind('<1>', lambda event: self.on_mouse_press(event))
        self.price_label.bind('<B1-Motion>', lambda event: self.on_mouse_move(event, self.price_window))

    def calculate_remain_time(self):
        target_time_text = self.remain_time_box.get()
        if not target_time_text:
            label_text = '00:00:00'

        else:
            target_time = int(target_time_text)*60
            remain_time = target_time - self.seconds
            label_text = time.strftime('%H:%M:%S', time.gmtime(remain_time))

            if remain_time == -2:
                self.say_time('finish')
            if remain_time <= 0:
                label_text = 'КОНЕЦ'
                self.set_background_color('red', self.root)
                self.set_background_color('red', self.price_window)
                self.set_background_color('red', self.remain_window)

        self.remain_label.config(text=label_text)

    def set_background_color(self, color, window):
            for widget in window.winfo_children():
                try:
                    widget.config(bg=color)
                except:
                    pass

    def set_label_size(self):
        pass

    def calculate_price(self):
        default_price = [
            ['200', '200', '200', '300', '400', '450', '500', '550', '600', '700', '800', '850', '900', '950', '1000', '1050', '1100', '1100', '1150', '1150', '1200', '1250', '1250', '1300', '1300', '1350', '1350', '1400', '1400', '1450','1500', '1550', '1600', '1650', '1700', '1750', '1800'],
            ['300', '300', '300', '500', '600', '700', '800', '900', '1050', '1200', '1350', '1500', '1600', '1700', '1800', '1900', '2000', '2050', '2100', '2150', '2200', '2200', '2250', '2300', '2400', '2500', '2600', '2650', '2700', '2750', '2900', '3000', '3050', '3050', '3100', '3150', '3200'],
            ['400', '400', '400', '600', '800', '900', '1000', '1200', '1350', '1500', '1700', '1900', '2000', '2100', '2200', '2300', '2400', '2450', '2500', '2550', '2600', '2700', '2900', '2950', '3000', '3100', '3200', '3300', '3400', '3500', '3600', '3650', '3700', '3750', '3800', '3900', '4000'],
            ['500', '500', '500', '750', '1000', '1100', '1200', '1400', '1600', '1800', '2000', '2150', '2300', '2400', '2600', '2700', '2900', '3000', '3100', '3200', '3300', '3350', '3400', '3450', '3500', '3600', '3700', '3800', '3900', '4000', '4100', '4200', '4300', '4400', '4500', '4600', '4700']
            ]
        players = int(self.players_box.get())-1
        time_interval = int(self.seconds // 60//5)
        discount = (100 - int(self.discount_box.get()))/100

        price = str(int(float(default_price[players][time_interval])*discount)) + 'р'

        self.price_label.config(text=price)

    def return_seconds(self):
        return self.seconds


def receive():
    global vr_timer
    print('сервер запущен')
    udp_port = 5678
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', udp_port))
    while True:
        data = sock.recv(1024)
        data = data.decode()
        if not data:
            break
        print('полученно сообщение: ', data)
        # print(sock)

        if data == '10':
            try:
                print('СООБЩЕНИЕ НОМЕР НОЛЬ')
                print(vr_timer.return_seconds)
            except:
                print('error')
    sock.close()


def create_timer():
    global vr_timer
    vr_timer = VrTimerTimer()
    vr_timer.start()


if __name__ == "__main__":
    timer_process = multiprocessing.Process(target=create_timer)
    timer_process.start()

    listner_process = multiprocessing.Process(target=receive)
    listner_process.start()




