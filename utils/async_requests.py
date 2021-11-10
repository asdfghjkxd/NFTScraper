"""
This is a helper script to asynchronously send requests
"""

import asyncio
import json
import aiohttp
import sys
import ast
import os

from asyncio import SelectorEventLoop


async def fetch(session, url):
    """
    Async sends a GET request to the URL of interest

    :param session:                 aiohttp ClientSession object
    :param url:                     URL to send GET requests to
    :return:                        JSON object or None
    """

    try:
        async with session.get(url) as resp:
            return await resp.json()
    except Exception as e:
        return None


async def bound_fetch(sem, session, url):
    """
    Async fetches the URL, uses the Semaphore class to asynchronously get all requests in parallel
    :param sem:                     Semaphore object
    :param session:                 aiohttp ClientResponse objecct
    :param url:                     URL to send GET requests to
    :return:                        awaitable coroutine
    """

    async with sem:
        return await fetch(session, url)


async def run(urls, sem_count=100):
    """
    Async main function to start the request sending
    :param urls:                    Literal representation of URLs, parsed into a list
    :param sem_count:               Number of Semaphore threads to init
    :return:                        List of responses in the JSON format
    """
    timeout = 15
    tasks = []

    sem = asyncio.Semaphore(sem_count)
    conn = aiohttp.TCPConnector(limit=64, ssl=False)

    async with aiohttp.ClientSession(connector=conn) as session:
        for url in urls:
            task = asyncio.wait_for(bound_fetch(sem, session, url), timeout)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
    return responses

if __name__ == '__main__':
    """
    This will run when this file is invoked with the python command on the CLI or through the app
    """

    base_filepath = os.path.join(os.getcwd(), 'dumps', 'data_dumps.json')

    # parse literal to list
    urls = sys.argv[1].strip('][').split(', ')

    # start async parallel loop
    loop = asyncio.SelectorEventLoop()
    data = loop.run_until_complete(run(urls))
    data = json.dumps(data)

    # dump json object into a temporary json file, saved for user reference and debugging
    # future releases may allow user to set debug level so that the temp files will be removed after the processing is
    # complete
    with open(f'{base_filepath}', 'w') as f:
        for d in data:
            f.write(d)
