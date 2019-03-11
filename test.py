from collections import deque
import time
import array as arr

items = arr.array('f')
times = arr.array('f')


try:
    x=9
    while True:
        x = x + 1
        for i in range(0, x):
            y = x
            if len(items) ==10:
                items = items.pop()
                times = times.pop()
            items.append(y)
            times.append(time.time())
            time.sleep(0.001)
            print(str(items) + ' ' + str(times))
except KeyboardInterrupt:
    exit(0)