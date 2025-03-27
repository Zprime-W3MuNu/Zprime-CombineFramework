import os

# Import the sig_norms dictionary from norms.py
from norms import sig_norms

# Define the template with placeholders for mass point and year
datacard_template = """imax 1 number of channels
jmax 1 number of backgrounds
kmax * number of nuisance parameters
------------
shapes  ZpToMuMu_M{mass_point}      ZpToMuMu_M{mass_point}_{year}      workspaces/workspace_sig_MZp{mass_point}_{year}.root        workspace_sig:gauss_dscb
shapes  bkg      ZpToMuMu_M{mass_point}_{year}      workspaces/workspace_data_MZp{mass_point}_{year}.root        workspace_data:multipdf_bkg
shapes  data_obs      ZpToMuMu_M{mass_point}_{year}      workspaces/workspace_data_MZp{mass_point}_{year}.root        workspace_data:data_obs
------------
# we have just one channel
bin         ZpToMuMu_M{mass_point}_{year}
observation -1
------------
# now we list the expected events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error) 
# on each process and bin
bin             ZpToMuMu_M{mass_point}_{year} ZpToMuMu_M{mass_point}_{year}
process         ZpToMuMu_M{mass_point}          bkg
process         0           1
rate        {signal_norm}   1
------------
lumi    lnN    1.023  -    lumi affects signal, and not bkg (extracted from fit). lnN = lognormal
xs_Zp   lnN    1.010  -    W->Zp->3mu cross section + signal efficiency + other minor ones.
pdfindex_bkg         discrete
"""

# List of mass points
mass_points = [2, 4, 5, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
#mass_points = [4] #, 5, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

year = 2016  # NOTE, just an optional variable, in case if we use a dedicated datacard for each era

output_dir = "datacards"
os.makedirs(output_dir, exist_ok=True)

for mass_point in mass_points:
    signal_norm = sig_norms.get(mass_point, 1.0)  # Default to 1.0 if not found

    datacard_content = datacard_template.format(mass_point=mass_point, year=year, signal_norm=signal_norm)
    datacard_filename = os.path.join(output_dir, f"datacard_MZp{mass_point}_{year}.txt")

    with open(datacard_filename, "w") as f:
        f.write(datacard_content)

    print(f"Generated: {datacard_filename}")

print("All datacards have been created successfully.")

