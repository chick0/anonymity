from argparse import ArgumentParser

from waitress import serve

from app import create_app

if __name__ == "__main__":
    parser = ArgumentParser(description="Anonymity Launcher")
    parser.add_argument("-p", "--port",
                        help="set port number (default:8082)",
                        action="store", type=int, default=8082)

    args = parser.parse_args()

    app = create_app()
    print(f"Starting 'Anonymity' with port number {args.port}")
    serve(app=app, port=args.port)
