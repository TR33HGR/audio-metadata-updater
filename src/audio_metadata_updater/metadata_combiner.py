from dataclasses import dataclass
from audio_metadata_updater.discogs_metadata_finder import DiscogsMetadata
from audio_metadata_updater.last_fm_metadata_finder \
    import LastFMMetadata, filter_tags


@dataclass
class Metadata:
    artist: str
    album: str
    year: int
    genre: str
    track_name: str


def combine_metadata(
    discogs: DiscogsMetadata, last_fm: LastFMMetadata
) -> Metadata:
    if discogs is None and last_fm is None:
        return None

    genre = discogs.styles[0] if discogs and len(discogs.styles) \
        else filter_tags(last_fm.tags)[0]

    return Metadata(
        discogs.artist if discogs else last_fm.artist,
        discogs.album if discogs else last_fm.album,
        discogs.year if discogs else None,
        genre.title(),
        discogs.track_name if discogs else last_fm.track_name,
    )
