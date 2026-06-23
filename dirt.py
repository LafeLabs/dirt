import base64
import copy
import io
import json
from pathlib import Path
import socket
import time
import urllib.parse
import urllib.request

import matplotlib.pyplot as plt
import numpy as np
with open("dirt.json", "r", encoding="utf-8") as file:
    file_contents = file.read()
dirt = json.loads(file_contents)
previous_dirt = copy.deepcopy(dirt)

python_response = {}
python_response['data'] = {}
python_response['data']['ace_mode'] = 'text'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen(5)
    server.settimeout(0.5)
    print("=== LIVE SERVER ACTIVE ===")
    try:
        while True:
            try:
                conn, addr = server.accept()
            except socket.timeout:
                continue 
            with conn:
                raw_web_input = conn.makefile('r', encoding='utf-8').readline()
                if not raw_web_input:
                    continue
                try:
                    dirt = json.loads(raw_web_input.strip())# get dirt
                except (json.JSONDecodeError, ValueError):
                    pass
                

                
                # use Python to take dirt and create response to send
                python_response['text'] = "z = "  + str(dirt['mouse']['z']) +  "PYTHON-----" + dirt['text'] + "-----PYTHON"
                
                python_response['data']['xlabel'] = 'x'
                python_response['data']['ylabel'] = 'y'
                python_response['data']['ymin'] = 1023
                python_response['data']['ymax'] = 0

                if dirt['text'] == 'html':
                    python_response['data']['ace_mode'] = "html"
                if dirt['text'] == 'json':
                    python_response['data']['ace_mode'] = "json"
                if dirt['text'] == 'markdown':
                    python_response['data']['ace_mode'] = "markdown"
                if dirt['text'] == 'python':
                    python_response['data']['ace_mode'] = "python"


                plt.cla()
                plt.figure(figsize=(6, 6))
                for stroke in dirt['icon']:
                    xdata = [point['x'] for point in stroke]
                    ydata = [point['y'] for point in stroke]
                    xdata += 8*np.random.randn(len(xdata))
                    ydata += 8*np.random.randn(len(xdata))
                    plt.plot(xdata, ydata, color='black', linewidth=10, solid_capstyle='round')

                plt.xlim(0, 1023)
                plt.ylim(python_response['data']['ymin'], python_response['data']['ymax'])
                plt.xlabel(python_response['data']['xlabel'])
                plt.ylabel(python_response['data']['ylabel'])        
                plt.tight_layout()
                img_buf = io.BytesIO()
                plt.savefig(img_buf, format='png')
                plt.close()
                img_buf.seek(0)
                b64_string = base64.b64encode(img_buf.read()).decode('utf-8')
                imagedata = f"data:image/png;base64,{b64_string}"
                python_response['image'] = imagedata                
                payload = json.dumps(python_response) + "\n"
                conn.sendall(payload.encode('utf-8'))
                conn.shutdown(socket.SHUT_WR)
                previous_dirt = copy.deepcopy(dirt)

    except KeyboardInterrupt:
        print("\n=== SERVER TERMINATED CLEANLY BY USER ===")