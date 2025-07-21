import asyncio
import websockets
import json
import logging

HOST = ""
PORT = 8001

logging.getLogger("websockets").setLevel(logging.INFO)

term_host_ws = None
term_client_ws = None

# WebSocket connection handler
async def root_handler(websocket):
    print(f"Client connected: {websocket.remote_address}")
    try:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")
            await websocket.send(message)
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")


async def terminal_host_handler(websocket):
    global term_host_ws
    term_host_ws = websocket
    print(f"[Host] Client connected: {websocket.remote_address}")
    try:
        while True:
            message = await websocket.recv()
            print(f"[Host] Received: {message}")
            if term_client_ws:
                await term_client_ws.send(message)
    except websockets.ConnectionClosed:
        print(f"[Host] Client disconnected: {websocket.remote_address}")
    finally:
        if term_host_ws == websocket:
            term_host_ws = None


async def terminal_client_handler(websocket):
    global term_client_ws
    term_client_ws = websocket
    print(f"[Client] Client connected to terminal client: {websocket.remote_address}")
    try:
        while True:
            message = await websocket.recv()
            print(f"[Client] Received: {message}")
            if term_host_ws:
                await term_host_ws.send(message)
    except websockets.ConnectionClosed:
        print(f"[Client] Client disconnected: {websocket.remote_address}")
    finally:
        if term_client_ws == websocket:
            term_client_ws = None


# Path router
ROUTES = {
    "/": root_handler,
    "/term/client": terminal_client_handler,
    "/term/host": terminal_host_handler,
}

# Dispatcher
async def handler(websocket):
    path = websocket.request.path
    the_chosen_handler = ROUTES.get(path)
    if the_chosen_handler:
        await the_chosen_handler(websocket)
    else:
        print(f"No route for {path}, closing connection.")
        await websocket.close(code=1000, reason="Invalid path")


# Run server
async def main():
    print(f"Starting WebSocket server at ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT) as server:
        await server.serve_forever()

if __name__ == "__main__":
    print("Starting websocket")
    asyncio.run(main())
