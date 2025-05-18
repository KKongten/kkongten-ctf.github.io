import wexpect
import string
import itertools
import time
import os

HOST = 'enabled.chal.cyberjousting.com'
PORT = 1352

SAVE_FILE = "last_command.txt"

default_args = [
    "1",
    "test",
    "\"hi\"",
    "x=1",
    "flag",
    "FLAG",
    "flag.txt",
    "help",
    "-a",
    "--help"
]

def send_cmd(child, cmd):
    child.sendline(cmd)
    try:
        child.expect('\n', timeout=2)
        output = child.before.decode(errors='ignore').strip()
    except Exception:
        output = "No response or timeout"
    return output

def load_last_command():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_command(cmd):
    with open(SAVE_FILE, "w") as f:
        f.write(cmd)

def generate_command_list():
    alphabet = string.ascii_lowercase
    cmds = []
    base_cmds = [''.join(c) for c in itertools.product(alphabet, repeat=2)]
    base_cmds += [''.join(c) for c in itertools.product(alphabet, repeat=3)]

    for cmd in base_cmds:
        for arg in default_args:
            cmds.append(f"{cmd} {arg}")
    return cmds

def main():
    commands = generate_command_list()

    last_cmd = load_last_command()
    start_index = 0
    if last_cmd:
        try:
            start_index = commands.index(last_cmd) + 1
            print(f"Resuming from command after: {last_cmd}")
        except ValueError:
            start_index = 0

    while start_index < len(commands):
        cmd = commands[start_index]
        print(f"[{start_index+1}/{len(commands)}] Trying command: {cmd}")

        try:
            child = wexpect.spawn(f"ncat {HOST} {PORT}")
            child.expect("Welcome to my new bash")
            time.sleep(0.1)

            output = send_cmd(child, cmd)
            print(f"[OUTPUT] {output}")

            child.close()

            save_last_command(cmd)
            start_index += 1

        except Exception as e:
            print(f"Connection lost or error: {e}")
            print("Reconnecting after 3 seconds...")
            time.sleep(3)

    print("All commands tested!")

if __name__ == "__main__":
    main()
