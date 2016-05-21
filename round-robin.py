import threading
import time

from queue import Queue, Empty
from random import randint
from tkinter import *


root = Tk()
lab = Label(root, text="Round Robin", bg='blue', font=("Helvetica", 16))
lab.pack()

canvas = Canvas(root, width=550, height=600)
canvas.create_text(110, 550, text='Очередь процессов')
canvas.create_rectangle(10, 30, 220, 520, outline='red', width=3)
canvas.pack()

data_queue = Queue()

colors = ['red', 'green', 'brown', 'blue', 'black', 'purple', 'grey', 'orange', 'white', 'pink']

x, y, x0, y0 = 35, 60, 25, 100
log_x, log_y = 420, 25


def logger(log):
    global log_x, log_y
    canvas.create_text(log_x, log_y, text=log)
    log_y += 20


def producer():
    global x, y, y0
    for c in colors:
        y0 = randint(3, 8) * 25
        time.sleep(0.1)
        element = canvas.create_rectangle([x0, x], [y0, y], fill=c)
        canvas.update()
        data_queue.put((element, {'x0': x0, 'x': x, 'y0': y0, 'y': y}, c))
        x += 50
        y += 50


def consumer():
    while True:
        try:
            time.sleep(1.5)
            data = data_queue.get()
            coordinates_dict = data[1]
            coordinates_dict['y0'] -= 25
            if coordinates_dict['y0'] > 25:
                canvas.coords(data[0], coordinates_dict['x0'], coordinates_dict['x'],
                              coordinates_dict['y0'], coordinates_dict['y'])
                canvas.update()
                data_queue.put((data[0], coordinates_dict, data[2]))
            else:
                canvas.delete(data[0])
                logger('"{}" выполнен'.format(data[2]))
        except Empty:
            pass


t_producer = threading.Thread(target=producer, name='Producer')
t_producer.daemon = True
t_producer.start()

t_consumer = threading.Thread(target=consumer, name='Consumer')
t_consumer.daemon = True
t_consumer.start()

root.mainloop()
