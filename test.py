from collections import deque
import time

items = []

try:
    x=9
    while True:
        x = x + 1
        for i in range(0, x):
            y = x
            z = time.time()
            if len(items) ==10:
                items = items.pop()
            lst = (y, z)
            items.append(lst)
            time.sleep(0.001)
            lst1, lst2 = zip(*items)
            print(str(lst1))
            print('next value')
            print(str(lst2))

except KeyboardInterrupt:
    exit(0)

