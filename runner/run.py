import subprocess
import sys
import os

def run_tests():
    """
    Execute Locust performance tests and validate against SLA.
    """
    os.makedirs("reports", exist_ok=True)

    print("Starting performance tests...")

    result = subprocess.run([
        "locust",
        "-f", "locustfiles/dynamic_tasks.py",
        "--headless",
        "-u", "50",
        "-r", "5",
        "-t", "60s",
        "--host", "https://jsonplaceholder.typicode.com",
        "--html", "reports/report.html",
        "--csv", "reports/results",
        "--exit-code-on-error", "1"
    ])

    if result.returncode != 0:
        print("❌ Performance tests failed")
        sys.exit(1)

    print("\n✅ Performance tests completed")
    print("Reports generated in reports/ directory")
    
    # Generate comprehensive report
    print("\n📊 Generating comprehensive report...")
    from report_generator import create_comprehensive_report
    create_comprehensive_report()

    # Run SLA validation
    print("\nValidating against SLA thresholds...")
    from validate import validate_sla
    validate_sla()

if __name__ == "__main__":
    run_tests()
