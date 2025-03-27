import ROOT, os
import numpy as np

from get_sumW import get_sumW_for_mass_point

# new weights from GenXSAnalyzer (https://twiki.cern.ch/twiki/bin/view/CMS/HowToGenXSecAnalyzer)

xs_sig_new = {  
    "p1": 20.54,      "m1": 15.78,
    "p2": 13.07,      "m2": 10.26,
    "p3": 9.623,      "m3": 7.594,
    "p4": 5.711,      "m4": 4.442,
    "p5": 4.209,      "m5": 3.302,
    "p10": 1.709,     "m10": 1.370,
    "p15": 0.8467,    "m15": 0.6966,
    "p20": 0.4606,    "m20": 0.3723,
    "p25": 0.2503,    "m25": 0.2059,
    "p30": 0.1360,    "m30": 0.1130,
    "p35": 0.07229,   "m35": 0.06055,
    "p40": 0.03737,   "m40": 0.03135,
    "p45": 0.01850,   "m45": 0.01533,
    "p50": 0.008626,  "m50": 0.007180,
    "p55": 0.003869,  "m55": 0.003125,
    "p60": 0.001738,  "m60": 0.001331,
    "p65": 0.0008205, "m65": 0.0005982,
    "p70": 0.0005049, "m70": 0.0003527,
}

#xs_sig_new = {  "m4":  4.398,     "p4":  5.68,
#                "m2":  10.26,     "p2":  13.07,
#                "m5":  3.30,     "p5":  4.21,
#                "m10": 1.367,     "p10": 1.741,
#                "m15": 0.6864,    "p15": 0.8659,
#                "m20": 0.3746,    "p20": 0.4600,
#                "m25": 0.2046,    "p25": 0.2491,
#                "m30": 0.1117,    "p30": 0.1367,
#                "m35": 0.06028,   "p35": 0.07311,
#                "m40": 0.03098,   "p40": 0.03744,
#                "m45": 0.01537,   "p45": 0.01843,
#                "m50": 0.007179,  "p50": 0.008727,
#                "m55": 0.003207,  "p55": 0.003846,
#                "m60": 0.001322,  "p60": 0.001692,
#                "m65": 0.0005871, "p65": 0.0008043,
#                "m70": 0.0003560, "p70": 0.0005102,
#                "m75": 0.0002392, "p75": 0.0003758,
#             }

xs_err_new = {  "m4":  0.04408,   "p4":  0.03075,
                "m2":  0.02938,     "p2":  0.02938,
                "m5":  0.03366,   "p5": 0.02822,
                "m10": 0.01292,   "p10": 0.01675,
                "m15": 0.005174,  "p15": 0.007221,
                "m20": 0.002926,  "p20": 0.002311,
                "m25": 0.001514,  "p25": 0.001323,
                "m30": 0.0008127, "p30": 0.000725,
                "m35": 0.0004161, "p35": 0.0004555,
                "m40": 0.0002478, "p40": 0.0001901,
                "m45": 0.0001217, "p45": 0.0001513,
                "m50": 5.679e-05, "p50": 7.805e-05,
                "m55": 3.839e-05, "p55": 3.117e-05,
                "m60": 1.064e-05, "p60": 2.192e-05,
                "m65": 5.764e-06, "p65": 1.472e-05,
                "m70": 1.504e-06, "p70": 4.247e-06,
                "m75": 8.201e-07, "p75": 1.413e-06,
             }

#sample_entries = {  "m4":  0.04408,   "p4":  0.03075,
#                "m5":  0.03366,   "p5": 0.02822,
#                "m10": 0.01292,   "p10": 0.01675,
#                "m15": 0.005174,  "p15": 0.007221,
#                "m20": 0.002926,  "p20": 0.002311,
#                "m25": 0.001514,  "p25": 0.001323,
#                "m30": 0.0008127, "p30": 0.000725,
#                "m35": 0.0004161, "p35": 0.0004555,
#                "m40": 0.0002478, "p40": 0.0001901,
#                "m45": 0.0001217, "p45": 0.0001513,
#                "m50": 5.679e-05, "p50": 7.805e-05,
#                "m55": 3.839e-05, "p55": 3.117e-05,
#                "m60": 1.064e-05, "p60": 2.192e-05,
#                "m65": 5.764e-06, "p65": 1.472e-05,
#                "m70": 1.504e-06, "p70": 4.247e-06,
#                "m75": 8.201e-07, "p75": 1.413e-06,
#             }



