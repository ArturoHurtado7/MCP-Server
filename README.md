# MCP-Server

## Description

This project implements an MCP (Model Context Protocol) server in Python. The server exposes tools to obtain weather information for cities using the Open-Meteo API, and can be consumed by MCP clients or inspected with the MCP Inspector for VS Code.

---

## Python dependencies installation

1. Create and activate a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

1. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## Local development run

You can run the MCP server locally without Nginx or systemd, ideal for development and quick testing.

From the `src` folder, run:

```bash
../venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

This starts the server in autoreload mode (useful for development). Access it from your browser at:

```bash
http://localhost:8000/
```

Or from another machine on the network using your Raspberry Pi's IP:

```bash
http://192.168.10.101:8000/
```

---

## Usage with MCP Inspector

You can use the [MCP Inspector](https://marketplace.visualstudio.com/items?itemName=modelcontextprotocol.inspector) to debug and explore your MCP server from VS Code.

### Recommended run with Inspector

From the project root, run:

```bash
npx -y @modelcontextprotocol/inspector /home/pi/Documents/Projects/MCP-Server/venv/bin/python /home/pi/Documents/Projects/MCP-Server/src/mcp_server/fast_mcp.py
```

Or if you use the `main.py` entrypoint:

```bash
npx -y @modelcontextprotocol/inspector /home/pi/Documents/Projects/MCP-Server/venv/bin/python /home/pi/Documents/Projects/MCP-Server/src/main.py
```

This will open the Inspector in your browser and connect to your MCP server using stdio.

---

## Deployment as a service (daemon) with systemd and Nginx

### 1. Launch the MCP server as a systemd service

Create the file `/etc/systemd/system/mcp-server.service` with:

```ini
[Unit]
Description=MCP Server (uvicorn)
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/Documents/Projects/MCP-Server/src
ExecStart=/home/pi/Documents/Projects/MCP-Server/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

Check the status:

```bash
sudo systemctl status mcp-server
```

---

### 2. Nginx configuration as a reverse proxy

Install Nginx:

```bash
sudo apt update
sudo apt install nginx
```

Create the file `/etc/nginx/sites-available/mcp` with:

```nginx
server {
    listen 80;
    server_name 192.168.10.101;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration and reload Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/mcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### 3. Access from the local network

With the server and Nginx running, access from any device on the network:

```bash
http://192.168.10.101/
```

---

### 4. Restart the service after code changes

```bash
sudo systemctl restart mcp-server
```

It is not necessary to restart Nginx after changes in the Python code.

---

## Additional notes

- For production, use the deployment with systemd and Nginx.
- For development, use `uvicorn` with `--reload`.
- MCP Inspector is useful for debugging and interactive testing.
