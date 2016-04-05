import pytest
from facts.grafts import user_grafts
from collections.abc import Mapping


@pytest.mark.asyncio
async def test_user():
    data = await user_grafts.user_data_info()
    assert isinstance(data.value, Mapping)
