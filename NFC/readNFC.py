import ndef
import subprocess
import asyncio
import websockets
import json

fileName = 'dump.mfd'
defaultName = 'default.mfd'
#nfcToolsPath = '/usr/local/bin/'
nfcToolsPath = subprocess.run(['which','nfc-mfultralight'],stdout=subprocess.PIPE).stdout.decode('ascii')[:-1]

async def producerHandler(websocket,path):
    revertCardRaw()
    try:
        while True:
            msg = await readCardRaw()
            await websocket.send(msg)
            await asyncio.sleep(3)
    except(websockets.exceptions.ConnectionClosed):
        revertCardRaw()

async def readCard():
    token='ERROR'
    returnCode = subprocess.call([nfcToolsPath,'r',fileName])
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

async def readCardRaw():
    token='ERROR!'
    userId=0
    data = json.dumps({'uid':userId,'token':token})
    returnCode = subprocess.call([nfcToolsPath,'r',fileName])
    if (returnCode == 0):
        with open(fileName, 'rb') as f:
            dump = f.read()
            token = dump[16:22].decode('ascii')
            userId = int.from_bytes(dump[24:28],byteorder='big')
            data = json.dumps({'uid':userId,'token':token})
            print(data)
            #print('Token: ' + token)
            #print('UID: ' + str(userId))
    return data

def revertCardRaw():
    returnCode = subprocess.call([nfcToolsPath,'w',defaultName])
   
server = websockets.serve(producerHandler,'0.0.0.0',8001)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
