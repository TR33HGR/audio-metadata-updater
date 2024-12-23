from dataclasses import dataclass
from difflib import SequenceMatcher
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


def are_duplicates(tag1: str, tag2: str, threshold=0.7) -> bool:
    return SequenceMatcher(None, tag1, tag2).ratio() > threshold


def longest_tag(tag1: str, tag2: str) -> bool:
    return tag1 if len(tag1) >= len(tag2) else tag2


def same_album(album1: str, album2: str, threshold=0.7) -> bool:
    return SequenceMatcher(
        None, album1.lower(), album2.lower()
    ).ratio() > threshold


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
            print(f"Error: find metadata: {response.status_code}")
            return None

        metadata = response.json().get("track")
        if metadata is None:
            return None

        album = metadata.get("album").get("title")
        if not same_album(track.album, album):
            album = self._get_compilation_album(track.album)
            if album is None:
                return None

        return LastFMMetadata(
            metadata.get("artist").get("name"),
            album,
            metadata.get("name"),
            [tag["name"] for tag in metadata.get("toptags").get("tag")]
        )

    def _get_compilation_album(self, track_album: str) -> str:
        params = self._base_request_params
        params["method"] = "album.getInfo"
        params["album"] = track_album
        params["artist"] = "Various Artists"

        response = requests.get(
            self._api_url,
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            print(f"Error: get comp album: {response.status_code}")
            return None

        metadata = response.json().get("album")
        return metadata.get("name")

    def filter_tags(self, tags: List[str]) -> List[str]:
        filtered_tags = []
        tags = [tag.lower() for tag in tags]

        for tag in tags:
            for i, filtered_tag in enumerate(filtered_tags):
                if are_duplicates(tag, filtered_tag):
                    filtered_tags[i] = longest_tag(tag, filtered_tag)
                    break
            else:
                filtered_tags.append(tag)

        filtered_tags = [tag.title() for tag in filtered_tags]
        return filtered_tags
