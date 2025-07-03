import pytest

from box_tools_generic import box_who_am_i


@pytest.mark.asyncio
async def test_box_who_am_i(ctx):
    result = await box_who_am_i(ctx)

    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result
    assert "login" in result
    assert "type" in result
    assert result["type"] == "user"
