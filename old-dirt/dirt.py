import asyncio
import json
import websockets
import io
import base64

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.figure(1, figsize=(6, 6))

async def handle_connection(websocket):
    print("[CONNECTED] Python is standing by for p5.js requests.")
    try:
        while True:
            p5js_data_raw = await websocket.recv()
            p5js_data = json.loads(p5js_data_raw)
            plt.clf()
            for stroke in p5js_data.get('glyph', []):
                if not stroke:
                    continue
                xdata = [point['x'] for point in stroke]
                ydata = [point['y'] for point in stroke]
                
                xdata += 8 * np.random.randn(len(xdata))
                ydata += 8 * np.random.randn(len(ydata))
                
                plt.plot(xdata, ydata, color='black', linewidth=10, solid_capstyle='round')
            plt.xlim(0, 1023)
            plt.ylim(0, 1023)
            p5js_data["mouse"]["x"] = np.round(p5js_data["mouse"]["x"])
            p5js_data["mouse"]["y"] = np.round(p5js_data["mouse"]["y"])

            plt.text(10,50,f'key = {p5js_data["keystroke"]}')
            plt.text(10,100,f'mouse x = {p5js_data["mouse"]["x"]}')
            plt.text(10,150,f'mouse y = {p5js_data["mouse"]["y"]}')
            plt.text(10,200,f'mouse wheel = {p5js_data["mouse"]["wheel"]}')
            peak_audio_frequency = np.argmax(p5js_data["audio_spectrum"])*p5js_data["spectrum_bin_frequency"]
            plt.text(10,250,f'peak frequency = {peak_audio_frequency} Hz')
            plt.gca().invert_yaxis() 
            plt.axis('off')          
            plt.tight_layout(pad=0)
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0)
            img_buf.seek(0)
            
            b64_string = base64.b64encode(img_buf.read()).decode('utf-8')
            imagedata = f"data:image/png;base64,{b64_string}"
            html_response = f'<img src="{imagedata}" style="width:100%; height:auto;">'
            await websocket.send(html_response)
    except websockets.exceptions.ConnectionClosed:
        print("[DISCONNECTED] p5.js stopped the stream.")

async def main():
    async with websockets.serve(handle_connection, "127.0.0.1", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
