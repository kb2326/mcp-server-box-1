from typing import List

import pytest

from box_tools_search import box_search_folder_by_name_tool, box_search_tool


@pytest.mark.asyncio
async def test_box_search_tool(ctx):
    query = "HAB-1"
    where_to_look_for_query = ["NAME", "DESCRIPTION"]
    result = await box_search_tool(
        ctx, query, where_to_look_for_query=where_to_look_for_query
    )

    assert isinstance(result, List)
    assert len(result) > 0
    assert "name" in result[0]
    assert "id" in result[0]
    assert "type" in result[0]
    assert any("HAB-1" in file["name"] for file in result)


@pytest.mark.asyncio
async def test_box_api_locate_folder_by_name(ctx):
    result = await box_search_folder_by_name_tool(ctx, "Airbyte-CI")
    assert isinstance(result, List)
    assert len(result) > 0
    assert "name" in result[0]
    assert "id" in result[0]
    assert "type" in result[0]
    assert any("Airbyte-CI" in folder["name"] for folder in result)
