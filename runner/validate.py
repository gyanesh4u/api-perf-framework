import csv, yaml, sys

with open("thresholds/sla.yaml") as f:
    sla = yaml.safe_load(f)

with open("reports/results_stats.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["Name"]
        if name in sla:
            p95 = float(row["95%"])
            if p95 > sla[name]["p95_ms"]:
                print(f"SLA breach: {name}")
                sys.exit(1)

print("All SLAs met")
