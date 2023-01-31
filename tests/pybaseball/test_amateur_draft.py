from typing import Callable

import pandas as pd
import pytest

from pybaseball.amateur_draft import _URL, amateur_draft

from .conftest import GetDataFrameCallable


@pytest.fixture(name="sample_html")
def _sample_html(get_data_file_contents: Callable[[str], str]) -> str:
    return get_data_file_contents('amateur_draft.html')


@pytest.fixture(name="sample_processed_result")
def _sample_processed_result(get_data_file_dataframe: GetDataFrameCallable) -> pd.DataFrame:
    return get_data_file_dataframe('amateur_draft_keep_stats.csv')


@pytest.fixture(name="sample_processed_result_no_stats")
def _sample_processed_result_no_stats(get_data_file_dataframe: GetDataFrameCallable) -> pd.DataFrame:
    return get_data_file_dataframe('amateur_draft_no_stats.csv')


def test_amateur_draft(response_get_monkeypatch: Callable, sample_html: str,
                       sample_processed_result: pd.DataFrame) -> None:
    expected_url = _URL.format(year=2019, draft_round=1)

    response_get_monkeypatch(sample_html, expected_url)
    result = amateur_draft(2019, 1)

    assert result is not None
    assert not result.empty

    pd.testing.assert_frame_equal(result, sample_processed_result, check_dtype=False)


def test_amateur_draft_no_stats(response_get_monkeypatch: Callable, sample_html: str,
                                sample_processed_result_no_stats: pd.DataFrame) -> None:
    expected_url = _URL.format(year=2019, draft_round=1)

    response_get_monkeypatch(sample_html, expected_url)
    result = amateur_draft(2019, 1, keep_stats=False)

    assert result is not None
    assert not result.empty

    pd.testing.assert_frame_equal(result, sample_processed_result_no_stats, check_dtype=False)
