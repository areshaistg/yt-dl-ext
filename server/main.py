from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys
from pytube import YouTube

hostName = "localhost"
serverPort = 6969

OUTPUT_FOLDER = "D:/SORTED/audio/music"

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

            yt.streams.filter(only_audio=True).first().download(output_path=OUTPUT_FOLDER);
        else:
            print(f"[ERROR]: unreachable {path}", file=sys.stderr);

if __name__ == "__main__":
    print(f"[INFO]: Creating output folder: {OUTPUT_FOLDER}.");
    try:
        os.mkdir(OUTPUT_FOLDER)
    except FileExistsError:
        print("[INFO]: Output folder already exists.");

    server = HTTPServer((hostName, serverPort), MyServer);
    print(f"[INFO]: Server started http://{hostName}:{serverPort}");

    try:
        server.serve_forever();
    except KeyboardInterrupt:
        pass

    server.server_close();
    print("[INFO]: Server stopped.")
