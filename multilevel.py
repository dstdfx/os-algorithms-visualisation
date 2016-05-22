import threading
import time

from tkinter import *
from random import randint, choice
from queue import Empty, PriorityQueue

from first_come_first_served import FCFS
from round_robin import RR
from shortest_job_first import SJF


root = Tk()
canvas = Canvas(root, width=800, height=600)
canvas.pack()


class _FCFS(FCFS):
    def __init__(self):
        super(_FCFS, self).__init__()
        self.x, self.y, self.x0, self.y0 = 35, 60, 770, 600
        # self.log_x, self.log_y = 420, 25
        canvas.create_rectangle(780, 30, 590, 520, outline='red', width=3)

    def producer(self):
        for c in self.colors:
            self.x0 = randint(26, 31) * 25
            element = canvas.create_rectangle([self.x0, self.x], [self.y0, self.y], fill=c)
            canvas.update()
            self.data_queue.put((element, {'x0': self.x0, 'x': self.x, 'y0': self.y0, 'y': self.y}, c))
            time.sleep(0.1)
            self.x += 50
            self.y += 50

    def consumer(self):
        while True:
            try:
                time.sleep(1)
                data = self.data_queue.get(block=False)
                coordinates_dict = data[1]
                while coordinates_dict['x0'] > 640:
                    coordinates_dict['x0'] -= 50
                    canvas.coords(data[0], coordinates_dict['x0'], coordinates_dict['x'],
                                  coordinates_dict['y0'], coordinates_dict['y'])
                    canvas.update()
                    time.sleep(1)
                canvas.delete(data[0])
            except Empty:
                break

    def runner(self):
        t_producer = threading.Thread(target=self.producer)
        t_producer.start()
        t_consumer = threading.Thread(target=self.consumer)
        t_consumer.start()

        t_producer.join()
        t_consumer.join()


class _RR(RR):
    def __init__(self):
        super(_RR, self).__init__()
        self.x, self.y, self.x0, self.y0 = 35, 60, 770, 600
        # self.log_x, self.log_y = 420, 25
        canvas.create_rectangle(780, 30, 590, 520, outline='red', width=3)

    def producer(self):
        for c in self.colors:
            self.x0 = randint(26, 31) * 25
            element = canvas.create_rectangle([self.x0, self.x], [self.y0, self.y], fill=c)
            canvas.update()
            self.data_queue.put((element, {'x0': self.x0, 'x': self.x, 'y0': self.y0, 'y': self.y}, c))
            time.sleep(0.1)
            self.x += 50
            self.y += 50

    def consumer(self):
        while True:
            try:
                time.sleep(1.5)
                data = self.data_queue.get(block=False)
                coordinates_dict = data[1]
                coordinates_dict['x0'] -= 50
                if coordinates_dict['x0'] > 640:
                    canvas.coords(data[0], coordinates_dict['x0'], coordinates_dict['x'],
                                  coordinates_dict['y0'], coordinates_dict['y'])
                    canvas.update()
                    self.data_queue.put((data[0], coordinates_dict, data[2]))
                else:
                    canvas.delete(data[0])
            except Empty:
                break

    def runner(self):
        t_producer = threading.Thread(target=self.producer)
        t_producer.start()
        t_consumer = threading.Thread(target=self.consumer)
        t_consumer.start()

        t_producer.join()
        t_consumer.join()


class _SJF(SJF):
    def __init__(self):
        super(_SJF, self).__init__()
        self.x, self.y, self.x0, self.y0 = 35, 60, 770, 600
        canvas.create_rectangle(780, 30, 590, 520, outline='red', width=3)

    def producer(self):
        for c in self.colors:
            time.sleep(0.1)
            self.x0 = randint(26, 31) * 25
            element = canvas.create_rectangle([self.x0, self.x], [self.y0, self.y], fill=c)
            canvas.update()
            self.data_queue.put((self.x0, element, {'x0': self.x0, 'x': self.x, 'y0': self.y0, 'y': self.y}, c))
            self.x += 50
            self.y += 50

    def consumer(self):
        while True:
            try:
                time.sleep(1)
                data = self.data_queue.get(block=False)
                coordinates_dict = data[2]
                while coordinates_dict['x0'] > 640:
                    coordinates_dict['x0'] -= 50
                    canvas.coords(data[1], coordinates_dict['x0'], coordinates_dict['x'],
                                  coordinates_dict['y0'], coordinates_dict['y'])
                    canvas.update()
                    time.sleep(1)
                canvas.delete(data[1])
            except Empty:
                break

    def runner(self):
        t_producer = threading.Thread(target=self.producer)
        t_producer.start()
        t_consumer = threading.Thread(target=self.consumer)
        t_consumer.start()

        t_producer.join()
        t_consumer.join()


class MultilevelQueue:
    def __init__(self):
        canvas.create_text(40, 550, text="Multilevel queue", anchor='w', font="Helvetica 16")
        self.alg_title = canvas.create_text(670, 550, text="", anchor='w', font="Helvetica 16")
        canvas.create_rectangle(10, 30, 220, 520, outline='red', width=3)
        canvas.pack()
        self.random_algorithms = [('FCFS', _FCFS), ('RR', _RR), ('SJF', _SJF)]
        self.proces_q = ['red', 'green', 'brown', 'blue', 'yellow', 'purple', 'grey', 'orange', 'white', 'pink']
        self.data_queue = PriorityQueue()
        self.x, self.y, self.x0, self.y0 = 35, 60, 20, 210
        self.text_x, self.text_y = 110, 45
        self.log_x, self.log_y = 420, 25

    def logger(self, log):
        canvas.create_text(self.log_x, self.log_y, text=log, font="Helvetica 12")
        canvas.update()
        self.log_y += 20

    def producer(self):
        for index, c in enumerate(self.proces_q):
            time.sleep(0.1)
            element = canvas.create_rectangle([self.x0, self.x], [self.y0, self.y], fill=c)
            current_algorithm = choice(self.random_algorithms)
            text_to_p = '{} "{}" с приоритетом {}'.format(current_algorithm[0], c, index)
            el_text = canvas.create_text(self.text_x, self.text_y, text=text_to_p)
            canvas.update()
            self.data_queue.put((element, current_algorithm, {'x0': self.x0, 'x': self.x, 'y0': self.y0, 'y': self.y}, c,
                                 text_to_p, el_text))
            self.x += 50
            self.y += 50
            self.text_y += 50

    def consumer(self):
        while True:
            try:
                data = self.data_queue.get(block=False)
                self.logger('Выполнение {}'.format(data[-2]))
                canvas.itemconfig(self.alg_title, text="{}".format(data[1][0]))
                data[1][1]().runner() # Class().runner()

                self.logger('{} выполнен.'.format(data[3]))
                canvas.delete(data[0])
                canvas.delete(data[-1])
            except Empty:
                pass


multi = MultilevelQueue()
t_producer = threading.Thread(target=multi.producer)
t_producer.daemon = True
t_producer.start()

t_consumer = threading.Thread(target=multi.consumer)
t_consumer.daemon = True
t_consumer.start()

root.mainloop()