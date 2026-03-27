from ut_params import *
import asyncio
import httpx
import urllib3
from contextlib import asynccontextmanager
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@asynccontextmanager
async def get_client(existing_client: httpx.AsyncClient = None):
    if existing_client is not None:
        yield existing_client
    else:
        async with httpx.AsyncClient(verify=False) as client:
            yield client


async def create_ditto_device(devicename, password, attributes, features, reused_client: httpx.AsyncClient = None):
    ret = []
    async with get_client(reused_client) as client:
        ret.append((await client.put(
            f'http://{DITTO_NGINX_ADDRESS}/api/2/things/{UT_TENANT}:{devicename}',
            auth=(DITTO_USER, DITTO_PW),
            headers={'Content-Type':'application/json'},
            json={
                "policyId": UT_POLICY,
                "attributes": attributes,
                "features": features
            }
        )).text)

        if HONO_REGISTRY_ADDRESS is None: return ret
        
        ret.append((await client.post(
            f"https://{HONO_REGISTRY_ADDRESS}/v1/devices/{UT_TENANT}/{UT_TENANT}:{devicename}",
        )).text)
        
        ret.append((await client.put(
            f"https://{HONO_REGISTRY_ADDRESS}/v1/credentials/{UT_TENANT}/{UT_TENANT}:{devicename}",
            headers={'Content-Type':'application/json'},
            json=[{
                "type": "hashed-password",
                "auth-id": devicename,
                "secrets": [{
                    "pwd-plain": password,
                    "hash-function": "sha-256"
                }],
            }],
        )).text)
    return ret


async def send_ditto_command(device, param, value, reused_client: httpx.AsyncClient = None):
    async with get_client(reused_client) as client:
        return await client.post(
            f"http://{DITTO_NGINX_ADDRESS}/api/2/things/{UT_TENANT}:{device}/inbox/messages/{param}?timeout=0",
            auth=(DITTO_USER, DITTO_PW),
            headers={'Content-Type': 'application/json'},
            json=value
        )


async def get_ha_device(device, reused_client: httpx.AsyncClient = None):
    async with get_client(reused_client) as client:
        return (await client.get(
            f'http://{HA_HTTP_ADDRESS}/api/states/{device}',
            headers={'Authorization': HA_TOKEN, 'Content-Type':'application/json'}
        )).json()


async def get_ha_devices(reused_client: httpx.AsyncClient = None):
    async with get_client(reused_client) as client:
        return (await client.get(
            f'http://{HA_HTTP_ADDRESS}/api/states',
            headers={'Authorization': HA_TOKEN, 'Content-Type':'application/json'}
        )).json()


async def get_hono_device(device, reused_client: httpx.AsyncClient = None):
    if HONO_REGISTRY_ADDRESS is None: return None
    async with get_client(reused_client) as client:
        return (await client.get(
            f'https://{HONO_REGISTRY_ADDRESS}/v1/devices/{UT_TENANT}/{HONO_GATEWAY_NAME}/{device}'
        )).json()


async def _get_hono_devices_page(client: httpx.AsyncClient, page_offset=0):
    if HONO_REGISTRY_ADDRESS is None: 
        devices = await get_ditto_devices(client)
        return {'result': [{'id':device['thingId']} for device in devices], 'total': len(devices)}
    return (await client.get(
        f"https://{HONO_REGISTRY_ADDRESS}/v1/devices/{UT_TENANT}?pageSize=200&pageOffset={int(page_offset)}"
    )).json()


async def get_hono_devices(reused_client: httpx.AsyncClient = None):
    async with get_client(reused_client) as client:
        data = await _get_hono_devices_page(client)
        devices = data['result']
        total = data['total']

        if total > 200:
            tasks = [_get_hono_devices_page(client, offset) for offset in range(int(total / 200))]

            for task in await asyncio.gather(*tasks):
                devices.extend(task['result'])

        return [device for device in devices if device['id'] != UT_POLICY]


