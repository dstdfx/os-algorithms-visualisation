import threading
import time

from queue import PriorityQueue, Empty
from random import randint
from tkinter import *


class SJF:
    def __init__(self):
        self.data_queue = PriorityQueue()
        self.colors = ['red', 'green', 'brown', 'blue', 'black', 'purple', 'grey', 'orange', 'white', 'pink']
        self.x, self.y, self.x0, self.y0 = 35, 60, 25, 100
        self.log_x, self.log_y = 420, 25

    def logger(self, log):
        canvas.create_text(self.log_x, self.log_y, text=log)
        self.log_y += 20

    def producer(self):
        for c in self.colors:
            time.sleep(0.1)
            self.y0 = randint(3, 8) * 25
            element = canvas.create_rectangle([self.x0, self.x], [self.y0, self.y], fill=c)
            canvas.update()
            self.data_queue.put((self.y0, element, {'x0': self.x0, 'x': self.x, 'y0': self.y0, 'y': self.y}, c))
            self.x += 50
            self.y += 50

    def consumer(self):
        while True:
            try:
                time.sleep(1)
                data = self.data_queue.get(block=False)
                coordinates_dict = data[2]
                while coordinates_dict['y0'] > 25:
                    coordinates_dict['y0'] -= 25
                    canvas.coords(data[1], coordinates_dict['x0'], coordinates_dict['x'],
                                  coordinates_dict['y0'], coordinates_dict['y'])
                    canvas.update()
                    time.sleep(1)
                canvas.delete(data[1])
                self.logger('"{}" выполнен.'.format(data[3]))
            except Empty:
                pass

if __name__ == '__main__':

    root = Tk()
    lab = Label(root, text="Shortest job first", bg='blue', font=("Helvetica", 16))
    lab.pack()

    canvas = Canvas(root, width=550, height=600)
    canvas.create_text(110, 550, text='Очередь процессов')
    canvas.create_rectangle(10, 30, 220, 520, outline='red', width=3)
    canvas.pack()

    sjf = SJF()
    t_producer = threading.Thread(target=sjf.producer, name='Producer')
    t_producer.daemon = True
    t_producer.start()

    t_consumer = threading.Thread(target=sjf.consumer, name='Consumer')
    t_consumer.daemon = True
    t_consumer.start()

    root.mainloop()
