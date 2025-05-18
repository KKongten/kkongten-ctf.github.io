import time

target = 1337
i = 2**63  # 큰 숫자부터 시작

last_print = time.time()
while True:
    if hash(i) == target and i != target and all(c in '0123456789' for c in str(i)):
        print("Collision value found:", i)
        break

    i += 1

    # 1초에 한 번씩 진행 상황 출력
    if time.time() - last_print >= 60:
        print(f"Currently testing: {i}")
        last_print = time.time()
