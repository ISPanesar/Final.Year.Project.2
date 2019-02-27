import threading
import queue
import time


def reeturn(x, y):
    return x, y


def reeturn2(x):
    return x * x


def reeturn3(y):
    return y ** y

for i in range(2):
    que = queue.Queue()
    que1 = queue.Queue()
    threads_list = list()

    t = threading.Thread(target=lambda q, arg1: q.put(reeturn(12, 15)), args=(que, 3))

    t3 = threading.Thread(target=lambda q, arg1: q.put(reeturn3(2*i)), args=(que1, 1))
    t.start()

    t3.start()
    threads_list.append(t)
    threads_list.clear()

    while not que.empty():
        values, values1 = que.get()
        print(str(values) + ' and ' + str(values1))

    time.sleep(1)
    print('swapping threads')
    time.sleep(1)


    t2 = threading.Thread(target=lambda q, arg1: q.put(reeturn2(13 *i)), args=(que, 2))
    t2.start()
    threads_list.append(t2)

    while not que.empty():
        values = que.get()
        print(values)


    while not que1.empty():
        time.sleep(1)
        print('test')
        time.sleep(1)
        values = que1.get()
        print(values)


