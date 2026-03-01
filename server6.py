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
        print(f"{username} connected")

        await send_users()

        async for message in websocket:
            data = json.loads(message)

            target = data["to"]
            text = data["msg"]
            sender = data["from"]

            if target in clients:
                await clients[target].send(
                    json.dumps({
                        "from": sender,
                        "msg": text
                    })
                )

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
