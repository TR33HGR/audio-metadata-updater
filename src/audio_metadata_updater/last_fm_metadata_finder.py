from dataclasses import dataclass
import os
from typing import List
import requests
from audio_metadata_updater.metadata_extractor import ExtractedMetadata


@dataclass
class LastFMMetadata:
    artist: str
    album: str
    track_name: str
    tags: List[str]


class LastFMMetadataFinder():
    def __init__(self):
        self._api_url = "http://ws.audioscrobbler.com/2.0/"
        self._base_request_params = {
            "api_key": os.getenv("LAST_FM_API_KEY"),
            "format": "json",
        }

    def find_metadata(self, track: ExtractedMetadata) -> LastFMMetadata:
        params = self._base_request_params
        params["method"] = "track.getInfo"
        params["artist"] = track.artist
        params["track"] = track.track_name

        response = requests.get(
            self._api_url,
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None

        metadata = response.json().get("track")

        return LastFMMetadata(
            metadata.get("artist").get("name"),
            metadata.get("album").get("title"),
            metadata.get("name"),
            [tag["name"] for tag in metadata.get("toptags").get("tag")]
        )
