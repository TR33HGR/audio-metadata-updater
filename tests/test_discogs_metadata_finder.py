from hamcrest import \
  assert_that, \
  equal_to_ignoring_case, \
  is_, \
  contains_inanyorder

from audio_metadata_updater.metadata_extractor import ExtractedMetadata
from audio_metadata_updater.discogs_metadata_finder \
    import DiscogsMetadataFinder


def test_discogs_metadata_finder_finds_metadata_given_extracted_metadata():
    expected_genres = ["Pop"]
    expected_styles = ["K-pop"]

    # Given
    metadata_finder = DiscogsMetadataFinder()
    extracted_metadata = ExtractedMetadata(
        "RUN2U",
        "STAYC",
        1,
        "Young-Luv.com"
    )

    # When
    found_metadata = metadata_finder.find_metadata(extracted_metadata)

    # Then
    assert_that(
        found_metadata.artist,
        equal_to_ignoring_case(extracted_metadata.artist)
    )
    assert_that(
        found_metadata.album,
        equal_to_ignoring_case("Young-Luv.com")
    )
    assert_that(
        found_metadata.year,
        is_(2022)
    )
    assert_that(
        found_metadata.genres,
        contains_inanyorder(*expected_genres)
    )
    assert_that(
        found_metadata.styles,
        contains_inanyorder(*expected_styles)
    )
    assert_that(
        found_metadata.track_name,
        equal_to_ignoring_case("RUN2U")
    )


def test_discogs_metadata_finder_finds_original_album_data_given_compilation():
    expected_genres = ["Hip Hop"]
    expected_styles = []

    # Given
    metadata_finder = DiscogsMetadataFinder()
    extracted_metadata = ExtractedMetadata(
        "The Bronx",
        "Kurtis Blow",
        10,
        "Electro: The Definitive Electro & Hip Hop Collection"
    )

    # When
    found_metadata = metadata_finder.find_metadata(extracted_metadata)

    # Then
    assert_that(
        found_metadata.artist,
        equal_to_ignoring_case(extracted_metadata.artist)
    )
    assert_that(
        found_metadata.album,
        equal_to_ignoring_case("The Definitive Electro & Hip Hop Collection")
    )
    assert_that(
        found_metadata.year,
        is_(1986)
    )
    assert_that(
        found_metadata.genres,
        contains_inanyorder(*expected_genres)
    )
    assert_that(
        found_metadata.styles,
        contains_inanyorder(*expected_styles)
    )
    assert_that(
        found_metadata.track_name,
        equal_to_ignoring_case("The Bronx")
    )


def test_discogs_metadata_finder_returns_none_if_track_not_found():
    # Given
    metadata_finder = DiscogsMetadataFinder()
    extracted_metadata = ExtractedMetadata(
        "ddflkja",
        "ojhalf",
        10,
        "okjhfoasihfjo"
    )

    # When
    found_metadata = metadata_finder.find_metadata(extracted_metadata)

    # Then
    assert_that(
        found_metadata,
        is_(None)
    )
