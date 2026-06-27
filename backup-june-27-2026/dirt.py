import asyncio
import json
import websockets
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# A clean handler function to isolate each connected browser window
async def handle_client(websocket):
    print(f"[CONNECTED] New active tab view linked.")
    fig, ax = plt.subplots(figsize=(6, 6))
    
    try:
        # This loop runs independently for this specific browser tab
        while True:
            p5js_data_raw = await websocket.recv()
            p5js_data = json.loads(p5js_data_raw)
            
            ax.cla()
            for stroke in p5js_data.get('glyph', []):
                if not stroke: 
                    continue
                xdata = [point['x'] for point in stroke]
                ydata = [point['y'] for point in stroke]
                
                xdata += 8 * np.random.randn(len(xdata))
                ydata += 8 * np.random.randn(len(ydata))
                
                ax.plot(xdata, ydata, color='black', linewidth=10, solid_capstyle='round')
            
            ax.set_xlim(0, 1023)
            ax.set_ylim(0, 1023)
            ax.invert_yaxis() 
            ax.axis('off')
            fig.tight_layout(pad=0)
            
            img_buf = io.BytesIO()
            fig.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0, dpi=100)
            img_buf.seek(0)
            
            b64_string = base64.b64encode(img_buf.read()).decode('utf-8')
            imagedata = f"data:image/png;base64,{b64_string}"
            html_response = f'<img src="{imagedata}" style="width:100%; height:auto;">'
            
            await websocket.send(html_response)
            
    except websockets.exceptions.ConnectionClosed:
        print("[DISCONNECTED] A tab view was closed.")
    finally:
        plt.close(fig)

async def main():
    print("[SERVER RUNNING] Standing by on port 8080...")
    # websockets.serve automatically spawns a new 'handle_client' routine for every connection
    async with websockets.serve(handle_client, "127.0.0.1", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
