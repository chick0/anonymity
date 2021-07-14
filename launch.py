from time import sleep
from datetime import datetime
from argparse import ArgumentParser
from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from multiprocessing import Process

from waitress import serve

from app import create_app


def task(port: int):
    try:
        print(f"- try to call cron at [{datetime.now().__str__().split('.')[0]}] ... ", end="")
        urlopen(f"http://localhost:{port}/cron", timeout=2)

        print("SUCCESS")
        sleep(5 * 60), task(port)
    except KeyboardInterrupt:
        pass
    except (URLError, HTTPError):
        print("FAILED. try again in 3 seconds...")
        sleep(3), task(port)


if __name__ == "__main__":
    parser = ArgumentParser(description="Anonymity Launcher")
    parser.add_argument("--set-port", metavar="PORT",
                        help="set the port number to run the waitress server",
                        action="store", type=int, default=8082)
    parser.add_argument("--no-cron-job",
                        help="disable cron job working with multiprocessing",
                        action="store_const", const=True)

    args = parser.parse_args()

    print(f"Starting 'Anonymity' with port number {args.port}")
    if args.no_cron_job is True:
        print("- cron job is disabled!")
        print("- You must register a curl command for the cron path with crontab.")
    else:
        p = Process(target=task, args=(args.port,))
        p.start()

    serve(app=create_app(), port=args.port)
