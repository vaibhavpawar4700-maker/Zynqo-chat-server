import asyncio
import websockets

clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients:
                await client.send(message)
    finally:
        clients.remove(websocket)

start_server = websockets.serve(handler, "0.0.0.0", 10000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()