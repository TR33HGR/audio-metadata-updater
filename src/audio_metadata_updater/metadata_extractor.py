from dataclasses import dataclass
from pathlib import Path
from mutagen import File
from mutagen.asf import ASF
from mutagen.aiff import AIFF


@dataclass
class ExtractedMetadata:
    track_name: str
    artist: str
    track_number: int


def extract_metadata_from_file(audio_file: Path) -> ExtractedMetadata:

    if audio_file.suffix == ".wma":
        metadata_file = ASF(audio_file)
        return ExtractedMetadata(
            metadata_file.get("Title")[0],
            metadata_file.get("Author")[0],
            int(str(metadata_file.get("WM/TrackNumber")[0])),
        )

    if audio_file.suffix in (".aiff", ".aif"):
        metadata_file = AIFF(audio_file)
        return ExtractedMetadata(
            metadata_file.get("TIT2")[0],
            metadata_file.get("TPE1")[0],
            int(metadata_file.get("TRCK")[0]),
        )

    metadata_file = File(audio_file)
    return ExtractedMetadata(
        metadata_file.get("title")[0],
        metadata_file.get("artist")[0],
        int(metadata_file.get("tracknumber")[0]),
    )
