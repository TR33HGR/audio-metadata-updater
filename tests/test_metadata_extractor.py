from pathlib import Path
from hamcrest import assert_that, is_

from audio_metadata_updater.metadata_extractor \
  import extract_metadata_from_file


def test_metadata_extractor_returns_english_file_track_name_from_flacs():
    # Given
    audio_file = Path("res/how_sweet.flac")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_name, is_("How Sweet"))


def test_metadata_extractor_returns_file_track_name_from_wmas():
    # Given
    audio_file = Path("res/RUN2U.wma")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_name, is_("RUN2U"))


def test_metadata_extractor_returns_file_track_name_from_aiffs():
    # Given
    audio_file = Path("res/Martini.aiff")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_name, is_("Martini"))


def test_metadata_extractor_returns_file_track_name_from_aifs():
    # Given
    audio_file = Path("res/Buffalo.aif")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_name, is_("Buffalo"))


def test_metadata_extractor_returns_artist_name_from_flacs():
    # Given
    audio_file = Path("res/how_sweet.flac")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.artist, is_("New Jeans"))


def test_metadata_extractor_returns_artist_from_wmas():
    # Given
    audio_file = Path("res/RUN2U.wma")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.artist, is_("STAYC"))


def test_metadata_extractor_returns_artist_from_aiffs():
    # Given
    audio_file = Path("res/Martini.aiff")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.artist, is_("device operator"))


def test_metadata_extractor_returns_artist_from_aifs():
    # Given
    audio_file = Path("res/Buffalo.aif")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.artist, is_("Mountain Man"))


def test_metadata_extractor_returns_english_track_number_from_flacs():
    # Given
    audio_file = Path("res/how_sweet.flac")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_number, is_(1))


def test_metadata_extractor_returns_track_number_from_wmas():
    # Given
    audio_file = Path("res/RUN2U.wma")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_number, is_(1))


def test_metadata_extractor_returns_track_number_from_aiffs():
    # Given
    audio_file = Path("res/Martini.aiff")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_number, is_(1))


def test_metadata_extractor_returns_track_number_from_aifs():
    # Given
    audio_file = Path("res/Buffalo.aif")

    # When
    metadata = extract_metadata_from_file(audio_file)

    # Then
    assert_that(metadata.track_number, is_(1))
