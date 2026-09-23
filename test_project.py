from project import dict_to_df, get_tickers_for_dash, make_user_dict


def test_dict_to_df():
    data = {"AAPL": [150.0, 155.0], "TSLA": [700.0, 690.0]}
    result = dict_to_df(data)

    # index should be exactly "Average" and "Current", in that order
    assert list(result.index) == ["Average", "Current"]

    # columns should match the tickers passed in
    assert list(result.columns) == ["AAPL", "TSLA"]

    assert result["AAPL"]["Average"] == 150.0
    assert result["AAPL"]["Current"] == 155.0
    assert result["TSLA"]["Average"] == 700.0
    assert result["TSLA"]["Current"] == 690.0


def test_get_tickers_for_dash():
    data = [("AAPL", 150.0), ("TSLA", 700.0), ("MSFT", 300.0)]
    assert get_tickers_for_dash(data) == ["AAPL", "TSLA", "MSFT"]

    # test empty data. It should return a list with nothing in it
    assert get_tickers_for_dash([]) == []

    assert get_tickers_for_dash(None) == []


def test_make_user_dict():
    assets_info = [("AAPL", 150.0), ("TSLA", 700.0)]
    tickers_price = {"AAPL": 155.0, "TSLA": 690.0, "MSFT": 300.0}

    result = make_user_dict(assets_info, tickers_price)
    assert result == {"AAPL": [150.0, 155.0], "TSLA": [700.0, 690.0]}

    # a ticker the user doesn't hold should be ignored, not included
    assert "MSFT" not in result

    # a ticker with no matching current price should not appear in the result
    assets_info_missing = [("GOOGL", 2800.0)]
    result_missing = make_user_dict(assets_info_missing, tickers_price)
    assert result_missing == {}