mass_point_weights = {}
mass_point_sumw = {}

output_dir = "files_wtd_entries_Feb18"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")
else:
    print(f"Directory already exists: {output_dir}")

def process_mass_point(mass_point):
    # Open the ROOT file based on the mass point
    #input_file = ROOT.TFile(f"/afs/cern.ch/user/c/caruta/public/forTahir/MiniTree_sgn_pDNN_{mass_point}.root", "READ")
    #input_file = ROOT.TFile(f"/eos/home-c/caruta/Zp_FinalTrees/Dec4/MiniTree_sgn_pDNN_{mass_point}.root", "READ")
    input_file = ROOT.TFile(f"/eos/user/c/caruta/Zp_FinalTrees/Feb18/MiniTree_sgn_pDNN_{mass_point}.root", "READ")

    tree = input_file.Get("passedEvents") 

    #output_file = ROOT.TFile(f"files_wtd/MiniTree_sgn_pDNN_{mass_point}_wt.root", "RECREATE")
#    output_file = ROOT.TFile(f"files_wtd_entries_Feb18/MiniTree_sgn_pDNN_{mass_point}_wt.root", "RECREATE")
    output_file = ROOT.TFile(f"{output_dir}/MiniTree_sgn_pDNN_{mass_point}_wt.root", "RECREATE")

    new_tree = tree.CloneTree(0)  # Clone the tree structure but do not copy the entries

    # Sum of weights from individual years for a given mass point
#    sumw = get_sumW_for_mass_point(mass_point) # FIXME
    sumw = 300000 # considering fix Gen Events 
    print("sumw:   ", sumw)
    mass_point_sumw[mass_point] = sumw  # Store sumw for the current mass point

    xs_mass_point = xs_sig_new["p"+str(mass_point)]+xs_sig_new["m"+str(mass_point)]
    # Compute event weight: (cross section * luminosity) / sumW
    print("mass: ", mass_point, "....... ,   XS:   ", xs_mass_point)
    evt_weight = xs_mass_point * (138 * 1000) / sumw
    #evt_weight = xs_mass_point * (137 * 1000) / sumw # Caterina using 137, for synch.

    # Apply k-factor for NLO corrections
    k_factor_nlo = 1.3
    weight_tot = evt_weight * k_factor_nlo
    mass_point_weights[mass_point] = weight_tot  # Store weight for the current mass point
    print("mass: ", mass_point, "....... ,   XS:   ", xs_mass_point, "...... total weight:  ", weight_tot)
    # Create a new branch for weight
    weight = np.array([1.0], dtype=float)
    new_branch = new_tree.Branch("weight", weight, "weight/D")

    # Loop over the events and fill the new branch with calculated weights
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        weight[0] = weight_tot
        new_tree.Fill()

    output_file.cd()   
    new_tree.Write()
    output_file.Close()
    input_file.Close()

mass_points = [2,4, 5, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
#mass_points = [4] #, 5, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
#mass_points = [5, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]

for mass in mass_points:
    process_mass_point(mass)

#process_mass_point(70)

with open("weights_knownMC.py", "w") as f:
    f.write("mass_point_weights = ")
    f.write(str(mass_point_weights))

# Plotting
#output_dir = "/eos/user/t/tjavaid/www/Wto3l/fits/2016/gauss_dscb/newWPs/discrete/mean/interpolations/norms_ent_Feb18/"
output_dir = "test"
os.makedirs(output_dir, exist_ok=True)

import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator


# Plotting mass_point_weights
masses = list(mass_point_weights.keys())
weights = list(mass_point_weights.values())
plt.figure()
pchip = PchipInterpolator(masses, weights)
masses_fine = np.linspace(min(masses), max(masses), 500)
weights_fine = pchip(masses_fine)
plt.plot(masses_fine, weights_fine, label='Mass Point Weights (PCHIP)', linestyle='-', color='blue')
plt.scatter(masses, weights, color='red', label='Data Points')
plt.xlabel('Mass Point')
plt.ylabel('Total Weight')
plt.title('Mass Point Weights')
plt.legend()
plt.grid()
plt.savefig(f"{output_dir}/weights_knownMC.png")
plt.savefig(f"{output_dir}/weights_knownMC.pdf")
plt.close()



