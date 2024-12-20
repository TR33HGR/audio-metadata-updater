from pathlib import Path
from mutagen import File
from mutagen.asf import ASF
from mutagen.aiff import AIFF

from audio_metadata_updater.metadata import Metadata


def extract_metadata_from_file(audio_file: Path) -> Metadata:

    if audio_file.suffix == ".wma":
        metadata_file = ASF(audio_file)
        return Metadata(
            metadata_file.get("Title")[0],
            metadata_file.get("Author")[0]
        )

    if audio_file.suffix in (".aiff", ".aif"):
        metadata_file = AIFF(audio_file)
        return Metadata(
            metadata_file.get("TIT2")[0],
            metadata_file.get("TPE1")[0]
        )

    metadata_file = File(audio_file)
    return Metadata(
        metadata_file.get("title")[0],
        metadata_file.get("artist")[0]
    )
