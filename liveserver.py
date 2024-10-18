import http.server
import socketserver
import argparse
import os
import glob
import time

# Global variable to store the Unix timestamp
startfrompl = None
starttime = None

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Use the directory specified in the command line argument as the root directory
        path = super().translate_path(path)

        if path.endswith("/video.m3u8"):
            if startfrompl is not None:
                # Calculate the time difference between the Unix timestamp of the .m3u8 file and the current time
                diff = int(time.time()) - starttime
                # Calculate the Unix timestamp of the .m3u8 file
                timestamp = startfrompl + diff
                if not os.path.exists(os.path.join(self.serve_dir, f"{timestamp}.m3u8")):
                    # If the .m3u8 file with the calculated Unix timestamp does not exist, try the next one
                    timestamp += 1
                # Replace the placeholder with the calculated Unix timestamp
                path = path.replace("video.m3u8", f"{timestamp}.m3u8")
                print("Serving .m3u8 file with timestamp:", path)

        relpath = os.path.relpath(path, os.getcwd())
        print(os.path.join(self.directory, self.serve_dir, relpath))
        return os.path.join(self.directory, self.serve_dir, relpath)

def main():
    global startfrompl, starttime

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Serve a directory over HTTP.')
    parser.add_argument('directory', type=str, help='The directory to serve')
    parser.add_argument('--port', type=int, default=8000, help='Port to serve on (default: 8000)')
    args = parser.parse_args()

    # Find the .m3u8 file with the least number in its name
    m3u8_files = glob.glob(os.path.join(args.directory, '*.m3u8'))
    if m3u8_files:
        min_file = min(m3u8_files, key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
        startfrompl = int(os.path.splitext(os.path.basename(min_file))[0])
        print(f"Found starting .m3u8 file: {min_file}")
        starttime = int(time.time())

    # Set up the HTTP server
    handler = CustomHTTPRequestHandler
    handler.serve_dir = args.directory
    with socketserver.TCPServer(("", args.port), handler) as httpd:
        httpd.allow_reuse_address = True
        print(f"Serving {args.directory} on port {args.port}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()