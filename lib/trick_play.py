"""
Create trick play for hls - based on Roku requirements.
"""
# TODO: Add reference to the Roku requirements.
# TODO: Add reference to apple hls trick play definitions.
# Built-in
from urllib.parse import urlparse

# Special

# App
from api.event import post_event


class TrickPlay:
    """
    Create images and needed manifests. This is based on some Roku Instructions.
    """

    master_manifest = None
    master_manifest_type = None

    def __init__(self, master) -> None:
        self.master_manifest = master
        self.master_manifest_type = get_source_type(master)

    def generate_trickplay_assets(self) -> bool:
        """
        Function to generate the trick play assets.
        """
        success = False
        func = f"{__name__}.{__class__.__name__}.generate_trickplay_assets"
        post_event(
            "log_debug",
            f"{func}",
            f"Generateing trick play assets...",
        )

        step_1_success = self.read_master_m3u8()
        if step_1_success:
            step_2_success = self.create_destination_folder()

        if step_2_success:
            step_3_success = self.generate_thumbnails()

        if step_3_success:
            step_4_success = self.create_image_playlist()

        if step_4_success:
            step_5_success = self.add_image_playlist_to_master()
            success = step_5_success

        return success

    def read_master_m3u8(self):
        """
        Read the contents of the master m3u8 file.
        """
        success = False
        func = f"{__name__}.{__class__.__name__}.read_master_m3u8"
        post_event(
            "log_debug",
            f"{func}",
            f"Reading the contents of the master m3u8 playlist...",
        )

        success = True
        return success

    def create_destination_folder(self):
        """
        Create the destination folder for the index.m3u8 and images.
        """
        success = False
        func = f"{__name__}.{__class__.__name__}.create_destination_folder"
        post_event("log_debug", f"{func}", f"Creating the image destination folder...")

        success = True
        return success

    def generate_thumbnails(self):
        """
        Generate the thumbnails for the image playlist.
        """
        success = False
        func = f"{__name__}.{__class__.__name__}.generate_thumbnails"
        post_event("log_debug", f"{func}", f"Generating thumbnail images...")

        success = True
        return success

    def create_image_playlist(self):
        """
        Create the image playlsit for the images.
        """
        success = False
        func = f"{__name__}.{__class__.__name__}.create_image_playlist"
        post_event("log_debug", f"{func}", f"Creating the image playlist...")

        success = True
        return success

    def add_image_playlist_to_master(self):
        """
        Add the image playlist to the master m3u8.
        """
        success = False
        func = f"{__name__}.{__class__.__name__}.add_image_playlist_to_master"
        post_event("log_debug", f"{func}", f"Creating the image playlist...")

        success = True
        return success


def get_source_type(source: str) -> str:
    """
    Determine if the source string is a web url or local file path.
    """
    parsed = urlparse(source)
    if parsed.scheme in ["http", "https"]:
        return "url"
    else:
        return "filepath"
