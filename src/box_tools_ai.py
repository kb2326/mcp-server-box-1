from typing import List

from box_ai_agents_toolkit import (
    box_file_ai_ask,
    box_file_ai_extract,
    box_hubs_ai_ask,
    box_multi_file_ai_ask,
    box_multi_file_ai_extract,
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client


async def box_ask_ai_tool(ctx: Context, file_id: str, prompt: str) -> dict:
    """
    Ask box ai about a file in Box.

    Args:
        file_id (str): The ID of the file to read.
        prompt (str): The prompt to ask the AI.
    return:
        dict: The text content of the file.
    """
    # check if file id isn't a string and convert to a string
    if not isinstance(file_id, str):
        file_id = str(file_id)

    box_client = get_box_client(ctx)
    response = box_file_ai_ask(box_client, file_id, prompt=prompt)
    return response


async def box_ask_ai_tool_multi_file(
    ctx: Context, file_ids: List[str], prompt: str
) -> dict:
    """
    Use Box AI to analyze and respond to a prompt based on the content of multiple files.

    This tool allows users to query Box AI with a specific prompt, leveraging the content
    of multiple files stored in Box. The AI processes the files and generates a response
    based on the provided prompt.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_ids (List[str]): A list of file IDs to be analyzed by the AI.
        prompt (str): The prompt or question to ask the AI.

    Returns:
        dict: The AI-generated response based on the content of the specified files.

    Raises:
        Exception: If there is an issue with the Box client, AI agent, or file processing.
    """
    box_client = get_box_client(ctx)
    response = box_multi_file_ai_ask(box_client, file_ids, prompt=prompt)
    return response


async def box_hubs_ask_ai_tool(ctx: Context, hubs_id: str, prompt: str) -> dict:
    """
    Ask box ai about a hub in Box. Currently there is no way to discover a hub
    in Box, so you need to know the id of the hub. We will fix this in the future.

    Args:
        hubs_id (str): The ID of the hub to read.
        prompt (str): The prompt to ask the AI.
    return:
        dict: The text content of the file.
    """
    # check if file id isn't a string and convert to a string
    if not isinstance(hubs_id, str):
        hubs_id = str(hubs_id)

    box_client = get_box_client(ctx)
    # ai_agent = box_claude_ai_agent_ask()
    response = box_hubs_ai_ask(box_client, hubs_id, prompt=prompt)
    return response


async def box_ai_extract_tool(ctx: Context, file_id: str, fields: str) -> dict:
    """ "
    Extract data from a single file in Box using AI.

    Args:
        file_id (str): The ID of the file to read.
        fields (str): The fields to extract from the file.
    return:
        dict: The extracted data in a json string format.
    """
    box_client = get_box_client(ctx)

    # check if file id isn't a string and convert to a string
    if not isinstance(file_id, str):
        file_id = str(file_id)

    response = box_file_ai_extract(box_client, file_id, fields)
    return response


async def box_ai_extract_tool_multi_file(
    ctx: Context, file_ids: List[str], fields: str
) -> dict:
    """ "
    Extract data from multiple files in Box using AI.

    Args:
        file_ids (List[str]): The IDs of the files to read.
        fields (str): The fields to extract from the files.
    return:
        dict: The extracted data in a json string format.
    """
    box_client = get_box_client(ctx)

    # check if file ids aren't a list of strings and convert to a list of strings
    if not isinstance(file_ids, list):
        file_ids = [str(file_ids)]
    else:
        file_ids = [str(file_id) for file_id in file_ids]

    response = box_multi_file_ai_extract(box_client, file_ids, fields)
    return response
