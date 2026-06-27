import asyncio
import json
import websockets
import io
import base64
import numpy as np

# Force Matplotlib to stay in the background without opening window GUIs
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

async def handle_connection(websocket):
    print("[CONNECTED] Python is standing by for p5.js requests.")
    try:
        while True:
            p5js_data_raw = await websocket.recv()
            p5js_data = json.loads(p5js_data_raw)
            
            # Use exactly one figure slot in memory to prevent thread clipping
            plt.figure(1, figsize=(6, 6))
            plt.clf() 
            
            for stroke in p5js_data.get('glyph', []):
                if not stroke:
                    continue
                xdata = [point['x'] for point in stroke]
                ydata = [point['y'] for point in stroke]
                
                # Apply random jitter arrays
                xdata += 8 * np.random.randn(len(xdata))
                ydata += 8 * np.random.randn(len(ydata))
                
                plt.plot(xdata, ydata, color='black', linewidth=10, solid_capstyle='round')
            
            plt.xlim(0, 1023)
            plt.ylim(0, 1023)
            
            # Match p5.js coordinates and remove chart borders
            plt.gca().invert_yaxis() 
            plt.axis('off')          
            plt.tight_layout(pad=0)
            
            # Save to memory bytes
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0)
            img_buf.seek(0)
            
            b64_string = base64.b64encode(img_buf.read()).decode('utf-8')
            imagedata = f"data:image/png;base64,{b64_string}"
            html_response = f'<img src="{imagedata}" style="width:100%; height:auto;">'
            
            # Send back the response (unblocks JavaScript)
            await websocket.send(html_response)
            
    except websockets.exceptions.ConnectionClosed:
        print("[DISCONNECTED] p5.js stopped the stream.")

async def main():
    async with websockets.serve(handle_connection, "127.0.0.1", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
