"""
HTML exporter for CacheKaro.

Produces interactive HTML reports with charts and tables.
"""

from __future__ import annotations

import html
import json
from datetime import datetime

from cachekaro.exporters.base import Exporter, ExportFormat
from cachekaro.models.scan_result import ScanResult


class HtmlExporter(Exporter):
    """
    Exports scan results to HTML format.

    Produces a standalone HTML page with:
    - Interactive charts (using Chart.js)
    - Sortable/filterable tables
    - Responsive design
    - Cyberpunk neon theme
    """

    def __init__(self, title: str = "CacheKaro Report", dark_mode: bool = True):
        """
        Initialize the HTML exporter.

        Args:
            title: Page title
            dark_mode: Use dark color scheme (default True for cyberpunk theme)
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

        # Build HTML with cyberpunk neon theme
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(self.title)}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

        :root {{
            --bg-dark: #0a0a0f;
            --bg-card: #12121a;
            --bg-card-hover: #1a1a25;
            --neon-cyan: #00f5ff;
            --neon-magenta: #ff00ff;
            --neon-purple: #bf00ff;
            --neon-pink: #ff0080;
            --neon-blue: #0080ff;
            --neon-green: #00ff88;
            --neon-yellow: #ffff00;
            --neon-orange: #ff8800;
            --text-primary: #ffffff;
            --text-secondary: #8888aa;
            --border-glow: rgba(0, 245, 255, 0.3);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Rajdhani', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
            background-image:
                radial-gradient(ellipse at top, rgba(191, 0, 255, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at bottom, rgba(0, 245, 255, 0.1) 0%, transparent 50%);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        /* Cyberpunk Header */
        header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 20px;
            background: linear-gradient(135deg, rgba(191, 0, 255, 0.15), rgba(0, 245, 255, 0.15), rgba(255, 0, 128, 0.1));
            border-radius: 20px;
            border: 1px solid var(--border-glow);
            position: relative;
            overflow: hidden;
        }}

        header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-yellow), var(--neon-magenta), var(--neon-cyan), transparent);
            animation: glow-line 3s linear infinite;
            box-shadow: 0 0 20px var(--neon-cyan), 0 0 40px var(--neon-magenta);
        }}

        header::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--neon-magenta), var(--neon-yellow), var(--neon-cyan), var(--neon-magenta), transparent);
            animation: glow-line 3s linear infinite reverse;
            box-shadow: 0 0 20px var(--neon-magenta), 0 0 40px var(--neon-cyan);
        }}

        @keyframes glow-line {{
            0% {{ opacity: 0.6; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.6; }}
        }}

        .ascii-art {{
            font-family: monospace;
            font-size: 0.55rem;
            line-height: 1.1;
            white-space: pre;
            background: linear-gradient(180deg, #ff0080, #ff00ff, #bf00ff, #8000ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 10px rgba(255, 0, 128, 0.8)) drop-shadow(0 0 20px rgba(191, 0, 255, 0.6)) drop-shadow(0 0 30px rgba(255, 0, 255, 0.4));
            margin-bottom: 15px;
            animation: ascii-glow 2s ease-in-out infinite alternate;
        }}

        @keyframes ascii-glow {{
            0% {{ filter: drop-shadow(0 0 10px rgba(255, 0, 128, 0.8)) drop-shadow(0 0 20px rgba(191, 0, 255, 0.6)); }}
            100% {{ filter: drop-shadow(0 0 15px rgba(255, 0, 128, 1)) drop-shadow(0 0 30px rgba(191, 0, 255, 0.8)) drop-shadow(0 0 40px rgba(255, 0, 255, 0.5)); }}
        }}

        header h1 {{
            font-family: 'Orbitron', monospace;
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--neon-cyan), var(--neon-magenta));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
            letter-spacing: 4px;
            display: none;
        }}

        header .subtitle {{
            font-size: 1.3rem;
            color: var(--text-secondary);
            letter-spacing: 3px;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(136, 136, 170, 0.3);
        }}

        header .timestamp {{
            margin-top: 15px;
            color: var(--neon-yellow);
            font-family: 'Orbitron', monospace;
            font-size: 0.95rem;
            text-shadow: 0 0 10px rgba(255, 255, 0, 0.5);
            letter-spacing: 1px;
        }}

        /* Grid Layout */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}

        /* Neon Cards */
        .card {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 25px;
            border: 1px solid rgba(0, 245, 255, 0.2);
            position: relative;
            transition: all 0.3s ease;
            overflow: hidden;
        }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 16px;
            padding: 1px;
            background: linear-gradient(135deg, var(--neon-cyan), transparent, var(--neon-magenta));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0, 245, 255, 0.2), 0 0 20px rgba(191, 0, 255, 0.1);
        }}

        .card:hover::before {{
            opacity: 1;
        }}

        .card h2 {{
            font-family: 'Orbitron', monospace;
            font-size: 1.1rem;
            margin-bottom: 20px;
            color: var(--neon-cyan);
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 245, 255, 0.5), 0 0 20px rgba(0, 245, 255, 0.3);
        }}

        .card h2.magenta {{
            color: var(--neon-magenta);
            text-shadow: 0 0 10px rgba(255, 0, 255, 0.5), 0 0 20px rgba(255, 0, 255, 0.3);
        }}

        .card h2.yellow {{
            color: var(--neon-yellow);
            text-shadow: 0 0 10px rgba(255, 255, 0, 0.5), 0 0 20px rgba(255, 255, 0, 0.3);
        }}

        .card h2.pink {{
            color: var(--neon-pink);
            text-shadow: 0 0 10px rgba(255, 0, 128, 0.5), 0 0 20px rgba(255, 0, 128, 0.3);
        }}

        .card h2.green {{
            color: var(--neon-green);
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5), 0 0 20px rgba(0, 255, 136, 0.3);
        }}

        /* Stats Grid */
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }}

        .stat {{
            text-align: center;
            padding: 20px 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            border: 1px solid rgba(0, 245, 255, 0.1);
            transition: all 0.3s ease;
        }}

        .stat:hover {{
            border-color: var(--neon-cyan);
            box-shadow: 0 0 20px rgba(0, 245, 255, 0.2);
        }}

        .stat-value {{
            font-family: 'Orbitron', monospace;
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--neon-cyan), var(--neon-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 8px rgba(0, 245, 255, 0.6));
        }}

        .stat-value.warning {{
            background: linear-gradient(135deg, var(--neon-orange), var(--neon-yellow));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 8px rgba(255, 136, 0, 0.6));
        }}

        .stat-value.magenta {{
            background: linear-gradient(135deg, var(--neon-magenta), var(--neon-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 8px rgba(255, 0, 255, 0.6));
        }}

        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 5px;
        }}

        /* Chart Container */
        .chart-container {{
            position: relative;
            height: 300px;
        }}

        /* Neon Table */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th, td {{
            padding: 15px 12px;
            text-align: left;
            border-bottom: 1px solid rgba(0, 245, 255, 0.1);
        }}

        th {{
            font-family: 'Orbitron', monospace;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--neon-cyan);
            background: rgba(0, 245, 255, 0.05);
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        th:hover {{
            background: rgba(0, 245, 255, 0.15);
            text-shadow: 0 0 10px var(--neon-cyan);
        }}

        tr {{
            transition: all 0.2s ease;
        }}

        tr:hover {{
            background: rgba(0, 245, 255, 0.05);
        }}

        /* Size Colors */
        .size-large {{
            color: var(--neon-magenta);
            font-weight: 700;
            text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
        }}
        .size-medium {{
            color: var(--neon-orange);
            font-weight: 600;
        }}
        .size-small {{
            color: var(--neon-green);
        }}

        /* Risk Badges */
        .risk-safe {{
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 255, 136, 0.1));
            color: var(--neon-green);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(0, 255, 136, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .risk-moderate {{
            background: linear-gradient(135deg, rgba(255, 136, 0, 0.2), rgba(255, 136, 0, 0.1));
            color: var(--neon-orange);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(255, 136, 0, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .risk-caution {{
            background: linear-gradient(135deg, rgba(255, 0, 128, 0.2), rgba(255, 0, 128, 0.1));
            color: var(--neon-pink);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(255, 0, 128, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        /* Search Box */
        .search-box {{
            width: 100%;
            padding: 15px 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(0, 245, 255, 0.3);
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.3);
            color: var(--text-primary);
            font-size: 1rem;
            font-family: 'Rajdhani', sans-serif;
            transition: all 0.3s ease;
        }}

        .search-box:focus {{
            outline: none;
            border-color: var(--neon-cyan);
            box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
        }}

        .search-box::placeholder {{
            color: var(--text-secondary);
        }}

        /* Footer */
        footer {{
            text-align: center;
            margin-top: 50px;
            padding: 30px;
            color: var(--text-secondary);
            border-top: 1px solid rgba(0, 245, 255, 0.1);
        }}

        footer p {{
            font-family: 'Orbitron', monospace;
            letter-spacing: 2px;
        }}

        footer .neon-text {{
            background: linear-gradient(135deg, var(--neon-cyan), var(--neon-magenta));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: var(--bg-dark);
        }}

        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(var(--neon-cyan), var(--neon-magenta));
            border-radius: 4px;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .stat-grid {{
                grid-template-columns: 1fr;
            }}
            header h1 {{
                font-size: 2rem;
            }}
            .stat-value {{
                font-size: 1.4rem;
            }}
        }}

        /* Glitch Animation for Header */
        @keyframes glitch {{
            0% {{ text-shadow: 2px 0 var(--neon-cyan), -2px 0 var(--neon-magenta); }}
            25% {{ text-shadow: -2px 0 var(--neon-cyan), 2px 0 var(--neon-magenta); }}
            50% {{ text-shadow: 2px 0 var(--neon-magenta), -2px 0 var(--neon-cyan); }}
            75% {{ text-shadow: -2px 0 var(--neon-magenta), 2px 0 var(--neon-cyan); }}
            100% {{ text-shadow: 2px 0 var(--neon-cyan), -2px 0 var(--neon-magenta); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="ascii-art">░█████╗░░█████╗░░█████╗░██╗░░██╗███████╗██╗░░██╗░█████╗░██████╗░░█████╗░
██╔══██╗██╔══██╗██╔══██╗██║░░██║██╔════╝██║░██╔╝██╔══██╗██╔══██╗██╔══██╗
██║░░╚═╝███████║██║░░╚═╝███████║█████╗░░█████═╝░███████║██████╔╝██║░░██║
██║░░██╗██╔══██║██║░░██╗██╔══██║██╔══╝░░██╔═██╗░██╔══██║██╔══██╗██║░░██║
╚█████╔╝██║░░██║╚█████╔╝██║░░██║███████╗██║░╚██╗██║░░██║██║░░██║╚█████╔╝
░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░</div>
            <h1>CACHEKARO</h1>
            <p class="subtitle">Storage & Cache Analysis Report</p>
            <p class="timestamp">// GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} //</p>
        </header>

        <!-- Summary Stats -->
        <div class="grid">
            <div class="card">
                <h2>// Disk Overview</h2>
                <div class="stat-grid">
                    <div class="stat">
                        <div class="stat-value">{result.formatted_disk_total}</div>
                        <div class="stat-label">Total Space</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value warning">{result.formatted_disk_used}</div>
                        <div class="stat-label">Used</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{result.formatted_disk_free}</div>
                        <div class="stat-label">Free</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value warning">{result.disk_usage_percent:.1f}%</div>
                        <div class="stat-label">Usage</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2 class="magenta">// Cache Summary</h2>
                <div class="stat-grid">
                    <div class="stat">
                        <div class="stat-value magenta">{result.formatted_total_size}</div>
                        <div class="stat-label">Total Cache</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{result.formatted_cleanable_size}</div>
                        <div class="stat-label">Cleanable (Safe)</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value magenta">{result.total_files:,}</div>
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
                <h2 class="yellow">// Space by Category</h2>
                <div class="chart-container">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2 class="pink">// Top Consumers</h2>
                <div class="chart-container">
                    <canvas id="topItemsChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Detailed Table -->
        <div class="card">
            <h2 class="green">// All Cache Locations</h2>
            <input type="text" class="search-box" id="searchBox" placeholder="&gt; Search cache locations...">
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
            <p>Generated by <span class="neon-text">CACHEKARO</span> | Cache Karo!</p>
        </footer>
    </div>

    <script>
        // Neon color palette for charts
        const neonColors = [
            '#00f5ff', '#ff00ff', '#bf00ff', '#ff0080',
            '#0080ff', '#00ff88', '#ffff00', '#ff8800',
            '#00ffcc', '#ff4444'
        ];

        // Category Doughnut Chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(categoryCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(category_data['labels'])},
                datasets: [{{
                    data: {json.dumps(category_data['values'])},
                    backgroundColor: neonColors,
                    borderColor: '#0a0a0f',
                    borderWidth: 3,
                    hoverBorderColor: '#ffffff',
                    hoverBorderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
                plugins: {{
                    legend: {{
                        position: 'right',
                        labels: {{
                            color: '#8888aa',
                            font: {{
                                family: "'Rajdhani', sans-serif",
                                size: 12
                            }},
                            padding: 15,
                            usePointStyle: true,
                            pointStyle: 'rectRounded'
                        }}
                    }}
                }}
            }}
        }});

        // Top Items Horizontal Bar Chart
        const topCtx = document.getElementById('topItemsChart').getContext('2d');
        new Chart(topCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(top_items_data['labels'])},
                datasets: [{{
                    label: 'Size (MB)',
                    data: {json.dumps(top_items_data['values'])},
                    backgroundColor: function(context) {{
                        const chart = context.chart;
                        const {{ctx, chartArea}} = chart;
                        if (!chartArea) return '#00f5ff';
                        const gradient = ctx.createLinearGradient(chartArea.left, 0, chartArea.right, 0);
                        gradient.addColorStop(0, '#00f5ff');
                        gradient.addColorStop(1, '#bf00ff');
                        return gradient;
                    }},
                    borderRadius: 6,
                    borderSkipped: false
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
                        grid: {{
                            color: 'rgba(0, 245, 255, 0.1)',
                            drawBorder: false
                        }},
                        ticks: {{
                            color: '#8888aa',
                            font: {{
                                family: "'Rajdhani', sans-serif"
                            }}
                        }}
                    }},
                    y: {{
                        grid: {{
                            display: false
                        }},
                        ticks: {{
                            color: '#00f5ff',
                            font: {{
                                family: "'Rajdhani', sans-serif",
                                weight: 600
                            }}
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
