import asyncio
import json
import websockets

async def handle_connection(websocket):
    print("[CONNECTED] Python is standing by for p5.js requests.")
    try:
        # Abandoned 'async for'. Use a standard infinite loop that 
        # responds purely to the p5.js execution frame.
        while True:
            # Wait cleanly for the incoming p5.js frame
            message = await websocket.recv()
            
            p5js_data = json.loads(message)
            mouse_data = p5js_data.get("mouse", {})
            wheel_value = mouse_data.get("wheel", 0)
            
            html_response = f"<p>mouse wheel: {wheel_value}</p>"
            
            # Instantly echo the payload back to the drawing thread
            await websocket.send(html_response)
            
    except websockets.exceptions.ConnectionClosed:
        print("[DISCONNECTED] p5.js stopped the stream.")

async def main():
    async with websockets.serve(handle_connection, "127.0.0.1", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
