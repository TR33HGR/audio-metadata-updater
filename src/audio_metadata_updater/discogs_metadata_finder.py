from dataclasses import dataclass
from difflib import SequenceMatcher
import difflib
import os
from typing import List, Tuple
import discogs_client
from audio_metadata_updater.metadata_extractor import ExtractedMetadata


@dataclass
class DiscogsMetadata:
    artist: str
    album: str
    year: int
    genres: List[str]
    styles: List[str]
    track_name: str


def same_album(album1: str, album2: str, threshold=0.7) -> bool:
    return SequenceMatcher(
        None, album1.lower(), album2.lower()
    ).ratio() > threshold


def get_album(title: str) -> str:
    return title if not " - " in title else title.split(" - ")[1]


def oldest_release(releases):
    releases = [release for release in releases if int(release.year) > 0]
    return sorted(releases, key=lambda release: int(release.year))[0]


class DiscogsMetadataFinder():
    def __init__(self):
        self._client = discogs_client.Client(
            "audio-metadata-updater/1.0",
            user_token=os.getenv("DISCOGS_TOKEN"),
        )

    def find_metadata(self, track: ExtractedMetadata) -> DiscogsMetadata:
        releases = self._client.search(
            track.track_name,
            artist=track.artist,
            format="album",
            type="release"
        )

        if len(releases) == 0:
            return None

        release = oldest_release(releases)

        artist = release.artists[0].name
        album = get_album(release.title)
        year = release.year
        genres = release.genres
        styles = release.styles

        track_index = track.track_number-1
        if not same_album(track.album, album):
            title, tracklist = self._get_compilation_release(track.album)
            album = get_album(title)
            track_name = tracklist[track_index].title
        else:
            track_name = release.tracklist[track_index].title

        return DiscogsMetadata(
            artist,
            album,
            year,
            genres,
            styles,
            track_name,
        )

    def _get_compilation_release(self, track_album: str) -> Tuple[str, str]:
        releases = self._client.search(
            track_album,
            type="release"
        )
        releases = [release for release in releases if same_album(get_album(release.title), track_album)]
        release = oldest_release(releases)
        return release.title, release.tracklist
