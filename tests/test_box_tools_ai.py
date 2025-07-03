from typing import List

import pytest

from box_tools_ai import (
    box_ai_extract_tool,
    box_ai_extract_tool_multi_file,
    box_ask_ai_tool,
    box_ask_ai_tool_multi_file,
    box_hubs_ask_ai_tool,
)

# @pytest.mark.asyncio
# async def test_box_search_tool(ctx):


@pytest.mark.asyncio
async def test_box_ask_ai_tool(ctx):
    # HAB-1-01.docx = 1728677291168. This file must exists
    resp = await box_ask_ai_tool(
        ctx, "1728677291168", "what are the key point of this file"
    )
    assert resp is not None
    assert len(resp) > 0
    assert resp is not None
    assert len(resp) > 0
    assert isinstance(resp, dict)
    assert "answer" in resp
    assert "HAB-1-01" in resp.get("answer")


@pytest.mark.asyncio
async def test_box_ai_extract_tool(ctx):
    resp: dict = await box_ai_extract_tool(
        ctx,
        "1728677291168",
        "contract date, start date, end date, lessee name, lessee email, rent, property id",
    )
    assert resp is not None
    assert len(resp) > 0
    answer = resp.get("answer")
    # convert answer str to dict
    answer = eval(answer)
    assert isinstance(answer, dict)
    assert answer.get("contract date") is not None
    assert answer.get("start date") is not None
    assert answer.get("end date") is not None
    assert answer.get("lessee name") is not None
    assert answer.get("lessee email") is not None


@pytest.mark.asyncio
async def test_box_ask_ai_tool_multi_file(ctx):
    file_ids = [
        "1823610366483",
        "1823610356883",
        "1823610359283",
        "1823610364083",
        "1823610368883",
    ]
    resp: dict = await box_ask_ai_tool_multi_file(
        ctx,
        file_ids,
        "what items where bought in these documents",
    )

    assert resp is not None
    assert len(resp) > 0
    assert isinstance(resp, dict)
    assert "answer" in resp


@pytest.mark.asyncio
async def test_box_api_ai_extract_multi(ctx):
    file_ids = [
        "1728675448213",
        "1728675498613",
        "1728675455413",
    ]
    resp: dict = await box_ai_extract_tool_multi_file(
        ctx,
        file_ids,
        "contract date, start date, end date, lessee name, lessee email, rent, property id",
    )

    assert resp is not None
    assert len(resp) > 0
    assert isinstance(resp, dict)
    assert "answer" in resp
