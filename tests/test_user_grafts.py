import pytest
from facts.grafts import user_grafts
from facts.grafts.helpers import as_graft
from collections.abc import Mapping


@pytest.mark.asyncio
async def test_user():
    data = await as_graft(user_grafts.user_data_info)()
    assert isinstance(data.value, Mapping)
