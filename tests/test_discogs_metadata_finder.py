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
    extracted_metadata = ExtractedMetadata("RUN2U", "STAYC", 1)

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
    assert_that(
        found_metadata.country,
        equal_to_ignoring_case("South Korea")
    )
    assert_that(
        found_metadata.label,
        equal_to_ignoring_case("High Up Entertainment")
    )
