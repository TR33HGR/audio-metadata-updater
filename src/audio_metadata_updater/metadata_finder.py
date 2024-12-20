from dataclasses import dataclass
import os
from typing import List
import discogs_client
from audio_metadata_updater.metadata_extractor import ExtractedMetadata


@dataclass
class FoundMetadata:
    artist: str
    album: str
    year: int
    genres: List[str]
    styles: List[str]


class MetadataFinder():
    def __init__(self):
        self._client = discogs_client.Client(
            "audio-metadata-updater/1.0",
            user_token=os.getenv("TOKEN"),
        )

    def find_metadata(self, track: ExtractedMetadata) -> FoundMetadata:
        releases = self._client.search(
            track.track_name,
            artist=track.artist,
            type="release"
        )

        return FoundMetadata(
            releases[0].artists[0].name,
            releases[0].title,
            releases[0].year,
            releases[0].genres,
            releases[0].styles,
        )
