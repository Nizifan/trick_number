import random
import socket

s = socket.socket()


def data_compare(arr1, arr2):
    if len(arr1) != 2 or arr1[0] > '9' or arr1[0] < '1' or arr1[1] < '1' or arr1[1] > '6':
        return -1

    if arr1[1] == '1' and arr2[2] != '1':
        arr1[1] = '7'
    if arr1[0] < arr2[0] or (arr1[0] == arr2[0] and arr1[1] < arr2[1]):
        return 0
    else:
        return 1


def server():
    host = socket.gethostname()
    port = 6789

    s.bind((host, port))
    s.listen(5)

    c1, addr1 = s.accept()
    c2, addr2 = s.accept()

    numpool = []
    random1 = []
    for p in range(5):
        i = random.randint(1, 6)
        random1.append(i)
        numpool.append(i)
    random1.sort()
    random2 = []
    for p in range(5):
        i = random.randint(1, 6)
        random2.append(i)
        numpool.append(i)
    random2.sort()
    numpool.sort()
    c1.send(','.join(str(i) for i in random1))
    c2.send(','.join(str(i) for i in random2))


    used_one = 0
    number = 0
    count = 0
    str1 = ''
    data = []

    while True:
        while True:
            c1.send('1')
            str1 = c1.recv(1024)
            if str1 == '-1,0':
                c1.send('end this game')
                break
            data1 = str1.split(',')
            ret = data_compare(data1, (count, number))
            if ret == -1:
                c1.send('incorrect format: inquire 2 numbers')
                pass
            elif ret == 0:
                c1.send('you should put correct number/counts')
                pass
            elif ret == 1:
                c1.send('get your numbers' + str1)
                break

        if str1 == '-1,0':
            break

        if data1[1] == 1:
            used_one = 1

        count = data1[0]
        number = data1[1]

        c2.send("Another players raises" + str1)

        while True:
            c2.send('1')
            str2 = c2.recv(1024)
            if str2 == '-1,0':
                c2.send('end this game')
                break
            data2 = str2.split(',')
            ret = data_compare(data2, (count, number))
            if ret == -1:
                c2.send('incorrect format: inquire 2 numbers')
                pass
            elif ret == 0:
                c2.send('you should put correct number/counts')
                pass
            elif ret == 1:
                c2.send('get your numbers' + str2)
                break

        if str2 == '-1,0':
            break

        if data2[1] == 1:
            used_one = 1

        count = data2[0]
        number = data2[1]

        c1.send("Another players raises" + str2)

    c1.send("result" + ','.join(str(i) for i in numpool))
    c2.send("result" + ','.join(str(i) for i in numpool))
    c1.close()
    c2.close()

if __name__ == '__main__':
    server()
