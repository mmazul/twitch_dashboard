import asyncio
from common import TMI_PING, TMI_PONG, TMI_SERVER, TMI_SERVER_PORT
import os
import websockets
import sys

async def listening_messages(channel):
    count = 0
    chunks = 20

    writing_template = "messages/messages_{}_writing.txt"
    finished_template = "messages/messages_{}_finished.txt"

    async with websockets.connect(f"{TMI_SERVER}:{str(TMI_SERVER_PORT)}") as ws:
        try:
            await ws.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
            print(f"""PASS {os.getenv("PASS")}""")
            await ws.send(f"""PASS {os.getenv("PASS")}""")
            await ws.send(f"""NICK {os.getenv("NICK")}""")
            await ws.send(f"JOIN #{channel}")
            while True:
                msg = await ws.recv()
                if msg.rstrip() == TMI_PING:
                    print(f"################## {TMI_PING}")
                    await ws.send(TMI_PONG)
                    print(f"################## {TMI_PONG}")
                else:
                    if count % chunks == 0:
                        if count > 0:
                            file_object.close()
                            os.rename(writing_template.format(count//chunks-1),
                                      finished_template.format(count//chunks-1))
                        print(f'################## Create messages chunk: {str(count//chunks)}')
                        file_object = open(writing_template.format(count//chunks), 'a')
                    file_object.write(msg)
                    count += 1
                    print(msg)
            await ws.close()
        except websockets.ConnectionClosed as e:
                print(f'Terminated', e)

channel = sys.argv[1]
print(f"##################Listening channel {channel}.")
loop = asyncio.get_event_loop()
loop.run_until_complete(listening_messages(channel))