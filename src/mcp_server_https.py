import argparse
import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from mcp.server.fastmcp import FastMCP

from box_tools_ai import (
    box_ai_ask_file_multi_tool,
    box_ai_ask_file_single_tool,
    box_ai_ask_hub_tool,
    box_ai_extract_freeform_tool,
    box_ai_extract_structured_enhanced_using_fields_tool,
    box_ai_extract_structured_enhanced_using_template_tool,
    box_ai_extract_structured_using_fields_tool,
    box_ai_extract_structured_using_template_tool,
)
from box_tools_docgen import (
    box_docgen_create_batch_tool,
    box_docgen_create_single_file_from_user_input_tool,
    box_docgen_get_job_by_id_tool,
    box_docgen_list_jobs_by_batch_tool,
    box_docgen_list_jobs_tool,
    box_docgen_template_create_tool,
    box_docgen_template_get_by_id_tool,
    box_docgen_template_get_by_name_tool,
    box_docgen_template_list_jobs_tool,
    # box_docgen_template_delete_tool, # very dangerous tool, use with caution
    box_docgen_template_list_tags_tool,
    box_docgen_template_list_tool,
)
from box_tools_files import (
    box_download_file_tool,
    box_read_tool,
    box_upload_file_from_content_tool,
    box_upload_file_from_path_tool,
)
from box_tools_folders import (
    box_list_folder_content_by_folder_id,
    box_manage_folder_tool,
)
from box_tools_generic import box_authorize_app_tool, box_who_am_i
from box_tools_metadata import (
    box_metadata_delete_instance_on_file_tool,
    box_metadata_get_instance_on_file_tool,
    box_metadata_set_instance_on_file_tool,
    box_metadata_template_create_tool,
    box_metadata_template_get_by_name_tool,
    box_metadata_update_instance_on_file_tool,
)
from box_tools_search import box_search_folder_by_name_tool, box_search_tool
from server_context import box_lifespan

# Disable all logging except CRITICAL
logging.basicConfig(level=logging.CRITICAL)
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)


def get_mcp_server(host: str, port: int) -> FastMCP:
    return FastMCP(
        "Box MCP HTTP Server",
        stateless_http=True,
        host=host,
        port=port,
        lifespan=box_lifespan,
    )


def register_tools(mcp: FastMCP):
    mcp.tool()(box_who_am_i)
    mcp.tool()(box_authorize_app_tool)
    mcp.tool()(box_search_tool)
    mcp.tool()(box_search_folder_by_name_tool)

    mcp.tool()(box_ai_ask_file_single_tool)
    mcp.tool()(box_ai_ask_file_multi_tool)
    mcp.tool()(box_ai_ask_hub_tool)
    mcp.tool()(box_ai_extract_freeform_tool)
    mcp.tool()(box_ai_extract_structured_using_fields_tool)
    mcp.tool()(box_ai_extract_structured_using_template_tool)
    mcp.tool()(box_ai_extract_structured_enhanced_using_fields_tool)
    mcp.tool()(box_ai_extract_structured_enhanced_using_template_tool)

    mcp.tool()(box_docgen_create_batch_tool)
    mcp.tool()(box_docgen_get_job_by_id_tool)
    mcp.tool()(box_docgen_list_jobs_tool)
    mcp.tool()(box_docgen_list_jobs_by_batch_tool)
    mcp.tool()(box_docgen_template_create_tool)
    mcp.tool()(box_docgen_template_list_tool)
    mcp.tool()(box_docgen_template_get_by_id_tool)
    mcp.tool()(box_docgen_template_list_tags_tool)
    mcp.tool()(box_docgen_template_list_jobs_tool)
    mcp.tool()(box_docgen_template_get_by_name_tool)
    mcp.tool()(box_docgen_create_single_file_from_user_input_tool)

    mcp.tool()(box_read_tool)
    mcp.tool()(box_upload_file_from_path_tool)
    mcp.tool()(box_upload_file_from_content_tool)
    mcp.tool()(box_download_file_tool)

    mcp.tool()(box_list_folder_content_by_folder_id)
    mcp.tool()(box_manage_folder_tool)

    mcp.tool()(box_metadata_template_get_by_name_tool)
    mcp.tool()(box_metadata_set_instance_on_file_tool)
    mcp.tool()(box_metadata_get_instance_on_file_tool)
    mcp.tool()(box_metadata_delete_instance_on_file_tool)
    mcp.tool()(box_metadata_update_instance_on_file_tool)
    mcp.tool()(box_metadata_template_create_tool)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Box MCP HTTP Server")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=10000,
        help="Port for HTTP transport (default: 10000 for Render)",
    )

    args = parser.parse_args()

    mcp = get_mcp_server(host=args.host, port=args.port)
    register_tools(mcp)

    # ✅ Add /callback handler for Box OAuth redirect
    app: FastAPI = mcp.app

    @app.get("/callback")
    async def box_oauth_callback(request: Request):
        code = request.query_params.get("code")
        state = request.query_params.get("state")
        print(f"[Box OAuth] Received code: {code}")
        print(f"[Box OAuth] Received state: {state}")
        return HTMLResponse("<h2>✅ Authorization successful. You may now close this tab.</h2>")

    # Optional: diagnostics
    @mcp.tool()
    def mcp_server_info():
        return {
            "server_name": mcp.name,
            "transport": "streamable-http",
            "host": args.host,
            "port": args.port,
        }

    mcp.run(transport="streamable-http")
