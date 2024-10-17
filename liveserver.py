import http.server
import socketserver
import argparse
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Use the directory specified in the command line argument as the root directory
        path = super().translate_path(path)
        relpath = os.path.relpath(path, os.getcwd())
        print(os.path.join(self.directory, self.serve_dir, relpath))
        return os.path.join(self.directory, self.serve_dir, relpath)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Serve a directory over HTTP.')
    parser.add_argument('directory', type=str, help='The directory to serve')
    parser.add_argument('--port', type=int, default=8000, help='Port to serve on (default: 8000)')
    args = parser.parse_args()

    # Set up the HTTP server
    handler = CustomHTTPRequestHandler
    handler.serve_dir = args.directory
    with socketserver.TCPServer(("", args.port), handler) as httpd:
        print(f"Serving {args.directory} on port {args.port}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()