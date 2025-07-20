import asyncio
import websockets
import json

HOST = ""
PORT = 8001

# WebSocket connection handler
async def handler(websocket):
    print(f"Client connected: {websocket.remote_address}")
    try:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")
            await websocket.send(message)
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")

# Run server
async def main():
    print(f"Starting WebSocket server at ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT) as server:
        await server.serve_forever()

if __name__ == "__main__":
    print("Starting websocket")
    asyncio.run(main())
