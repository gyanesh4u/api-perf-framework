import os

os.makedirs("reports", exist_ok=True)

os.system(
    "locust -f locustfiles/dynamic_tasks.py "
    "--headless -u 50 -r 5 -t 1m "
    "--html reports/report.html "
    "--csv reports/results"
)
