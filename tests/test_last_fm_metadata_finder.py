from hamcrest import \
  assert_that, \
  contains_inanyorder, \
  equal_to_ignoring_case, \
  is_

from audio_metadata_updater.last_fm_metadata_finder import LastFMMetadataFinder, filter_tags
from audio_metadata_updater.metadata_extractor import ExtractedMetadata


def test_last_fm_metadata_finder_finds_metadata_given_extracted_metadata():
    expected_tags = ["k-pop", "Kpop", "electronic", "pop", "Electroclash"]

    # Given
    metadata_finder = LastFMMetadataFinder()
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
        found_metadata.tags,
        contains_inanyorder(*expected_tags)
    )
    assert_that(
        found_metadata.track_name,
        equal_to_ignoring_case("RUN2U")
    )


def test_last_fm_metadata_finder_finds_tags_from_artist_if_no_track_tags_found():
    expected_tags = ["japan", "J-rock", "J-Emo", "japanese", "j-alternative rock", "j-shoegaze", "j-dream pop", "alt-idol", "j-pixie"]

    # Given
    metadata_finder = LastFMMetadataFinder()
    extracted_metadata = ExtractedMetadata(
        "ghost girls generation",
        "airattic",
        1,
        "Whatever"
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
        equal_to_ignoring_case("Whatever")
    )
    assert_that(
        found_metadata.tags,
        contains_inanyorder(*expected_tags)
    )
    assert_that(
        found_metadata.track_name,
        equal_to_ignoring_case("ghost girls generation")
    )


def test_last_fm_metadata_finder_queies_album_metadata_if_track_metadata_not_found():
    expected_tags = ["japan", "J-rock", "J-Emo", "japanese", "j-alternative rock", "j-shoegaze", "j-dream pop", "alt-idol", "j-pixie"]

    # Given
    metadata_finder = LastFMMetadataFinder()
    extracted_metadata = ExtractedMetadata(
        "オイルド・クラーケン",
        "airattic",
        2,
        "Whatever"
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
        equal_to_ignoring_case("Whatever")
    )
    assert_that(
        found_metadata.tags,
        contains_inanyorder(*expected_tags)
    )
    assert_that(
        found_metadata.track_name,
        equal_to_ignoring_case("オイルド・クラーケン")
    )


def test_last_fm_metadata_finder_finds_original_album_data_given_compilation():
    expected_tags = ["Hip-Hop", "80s", "rap", "needleontherecord", "NYC"]

    # Given
    metadata_finder = LastFMMetadataFinder()
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
        equal_to_ignoring_case(
            "Electro: The Definitive Electro & Hip Hop Collection"
        )
    )
    assert_that(
        found_metadata.tags,
        contains_inanyorder(*expected_tags)
    )
    assert_that(
        found_metadata.track_name,
        equal_to_ignoring_case("The Bronx")
    )


def test_last_fm_metadata_finder_returns_none_if_track_not_found():
    # Given
    metadata_finder = LastFMMetadataFinder()
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


def test_last_fm_metadata_finder_tags_filter_removes_duplicate_tags():
    expected_tags = ["K-Pop"]

    # Given
    found_tags = ["K-Pop", "Kpop"]

    # When
    filtered_tags = filter_tags(found_tags)

    # Then
    assert_that(
        filtered_tags,
        contains_inanyorder(*expected_tags)
    )


def test_last_fm_metadata_finder_tags_filter_favours_more_specific_tags():
    expected_tags = ["K-Pop", "Electroclash"]

    # Given
    found_tags = ["Pop", "K-Pop", "Electronic", "Electroclash"]

    # When
    filtered_tags = filter_tags(found_tags)

    # Then
    assert_that(
        filtered_tags,
        contains_inanyorder(*expected_tags)
    )


def test_last_fm_metadata_finder_tags_filter_formats_tags_to_title_case():
    expected_tags = ["K-Pop"]

    # Given
    found_tags = ["k-pop"]

    # When
    filtered_tags = filter_tags(found_tags)

    # Then
    assert_that(
        filtered_tags,
        contains_inanyorder(*expected_tags)
    )


def test_last_fm_metadata_finder_tags_filter_removes_country_from_tags():
    expected_tags = ["J-Rock", "J-Emo", "J-Alternative Rock", "J-Shoegaze", "J-Dream Pop", "Alt-Idol", "J-Pixie"]

    # Given
    found_tags = ["japan", "J-rock", "J-Emo", "japanese", "j-alternative rock", "j-shoegaze", "j-dream pop", "alt-idol", "j-pixie"]

    # When
    filtered_tags = filter_tags(found_tags)

    # Then
    assert_that(
        filtered_tags,
        contains_inanyorder(*expected_tags)
    )
