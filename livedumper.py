import argparse
import time
import os
import sys
import logging
import aiohttp
import asyncio
import m3u8

async def download_playlist(url, retries, wait):
    attempt = 0
    while attempt < retries:
        try:
            async with aiohttp.ClientSession() as session:
                logging.info(f"Fetching URL: {url}, Attempt: {attempt + 1}")
                async with session.get(url) as response:
                    response.raise_for_status()
                    logging.info(f"Successfully fetched URL: {url}, Attempt: {attempt + 1}")
                    return await response.text()
        except aiohttp.ClientError as e:
            logging.error(f"{int(time.time())}, {str(e)}, {attempt + 1}")
            attempt += 1
            await asyncio.sleep(wait)
    return None

def save_playlist(content, url):
    timestamp = int(time.time())
    filename = f"{timestamp}.m3u8"
    directory_name = os.path.splitext(os.path.basename(url))[0]

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    with open(os.path.join(directory_name, filename), 'w') as file:
        file.write(content)

async def download_segment(url, directory_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            segment_filename = os.path.join(directory_name, os.path.basename(url))
            with open(segment_filename, 'wb') as segment_file:
                segment_file.write(await response.read())

async def check_and_download_segments(playlist_content, directory_name, base_url):
    playlist = m3u8.loads(playlist_content)
    tasks = []

    if playlist.keys and playlist.keys[0].uri:
        init_segment_uri = playlist.keys[0].uri
        init_segment_filename = os.path.join(directory_name, os.path.basename(init_segment_uri))
        if not os.path.exists(init_segment_filename):
            logging.info(f"Initialization segment {init_segment_uri} is missing, scheduling download.")
            full_url = base_url + init_segment_uri
            tasks.append(download_segment(full_url, directory_name))

    for segment in playlist.segments:
        segment_filename = os.path.join(directory_name, os.path.basename(segment.uri))
        if not os.path.exists(segment_filename):
            logging.info(f"Segment {segment.uri} is missing, scheduling download.")
            full_url = base_url + segment.uri
            tasks.append(download_segment(full_url, directory_name))
    await asyncio.gather(*tasks)

async def main():
    parser = argparse.ArgumentParser(description="Download HLS playlist at a configurable interval.")
    parser.add_argument("url", help="The URL of the m3u8 playlist to download.")
    parser.add_argument("--interval", type=int, default=1, help="The interval (in seconds) at which to download the playlist. Default is 1 second.")
    parser.add_argument("--retries", type=int, default=3, help="The number of retry attempts in case of an error. Default is 3.")
    parser.add_argument("--wait", type=int, default=1, help="The wait time (in seconds) between retry attempts. Default is 1 second.")
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')

    base_url = os.path.dirname(args.url) + "/"

    while True:
        logging.info(f"Starting download for URL: {args.url}")
        playlist_content = await download_playlist(args.url, args.retries, args.wait)
        if playlist_content:
            save_playlist(playlist_content, args.url)
            logging.info(f"Playlist saved for URL: {args.url}")
            directory_name = os.path.splitext(os.path.basename(args.url))[0]
            await check_and_download_segments(playlist_content, directory_name, base_url)
        await asyncio.sleep(args.interval)

if __name__ == "__main__":
    asyncio.run(main())
