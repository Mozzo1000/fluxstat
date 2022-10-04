import argparse
from threading import Timer
    

def main():
    parser = argparse.ArgumentParser("Fluxstat Server")
    parser.add_argument("-i", "--interval", type=int, default=5, help="How often to retrieve metrics from agents in seconds")
    parser.add_argument("-a", "--agent", type=str, nargs="+", default=["localhost"], help="IP address of agent(s) to retrieve metrics from. Multiple can be listed at the same time.")

    print(parser.parse_args().agent)
    interval = parser.parse_args().interval
    for i in parser.parse_args().agent:
        get_metrics(interval, i)

def get_metrics(interval, url):
        thread = Timer(interval, get_metrics, [interval, url])
        thread.start()
        print("Getting metrics : " + url)

if __name__ == "__main__":
    main()

