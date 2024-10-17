Livedumper is a simple Python tool to grab (dump) HLS Live playlist and reproduce it later for testing purposes

## Usage

To use the livedumper script, run the following command:

```
python livedumper.py <m3u8_url> --interval <interval> --retries <retries> --wait <wait>
```

- `<m3u8_url>`: The URL of the m3u8 playlist to download.
- `--interval`: The interval (in seconds) at which to download the playlist. Default is 1 second.
- `--retries`: The number of retry attempts in case of an error. Default is 3.
- `--wait`: The wait time (in seconds) between retry attempts. Default is 1 second.

## Description

The livedumper script accepts an m3u8 URL as a command-line parameter and downloads the HLS playlist at a configurable interval. Each playlist is stored on the filesystem using a Unix timestamp when the playlist was grabbed. The script also implements a retry mechanism to handle errors when downloading the playlist and logs errors to a file.

## Asynchronous Implementation

The livedumper script now uses `asyncio` for asynchronous programming. The `download_playlist` function is an asynchronous function using `aiohttp` for non-blocking HTTP requests. The `main` function is also an asynchronous function using `asyncio.sleep` for non-blocking sleep intervals. This allows the script to handle multiple tasks concurrently and improve performance.
