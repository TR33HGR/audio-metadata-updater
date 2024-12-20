from hamcrest import assert_that, is_
from audio_metadata_updater.template import is_true


def test():
    assert_that(is_true(), is_(True))
