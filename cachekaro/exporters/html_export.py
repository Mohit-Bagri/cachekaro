"""
HTML exporter for CacheKaro.

Produces interactive HTML reports with charts and tables.
"""

from datetime import datetime
import html
import json
from typing import Any

from cachekaro.exporters.base import Exporter, ExportFormat
from cachekaro.models.scan_result import ScanResult
from cachekaro.platforms.base import Category


class HtmlExporter(Exporter):
    """
    Exports scan results to HTML format.

    Produces a standalone HTML page with:
    - Interactive charts (using Chart.js)
    - Sortable/filterable tables
    - Responsive design
    - Dark/light mode support
    """

    def __init__(self, title: str = "CacheKaro Report", dark_mode: bool = False):
        """
        Initialize the HTML exporter.

        Args:
            title: Page title
            dark_mode: Use dark color scheme
        """
        self.title = title
        self.dark_mode = dark_mode

    @property
    def format(self) -> ExportFormat:
        return ExportFormat.HTML

    @property
    def file_extension(self) -> str:
        return "html"

    def export(self, result: ScanResult) -> str:
        """Export scan result to HTML format."""
        # Prepare data for charts
        category_data = self._prepare_category_data(result)
        top_items_data = self._prepare_top_items_data(result)

        # Build HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en" data-theme="{'dark' if self.dark_mode else 'light'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(self.title)}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --border-color: #dee2e6;
            --accent-color: #0d6efd;
            --success-color: #198754;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
        }}

        [data-theme="dark"] {{
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --text-primary: #eaeaea;
            --text-secondary: #a0a0a0;
            --border-color: #404040;
            --accent-color: #4da6ff;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, var(--accent-color), #6610f2);
            border-radius: 12px;
            color: white;
        }}

        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}

        header .subtitle {{
            opacity: 0.9;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background-color: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border-color);
        }}

        .card h2 {{
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: var(--accent-color);
        }}

        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }}

        .stat {{
            text-align: center;
            padding: 15px;
            background-color: var(--bg-primary);
            border-radius: 8px;
        }}

        .stat-value {{
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--accent-color);
        }}

        .stat-label {{
            font-size: 0.9rem;
            color: var(--text-secondary);
        }}

        .chart-container {{
            position: relative;
            height: 300px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}

        th {{
            background-color: var(--bg-primary);
            font-weight: 600;
            cursor: pointer;
        }}

        th:hover {{
            background-color: var(--border-color);
        }}

        tr:hover {{
            background-color: var(--bg-primary);
        }}

        .size-large {{ color: var(--danger-color); font-weight: bold; }}
        .size-medium {{ color: var(--warning-color); }}
        .size-small {{ color: var(--success-color); }}

        .risk-safe {{
            background-color: #d4edda;
            color: #155724;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
        }}
        .risk-moderate {{
            background-color: #fff3cd;
            color: #856404;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
        }}
        .risk-caution {{
            background-color: #f8d7da;
            color: #721c24;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
        }}

        .search-box {{
            width: 100%;
            padding: 10px 15px;
            margin-bottom: 15px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-size: 1rem;
        }}

        footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: var(--text-secondary);
        }}

        @media (max-width: 768px) {{
            .stat-grid {{
                grid-template-columns: 1fr;
            }}
            header h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>CacheKaro</h1>
            <p class="subtitle">Storage & Cache Analysis Report</p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>

        <!-- Summary Stats -->
        <div class="grid">
            <div class="card">
                <h2>Disk Overview</h2>
                <div class="stat-grid">
                    <div class="stat">
                        <div class="stat-value">{result.formatted_disk_total}</div>
                        <div class="stat-label">Total Space</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{result.formatted_disk_used}</div>
                        <div class="stat-label">Used</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{result.formatted_disk_free}</div>
                        <div class="stat-label">Free</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{result.disk_usage_percent:.1f}%</div>
                        <div class="stat-label">Usage</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>Cache Summary</h2>
                <div class="stat-grid">
                    <div class="stat">
                        <div class="stat-value">{result.formatted_total_size}</div>
                        <div class="stat-label">Total Cache</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{result.formatted_cleanable_size}</div>
                        <div class="stat-label">Cleanable (Safe)</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{result.total_files:,}</div>
                        <div class="stat-label">Files</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{len(result.items)}</div>
                        <div class="stat-label">Locations</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts -->
        <div class="grid">
            <div class="card">
                <h2>Space by Category</h2>
                <div class="chart-container">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>Top Consumers</h2>
                <div class="chart-container">
                    <canvas id="topItemsChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Detailed Table -->
        <div class="card">
            <h2>All Cache Locations</h2>
            <input type="text" class="search-box" id="searchBox" placeholder="Search cache locations...">
            <table id="cacheTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Name</th>
                        <th onclick="sortTable(1)">Category</th>
                        <th onclick="sortTable(2)">Size</th>
                        <th onclick="sortTable(3)">Files</th>
                        <th onclick="sortTable(4)">Age (Days)</th>
                        <th onclick="sortTable(5)">Risk</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_table_rows(result)}
                </tbody>
            </table>
        </div>

        <footer>
            <p>Generated by CacheKaro | Cache Karo!</p>
        </footer>
    </div>

    <script>
        // Category Pie Chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(categoryCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(category_data['labels'])},
                datasets: [{{
                    data: {json.dumps(category_data['values'])},
                    backgroundColor: [
                        '#0d6efd', '#6610f2', '#6f42c1', '#d63384',
                        '#dc3545', '#fd7e14', '#ffc107', '#198754',
                        '#20c997', '#0dcaf0'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'right',
                        labels: {{
                            color: getComputedStyle(document.body).getPropertyValue('--text-primary')
                        }}
                    }}
                }}
            }}
        }});

        // Top Items Bar Chart
        const topCtx = document.getElementById('topItemsChart').getContext('2d');
        new Chart(topCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(top_items_data['labels'])},
                datasets: [{{
                    label: 'Size (MB)',
                    data: {json.dumps(top_items_data['values'])},
                    backgroundColor: '#0d6efd'
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    x: {{
                        ticks: {{
                            color: getComputedStyle(document.body).getPropertyValue('--text-primary')
                        }}
                    }},
                    y: {{
                        ticks: {{
                            color: getComputedStyle(document.body).getPropertyValue('--text-primary')
                        }}
                    }}
                }}
            }}
        }});

        // Table sorting
        let sortDirection = {{}};
        function sortTable(columnIndex) {{
            const table = document.getElementById('cacheTable');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));

            sortDirection[columnIndex] = !sortDirection[columnIndex];
            const direction = sortDirection[columnIndex] ? 1 : -1;

            rows.sort((a, b) => {{
                let aValue = a.cells[columnIndex].textContent;
                let bValue = b.cells[columnIndex].textContent;

                // Handle numeric columns
                if (columnIndex === 2 || columnIndex === 3 || columnIndex === 4) {{
                    aValue = parseFloat(aValue.replace(/[^0-9.-]/g, '')) || 0;
                    bValue = parseFloat(bValue.replace(/[^0-9.-]/g, '')) || 0;
                    return (aValue - bValue) * direction;
                }}

                return aValue.localeCompare(bValue) * direction;
            }});

            rows.forEach(row => tbody.appendChild(row));
        }}

        // Search filtering
        document.getElementById('searchBox').addEventListener('input', function() {{
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('#cacheTable tbody tr');

            rows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            }});
        }});
    </script>
