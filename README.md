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

The script will create a separate directory named after the m3u8 filename (without extension) and save the downloaded playlists in that directory. It will also check for missing media segment files in the same directory and schedule their download if they do not exist.

## Description

The livedumper script accepts an m3u8 URL as a command-line parameter and downloads the HLS playlist at a configurable interval. Each playlist is stored on the filesystem using a Unix timestamp when the playlist was grabbed. The script also implements a retry mechanism to handle errors when downloading the playlist and logs errors to stdout.

The script creates a separate directory named after the m3u8 filename (without extension) and saves the downloaded playlists in that directory. It also checks for missing media segment files in the same directory and schedules their download if they do not exist.

## Asynchronous Implementation

The livedumper script now uses `asyncio` for asynchronous programming. The `download_playlist` function is an asynchronous function using `aiohttp` for non-blocking HTTP requests. The `main` function is also an asynchronous function using `asyncio.sleep` for non-blocking sleep intervals. This allows the script to handle multiple tasks concurrently and improve performance.

The script also includes a function `check_and_download_segments` to parse the m3u8 playlist, check for missing media segment files, and schedule their download. This ensures that all media segment files are available in the same directory as the stored playlist file.

## Handling Initialization Segment

The livedumper script now handles the `#EXT-X-MAP:URI=` tag in the playlist. If the playlist contains an initialization segment specified by the `#EXT-X-MAP:URI=` tag, the script will check if the initialization segment file is missing and schedule its download if necessary. This ensures that the initialization segment is available along with the media segment files.
