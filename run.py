import asyncio
import subprocess
from time import sleep

def stream_process(process):
    go = process.poll() is None
    for line in process.stdout:
        print(line.decode('utf8'), end="")
    return go

def main():
    process = subprocess.Popen(
        "flask --app simple_crud_api run --debug --reload".split(" "),
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT
        )
    while stream_process(process):
        sleep(0)
    return False

    
    
if __name__ == "__main__":
    main()