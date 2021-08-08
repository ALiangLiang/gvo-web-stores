import os
import re
import json
from datetime import datetime
from typing import List, Tuple
from urllib.parse import urlparse, parse_qs
import logging
import time
from types import SimpleNamespace
import asyncio
from aiohttp import ClientSession, TraceConfig, TraceRequestStartParams, TraceRequestEndParams, TCPConnector, ClientTimeout
from aiohttp_retry import RetryClient, ExponentialRetry
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

global index
index = 1
global count
count = 1
global start
start = time.time()

class WebGvo:
    def __init__(self):
        conn = TCPConnector(limit_per_host=30)
        retry_options = ExponentialRetry(attempts=3)

        async def on_request_start(
            session: ClientSession,
            trace_config_ctx: SimpleNamespace,
            params: TraceRequestStartParams,
        ) -> None:
            trace_request_ctx = trace_config_ctx.trace_request_ctx
            if trace_request_ctx.get('api') != 'search_company':
                return

            global index
            trace_request_ctx['index'] = index
            index += 1
            trace_request_ctx['start_time'] = time.time()
            
        async def on_request_end(
            session: ClientSession,
            trace_config_ctx: SimpleNamespace,
            params: TraceRequestEndParams,
        ) -> None:
            trace_request_ctx = trace_config_ctx.trace_request_ctx
            if trace_request_ctx.get('api') != 'search_company':
                return

            global count
            global start
            logger.info(
                '%d %d %f %d %d %d %f',
                count,
                index,
                time.time() -  start,
                trace_request_ctx['current_attempt'],
                trace_request_ctx['tid'],
                trace_request_ctx['cid'], 
                time.time() -  trace_request_ctx['start_time'],
            )
            count += 1

        trace_config = TraceConfig()
        trace_config.on_request_start.append(on_request_start)
        trace_config.on_request_end.append(on_request_end)
        trace_config.on_request_exception.append(on_request_end)
        self.session = RetryClient(connector=conn, raise_for_status=False, retry_options=retry_options, trace_configs=[trace_config])

    async def __aenter__(self):
        self.__init__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        return

    async def login(self):
        async with self.session.post(
                'http://webgvo.wasabii.com.tw/dol/web/d', 
                data={
                    'Act': 'contract',
                    'gcid': os.environ['USER'],
                    'pass': os.environ['PASS'],
                    'log.x': '77',
                    'log.y': '8'
                }
            ):
                pass

    async def get_server_ids_names(self) -> List[Tuple[int, str]]:
        async with self.session.post(
                'http://webgvo.wasabii.com.tw/dol/web/d', 
                data={
                    'Act': 'config_wd',
                }
            ) as resp:
                server_ids_names = []
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                form_tag = soup.find('form', attrs={'name': 'selwd'})
                if form_tag is None:
                    return server_ids_names

                td_tags = form_tag.find_all('td')
                for i in range(0, len(td_tags), 2):
                    server_id_str = td_tags[i].find('input', attrs={'name': 'Wd'})['value']
                    server_id = int(server_id_str)
                    server_name = td_tags[i + 1].text.strip()
                    server_ids_names.append((server_id, server_name))

                return server_ids_names

    async def get_charater_ids(self, wd: int):
        async with self.session.post(
                'http://webgvo.wasabii.com.tw/dol/web/d', 
                data={
                    'Act': 'config_ch2',
                    'Wd': str(wd),
                    'submit.x': '74',
                    'submit.y': '11',
                }
            ) as resp:
                charater_ids = []
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                form_tag = soup.find('form', attrs={'name': 'selch'})
                if form_tag is None:
                    return charater_ids

                input_tags = form_tag.find_all('input', attrs={'name': 'Ch'})
                for input_tag in input_tags:
                    charater_id = int(input_tag['value'])
                    charater_ids.append(charater_id)
                return charater_ids

    async def select_charater(self, charater_id):
        async with self.session.post(
                'http://webgvo.wasabii.com.tw/dol/web/d', 
                data={
                    'Act': 'config_end',
                    'Ch': str(charater_id),
                    'submit.x': '75',
                    'submit.y': '15'
                }
            ) as resp:
                pass

    async def search_company(self, tid: int, cid: int) -> List[dict]:
        async with self.session.post(
                'http://webgvo.wasabii.com.tw/dol/web/d', 
                data={
                    'Act': 'company_search_sub_display_cd',
                    'Tid': str(tid),
                    'Cid': str(cid),
                    'Caid': '0',
                    'Nscp': '0',
                    'Pscp': '0',
                },
                trace_request_ctx={'api':'search_company', 'tid':tid, 'cid':cid}
            ) as resp_2:
                products = []
                soup = BeautifulSoup(await resp_2.text(), 'html.parser')
                tbody_tag = soup.find(id='sort')
                if tbody_tag is None:
                    return []

                tr_tags = tbody_tag.find_all('tr')
                for tr_tag in tr_tags:
                    td_tags = tr_tag.find_all('td')
                    prod_name = td_tags[0].text.strip()
                    amount = int(td_tags[1].text.strip())
                    unit_price = int(td_tags[2].text.strip())
                    products.append({
                        'name': prod_name,
                        'amount': amount,
                        'unit_price': unit_price
                    })
                return products

    async def get_town_ids_names(self) -> List[Tuple[int, str]]:
        coros = []
        # 搜尋城市裡的商會
        async with self.session.post(
                'http://webgvo.wasabii.com.tw/dol/web/d', 
                data={
                    'Act': 'company_search_sub_townlist',
                }
            ) as resp:
                town_ids_names = []
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                td_tags = soup.find_all('td', class_='chara', attrs={'width': '168'})

                for td_tag in td_tags:
                    a_tag = td_tag.find('a')
                    href = a_tag['href']
                    parsed_url = urlparse(href)
                    qs = parse_qs(parsed_url.query)
                    town_id = qs.get('Tid')[0]
                    town_name = a_tag.text.strip()
                    town_ids_names.append((int(town_id), town_name))
                return town_ids_names

    async def search_town(self, town_id):
        # 搜尋城市裡的商會
        async with self.session.post(
                'http://webgvo.wasabii.com.tw/dol/web/d', 
                data={
                    'Act': 'company_search_sub_comlist',
                    'Tid': str(town_id),
                    'Caid': '0',
                    'Nscp': '0',
                    'Pscp': '0',
                }
            ) as resp:
                results = []
                coros = []
                product_amount: int = 0
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                tags = soup.find(id='shop0')
                if tags is None:
                    return results, 0

                tags = tags.find_all('td', attrs={'width': '225'})
                for tag in tags:
                    name = tag.text
                    a_tag = tag.find('a')
                    href: str = a_tag['href']
                    id_str = re.findall(r'javascript:Click_Sub\( (\d*) \)', href)[0]
                    cid = int(id_str)

                    async def search_company(company_name, town_id, cid):
                        products = await self.search_company(town_id, cid)
                        return {
                            'company_name': company_name,
                            'products': products
                        }

                    r = await search_company(name, town_id, cid)
                    product_amount += len(r['products'])
                    results.append(r)
                    # coros.append(asyncio.ensure_future(search_company(asyncio_semaphore, name, town_id, cid)))

                # result = await asyncio.gather(*coros)
                return results, product_amount

async def main():
    async with WebGvo() as web_gvo:
        await web_gvo.login()

        servers = {}
        directory = f'dist/data/'

        server_ids_names = await web_gvo.get_server_ids_names()
        for server_id, server_name in server_ids_names:
            servers[server_name] = server = {}

            charater_ids = await web_gvo.get_charater_ids(server_id)
            if len(charater_ids) == 0:
                logger.warning('No charater found in server %s', server_name)
                continue

            charater_id = charater_ids[0]
            await web_gvo.select_charater(charater_id)
            town_ids_names = await web_gvo.get_town_ids_names()
            if len(town_ids_names) == 0:
                logger.warning('There is no town be found')
                continue

            for town_id, town_name in town_ids_names:
                server[town_name] = 0

                if not os.path.exists(directory):
                    os.makedirs(directory)
                file_path = f'{directory}{str(server_name)}-{town_name}.json'
                companies, amount = await web_gvo.search_town(town_id)

                server[town_name] = amount
            
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(
                        json.dumps({
                            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'companies': companies
                        })
                    )

                with open(directory + 'stats.json', 'w', encoding='utf-8') as file:
                    file.write(json.dumps(servers))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
