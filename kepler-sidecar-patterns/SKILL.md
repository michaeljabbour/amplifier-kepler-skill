---
name: kepler-sidecar-patterns
description: Python sidecar patterns — FastAPI routes, spawn capability, streaming, and approvals
---

# Kepler Sidecar Patterns

The Kepler sidecar is a Python process (FastAPI) that bridges the desktop frontend to Amplifier Core. It manages agent lifecycle, translates streaming events, and enforces desktop-specific guardrails.

## Route Structure

Routes follow the **`create_*_router` factory pattern**. Each route module exports a factory function that returns a configured `APIRouter`.

```python
# sidecar/routes/agent.py
from fastapi import APIRouter

def create_agent_router(agent_service, approval_system) -> APIRouter:
    router = APIRouter(prefix="/agent", tags=["agent"])

    @router.post("/spawn")
    async def spawn_agent(request: SpawnRequest):
        ...

    @router.get("/stream/{session_id}")
    async def stream_events(session_id: str):
        ...

    return router
```

```python
# sidecar/main.py — registration
app = FastAPI()
app.include_router(create_agent_router(agent_service, approval_system))
app.include_router(create_session_router(session_store))
app.include_router(create_tools_router(tool_registry))
```

### Adding a New Route

1. **Create the module**: `sidecar/routes/my_feature.py` with a `create_my_feature_router()` factory function.
2. **Register in main.py**: Import and call `app.include_router(create_my_feature_router(...))` with required dependencies.
3. **Add tests**: Create `tests/sidecar/test_my_feature.py` exercising the new endpoints.

## Spawn Capability

When the desktop app spawns an agent, the sidecar:

1. **Receives the spawn request** with prompt, model, and options
2. **Strips the child mount plan** — removes filesystem mounts that don't apply to the child context
3. **Applies depth cap** — enforces a maximum delegation depth to prevent unbounded recursion
4. **Streams results** back to the frontend as server-sent events (SSE)

```python
async def spawn_agent(request: SpawnRequest):
    # Strip child mount plan for security
    config = strip_child_mounts(request.config)

    # Enforce depth cap
    if request.depth >= MAX_DEPTH:
        raise DepthExceeded(f"depth cap of {MAX_DEPTH} reached")

    # Run agent with result streaming
    async for event in agent_service.run(config, request.prompt):
        yield format_sse(event)
```

The depth cap prevents runaway delegation chains. Default is typically 5 levels.

## Streaming Translation

The sidecar translates Amplifier Core events into frontend-consumable SSE. There are 4 key events:

| Event | Source | Frontend Action |
|-------|--------|-----------------|
| `token` | Provider stream chunk | Append text to message display |
| `tool_call` | Agent loop tool dispatch | Show tool execution indicator |
| `tool_result` | Tool execution complete | Display tool output |
| `turn_complete` | Agent loop turn finished | Finalize message, enable input |

```python
async def translate_event(core_event) -> SSEEvent:
    match core_event.type:
        case "token":
            return SSEEvent(event="token", data=core_event.content)
        case "tool_call":
            return SSEEvent(event="tool_call", data=core_event.tool_info)
        case "tool_result":
            return SSEEvent(event="tool_result", data=core_event.result)
        case "turn_complete":
            return SSEEvent(event="turn_complete", data=core_event.summary)
```

## Approval Protocol

Desktop approval uses the **`DesktopApprovalSystem`** which bridges tool execution to the UI for user consent.

```python
class DesktopApprovalSystem:
    """Routes approval requests to the desktop UI."""

    def __init__(self, websocket_manager, auto_approve: bool = False):
        self.ws = websocket_manager
        self.auto_approve = auto_approve

    async def request_approval(self, tool_name: str, args: dict) -> bool:
        if self.auto_approve:
            return True

        # Send approval request to frontend via WebSocket
        request_id = uuid4()
        await self.ws.send("approval_request", {
            "id": request_id,
            "tool": tool_name,
            "args": args
        })

        # Wait for user response
        response = await self.ws.wait_for(f"approval_{request_id}")
        return response.approved
```

When `auto_approve` is `True`, all tool executions proceed without user confirmation. This is useful for development but should be disabled in production use.

The approval flow:
1. Agent requests tool execution
2. Sidecar sends approval request to frontend via WebSocket
3. Frontend displays approval dialog to user
4. User approves or denies
5. Sidecar relays decision back to agent loop

## Guardrails

The sidecar enforces 4 rules that protect the desktop environment:

1. **Depth Cap**: Maximum delegation depth prevents unbounded agent recursion. Spawned agents inherit a decremented depth counter.
2. **Mount Stripping**: Child agents cannot inherit parent filesystem mounts. Each spawn gets a clean, scoped context.
3. **Approval Gate**: Destructive tool calls (file writes, shell commands) require explicit user approval unless `auto_approve` is enabled.
4. **Timeout Enforcement**: Every agent turn has a maximum execution time. Hung agents are killed and their partial results returned to the frontend.

These guardrails are non-negotiable in the desktop context. They exist to protect the user's machine and prevent runaway resource consumption.
