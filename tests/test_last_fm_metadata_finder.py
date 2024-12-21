from hamcrest import \
  assert_that, \
  contains_inanyorder, \
  equal_to_ignoring_case

from audio_metadata_updater.last_fm_metadata_finder import LastFMMetadataFinder
from audio_metadata_updater.metadata_extractor import ExtractedMetadata


def test_last_fm_metadata_finder_finds_metadata_given_extracted_metadata():
    expected_tags = ["k-pop", "Kpop", "electronic", "pop", "Electroclash"]

    # Given
    metadata_finder = LastFMMetadataFinder()
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
        found_metadata.tags,
        contains_inanyorder(*expected_tags)
    )
    assert_that(
        found_metadata.track_name,
        equal_to_ignoring_case("RUN2U")
    )
