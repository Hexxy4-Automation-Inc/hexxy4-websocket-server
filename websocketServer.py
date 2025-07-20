import asyncio
import websockets
import json

HOST = 'localhost'
PORT = 8765

# Template-based request handler
async def handle_request(data: str) -> dict:
    try:
        request = json.loads(data)
        action = request.get("action")
        payload = request.get("payload", {})

        match action:
            case "ping":
                return {"status": "success", "response": "pong"}
            case "echo":
                return {"status": "success", "response": payload}
            case _:
                return {"status": "error", "message": f"Unknown action '{action}'"}
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON"}

# WebSocket connection handler
async def handler(websocket, path):
    print(f"Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            response = await handle_request(message)
            await websocket.send(json.dumps(response))
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")

# Run server
async def main():
    print(f"Starting WebSocket server at ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    print("Starting websocket")
    asyncio.run(main())
