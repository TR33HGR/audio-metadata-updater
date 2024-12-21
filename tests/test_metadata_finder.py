from hamcrest import \
  assert_that, \
  equal_to_ignoring_case, \
  is_, \
  contains_inanyorder

from audio_metadata_updater.metadata_extractor import ExtractedMetadata
from audio_metadata_updater.metadata_finder import MetadataFinder


def test_metadata_finder_finds_correct_artist_given_extracted_metadata():
    # Given
    metadata_finder = MetadataFinder()
    extracted_metadata = ExtractedMetadata("RUN2U", "STAYC", 1)

    # When
    found_metadata = metadata_finder.find_metadata(extracted_metadata)

    # Then
    assert_that(
        found_metadata.artist,
        equal_to_ignoring_case(extracted_metadata.artist)
    )


def test_metadata_finder_finds_album_name_given_extracted_metadata():
    # Given
    metadata_finder = MetadataFinder()
    extracted_metadata = ExtractedMetadata("RUN2U", "STAYC", 1)

    # When
    found_metadata = metadata_finder.find_metadata(extracted_metadata)

    # Then
    assert_that(
        found_metadata.album,
        equal_to_ignoring_case("Young-Luv.com")
    )


def test_metadata_finder_finds_release_year_given_extracted_metadata():
    # Given
    metadata_finder = MetadataFinder()
    extracted_metadata = ExtractedMetadata("RUN2U", "STAYC", 1)

    # When
    found_metadata = metadata_finder.find_metadata(extracted_metadata)

    # Then
    assert_that(
        found_metadata.year,
        is_(2022)
    )


def test_metadata_finder_finds_genres_and_styles_given_extracted_metadata():
    expected_genres = ["Pop"]
    expected_styles = ["K-pop"]

    # Given
    metadata_finder = MetadataFinder()
    extracted_metadata = ExtractedMetadata("RUN2U", "STAYC", 1)

    # When
    found_metadata = metadata_finder.find_metadata(extracted_metadata)

    # Then
    assert_that(
        found_metadata.genres,
        contains_inanyorder(*expected_genres)
    )
    assert_that(
        found_metadata.styles,
        contains_inanyorder(*expected_styles)
    )
