import ndef
import subprocess
import asyncio
import websockets

fileName = 'dump.mfd'

async def producerHandler(websocket,path):
    msg= await readCard()
    await websocket.send(msg)
async def readCard():
    token='ERROR'
    returnCode = subprocess.call(['nfc-mfultralight','r','dump.mfd'])
    if (returnCode == 0):
        with open(fileName, 'rb') as f:
            dump = f.read()
            if (hex(dump[12])=='0xe1'):
                length = dump[17]
                message = dump[18:(18+length)]
                #print(message)
                for record in ndef.message_decoder(message):
                    if (record.type=='urn:nfc:wkt:T'):
                        token=record.text
    return token

server = websockets.serve(producerHandler,'0.0.0.0',8001)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
