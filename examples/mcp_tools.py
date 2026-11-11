"""Optional FastMCP adapter for fictional read-only task data.

Requires a separately installed `fastmcp` library. No live FileMaker access.
"""

try:
    from fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("Install the optional FastMCP package to run this example") from exc

from findit_showcase.structured import TaskStore

mcp = FastMCP(name="FindIt AI Synthetic Tools")
_store = TaskStore.synthetic()


@mcp.tool
def count_sample_tasks(status: str = "open") -> int:
    """Count fictional tasks for a fixed example identity."""
    return _store.count_tasks("user-001", status)


@mcp.tool
def list_sample_tasks() -> list[dict]:
    """List fictional tasks for a fixed example identity."""
    return _store.list_tasks("user-001")


if __name__ == "__main__":
    mcp.run(transport="stdio")
