import pytest
from facts.formatters import BytesType, MetricType, PercType, TimeType, mark


@pytest.mark.parametrize("input, raw, human", [
    (0, 0.0, "0"),
    (1, 1, "1"),
    (999, 999, "999"),
    (1000, 1000, "1 K"),
    (1024, 1024, "1.02 K"),
    (1536, 1536, "1.54 K"),
    (1048576, 1048576, "1.05 M"),
])
def test_metric(input, raw, human):
    data = MetricType(input)
    assert isinstance(data, int)
    assert isinstance(data, MetricType)
    assert data == raw
    assert data.human == human


@pytest.mark.parametrize("input, raw, human", [
    (0, 0.0, "0 B"),
    (1, 1, "1 B"),
    (1024, 1024, "1 KB"),
    (1536, 1536, "1.50 KB"),
    (1048576, 1048576, "1 MB"),
])
def test_bytes(input, raw, human):
    data = BytesType(input)
    assert isinstance(data, int)
    assert isinstance(data, BytesType)
    assert data == raw
    assert data.human == human


@pytest.mark.parametrize("input, raw, human", [
    (1.5, 1.5, "1.50%"),
    (12.5, 12.5, "12.50%"),
    (75.0, 75.0, "75%"),
    (100, 100, "100%"),
])
def test_perc(input, raw, human):
    data = PercType(input)
    assert isinstance(data, float)
    assert isinstance(data, PercType)
    assert data == raw
    assert data.human == human


@pytest.mark.parametrize("input, raw, human", [
    (1, 1, "T01S"),
    (59, 59, "T59S"),
    (60, 60, "T01M"),
    (61, 61, "T01M01S"),
    (3600, 3600, "T01H"),
    (3601, 3601, "T01H01S"),
    (3660, 3660, "T01H01M"),
    (3661, 3661, "T01H01M01S"),
    (86400, 86400, "T24H"),
    (86401, 86401, "T24H01S"),
    (86461, 86461, "T24H01M01S"),
    (90000, 90000, "P1DT01H")
])
def test_time(input, raw, human):
    data = TimeType(input)
    assert isinstance(data, float)
    assert isinstance(data, TimeType)
    assert data == raw
    assert data.human == human


@pytest.mark.parametrize("input, type, human", [
    (1, None, 1),
    (1, 'metric', "1"),
    (1, 'bytes', "1 B"),
    (1, 'percentage', "1%"),
    (1, 'duration', "T01S"),
    (100, None, 100),
    (100, 'metric', "100"),
    (100, 'bytes', "100 B"),
    (100, 'percentage', "100%"),
    (100, 'duration', "T01M40S"),
])
def test_mark(input, type, human):
    data = mark(input, type)
    data = getattr(data, 'human', data)
    assert data == human
