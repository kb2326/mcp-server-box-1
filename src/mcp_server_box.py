import logging

from mcp.server.fastmcp import FastMCP

from server_context import box_lifespan
import box_tools

# Disable all logging
logging.basicConfig(level=logging.CRITICAL)
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

# Override the logging call that's visible in the original code
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

# Initialize FastMCP server
mcp = FastMCP("Box MCP Server", lifespan=box_lifespan)

# Register all tools
mcp.tool()(box_tools.box_who_am_i)
mcp.tool()(box_tools.box_authorize_app_tool)
mcp.tool()(box_tools.box_search_tool)
mcp.tool()(box_tools.box_read_tool)
mcp.tool()(box_tools.box_ask_ai_tool)
mcp.tool()(box_tools.box_ask_ai_tool_multi_file)
mcp.tool()(box_tools.box_hubs_ask_ai_tool)
mcp.tool()(box_tools.box_search_folder_by_name)
mcp.tool()(box_tools.box_ai_extract_data)
mcp.tool()(box_tools.box_list_folder_content_by_folder_id)
mcp.tool()(box_tools.box_manage_folder_tool)
mcp.tool()(box_tools.box_upload_file_from_path_tool)
mcp.tool()(box_tools.box_upload_file_from_content_tool)
mcp.tool()(box_tools.box_download_file_tool)
mcp.tool()(box_tools.box_docgen_create_batch_tool)
mcp.tool()(box_tools.box_docgen_get_job_tool)
mcp.tool()(box_tools.box_docgen_list_jobs_tool)
mcp.tool()(box_tools.box_docgen_list_jobs_by_batch_tool)
mcp.tool()(box_tools.box_docgen_template_create_tool)
mcp.tool()(box_tools.box_docgen_template_list_tool)
mcp.tool()(box_tools.box_docgen_template_delete_tool)
mcp.tool()(box_tools.box_docgen_template_get_by_id_tool)
mcp.tool()(box_tools.box_docgen_template_list_tags_tool)
mcp.tool()(box_tools.box_docgen_template_list_jobs_tool)


if __name__ == "__main__":
    # Run with stdio transport (default)
    mcp.run(transport="stdio")
