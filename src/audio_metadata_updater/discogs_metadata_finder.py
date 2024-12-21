from dataclasses import dataclass
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

        return DiscogsMetadata(
            releases[0].artists[0].name,
            releases[0].title,
            releases[0].year,
            releases[0].genres,
            releases[0].styles,
            releases[0].tracklist[track.track_number-1].title,
            releases[0].country,
            releases[0].labels[0].name,
        )
