# 📊 Remote MCP Expense Tracker Server

An autonomous, production-ready Model Context Protocol (MCP) server built with FastMCP and SQLite3. This server exposes local financial ledger capabilities—adding, listing, and summarizing expenses—to any LLM client (like Claude or LangChain agents) over a remote network connection via Server-Sent Events (SSE).

## 🚀 Features

### Persistent Ledger
Automatically initializes and manages a local `expenses.db` SQLite instance.

### Intelligent Tool Suite

- **add_expense**: Records transactions with dates, categories, subcategories, and metadata.
- **list_expense**: Queries transactional history between specific date boundaries.
- **summarize**: Generates category-wise financial summaries.

### Static Resource Routing

Exposes a dedicated `expense://categories` URI providing JSON schemas of valid budgeting categories.

### Remote-Ready Architecture

Switches from traditional Standard I/O (`stdio`) to a distributed network layer (`sse`), listening globally on port `8000`.

## 🛠️ Tech Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.11+ |
| Core Framework | FastMCP (Model Context Protocol SDK) |
| Database | SQLite3 (Embedded) |
| Transport Layer | SSE (Server-Sent Events) over HTTP |

## 📦 Installation & Setup

This repository uses **uv** for lightning-fast Python package and environment management.

### 1. Clone the Repository

```bash
git clone https://github.com/DebarghaNath/remote-mcp-server.git
cd remote-mcp-server
```

### 2. Install Dependencies

```bash
uv sync
```

Alternatively:

```bash
uv add fastmcp
```

### 3. Initialize Configuration Files

Ensure you have a `categories.json` file in the root folder, or let the server automatically generate a default configuration on its first run.

```json
[
  "Food",
  "Utilities",
  "Entertainment",
  "Housing",
  "Transportation"
]
```

## 🏃‍♂️ Running the Server

To launch the remote server and open it up to network traffic, run:

```bash
uv run main.py
```

Upon startup, the terminal will indicate that the SSE server is actively listening:

```text
🚀 Launching Remote Expense Tracker Server on port 8000...
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 🔌 Connecting Your Client

To wire this server into an LLM Agent framework (such as LangChain's `MultiServerMCPClient` or an Anthropic Claude Desktop setup), configure your client transport block using the network endpoint.

### LangChain Client Example (`client.py`)

```python
SERVERS = {
    "expense_tracker": {
        "transport": "sse",
        "url": "http://<SERVER_IP_ADDRESS>:8000/sse"
    }
}
```

### Claude Desktop Configuration (`mcp.json`)

```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "mcp.client.sse",
        "http://localhost:8000/sse"
      ]
    }
  }
}
```

## 🔒 Security Note

> [!WARNING]
> Because `host="0.0.0.0"` binds the server to all network interfaces, anyone who can reach your machine's IP address on port `8000` can read or write to your expense database.
>
> If exposing this outside a home Wi-Fi network, consider placing it behind a reverse proxy (such as Nginx) or a secure VPN tunnel (such as Tailscale).

## 📄 License

This project is open-source and available under the MIT License.
