import socket

s = socket.socket()


def client():
    host = '192.168.16.206'
    port = 6789

    s.connect((host, port))

    print(s.recv(1024))

    while True:
        str1 = s.recv(1024)
        if len(str1) == 0:
            continue
        if str1 == '1':
            print('please input:')
            a = input()
            s.send(','.join(str(i) for i in a))
        elif str1.find('result') != -1:
            print(str1)
            break
        else:
            print(str1)


if __name__ == '__main__':
    client()
