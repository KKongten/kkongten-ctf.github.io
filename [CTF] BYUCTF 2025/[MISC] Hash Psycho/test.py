import socket
import time

HOST = 'psycho.chal.cyberjousting.com'
PORT = 1353

def recv_until(s, keyword):
    data = b''
    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        data += chunk
        if keyword.encode() in data:
            break
    return data.decode()

def send_line(s, line):
    s.sendall((line + '\n').encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # 1) 환영 메시지 나오고 이름 입력 요청 기다리기
        print(recv_until(s, "Go ahead and tell me your name:"))

        # 2) 이름 입력
        send_line(s, "TTTTT")

        # 3) 이름 환영 메시지와 ID 입력 요청 대기
        print(recv_until(s, "Go ahead and choose that now:"))

        # 4) ID 입력 (1337 테스트)
        send_line(s, "9223372036854777141")

        # 5) id_ 검사 후 office 선택지 출력 대기
        print(recv_until(s, "Choose a door"))

        # 6) office 선택 (1 또는 2)
        send_line(s, "2")

        # 7) 결과 출력 (FLAG 또는 그 외)
        data = s.recv(4096)
        print(data.decode())

if __name__ == "__main__":
    main()