async def get_hono_gateway_devices(reused_client: httpx.AsyncClient = None):
    return [d['id'] for d in await get_hono_devices(reused_client) if d['id'].startswith(UT_TENANT)]


async def delete_hono_device(devicename, reused_client: httpx.AsyncClient = None):
    if HONO_REGISTRY_ADDRESS is None: return 404
    async with get_client(reused_client) as client:
        return (await client.delete(
            f"https://{HONO_REGISTRY_ADDRESS}/v1/devices/{UT_TENANT}/{devicename}"
        )).status_code



async def get_ditto_device(devicename, reused_client: httpx.AsyncClient = None):
    async with get_client(reused_client) as client:
        return (await client.get(
            f'http://{DITTO_NGINX_ADDRESS}/api/2/things/{UT_TENANT}:{devicename}',
            auth=(DITTO_USER, DITTO_PW)
        )).json()


async def _get_ditto_devices_page(client: httpx.AsyncClient, cursor=None):
    return (await client.get(
        f'http://{DITTO_NGINX_ADDRESS}/api/2/search/things?option=size(200){f',cursor({cursor})' if cursor is not None else ''}', 
        auth=(DITTO_USER, DITTO_PW)
    )).json()


async def get_ditto_devices(reused_client: httpx.AsyncClient = None):
    import time
    async with get_client(reused_client) as client:
        resp = await _get_ditto_devices_page(client)
        devices = resp['items']
        cursor = resp.get('cursor')
        while cursor is not None:
            # print('req'); t = time.time()
            resp = await _get_ditto_devices_page(client, cursor)
            # print('resp', time.time()-t)
            devices.extend(resp['items'])
            cursor = resp.get('cursor')

        return [device for device in devices if device['thingId'] != UT_POLICY]


async def delete_ditto_device(devicename, reused_client: httpx.AsyncClient = None):
    async with get_client(reused_client) as client:
        return [
            (await client.delete(
                f'http://{DITTO_NGINX_ADDRESS}/api/2/things/{UT_TENANT}:{devicename}',
                auth=(DITTO_USER, DITTO_PW)
            )).status_code,
            await delete_hono_device(f'{UT_TENANT}:{devicename}', client)
        ]


async def create_hono_gateway_device(reused_client: httpx.AsyncClient = None, hono_tqdm=None):
    if HONO_REGISTRY_ADDRESS is None: return
    async with get_client(reused_client) as client:
        await client.post(f"https://{HONO_REGISTRY_ADDRESS}/v1/devices/{UT_TENANT}/{HONO_GATEWAY_NAME}")
        await client.put(
            f"https://{HONO_REGISTRY_ADDRESS}/v1/credentials/{UT_TENANT}/{HONO_GATEWAY_NAME}",
            headers={'Content-Type':'application/json'},
            json=[{
                "type": "hashed-password",
                "auth-id": HONO_GATEWAY_NAME,
                "secrets": [{
                    "pwd-plain": HONO_GATEWAY_PW,
                    "hash-function": "sha-256"
                }]
            }]
        )

        semaphore = asyncio.Semaphore(8)
        async def limited_add(device):
            async with semaphore:
                await add_hono_device_to_gateway(device,client)

        tasks = [limited_add(device) for device in await get_hono_gateway_devices(client)]
        if hono_tqdm is not None:
            hono_tqdm.total = len(tasks)
            hono_tqdm.refresh()
        for task in asyncio.as_completed(tasks):
            await task
            if hono_tqdm is not None: hono_tqdm.update(1)
        if hono_tqdm is not None: hono_tqdm.close()


async def add_hono_device_to_gateway(device, reused_client: httpx.AsyncClient = None):
    if HONO_REGISTRY_ADDRESS is None: return
    async with get_client(reused_client) as client:
        await client.put(
            f"https://{HONO_REGISTRY_ADDRESS}/v1/devices/{UT_TENANT}/{device}",
            headers={'Content-Type':'application/json'},
            json={"via": [HONO_GATEWAY_NAME]}
        )