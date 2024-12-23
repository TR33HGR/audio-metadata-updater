import argparse
from pathlib import Path

from audio_metadata_updater.discogs_metadata_finder \
    import DiscogsMetadataFinder
from audio_metadata_updater.last_fm_metadata_finder \
    import LastFMMetadataFinder
from audio_metadata_updater.metadata_combiner \
    import combine_metadata
from audio_metadata_updater.metadata_extractor \
    import extract_metadata_from_file


EXTENSIONS = [".wma", ".flac", ".aif", ".aiff"]


class MetadataUpdater():
    def __init__(self):
        self.discogs_metadata_finder = DiscogsMetadataFinder()
        self.last_fm_metadata_finder = LastFMMetadataFinder()

    def update_file(self, file: Path):
        print(f"finding metadata for {file}")
        current_metadata = extract_metadata_from_file(file)
        print(f"current metadata is {current_metadata}")
        discogs_metadata = \
            self.discogs_metadata_finder.find_metadata(current_metadata)
        print(f"discogs metadata is {discogs_metadata}")
        last_fm_metadata = \
            self.last_fm_metadata_finder.find_metadata(current_metadata)
        print(f"last_fm metadata is {last_fm_metadata}")
        combined_metadata = \
            combine_metadata(discogs_metadata, last_fm_metadata)

        print(combined_metadata.genre)


def process_music_library(library_path: str):
    path = Path(library_path)
    if not path.exists():
        print(f"Error: {path.resolve()} does not exist")
        return
    if not path.is_dir():
        print(f"Error: {path.resolve()} is not a directory")
        return

    metadata_updater = MetadataUpdater()

    for file in path.rglob("*"):
        if file.suffix.lower() in EXTENSIONS:
            metadata_updater.update_file(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update the metadata of a music library."
    )
    parser.add_argument(
        "library_path",
        type=str,
        help="Path to the music library"
    )
    args = parser.parse_args()

    process_music_library(args.library_path)
