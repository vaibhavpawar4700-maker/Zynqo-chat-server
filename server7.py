import asyncio
import websockets
import json
import os

clients = {}  # username : websocket


async def handler(websocket):
    username = None
    try:
        username = await websocket.recv()
        clients[username] = websocket

        await send_users()

        async for message in websocket:
            data = json.loads(message)

            # typing indicator broadcast
            if data.get("type") == "typing":
                target = data["to"]
                if target in clients:
                    await clients[target].send(json.dumps(data))
                continue

            target = data["to"]

            if target in clients:
                await clients[target].send(json.dumps(data))

    except:
        pass

    finally:
        if username in clients:
            del clients[username]
            await send_users()


async def send_users():
    user_list = json.dumps({
        "type": "users",
        "list": list(clients.keys())
    })

    for ws in clients.values():
        await ws.send(user_list)


async def main():
    port = int(os.environ.get("PORT", 10000))
    async with websockets.serve(handler, "0.0.0.0", port):
        print("Server started")
        await asyncio.Future()


asyncio.run(main())