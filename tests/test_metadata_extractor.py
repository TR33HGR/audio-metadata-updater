from pathlib import Path
from hamcrest import assert_that, is_

from audio_metadata_updater.metadata_extractor \
  import extract_metadata_from_file


def test_metadata_extractor_returns_metadata_from_flacs():
    # Given
    audio_file = Path("res/how_sweet.flac")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_name, is_("How Sweet"))
    assert_that(metadata.artist, is_("New Jeans"))
    assert_that(metadata.track_number, is_(1))
    assert_that(metadata.album, is_("How Sweet & Bubble Gum"))


def test_metadata_extractor_returns_metadata_from_wmas():
    # Given
    audio_file = Path("res/RUN2U.wma")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_name, is_("RUN2U"))
    assert_that(metadata.artist, is_("STAYC"))
    assert_that(metadata.track_number, is_(1))
    assert_that(metadata.album, is_("YOUNG-LUV.COM"))


def test_metadata_extractor_returns_metadata_from_aiffs():
    # Given
    audio_file = Path("res/Martini.aiff")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_name, is_("Martini"))
    assert_that(metadata.artist, is_("device operator"))
    assert_that(metadata.track_number, is_(1))
    assert_that(metadata.album, is_("Cherry Fortune"))


def test_metadata_extractor_returns_metadata_from_aifs():
    # Given
    audio_file = Path("res/Buffalo.aif")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_name, is_("Buffalo"))
    assert_that(metadata.artist, is_("Mountain Man"))
    assert_that(metadata.track_number, is_(1))
    assert_that(metadata.album, is_("Made the Harbor"))
