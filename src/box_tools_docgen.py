import json
import os

from box_ai_agents_toolkit import (
    box_docgen_create_batch_from_user_input,
    # box_docgen_create_batch,
    box_docgen_get_job_by_id,
    box_docgen_list_jobs,
    box_docgen_list_jobs_by_batch,
    box_docgen_template_create,
    box_docgen_template_delete,
    box_docgen_template_get_by_id,
    box_docgen_template_list,
    box_docgen_template_list_jobs,
    box_docgen_template_list_tags,
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client


async def box_docgen_create_batch_tool(
    ctx: Context,
    file_id: str,
    destination_folder_id: str,
    user_input_file_path: str,
    output_type: str = "pdf",
) -> str:
    """
    Generate documents from a Box Doc Gen template using a local JSON file.

    Args:
        file_id (str): ID of the template file in Box.
        destination_folder_id (str): Where to save the generated documents.
        user_input_file_path (str): Path to a local JSON file containing
            either a single dict or a list of dicts for document generation.
        output_type (str): Output format (e.g. 'pdf'). Defaults to 'pdf'.

    Returns:
        str: JSON-serialized response from Box, or an error message.
    """
    box_client = get_box_client(ctx)
    try:
        path = os.path.expanduser(user_input_file_path)
        if not os.path.isfile(path):
            return f"Error: user_input_file_path '{user_input_file_path}' not found"
        with open(path, "r", encoding="utf-8") as f:
            raw_input = json.load(f)

        # If no explicit generated_file_name, use any override provided in JSON
        if "file_name" in raw_input and isinstance(raw_input, dict):
            generated_file_name = raw_input.pop("file_name")
        else:
            generated_file_name = "Test_Name"

        batch = box_docgen_create_batch_from_user_input(
            client=box_client,
            file_id=file_id,
            destination_folder_id=destination_folder_id,
            user_input=raw_input,
            generated_file_name=generated_file_name,
            output_type=output_type,
        )
        # Return the serialized batch result as pretty JSON
        return json.dumps(_serialize(batch), indent=2)
    except Exception as e:
        return f"Error generating document batch: {str(e)}"


async def box_docgen_get_job_tool(ctx: Context, job_id: str) -> str:
    """
    Fetch a single DocGen job by its ID.
    """
    box_client = get_box_client(ctx)
    response = box_docgen_get_job_by_id(box_client, job_id)
    # Serialize SDK object to JSON-safe structures
    return json.dumps(_serialize(response), indent=2)


async def box_docgen_list_jobs_tool(
    ctx: Context,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all DocGen jobs for the current user (paginated).
    """
    box_client = get_box_client(ctx)
    response = box_docgen_list_jobs(box_client, marker=marker, limit=limit)
    # Serialize SDK object to JSON-safe structures
    return json.dumps(_serialize(response), indent=2)


async def box_docgen_list_jobs_by_batch_tool(
    ctx: Context,
    batch_id: str,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all DocGen jobs that belong to a particular batch.
    """
    box_client = get_box_client(ctx)
    try:
        response = box_docgen_list_jobs_by_batch(
            box_client, batch_id=batch_id, marker=marker, limit=limit
        )

        # Create a simple dictionary with basic information
        result = {
            "batch_id": batch_id,
            "response_type": str(type(response)),
            "available_attributes": dir(response),
        }

        # Try to access some common attributes safely
        if hasattr(response, "total_count"):
            result["total_count"] = response.total_count

        if hasattr(response, "entries"):
            result["job_count"] = len(response.entries)
            result["jobs"] = []
            for job in response.entries:
                try:
                    job_info = {"type": str(type(job)), "attributes": dir(job)}
                    # Try to safely get some common job attributes
                    for attr in ["id", "status", "created_at", "modified_at"]:
                        if hasattr(job, attr):
                            job_info[attr] = str(getattr(job, attr))
                    result["jobs"].append(job_info)
                except Exception as job_error:
                    result["jobs"].append({"error": str(job_error)})

        return json.dumps(result, indent=2)
    except Exception as e:
        # Return a formatted error JSON
        return json.dumps(
            {
                "error": str(e),
                "batch_id": batch_id,
                "details": "Error occurred while processing the response",
            },
            indent=2,
        )


async def box_docgen_template_create_tool(ctx: Context, file_id: str) -> str:
    """
    Mark a file as a Box Doc Gen template.
    """
    box_client = get_box_client(ctx)
    response = box_docgen_template_create(box_client, file_id)
    # The SDK returns a DocGenTemplateBase object which isn't directly JSON-serializable.
    # Use the common _serialize helper to convert it into plain dict/list primitives before dumping to JSON.
    return json.dumps(_serialize(response))


async def box_docgen_template_list_tool(
    ctx: Context,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all Box Doc Gen templates accessible to the user.
    """
    box_client = get_box_client(ctx)
    templates = box_docgen_template_list(box_client, marker=marker, limit=limit)
    return json.dumps(_serialize(templates))


async def box_docgen_template_delete_tool(ctx: Context, template_id: str) -> str:
    """
    Remove the Doc Gen template marking from a file.
    """
    box_client = get_box_client(ctx)
    box_docgen_template_delete(box_client, template_id)
    return json.dumps({"deleted_template": template_id})


async def box_docgen_template_get_by_id_tool(ctx: Context, template_id: str) -> str:
    """
    Retrieve details of a specific Box Doc Gen template.
    """
    box_client = get_box_client(ctx)
    template = box_docgen_template_get_by_id(box_client, template_id)
    return json.dumps(_serialize(template))


async def box_docgen_template_list_tags_tool(
    ctx: Context,
    template_id: str,
    template_version_id: str | None = None,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all tags on a Box Doc Gen template.
    """
    box_client = get_box_client(ctx)
    tags = box_docgen_template_list_tags(
        box_client,
        template_id,
        template_version_id=template_version_id,
        marker=marker,
        limit=limit,
    )
    return json.dumps(_serialize(tags))


async def box_docgen_template_list_jobs_tool(
    ctx: Context,
    template_id: str,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all Doc Gen jobs that used a specific template.
    """
    box_client = get_box_client(ctx)
    jobs = box_docgen_template_list_jobs(
        box_client, template_id=template_id, marker=marker, limit=limit
    )
    return json.dumps(_serialize(jobs))


# Helper to make Box SDK objects JSON-serializable
def _serialize(obj):
    """Recursively convert Box SDK objects (which expose __dict__) into
    plain dict / list structures so they can be json.dumps-ed."""

    if isinstance(obj, list):
        return [_serialize(i) for i in obj]

    # Primitive types are fine
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj

    # Handle dictionary-like objects
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}

    # SDK models generally have __dict__ with public attributes
    try:
        if hasattr(obj, "__dict__"):
            return {
                k: _serialize(v)
                for k, v in obj.__dict__.items()
                if not k.startswith("_")
            }

        # Try to get all public attributes if __dict__ is not available
        return {
            k: _serialize(getattr(obj, k))
            for k in dir(obj)
            if not k.startswith("_") and not callable(getattr(obj, k))
        }
    except Exception:
        # If all else fails, convert to string
        return str(obj)
