import sqlite3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

conn = sqlite3.connect('delivery.db')
conn.row_factory = sqlite3.Row

class DatabaseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0]
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.encode())
        
        elif path == '/api/tables':
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.send_json({"tables": tables})
        
        elif path.startswith('/api/table/'):
            table = path.split('/')[-1]
            limit = 100
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} LIMIT {limit}")
            columns = [desc[0] for desc in cursor.description]
            rows = [dict(row) for row in cursor.fetchall()]
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total = cursor.fetchone()[0]
            self.send_json({
                "table": table,
                "columns": columns,
                "rows": rows,
                "total": total,
                "showing": len(rows)
            })
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        pass  # Suppress logging

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MoveEasy Delivery Database Viewer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; margin-bottom: 20px; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .tables { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-bottom: 20px; }
        .table-btn { 
            padding: 15px; background: #4ECDC4; color: white; border: none; border-radius: 6px;
            cursor: pointer; font-weight: bold; transition: all 0.2s;
        }
        .table-btn:hover { background: #45B7D1; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .table-btn.active { background: #FF6B6B; }
        .content { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .table-info { color: #666; margin-bottom: 15px; font-size: 14px; }
        table { width: 100%; border-collapse: collapse; }
        th { background: #f8f8f8; padding: 12px; text-align: left; border-bottom: 2px solid #ddd; font-weight: bold; }
        td { padding: 12px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f9f9f9; }
        .loading { text-align: center; color: #666; padding: 40px; }
        .error { color: #FF6B6B; padding: 10px; background: #ffe0e0; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚚 MoveEasy Delivery Database Viewer</h1>
        <div class="tables" id="tables"></div>
        <div class="content" id="content"><div class="loading">Select a table to view data...</div></div>
    </div>

    <script>
        let currentTable = null;

        document.addEventListener('DOMContentLoaded', function() {
            fetch('/api/tables')
                .then(r => r.json())
                .then(data => {
                    console.log('Tables loaded:', data);
                    const container = document.getElementById('tables');
                    data.tables.forEach(table => {
                        const btn = document.createElement('button');
                        btn.className = 'table-btn';
                        btn.textContent = table + ' 📊';
                        btn.setAttribute('data-table', table);
                        btn.onclick = function() { loadTable(table); };
                        container.appendChild(btn);
                    });
                })
                .catch(e => {
                    console.error('Failed to load tables:', e);
                    document.getElementById('tables').innerHTML = `<div class="error">Failed to load tables: ${e}</div>`;
                });
        });

        function loadTable(table) {
            currentTable = table;
            document.querySelectorAll('.table-btn').forEach(b => b.classList.remove('active'));
            document.querySelector(`[data-table="${table}"]`).classList.add('active');
            
            document.getElementById('content').innerHTML = '<div class="loading">Loading...</div>';
            
            fetch(`/api/table/${table}`)
                .then(r => r.json())
                .then(data => {
                    let html = `<div class="table-info">📌 ${data.table} | Total: ${data.total.toLocaleString()} rows | Showing: ${data.showing}</div>`;
                    html += '<table><thead><tr>';
                    data.columns.forEach(col => html += `<th>${col}</th>`);
                    html += '</tr></thead><tbody>';
                    data.rows.forEach(row => {
                        html += '<tr>';
                        data.columns.forEach(col => {
                            let val = row[col];
                            if (val === null) val = '<em>NULL</em>';
                            else if (typeof val === 'string' && val.length > 100) val = val.substring(0, 100) + '...';
                            html += `<td>${val}</td>`;
                        });
                        html += '</tr>';
                    });
                    html += '</tbody></table>';
                    document.getElementById('content').innerHTML = html;
                })
                .catch(e => {
                    console.error('Failed to load table:', e);
                    document.getElementById('content').innerHTML = `<div class="error">Error loading table: ${e}</div>`;
                });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = 8888
    server = HTTPServer(('127.0.0.1', port), DatabaseHandler)
    print(f"✅ Database viewer running at http://localhost:{port}")
    print(f"   Open this URL in your browser to explore delivery.db")
    server.serve_forever()
