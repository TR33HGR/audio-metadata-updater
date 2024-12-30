from dataclasses import dataclass
from difflib import SequenceMatcher
import os
from typing import Callable, List
import requests
from audio_metadata_updater.metadata_extractor import ExtractedMetadata


COUNTRIES = ["japan", "japanese", "korea", "korean"]


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
        return self._find_metadata(
            track,
            self._get_album
        )

    def find_compilation_metadata(
        self,
        track: ExtractedMetadata
    ) -> LastFMMetadata:
        return self._find_metadata(
            track,
            lambda album, _:
                self._get_compilation_album(album)
        )

    def _find_metadata(
        self,
        track: ExtractedMetadata,
        resolve_album_mismatch: Callable[[str, str], str]
    ) -> LastFMMetadata:
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

        print(response.json())
        metadata = response.json().get("track")
        if metadata is None:
            return None

        artist = metadata.get("artist").get("name")

        album = metadata.get("album").get("title") \
            if metadata.get("album") \
            else self._get_album(track.album, artist)

        if not same_album(track.album, album):
            album = resolve_album_mismatch(track.album, artist)
            if album is None:
                return None

        track_name = metadata.get("name")

        tags = [tag["name"] for tag in metadata.get("toptags").get("tag")]
        if len(tags) == 0:
            tags = self._get_album_tags(album, artist)
        if len(tags) == 0:
            tags = self._get_artist_tags(artist)

        return LastFMMetadata(
            artist,
            album,
            track_name,
            tags
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

    def _get_album(self, album: str, artist: str) -> str:
        params = self._base_request_params
        params["method"] = "album.getInfo"
        params["album"] = album
        params["artist"] = artist

        response = requests.get(
            self._api_url,
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            print(f"Error: get album: {response.status_code}")
            return None

        metadata = response.json().get("album")
        return metadata.get("name")

    def _get_album_tags(self, album: str, artist: str) -> List[str]:
        params = self._base_request_params
        params["method"] = "album.getTopTags"
        params["album"] = album
        params["artist"] = artist

        response = requests.get(
            self._api_url,
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            print(f"Error: get tags: {response.status_code}")
            return None

        metadata = response.json().get("toptags")
        return [tag["name"] for tag in metadata.get("tag")]

    def _get_artist_tags(self, artist: str) -> List[str]:
        params = self._base_request_params
        params["method"] = "artist.getTopTags"
        params["artist"] = artist

        response = requests.get(
            self._api_url,
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            print(f"Error: get tags: {response.status_code}")
            return None

        metadata = response.json().get("toptags")
        return [tag["name"] for tag in metadata.get("tag")]


def filter_tags(tags: List[str]) -> List[str]:
    filtered_tags = []
    tags = [tag.lower() for tag in tags]

    tags = [tag for tag in tags if tag not in COUNTRIES]

    for tag in tags:
        for i, filtered_tag in enumerate(filtered_tags):
            if are_duplicates(tag, filtered_tag):
                filtered_tags[i] = longest_tag(tag, filtered_tag)
                break
        else:
            filtered_tags.append(tag)

    filtered_tags = [tag.title() for tag in filtered_tags]
    return filtered_tags
