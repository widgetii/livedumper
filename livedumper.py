import argparse
import time
import os
import logging
import aiohttp
import asyncio

async def download_playlist(url, retries, wait):
    attempt = 0
    while attempt < retries:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.text()
        except aiohttp.ClientError as e:
            logging.error(f"{int(time.time())}, {str(e)}, {attempt + 1}")
            attempt += 1
            await asyncio.sleep(wait)
    return None

def save_playlist(content):
    timestamp = int(time.time())
    filename = f"{timestamp}.m3u8"
    with open(filename, 'w') as file:
        file.write(content)

async def main():
    parser = argparse.ArgumentParser(description="Download HLS playlist at a configurable interval.")
    parser.add_argument("url", help="The URL of the m3u8 playlist to download.")
    parser.add_argument("--interval", type=int, default=1, help="The interval (in seconds) at which to download the playlist. Default is 1 second.")
    parser.add_argument("--retries", type=int, default=3, help="The number of retry attempts in case of an error. Default is 3.")
    parser.add_argument("--wait", type=int, default=1, help="The wait time (in seconds) between retry attempts. Default is 1 second.")
    args = parser.parse_args()

    logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(message)s')

    while True:
        playlist_content = await download_playlist(args.url, args.retries, args.wait)
        if playlist_content:
            save_playlist(playlist_content)
        await asyncio.sleep(args.interval)

if __name__ == "__main__":
    asyncio.run(main())
