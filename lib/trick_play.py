"""
Create trick play for hls - based on Roku requirements.
"""
# TODO: Add reference to the Roku requirements.
# TODO: Add reference to apple hls trick play definitions.
# Built-in

# Special

# App
from api.event import post_event


class TrickPlay:
    """
    Create images and needed manifests. This is based on some Roku Instructions.
    """

    master_manifest = None

    def __init__(self) -> None:
        pass

    def read_master_m3u8(self):
        """
        Read the contents of the master m3u8 file.
        """
        success = False
        func = f"{__name__}.{__class__}.read_master_m3u8"
        post_event(
            "log_debug",
            f"{func}",
            f"Reading the contents of the master m3u8 playlist...",
        )

        pass

    def create_destination_folder(self):
        """
        Create the destination folder for the index.m3u8 and images.
        """
        success = False
        func = f"{__name__}.{__class__}.create_destination_folder"
        post_event("log_debug", f"{func}", f"Creating the image destination folder...")

        pass

    def generate_thumbnails():
        """
        Generate the thumbnails for the image playlist.
        """
        success = False
        func = f"{__name__}.{__class__}.generate_thumbnails"
        post_event("log_debug", f"{func}", f"Generating thumbnail images...")

        pass

    def create_image_playlist():
        """
        Create the image playlsit for the images.
        """
        success = False
        func = f"{__name__}.{__class__}.create_image_playlist"
        post_event("log_debug", f"{func}", f"Creating the image playlist...")

        pass

    def add_image_playlist_to_master():
        """
        Add the image playlist to the master m3u8.
        """
        success = False
        func = f"{__name__}.{__class__}.add_image_playlist_to_master"
        post_event("log_debug", f"{func}", f"Creating the image playlist...")

        pass
