# -*- coding: UTF-8 -*-
import sys
import json
import asyncio
from curl_cffi.requests import AsyncSession

url = sys.argv[1]

semaphore = asyncio.Semaphore(int(sys.argv[2]))

proxies = sys.argv[3]

model = sys.argv[4]

tasks = []

async def request_key(key):
    global tasks
    async with semaphore:
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": f"Bearer {key}",
            "Content-Language": "zh-CN",
            "Content-Type": "application/json",
            "Priority": "u=1, i",
            "Sec-CH-UA": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        json_data = {
            "model": model,
            "messages": [{"role": "user", "content": "hi"}],
            "temperature": 0
        }
        try:
            async with AsyncSession() as session:
                cont = await session.post(url, headers=headers, impersonate="chrome136", json=json_data, proxy=proxies, timeout=10)
                req = json.loads(cont.text)
                if cont.status_code == 200 and len(req.get("choices", [])) > 0 and len(req.get("choices", [])[0].get("message", {}).get("content", {})) > 0:
                    with open(f"alive.txt","a+") as f:
                        f.write(key + '\n')
                    print(str(cont.status_code) + ' ' + req.get('id', ''))
                    return
                with open(f"dead.txt","a+") as f:
                    f.write(key + '\n')
                print(str(cont.status_code) + ' ' + req.get('id', ''))
        except Exception as e:
            try:
                print(cont.text)
            except:
                pass
            print(e)
            tasks.append(asyncio.create_task(request_key(key)))
            await asyncio.sleep(2)


async def main():
    global tasks
    with open('key.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    keys = list(set(data.split('\n')))
    for key in keys:
        if len(key.split('-')) < 2:
            continue
        tasks.append(asyncio.create_task(request_key(key)))
    await asyncio.gather(*tasks)
            
if __name__ == '__main__':
    asyncio.run(main())
