from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys
from pytube import YouTube

hostName = "localhost"
serverPort = 32945

def get_configs_path():
    if os.name == "nt":
        return os.path.expanduser("~/AppData/Local/")
    elif os.name == "posix":
        return os.path.expanduser("~/.config/")

output_folder = None;
OUTPUT_CONFIG_NAME = "yt-dl-ext-path.txt";

def configure_output_folder():
    try:
        output_folder = input("Please enter path: ")
        with open(file_path, "w") as file:
            output_folder = file.write(output_folder);
            return output_folder
    except KeyboardInterrupt:
        return
    except OSError:
        print(f"[ERROR]: cannot open {file_path}.", file=sys.stderr);
        return

def get_output_folder():
    global output_folder;
    if output_folder:
        return output_folder;

    configs_path = get_configs_path()
    file_path = configs_path + OUTPUT_CONFIG_NAME

    if os.path.isfile(file_path):
        try:
            with open(file_path, "r") as file:
                output_folder = file.readline();
        except OSError:
            print(f"[ERROR]: cannot open {file_path}.", file=sys.stderr);
            return
    else:
        print("[INFO]: No output folder found");
        return configure_output_folder();
    return output_folder

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path;
        if path.startswith("/"):
            path = path[1:len(path)];

        if path.startswith("mp3?"):
            self.send_response(200);
            self.send_header("Content-type", "application/json");
            self.end_headers();

            url = path[len("mp3?"):len(path)];
            
            print(f"[INFO]: downloading {url}.");
            yt = YouTube(url);
            print(f"[INFO]: {yt.title}")

            yt.streams.filter(only_audio=True).first().download(output_path=output_folder);
        else:
            print(f"[ERROR]: unreachable {path}", file=sys.stderr);


def server():
    get_output_folder()
    if output_folder == None:
        print("\n[INFO]: no output folder, exiting.")
        exit(1)

    print(f"[INFO]: Output folder: {output_folder}")

    server = HTTPServer((hostName, serverPort), MyServer);
    print(f"[INFO]: Server started http://{hostName}:{serverPort}");

    try:
        server.serve_forever();
    except KeyboardInterrupt:
        pass

    server.server_close();
    print("[INFO]: Server stopped.")

def usage(program):
    print(f"{program} [SUBCOMMAND]")
    print("    path        print configured path, or set if does not exist.")
    print("         -s     force set path")

if __name__ == "__main__":
    argv = sys.argv;
    program = argv.pop(0);

    if len(argv) < 1:
        server();
    else:
        opt = argv.pop(0)
        if opt == "server":
            server();
        elif opt == "path":
            if "-s" in argv:
                if configure_output_folder() == None:
                    print("\n[INFO]: Cancel configuration.")
            else:
                print(get_output_folder());
        else:
            print(f"[ERROR]: subcommand unreachable: {opt}", file=sys.stderr);
            usage(program);
