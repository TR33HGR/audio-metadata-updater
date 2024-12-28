from hamcrest import assert_that, is_

from audio_metadata_updater.discogs_metadata_finder import DiscogsMetadata
from audio_metadata_updater.last_fm_metadata_finder import LastFMMetadata
from audio_metadata_updater.metadata_combiner \
  import combine_metadata


def test_metadata_combiner_returns_none_if_there_is_no_metadata():
    # Given
    discogs_metadata = None
    last_fm_metadata = None

    # When
    combined_metadata = combine_metadata(discogs_metadata, last_fm_metadata)

    # Then
    assert_that(combined_metadata, is_(None))


def test_metadata_combiner_returns_metadata_from_discogs_if_last_fm_in_none():
    # Given
    discogs_metadata = DiscogsMetadata(
        "artist",
        "album",
        2020,
        ["genre"],
        ["style"],
        "track_name",
    )
    last_fm_metadata = None

    # When
    combined_metadata = combine_metadata(discogs_metadata, last_fm_metadata)

    # Then
    assert_that(
        combined_metadata.artist,
        is_(discogs_metadata.artist)
    )
    assert_that(
        combined_metadata.album,
        is_(discogs_metadata.album)
    )
    assert_that(
        combined_metadata.year,
        is_(discogs_metadata.year)
    )
    assert_that(
        combined_metadata.genre,
        is_(discogs_metadata.styles[0].title())
    )
    assert_that(
        combined_metadata.track_name,
        is_(discogs_metadata.track_name)
    )


def test_metadata_combiner_returns_metadata_from_last_fm_if_discogs_in_none():
    # Given
    discogs_metadata = None
    last_fm_metadata = LastFMMetadata(
        "artist",
        "album",
        "track_name",
        ["tags"],
    )

    # When
    combined_metadata = combine_metadata(discogs_metadata, last_fm_metadata)

    # Then
    assert_that(
        combined_metadata.artist,
        is_(last_fm_metadata.artist)
    )
    assert_that(
        combined_metadata.album,
        is_(last_fm_metadata.album)
    )
    assert_that(
        combined_metadata.year,
        is_(None)
    )
    assert_that(
        combined_metadata.genre,
        is_(last_fm_metadata.tags[0].title())
    )
    assert_that(
        combined_metadata.track_name,
        is_(last_fm_metadata.track_name)
    )


def test_metadata_combiner_prefers_discogs():
    # Given
    discogs_metadata = DiscogsMetadata(
        "discogs_artist",
        "discogs_album",
        2020,
        ["discogs_genre"],
        ["discogs_style"],
        "discogs_track_name",
    )
    last_fm_metadata = LastFMMetadata(
        "last_fm_artist",
        "last_fm_album",
        "last_fm_track_name",
        ["last_fm_tags"],
    )

    # When
    combined_metadata = combine_metadata(discogs_metadata, last_fm_metadata)

    # Then
    assert_that(
        combined_metadata.artist,
        is_(discogs_metadata.artist)
    )
    assert_that(
        combined_metadata.album,
        is_(discogs_metadata.album)
    )
    assert_that(
        combined_metadata.year,
        is_(discogs_metadata.year)
    )
    assert_that(
        combined_metadata.genre,
        is_(discogs_metadata.styles[0].title())
    )
    assert_that(
        combined_metadata.track_name,
        is_(discogs_metadata.track_name)
    )


def test_metadata_combiner_uses_last_fm_tags_if_no_discogs_styles():
    # Given
    discogs_metadata = DiscogsMetadata(
        "discogs_artist",
        "discogs_album",
        2020,
        ["discogs_genre"],
        [],
        "discogs_track_name",
    )
    last_fm_metadata = LastFMMetadata(
        "last_fm_artist",
        "last_fm_album",
        "last_fm_track_name",
        ["last_fm_tags"],
    )

    # When
    combined_metadata = combine_metadata(discogs_metadata, last_fm_metadata)

    # Then
    assert_that(
        combined_metadata.genre,
        is_(last_fm_metadata.tags[0].title())
    )
