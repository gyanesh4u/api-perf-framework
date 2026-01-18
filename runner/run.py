import subprocess
import sys
import os

def run_tests():
    """
    Execute Locust performance tests and validate against SLA.
    """
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    
    # Run Locust tests
    print("Starting performance tests...")
    result = subprocess.run([
        "locust",
        "-f", "locustfiles/dynamic_tasks.py",
        "--headless",
        "-u", "50",
        "-r", "5",
        "-t", "1m",
        "--html", "reports/report.html",
        "--csv", "reports/results"
    ])
    
    if result.returncode != 0:
        print("❌ Performance tests failed")
        sys.exit(1)
    
    print("\n✅ Performance tests completed")
    print("Reports generated in reports/ directory")
    
    # Run SLA validation
    print("\nValidating against SLA thresholds...")
    from runner.validate import validate_sla
    validate_sla()

if __name__ == "__main__":
    run_tests()
