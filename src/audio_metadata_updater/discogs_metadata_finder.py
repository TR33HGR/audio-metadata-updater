from dataclasses import dataclass
from difflib import SequenceMatcher
import difflib
import os
from typing import List
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
    country: str
    label: str


def same_album(album1: str, album2: str, threshold=0.7) -> bool:
    return SequenceMatcher(None, album1, album2).ratio() > threshold


def get_track_index(track: str, album_tracklist: List[str]) -> int:
    album_tracklist = [track.title for track in album_tracklist]
    print(album_tracklist)
    matching_track = difflib.get_close_matches(
        track, album_tracklist, n=1, cutoff=0.6
    )
    return album_tracklist.index(matching_track[0])


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
            type="release"
        )

        track_index = \
            track.track_number-1 \
            if same_album(track.album, releases[0].title) \
            else get_track_index(track.track_name, releases[0].tracklist)

        return DiscogsMetadata(
            releases[0].artists[0].name,
            releases[0].title,
            releases[0].year,
            releases[0].genres,
            releases[0].styles,
            releases[0].tracklist[track_index].title,
            releases[0].country,
            releases[0].labels[0].name,
        )
