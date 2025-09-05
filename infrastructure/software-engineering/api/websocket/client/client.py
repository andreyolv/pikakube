"""Client example using the asyncio API."""

import asyncio

from websockets.asyncio.client import connect

URI = "ws://localhost:8080"

async def hello():
    async with connect(URI) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())