import csv
import json
import os
from datetime import datetime
from pathlib import Path

def parse_csv_reports():
    """
    Parse Locust CSV reports and extract metrics.
    """
    stats_file = "reports/results_stats.csv"
    
    if not os.path.exists(stats_file):
        raise FileNotFoundError(f"Report file not found: {stats_file}")
    
    metrics = []
    with open(stats_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Name'] != 'Aggregated':
                metrics.append({
                    'name': row['Name'],
                    'method': row['Type'],
                    'requests': int(row['# requests']),
                    'failures': int(row['# failures']),
                    'median': float(row['Median']),
                    'average': float(row['Average']),
                    'min': float(row['Min']),
                    'max': float(row['Max']),
                    'p95': float(row['95%']),
                    'p99': float(row['99%']),
                    'failure_rate': float(row['Failure Rate %'])
                })
    
    return metrics

def calculate_statistics(metrics):
    """
    Calculate aggregate statistics across all requests.
    """
    total_requests = sum(m['requests'] for m in metrics)
    total_failures = sum(m['failures'] for m in metrics)
    
    return {
        'total_requests': total_requests,
        'total_failures': total_failures,
        'success_rate': ((total_requests - total_failures) / total_requests * 100) if total_requests > 0 else 0,
        'avg_response_time': sum(m['average'] * m['requests'] for m in metrics) / total_requests if total_requests > 0 else 0,
        'max_response_time': max(m['max'] for m in metrics) if metrics else 0,
        'min_response_time': min(m['min'] for m in metrics) if metrics else 0,
        'p95_response_time': max(m['p95'] for m in metrics) if metrics else 0,
        'p99_response_time': max(m['p99'] for m in metrics) if metrics else 0,
    }

def generate_html_report(metrics, stats):
    """
    Generate a comprehensive HTML report.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Performance Test Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .header p {{
                opacity: 0.9;
                font-size: 1.1em;
            }}
            
            .content {{
                padding: 40px 30px;
            }}
            
            .timestamp {{
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 0.95em;
            }}
            
            .summary-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            
            .summary-card {{
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 25px;
                border-radius: 10px;
                border-left: 5px solid #667eea;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            
            .summary-card.success {{
                border-left-color: #10b981;
            }}
            
            .summary-card.warning {{
                border-left-color: #f59e0b;
            }}
            
            .summary-card.error {{
                border-left-color: #ef4444;
            }}
            
            .summary-card h3 {{
                color: #333;
                font-size: 0.9em;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 10px;
                opacity: 0.7;
            }}
            
            .summary-card .value {{
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
            }}
            
            .summary-card.success .value {{
                color: #10b981;
            }}
            
            .summary-card.error .value {{
                color: #ef4444;
            }}
            
            .summary-card .unit {{
                font-size: 0.4em;
                opacity: 0.7;
                margin-left: 5px;
            }}
            
            .section {{
                margin-bottom: 40px;
            }}
            
            .section-title {{
                font-size: 1.5em;
                color: #333;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
            }}
            
            .metrics-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            
            .metrics-table th {{
                background: #f3f4f6;
                padding: 15px;
                text-align: left;
                font-weight: 600;
                color: #333;
                border-bottom: 2px solid #e5e7eb;
            }}
            
            .metrics-table td {{
                padding: 15px;
                border-bottom: 1px solid #e5e7eb;
            }}
            
            .metrics-table tr:hover {{
                background: #f9fafb;
            }}
            
            .method-badge {{
                display: inline-block;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
            }}
            
            .method-badge.get {{
                background: #dbeafe;
                color: #1e40af;
            }}
            
            .method-badge.post {{
                background: #dcfce7;
                color: #15803d;
            }}
            
            .method-badge.put {{
                background: #fef3c7;
                color: #92400e;
            }}
            
            .method-badge.delete {{
                background: #fee2e2;
                color: #b91c1c;
            }}
            
            .status-badge {{
                display: inline-block;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
            }}
            
            .status-badge.success {{
                background: #dcfce7;
                color: #15803d;
            }}
            
            .status-badge.warning {{
                background: #fef3c7;
                color: #92400e;
            }}
            
            .status-badge.error {{
                background: #fee2e2;
                color: #b91c1c;
            }}
            
            .footer {{
                background: #f9fafb;
                padding: 20px 30px;
                text-align: center;
                color: #666;
                border-top: 1px solid #e5e7eb;
                font-size: 0.9em;
            }}
            
            .chart-container {{
                margin-top: 30px;
                padding: 20px;
                background: #f9fafb;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 API Performance Test Report</h1>
                <p>Load Testing Analysis & Metrics</p>
            </div>
            
            <div class="content">
                <div class="timestamp">Generated on {timestamp}</div>
                
                <div class="summary-grid">
                    <div class="summary-card success">
                        <h3>Total Requests</h3>
                        <div class="value">{stats['total_requests']:,.0f}</div>
                    </div>
                    
                    <div class="summary-card {'success' if stats['success_rate'] >= 99 else 'warning' if stats['success_rate'] >= 95 else 'error'}">
                        <h3>Success Rate</h3>
                        <div class="value">{stats['success_rate']:.2f}<span class="unit">%</span></div>
                    </div>
                    
                    <div class="summary-card error">
                        <h3>Failed Requests</h3>
                        <div class="value">{stats['total_failures']:,.0f}</div>
                    </div>
                    
                    <div class="summary-card">
                        <h3>Average Response Time</h3>
                        <div class="value">{stats['avg_response_time']:.0f}<span class="unit">ms</span></div>
                    </div>
                    
                    <div class="summary-card">
                        <h3>P95 Response Time</h3>
                        <div class="value">{stats['p95_response_time']:.0f}<span class="unit">ms</span></div>
                    </div>
                    
                    <div class="summary-card">
                        <h3>Max Response Time</h3>
                        <div class="value">{stats['max_response_time']:.0f}<span class="unit">ms</span></div>
                    </div>
                </div>
                
                <div class="section">
                    <h2 class="section-title">📊 Detailed Metrics by Endpoint</h2>
                    <table class="metrics-table">
                        <thead>
                            <tr>
                                <th>Endpoint</th>
                                <th>Method</th>
                                <th>Requests</th>
                                <th>Failures</th>
                                <th>Avg (ms)</th>
                                <th>Min (ms)</th>
                                <th>Max (ms)</th>
                                <th>P95 (ms)</th>
                                <th>P99 (ms)</th>
                                <th>Failure Rate</th>
                            </tr>
                        </thead>
                        <tbody>
"""
    
    for metric in metrics:
        method_class = metric['method'].lower()
        failure_rate = metric['failure_rate']
        status_class = 'success' if failure_rate == 0 else 'warning' if failure_rate < 5 else 'error'
        
        html_content += f"""
                            <tr>
                                <td><strong>{metric['name']}</strong></td>
                                <td><span class="method-badge {method_class}">{metric['method']}</span></td>
                                <td>{metric['requests']:,}</td>
                                <td>{metric['failures']}</td>
                                <td>{metric['average']:.0f}</td>
                                <td>{metric['min']:.0f}</td>
                                <td>{metric['max']:.0f}</td>
                                <td>{metric['p95']:.0f}</td>
                                <td>{metric['p99']:.0f}</td>
                                <td><span class="status-badge {status_class}">{failure_rate:.2f}%</span></td>
                            </tr>
"""
    
    html_content += """
                        </tbody>
                    </table>
                </div>
                
                <div class="section">
                    <h2 class="section-title">📈 Performance Summary</h2>
                    <table class="metrics-table">
                        <tbody>
"""
    
    html_content += f"""
                            <tr>
                                <td><strong>Min Response Time</strong></td>
                                <td>{stats['min_response_time']:.0f} ms</td>
                            </tr>
                            <tr>
                                <td><strong>Average Response Time</strong></td>
                                <td>{stats['avg_response_time']:.0f} ms</td>
                            </tr>
                            <tr>
                                <td><strong>P95 Response Time</strong></td>
                                <td>{stats['p95_response_time']:.0f} ms</td>
                            </tr>
                            <tr>
                                <td><strong>P99 Response Time</strong></td>
                                <td>{stats['p99_response_time']:.0f} ms</td>
                            </tr>
                            <tr>
                                <td><strong>Max Response Time</strong></td>
                                <td>{stats['max_response_time']:.0f} ms</td>
                            </tr>
"""
    
    html_content += """
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="footer">
                <p>API Performance Testing Framework | Generated automatically</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def generate_json_report(metrics, stats):
    """
    Generate a JSON report for programmatic access.
    """
    return {
        'timestamp': datetime.now().isoformat(),
        'summary': stats,
        'metrics': metrics
    }

def create_comprehensive_report():
    """
    Create comprehensive report in multiple formats.
    """
    try:
        print("📊 Parsing test results...")
        metrics = parse_csv_reports()
        stats = calculate_statistics(metrics)
        
        print("📝 Generating HTML report...")
        html_report = generate_html_report(metrics, stats)
        
        with open("reports/performance_report.html", "w") as f:
            f.write(html_report)
        print("✅ HTML report saved: reports/performance_report.html")
        
        print("📝 Generating JSON report...")
        json_report = generate_json_report(metrics, stats)
        
        with open("reports/performance_report.json", "w") as f:
            json.dump(json_report, f, indent=2)
        print("✅ JSON report saved: reports/performance_report.json")
        
        # Print summary to console
        print("\n" + "="*60)
        print("🎯 TEST SUMMARY")
        print("="*60)
        print(f"Total Requests: {stats['total_requests']:,.0f}")
        print(f"Success Rate: {stats['success_rate']:.2f}%")
        print(f"Failed Requests: {stats['total_failures']:,.0f}")
        print(f"Avg Response Time: {stats['avg_response_time']:.0f} ms")
        print(f"P95 Response Time: {stats['p95_response_time']:.0f} ms")
        print(f"Max Response Time: {stats['max_response_time']:.0f} ms")
        print("="*60)
        
        return True
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return False

if __name__ == "__main__":
    create_comprehensive_report()
