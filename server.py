import http.server
import socketserver
import os
import webbrowser
PORT = 8000
DIRECTORY = os.path.join(os.getcwd(), 'excel_files')  # Adjust this path
import webbrowser

webbrowser.open('https://github.com/itsme-kavinkumar/excelfile/raw/main/jsw-copy.xlsx')
os.chdir(DIRECTORY)  # Change the current working directory to the specified directory

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()

webbrowser.open('https://github.com/itsme-kavinkumar/excelfile/raw/main/jsw-copy.xlsx')