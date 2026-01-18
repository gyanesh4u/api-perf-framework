import csv
import yaml
import sys
import os

def validate_sla():
    """
    Validate that test results meet SLA thresholds.
    
    Checks both p95 response time and error rate against thresholds.
    """
    # Check if report file exists
    report_file = "reports/results_stats.csv"
    if not os.path.exists(report_file):
        print(f"Error: Report file not found at {report_file}")
        print("Make sure to run the tests first with: python runner/run.py")
        sys.exit(1)
    
    # Load SLA thresholds
    try:
        with open("thresholds/sla.yaml") as f:
            sla = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: SLA thresholds file not found at thresholds/sla.yaml")
        sys.exit(1)
    
    # Validate results against SLA
    violations = []
    
    try:
        with open(report_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Name"]
                if name in sla:
                    try:
                        p95 = float(row["95%"])
                        error_rate = float(row["Failure Rate %"])
                        
                        # Check p95 threshold
                        if p95 > sla[name]["p95_ms"]:
                            violations.append(
                                f"P95 breach: {name} ({p95}ms > {sla[name]['p95_ms']}ms)"
                            )
                        
                        # Check error rate threshold
                        if error_rate > sla[name]["error_rate"]:
                            violations.append(
                                f"Error rate breach: {name} ({error_rate}% > {sla[name]['error_rate']}%)"
                            )
                    except (ValueError, KeyError) as e:
                        print(f"Warning: Could not parse metrics for {name}: {e}")
    except Exception as e:
        print(f"Error reading report file: {e}")
        sys.exit(1)
    
    # Report results
    if violations:
        print("❌ SLA Violations Found:")
        for violation in violations:
            print(f"  - {violation}")
        sys.exit(1)
    else:
        print("✅ All SLAs met successfully!")
        sys.exit(0)

if __name__ == "__main__":
    validate_sla()
