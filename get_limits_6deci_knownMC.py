# NOTE: this reads the output files from macro extract_limits_knownMC.sh
import uproot
import csv

mass_points = [2, 4, 5, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

limits_dict = {}
limits_stat_dict = {}

for mass in mass_points:
    file_name = f"higgsCombineM{mass}.AsymptoticLimits.mH120.root"
    stat_file_name = f"higgsCombineM{mass}_stat.AsymptoticLimits.mH120.root"
    
    try:
        file = uproot.open(file_name)
        tree = file["limit"]
        limit_values = tree["limit"].array()
        limit_50 = limit_values[2]  #  50% expected limit
        limits_dict[mass] = float(f"{limit_50:.6f}")
    except FileNotFoundError:
        print(f"File not found for mass {mass} GeV. Skipping nominal...")
        limits_dict[mass] = None
    
    try:
        stat_file = uproot.open(stat_file_name)
        stat_tree = stat_file["limit"]
        stat_limit_values = stat_tree["limit"].array()
        stat_limit_50 = stat_limit_values[2]  #  50% expected limit
        limits_stat_dict[mass] = float(f"{stat_limit_50:.6f}")
    except FileNotFoundError:
        print(f"File not found for mass {mass} GeV. Skipping stat-only...")
        limits_stat_dict[mass] = None

output_file = "expected_limits_6deci_knownMC.py"
with open(output_file, "w") as f:
    f.write("expected_limits = {\n")
    for mass, limit in limits_dict.items():
        f.write(f"    {mass}: {limit},\n")
    f.write("}\n\n")
    
    f.write("expected_limits_stat = {\n")
    for mass, limit in limits_stat_dict.items():
        f.write(f"    {mass}: {limit},\n")
    f.write("}\n")

csv_file = "expected_limits_6deci_knownMC.csv"
with open(csv_file, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Mass (GeV)", "50% Expected Limit", "50% Expected Limit (Stat-Only)"])
    for mass in mass_points:
        limit = limits_dict.get(mass, "N/A")
        stat_limit = limits_stat_dict.get(mass, "N/A")
        
        limit_str = f"{limit:.6f}" if isinstance(limit, float) else limit
        stat_limit_str = f"{stat_limit:.6f}" if isinstance(stat_limit, float) else stat_limit
        
        csv_writer.writerow([mass, limit_str, stat_limit_str])

print(f"\nSaved limits to {output_file} and {csv_file}")


# python3 get_limits_6deci_knownMC.py
