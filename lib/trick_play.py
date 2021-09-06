"""
Create trick play for hls - based on Roku requirements.
'''''''
Based on specs defined by Roku for HLS streams.
https://developer.roku.com/docs/developer-program/media-playback/trick-mode/hls-and-dash.md
- See "HLS considerations"
Also:
https://github.com/rokudev/samples/tree/master/media/TrickPlayThumbnailsHLS

"""
# Built-in
from os import environ
from urllib.parse import urlparse
import pathlib

from dataclasses import dataclass, field
from typing import List

# Special
import m3u8

# App
from .utilities import get_source_type
from .ffmpeg import FFMPEG
from api.event import post_event
from .config import App

app = App()


@dataclass
class TrickPlayResult:
    """
    Result for when generating Trick Play assets.
    """

    data: str = None
    message: str = "Unknown Error."
    success: bool = False


class TrickPlay:
    """
    Create images and needed manifests. This is based on some Roku Instructions.
    """

    master_manifest_path = None
    master_manifest_type = None
    # master manifest data
    master_content = None
    source_index = None
    # trickplay
    trickplay_index = None
    trickplay_path = None
    trickplay_foldername = "images-1"
    default_trickplay_path = None
    trickplay_index_name = "index.m3u8"
    master_manifest_trickplay_string = None
    # thumbnails
    thumb_interval = 6
    thumb_extension = ".jpg"
    thumb_prefix = "thumb"
    thumb_resolution = "320x180"
    thumb_bandwidth = 0  # @ 16460 for 320x180 @ 32920 for 640x360

    def __init__(self, master) -> None:
        self.master_manifest_path = master
        self.master_manifest_type = get_source_type(master)
        self.name = pathlib.Path(__file__).name.replace(".py", "")

        print(f"environ [{type(environ)}]:{environ}")

        if "DEFAULT_RESULT_FOLDER_NAME" in environ:
            self.default_trickplay_path = pathlib.Path.joinpath(
                pathlib.Path(__file__).parent.parent,
                environ["DEFAULT_RESULT_FOLDER_NAME"],
            )
        else:
            self.default_trickplay_path = pathlib.Path(__file__).parent.parent

    def generate_trickplay_assets(self) -> bool:
        """
        Function to generate the trick play assets.
        """
        func = (
            f"{__package__}.{self.name}.{__class__.__name__}.generate_trickplay_assets"
        )
        post_event(
            "log_debug",
            f"{func}",
            f"Generateing trick play assets...",
        )

        trick_play_result = TrickPlayResult()

        step_1_success = self.read_master_m3u8()
        if step_1_success:
            step_2_success = self.create_destination_folder()
            trick_play_result.message = "Successfuly read master.m3u8"

        if step_2_success:
            step_3_success = self.generate_thumbnails()
            trick_play_result.message = "Successfuly generated thumbnail files"

        if step_3_success:
            step_4_success = self.create_image_playlist()
            trick_play_result.message = "Successfuly generated image playlist"

        if step_4_success:
            step_5_success = self.add_image_playlist_to_master()
            trick_play_result.success = step_5_success

            if self.master_manifest_type == "filepath":
                message = "Successfuly added the image playlist to the master.m3u8"
            else:
                web_url = self.master_manifest_path
                if self.master_manifest_path.endswith(".m3u8"):
                    replace_string = self.master_manifest_path.split("/")[-1]
                    web_url = self.master_manifest_path.replace(replace_string, "")

                message = f"Add this string to the master.m3u8 and upload the assets to the web url {web_url}"

                trick_play_result.data = self.master_manifest_trickplay_string

            trick_play_result.message = message

        return trick_play_result

    def read_master_m3u8(self):
        """
        Read the contents of the master m3u8 file.
        """
        success = False
        func = f"{__package__}.{self.name}.{__class__.__name__}.read_master_m3u8"
        post_event(
            "log_debug",
            f"{func}",
            f"Reading the contents of the master m3u8 playlist...",
        )

        self.master_content = m3u8.load(self.master_manifest_path)

        highest_bandwidth = 0
        highest_bandwidth_index = None
        index_count = 0
        for index in self.master_content.data.get("playlists"):
            index_bandwidth = index.get("stream_info").get("bandwidth")
            if index_bandwidth > highest_bandwidth:
                highest_bandwidth = index_bandwidth
                highest_bandwidth_index = index_count

            index_count += 1

        self.source_index = self.master_content.data.get("playlists")[
            highest_bandwidth_index
        ]
        post_event(
            "log_debug",
            f"{func}",
            f"It appears that the highest bandwidth is {highest_bandwidth} with a resolution of {self.source_index.get('stream_info').get('resolution')}",
        )

        if self.source_index is not None:
            success = True

        return success

    def create_destination_folder(self):
        """
        Create the destination folder for the index.m3u8 and images.
        """
        success = False
        func = (
            f"{__package__}.{self.name}.{__class__.__name__}.create_destination_folder"
        )
        post_event("log_debug", f"{func}", f"Creating the image destination folder...")

        # expected types -> filepath or url
        if self.master_manifest_type == "filepath":
            # Get master.m3u8 folder
            self.trickplay_path = pathlib.Path.joinpath(
                pathlib.Path(self.master_manifest_path),
                self.trickplay_foldername,
            )

        else:
            # Use the default folder
            self.trickplay_path = pathlib.Path.joinpath(
                pathlib.Path(self.default_trickplay_path),
                self.trickplay_foldername,
            )

        # Create image folder
        pathlib.Path(self.trickplay_path).mkdir(parents=True, exist_ok=True)

        if pathlib.Path(self.trickplay_path).exists():
            success = True

        return success

    def generate_thumbnails(self):
        """
        Generate the thumbnails for the image playlist.
        """
        success = False
        func = f"{__package__}.{self.name}.{__class__.__name__}.generate_thumbnails"
        post_event("log_debug", f"{func}", f"Generating thumbnail images...")

        thumb_path = (
            f"{self.trickplay_path}/{self.thumb_prefix}-%03d{self.thumb_extension}"
        )

        # ffmpeg -i $INFILE -vf fps=1/$INTERVAL -s $RESOLUTION $OUTPREFIX-%03d.jpg
        args = [
            "-i",
            f"{self.source_index.get('uri')}",
            "-vf",
            f"fps=1/{self.thumb_interval}",
            "-s",
            f"{self.thumb_resolution}",
            f"{thumb_path}",
        ]

        ffmpeg = FFMPEG()
        image_creation = ffmpeg.run(arguments=args)

        success = image_creation.success

        return success

    def create_image_playlist(self):
        """
        Create the image playlsit for the images.
        """
        success = False
        func = f"{__package__}.{self.name}.{__class__.__name__}.create_image_playlist"
        post_event("log_debug", f"{func}", f"Creating the image playlist...")

        image_info_1 = f"#EXTINF:{self.thumb_interval}.000,"
        image_info_2 = f"#EXT-X-TILES:RESOLUTION={self.thumb_resolution},LAYOUT=1x1,DURATION={self.thumb_interval}.000"

        image_files = [
            e.name
            for e in pathlib.Path(self.trickplay_path).iterdir()
            if e.is_file() and e.name.endswith(self.thumb_extension)
        ]

        index_list = []
        # Build header
        index_list.append("#EXTM3U")
        index_list.append(f"#EXT-X-TARGETDURATION:{self.thumb_interval}")
        index_list.append("#EXT-X-VERSION:7")
        index_list.append("#EXT-X-MEDIA-SEQUENCE:1")
        index_list.append("#EXT-X-PLAYLIST-TYPE:VOD")
        index_list.append("#EXT-X-IMAGES-ONLY")
        index_list.append("\n\n")

        max_image_size = 0
        # Add Images
        for image in sorted(image_files):
            size = (
                pathlib.Path(pathlib.Path(self.trickplay_path).joinpath(image))
                .stat()
                .st_size
            )
            if size > max_image_size:
                max_image_size = size

            index_list.append(image_info_1)
            index_list.append(image_info_2)
            index_list.append(image)

        self.thumb_bandwidth = int(max_image_size + (max_image_size * 0.05))

        # Build footer
        index_list.append("\n\n")
        index_list.append("#EXT-X-ENDLIST")

        # Create the playlists in the local folder.
        index_string = "\n".join(index_list)
        index = m3u8.loads(index_string)

        with open(
            pathlib.Path(self.trickplay_path).joinpath(self.trickplay_index_name), "w"
        ) as f:
            f.write(index.dumps())

        if pathlib.Path(
            pathlib.Path(self.trickplay_path).joinpath(self.trickplay_index_name)
        ).exists():
            success = True

        return success

    def add_image_playlist_to_master(self):
        """
        Add the image playlist to the master m3u8.
        """
        success = False
        func = f"{__package__}.{self.name}.{__class__.__name__}.add_image_playlist_to_master"
        post_event(
            "log_debug", f"{func}", f"Adding the image playlist to the master.m3u8"
        )

        self.master_manifest_trickplay_string = f'#EXT-X-IMAGE-STREAM-INF:BANDWIDTH={self.thumb_bandwidth},RESOLUTION={self.thumb_resolution},CODECS="jpeg",URI="{self.trickplay_foldername}/{self.trickplay_index_name}"'

        if self.master_manifest_type == "filepath":
            with open(self.master_manifest_path, "a") as f:
                f.write("\n\n")
                f.write(self.master_manifest_trickplay_string)

            success = True

        return success


if __name__ == "__main__":
    from api.log_listener import setup_log_event_handlers

    setup_log_event_handlers()

    master = "/samples/master.m3u8"

    trickplay = TrickPlay(master=master)
    trickplay.generate_trickplay_assets()
