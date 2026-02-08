import subprocess
import sys
import os
from datetime import datetime

def run_tests():
    """
    Execute Locust performance tests and validate against SLA.
    """
    # Create timestamped report folder
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    reports_dir = f"reports/{timestamp}"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Verify directory was created
    if not os.path.exists(reports_dir):
        print(f"❌ Failed to create reports directory: {reports_dir}")
        sys.exit(1)

    print("Starting performance tests...")

    result = subprocess.run([
        "locust",
        "-f", "locustfiles/dynamic_tasks.py",
        "--headless",
        "-u", "50",
        "-r", "5",
        "-t", "60s",
        "--host", "https://jsonplaceholder.typicode.com",
        "--html", f"{reports_dir}/report.html",
        "--csv", f"{reports_dir}/results",
        "--exit-code-on-error", "1"
    ])

    if result.returncode != 0:
        print("❌ Performance tests failed")
        sys.exit(1)

    print("\n✅ Performance tests completed")
    print(f"Reports generated in {reports_dir}/ directory")
    
    # Generate comprehensive report
    print("\n📊 Generating comprehensive report...")
    from report_generator import create_comprehensive_report
    create_comprehensive_report(reports_dir)

    # Run SLA validation
    print("\nValidating against SLA thresholds...")
    from validate import validate_sla
    validate_sla(reports_dir)

if __name__ == "__main__":
    run_tests()
