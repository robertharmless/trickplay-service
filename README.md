## Trick Play Service

This is a REST API Service to generate the trick play assets for an HLS master.m3u8.

<br/>

### Assumptions:
---

- There is a proper HLS manifest 'master.m3u8' availble locally or via the web.
- There is at least 1 video stream to extract thumbnails from.
- The stream is not encrypted.

<br/>

### Instructions:
---

- Install FFMPEG.
- Create an .env file.<br>
    ```
    cat env_sample > .env
    ```
- Update the local .env file with the needed info.<br>
    ```
    vi .env
    ```
- Run this flask based trick play service.
- Can import the postman collection [from here.](postman)

<br/>

### System Info:
---

- Created for and tested on Mac OS.
- Tested with Python 3.9.
<br/><br/>

### Reference:
---
The trick play module was developed based on specs defined by Roku for HLS streams.

https://developer.roku.com/docs/developer-program/media-playback/trick-mode/hls-and-dash.md

See "HLS considerations" section.

Also notice their code samples:
https://github.com/rokudev/samples/tree/master/media/TrickPlayThumbnailsHLS
