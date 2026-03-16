import asyncio
import cowsay

PORT = 7777
clients = {}

async def command(line, name, queue):
    args = line.split(maxsplit=2)
    cmd = args[0].lower().strip()

    if cmd == 'who':
        users = list(clients.keys())
        if users:
            return {"msg": f"logged users: {' '.join(users)}"}
        else:
            return {"msg": f"no logged users"}

    elif cmd == 'cows':
        cows = set(cowsay.list_cows())
        users = set(clients.keys())
        return {"msg": f"cows available: {' '.join(sorted(list(cows - users)))}"}

    elif cmd == 'login':
        if len(args) < 2:
            return {"msg": f"cow was not chosen"}

        if name is not None:
            return {"msg": f"you already have been registered as {name}"}
        
        cow_name = args[1]

        if cow_name in cowsay.list_cows():
            if cow_name in clients:
                return {"msg": f"name ({cow_name}) is already taken"}
            else:
                clients[cow_name] = queue
                return {"msg": f"your name is {cow_name}", "name": cow_name}
        else:
            return {"msg": f"{cow_name} is not available name"}
        
    elif cmd == 'say':
        if not name:
            return {"msg": "you must login first"}
        if len(args) < 3:
            return {"msg": f"no cow or no message"}
        
        if args[1] not in clients:
            return {"msg": f"cow is not logged"}

        msg = cowsay.cowsay(args[2], cow=name)
        await clients[args[1]].put(msg)
        return {}

    elif cmd == "yield":
        if not name:
            return {"msg": "you must login first"}
        
        if len(args) < 2:
            return {"msg": f"no message"}
        
        msg = cowsay.cowsay(line.split(maxsplit=1)[1], cow=name)
        for user in clients:
            if user != name:
                await clients[user].put(msg)
        return {}
    
    elif cmd == "quit":
        return {"quit": True, "msg": "goodbye"}
    
    else:
        return {"msg": "unknown command"}


async def chat(reader, writer):
    addr = writer.get_extra_info('peername')
    
    me = None
    print(f"[+] Connected: {addr[0]}:{addr[1]}")
    queue = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())
    try:
        while not reader.at_eof():
            done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                if task is send:
                    send = asyncio.create_task(reader.readline())

                    line = task.result().decode().strip()
                    if not line:
                        continue

                    response = await command(line, me, queue)

                    if 'name' in response:
                        me = response['name']

                    if 'msg' in response:
                        msg = response['msg'] + '\n'
                        writer.write(msg.encode())
                        await writer.drain()
                    
                    if 'quit' in response:
                        raise ConnectionResetError('quit')

                elif task is receive:
                    receive = asyncio.create_task(clients[me].get())
                    writer.write(f"{task.result()}\n".encode())
                    await writer.drain()
    except ConnectionResetError:
        pass
    finally:
        send.cancel()
        receive.cancel()
        print(f"[-] disconnected: {addr[0]}:{addr[1]}", end='')
        if me is None:
            print()
        else:
            print(f" ({me})")
        if me and me in clients:
            del clients[me]
        writer.close()
        await writer.wait_closed()



async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", PORT)
    async with server:
        await server.serve_forever()


asyncio.run(main())