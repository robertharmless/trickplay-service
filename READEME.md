## Trick Play Service

This is a REST API Service to generate the trick play assets for an HLS master.m3u8.

<br/>

### Assumptions:
---

- There is a proper HLS manifest 'master.m3u8' availble locally or via the web.
- There is at least 1 video stream to extract thumbnails from.

<br/>

### Instructions:
---

- Install FFMPEG.
- Create an .env file.
    cat env_sample > .env
- Update the local .env file with the needed info.
    vi .env
- Run this flask based trick play service.
- Can import the postman collection in postman/trickplay-service.postman_collection.json

<br/>

### System Info:
---

- Created for and tested on Mac OS.
- Tested with Python 3.9.