</body>
</html>"""

        return html_content

    def _prepare_category_data(self, result: ScanResult) -> dict:
        """Prepare data for category pie chart."""
        summaries = result.get_category_summaries()
        sorted_summaries = sorted(
            summaries.values(),
            key=lambda x: x.total_size,
            reverse=True
        )

        labels = []
        values = []
        for summary in sorted_summaries[:10]:  # Top 10 categories
            name = summary.category.value.replace("_", " ").title()
            labels.append(name)
            values.append(round(summary.total_size / (1024 * 1024), 2))  # MB

        return {"labels": labels, "values": values}

    def _prepare_top_items_data(self, result: ScanResult) -> dict:
        """Prepare data for top items bar chart."""
        top_items = result.get_top_items(10)

        labels = []
        values = []
        for item in top_items:
            labels.append(item.name[:30])  # Truncate long names
            values.append(round(item.size_bytes / (1024 * 1024), 2))  # MB

        return {"labels": labels, "values": values}

    def _generate_table_rows(self, result: ScanResult) -> str:
        """Generate HTML table rows for all items."""
        rows = []
        for item in sorted(result.items, key=lambda x: x.size_bytes, reverse=True):
            size_class = "size-large" if item.size_bytes > 100 * 1024 * 1024 else (
                "size-medium" if item.size_bytes > 10 * 1024 * 1024 else "size-small"
            )
            risk_class = f"risk-{item.risk_level.value}"

            rows.append(f"""
                <tr>
                    <td>{html.escape(item.name)}</td>
                    <td>{item.category.value.replace('_', ' ').title()}</td>
                    <td class="{size_class}">{item.formatted_size}</td>
                    <td>{item.file_count:,}</td>
                    <td>{item.age_days}</td>
                    <td><span class="{risk_class}">{item.risk_level.value.upper()}</span></td>
                </tr>
            """)

        return "\n".join(rows)
