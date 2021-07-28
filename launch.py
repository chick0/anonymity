from argparse import ArgumentParser

from waitress import serve

from app import create_app


if __name__ == "__main__":
    parser = ArgumentParser(description="Anonymity Launcher")
    parser.add_argument("--set-port", metavar="PORT",
                        help="set the port number to run the waitress server",
                        action="store", type=int, default=8082)

    args = parser.parse_args()

    print(f"Starting 'Anonymity' with port number {args.set_port}")
    serve(app=create_app(), port=args.set_port)
