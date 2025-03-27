import ROOT 
from config import plot_dir
from update_norms_knownMC import *
from store_fit_parameters import load_fit_parameters, save_fit_parameters, store_fit_parameters

#from sig_bkg_functions_test_orig_forFeb18_fixpDNN import create_background_workspace, create_signal_workspace
from sig_bkg_functions import create_background_workspace, create_signal_workspace

import csv
ROOT.gROOT.SetBatch(True)
import re
import glob,os,argparse,sys
import shutil
from get_pDNN_cuts import get_pDNN_cuts

DNN_scores = get_pDNN_cuts()

print(DNN_scores)


parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--era",action="store")
parser.add_argument("--pattern",action="store",default="window_*.txt")

option = parser.parse_args()

inputDir = option.inputDir
era=option.era
#
#if era == "Full":
#    years = ["-2016","2016", "2017", "2018"]
#    #years = ["-2016","2016"] #, "2017", "2018"]
#elif era == "-2016":
#    years = ["-2016"]
#elif era == "2016":
#    years = ["2016"]
#elif era == "2017":
#    years = ["2017"]
#else:
#    era ='-2016'
#    years = ["-2016"]
#
# Output the list of years
#print(years)


pattern = option.pattern

#DNN_scores = {30: 0.78, 45: 0.83, 60:0.50, 70:0.80} # before Dec. 5, 2024
# 0.8704166412353516
#DNN_scores = {30 : 0.75, 35 : 0.78, 40 : 0.92, 45 : 0.92, 50 : 0.89, 55 : 0.87, 60 : 0.81, 65 : 0.75, 70 : 0.89} # https://cernbox.cern.ch/text-editor/eos/user/c/caruta/Zp_FinalTrees/Dec4/pDNN_cuts.txt?contextRouteName=files-spaces-generic&contextRouteParams.driveAliasAndItem=eos/user/c/caruta/Zp_FinalTrees/Dec4 
# received on Dec. 5 from Caterina

# as received on Feb18, 2025
##/eos/user/c/caruta/Zp_FinalTrees/Feb18/pDNN_cuts.txt
#DNN_scores = {2: 0.95, 4: 0.92, 5: 0.96, 15: 0.88, 20: 0.91, 25: 0.94, 30: 0.94, 35: 0.93, 40: 0.93, 45: 0.96, 50: 0.96, 55: 0.93, 60: 0.88, 65: 0.89, 70: 0.96}

# https://docs.google.com/spreadsheets/d/1F04CA_YLzRHP918QCN4_2MtIUkyBi9ry8wHQq0OL2uA/edit?gid=1720491868#gid=1720491868
# from GenXS Analyzer
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
#                "m2":  10.21,     "p2":  10.21,
#                "m5":  3.255,     "p5":  4.17,
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


def createZPworkspace_knownMC(mass, year, fit_parameters_file="fit_parameters.py"):

    norm_sig, sumw_mc, num_mc, pDNN_eff_sig_num, pDNN_eff_sig_sum, entries_noWt, fit_results_sig = create_signal_workspace(mass, year, "workspaces",DNN_scores)
    N_background, pDNN_eff_bkg, fit_results_bkg = create_background_workspace(mass, year, "workspaces",DNN_scores)
    fit_results = {}
    fit_results = fit_results_sig | fit_results_bkg

    print("fit_results:  ", fit_results)

    N_signal = sumw_mc

    print("mass:  ", mass," N_signal:  ",N_signal, "    N_background (no ZpMass cut):  ", N_background)
    xs_mass = xs_sig_new["p"+str(mass)]+xs_sig_new["m"+str(mass)]
    update_norms(mass,norm_sig, sumw_mc, num_mc, N_background, xs_mass, pDNN_eff_bkg, pDNN_eff_sig_num, pDNN_eff_sig_sum, entries_noWt)

    return fit_results
##
##createZPworkspace_knownMC(70,2016)
#
mass_points = [2, 4, 5, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

fit_parameters = load_fit_parameters("fit_parameters.py")

for mass in mass_points:
    fit_results_for_mass = createZPworkspace_knownMC(mass, 2016)

    print("fit_results_for_mass:    ", fit_results_for_mass)

    for model_name, fit_result in fit_results_for_mass.items():
        params_list = [
            fit_result.floatParsFinal().at(i)
            for i in range(fit_result.floatParsFinal().getSize())
        ]
        fit_parameters = store_fit_parameters(
            fit_parameters, 
            fit_result=fit_result, 
            model_name=model_name, 
            mass_point=mass, 
            params_list=params_list
        )
    save_fit_parameters(fit_parameters, "fit_parameters.py")



