import os
import ROOT
from config import plot_dir
import shutil
#DNN_scores = {30 : 0.75, 35 : 0.78, 40 : 0.92, 45 : 0.92, 50 : 0.89, 55 : 0.87, 60 : 0.81, 65 : 0.75, 70 : 0.89}
#DNN_scores = {2: 0.95, 4: 0.92, 5: 0.96, 15: 0.88, 20: 0.91, 25: 0.94, 30: 0.94, 35: 0.93, 40: 0.93, 45: 0.96, 50: 0.96, 55: 0.93, 60: 0.88, 65: 0.89, 70: 0.96}


#def create_signal_workspace(mass, year, output_dir):
def create_signal_workspace(mass, year, output_dir,DNN_scores): # TJ 12.03.2025 # updated pDNN score from Cat. /eos/user/c/caruta/Zp_FinalTrees/Feb18/pDNN_cuts_AMS.txt

    print(f"Creating signal workspace for mass point: {mass}, year: {year}")

    #sig_file_path = f"/eos/home-c/caruta/Zp_FinalTrees/Dec4/MiniTree_sig_pDNN_{mass}.root"
#    sig_file_path = f"files_wtd_entries_Feb18/MiniTree_sgn_pDNN_{mass}.root"
    f_sig = ROOT.TFile("files_wtd_entries_Feb18/MiniTree_sgn_pDNN_%s_wt.root"%(mass), "r")

    #DNN_score = 0.87
    #score = DNN_scores[mass]
    score = 0.915 # NOTE fixing for smooth pDNN effs. proposal in sig. & bkg. from Caterina
    print("DNN_score:     ", score)
    w3l_sig_lo = mass - 0.02 * mass  # 2 sigma below mass
    w3l_sig_hi = mass + 0.02 * mass  # 2 sigma above mass
    w3l_lo = mass - 0.2 * mass       # 20% below mass
    w3l_hi = mass + 0.2 * mass       # 20% above mass
    n_bins_sig = 80 
    fit_range_sig = "full"

    pDNN_eff_sig = 0

    if not f_sig or f_sig.IsZombie():
        raise FileNotFoundError(f"Cannot open signal ROOT file: {sig_file_path}")

    t_sig = f_sig.Get("passedEvents")

    print("mass:  ", mass)
    massZ1 = ROOT.RooRealVar("massZ1", "massZ1", w3l_lo, w3l_hi)
    massZ2 = ROOT.RooRealVar("massZ2", "massZ2", w3l_lo, w3l_hi)
    ZpMass = ROOT.RooRealVar("ZpMass", "ZpMass", 0.5,80)  
    weight = ROOT.RooRealVar("weight", "weight", 0,0,15)
    mass_variable = massZ2 if mass <= 25 else massZ1

    print("mass_variable:   ", mass_variable)

    mass_variable_name = mass_variable.GetName()
    print("mass_variable_name:   ", mass_variable_name)

    mass_variable.setBins(n_bins_sig)
    DNN_score = ROOT.RooRealVar("DNN_score", "DNN_score", 0, 1)
    pTL4 = ROOT.RooRealVar("pTL4", "pTL4", 0,0,200) # required for 4 muons event veto

    mass_variable.setRange("loSB", w3l_lo, w3l_sig_lo)
    mass_variable.setRange("hiSB", w3l_sig_hi, w3l_hi)
    mass_variable.setRange("full", w3l_lo, w3l_hi)


    arg_set = ROOT.RooArgSet(DNN_score, mass_variable, pTL4)
    mass_variable_name = mass_variable.GetName()


    arg_set = ROOT.RooArgSet(DNN_score, ZpMass, weight, mass_variable, pTL4)
    
    cut_string = f"(DNN_score > {score} && pTL4 == 0 && ZpMass == {mass} && {mass_variable_name} >= {w3l_lo} && {mass_variable_name} <= {w3l_hi})"
    cut_string_noDNN = f"(pTL4 == 0 && ZpMass == {mass} && {mass_variable_name} >= {w3l_lo} && {mass_variable_name} <= {w3l_hi})"
#    if mass>=30:
#        cut_string = f"((DNN_score >= {score} && pTL4 == 0 && ZpMass == {mass} && {mass_variable_name} >= {w3l_lo} && {mass_variable_name} <= {w3l_hi}) && (massZ2<9.0 | massZ2>11.0))"
#        cut_string_noDNN = f"((pTL4 == 0 && ZpMass == {mass} && {mass_variable_name} >= {w3l_lo} && {mass_variable_name} <= {w3l_hi}) && (massZ2<9.0 | massZ2>11.0))"
#        arg_set = ROOT.RooArgSet(DNN_score, ZpMass, weight, mass_variable, pTL4, massZ2)
    print(f"Applying selection: {cut_string}")
    
    sig_mc = ROOT.RooDataSet("passedEvents", "passedEvents", t_sig,
                             arg_set, cut_string, "weight")    
    
    sig_mc_noDNN = ROOT.RooDataSet("passedEvents", "passedEvents", t_sig,
                             arg_set, cut_string_noDNN, "weight")    
    
    sig_mc_noWt = ROOT.RooDataSet("passedEvents", "passedEvents", t_sig,
                             arg_set, cut_string) 


    sig_mc_hist = ROOT.RooDataHist("sig_mc_hist", "sig_mc_hist", ROOT.RooArgSet(mass_variable), sig_mc)

    pDNN_eff_sig_num = sig_mc.numEntries()/sig_mc_noDNN.numEntries()
    pDNN_eff_sig_sum = sig_mc.sumEntries()/sig_mc_noDNN.sumEntries()
    entries_noWt = sig_mc_noWt.numEntries()
    print("mass:   ", mass)
    print("pDNN_eff_sig_num:    ", pDNN_eff_sig_num)
    print("pDNN_eff_sig_sum:    ", pDNN_eff_sig_sum)
    print("Sum of weight entries in sig_mc:", sig_mc.sumEntries())
    print("Sum of weight entries in sig_mc:", sig_mc.sumEntries())

    print(f"Total events before cut from tree  : {t_sig.GetEntries()}")
#    print(f"Total events before cut RooDataset: {sig_mc_noCut.numEntries()}")
#    print(f"Total events after DNN cut: {sig_mc_DNN.numEntries()}")
    print(f"Total events after both DNN and ZpMass cuts: {sig_mc.numEntries()}")
    print(f"Total events after cut: {sig_mc.numEntries()}")
    print(f"Total events after cut  from sig_mc_hist   : {sig_mc_hist.numEntries()}")
    print(f"Total/sum of weights after cut  from sig_mc_hist   : {sig_mc_hist.sumEntries()}")

    sumw_mc = sig_mc.sumEntries()
    num_mc = sig_mc.numEntries()
    norm_sig = sumw_mc #* lumis["Full"] * 1000
    print ("expected signal yield is:  ", norm_sig)

    sig_mc_binned = sig_mc.binnedClone()

    if mass <= 10:
        mean = ROOT.RooRealVar("mean", f"mean_{mass}", mass, mass - 0.1, mass + 0.1)
    
        # Width parameters (scaled with mass)
        sigma_gaus = ROOT.RooRealVar("sigma_gaus",  f"sigma_gaus_{mass}", 0.03 * mass, 0.005 * mass, 0.1 * mass)
        sigma_dscb = ROOT.RooRealVar("sigma_dscb",  f"sigma_dscb_{mass}", 0.07 * mass, 0.01 * mass, 0.15 * mass)
    
        # DSCB tail parameters
        alpha_left = ROOT.RooRealVar("alpha_left",  f"alpha_left_{mass}", 1.5, 1.0, 3.0)
        alpha_right = ROOT.RooRealVar("alpha_right",  f"alpha_right_{mass}", 1.5, 1.0, 3.0)
        n_left = ROOT.RooRealVar("n_left",  f"n_left_{mass}", 2.5, 1.0, 10.0)
        n_right = ROOT.RooRealVar("n_right",  f"n_right_{mass}", 2.5, 1.0, 10.0)
    
        # Create Gaussian and DSCB functions
        gaussian = ROOT.RooGaussian("gaussian", "Gaussian PDF", mass_variable, mean, sigma_gaus)
        dscb = ROOT.RooCrystalBall("dscb", "Double-Sided Crystal Ball", mass_variable, mean, sigma_dscb, alpha_left, n_left, alpha_right, n_right)
    
        # Fraction of Gaussian in the combined PDF
        frac_gaus = ROOT.RooRealVar("frac_gaus", "Fraction of Gaussian", max(0.1, min(0.5, 5.0/mass)), 0.05, 0.85)
    elif mass>10 and mass<30:
# below is good for mass points 15, 20, 25
        mean = ROOT.RooRealVar("mean", f"mean_{mass}", mass, mass - 0.2 * mass, mass + 0.2 * mass)
        
        sigma_gaus = ROOT.RooRealVar("sigma_gaus", f"sigma_gaus_{mass}", 3, 0.1, 5)
    
        # Define the Gaussian PDF
        gaussian = ROOT.RooGaussian("gaussian", "Gaussian PDF", mass_variable, mean, sigma_gaus)

        # Double-Sided Crystal Ball parameters with adjusted initialization for higher masses
        sigma_dscb = ROOT.RooRealVar("sigma_dscb", f"sigma_dscb_{mass}", 10, 0.1, 150)  # Wider range
        alpha_left = ROOT.RooRealVar("alpha_left", f"alpha_left_{mass}", 1.5, 0.01, 10)
        n_left = ROOT.RooRealVar("n_left", f"n_left_{mass}", 2.0, 0.1, 10)
        alpha_right = ROOT.RooRealVar("alpha_right", f"alpha_right_{mass}", 1.5, 0.01, 10)
        n_right = ROOT.RooRealVar("n_right", f"n_right_{mass}", 2.0, 0.1, 10)
    
        # Define the DSCB PDF
        dscb = ROOT.RooCrystalBall("dscb", "Double-Sided Crystal Ball", mass_variable,
                                    mean, sigma_dscb, alpha_left, n_left,
                                    alpha_right, n_right)
    
        if mass == 20:
            frac_gaus = ROOT.RooRealVar("frac_gaus", f"frac_gaus_{mass}", 0.5, 0.2, 0.8)  # Adjust for 20 GeV
        else:
            frac_gaus = ROOT.RooRealVar("frac_gaus", f"frac_gaus_{mass}", 0.6, 0.2, 1.0)  # Slightly different for others
    else:
        mean = ROOT.RooRealVar("mean", f"mean_{mass}", mass, mass - 0.2 * mass, mass + 0.2 * mass)
        sigma_gaus = ROOT.RooRealVar("sigma_gaus", f"sigma_gaus_{mass}", 2, 0.1, 5)  # Width of Gaussian
        # Define the Gaussian PDF
        gaussian = ROOT.RooGaussian("gaussian", "Gaussian PDF", mass_variable, mean, sigma_gaus)
        # Define parameters for Double-Sided Crystal Ball
#                                   alpha_right, n_right)
# okay except mass 70
        if mass==70:
            sigma_dscb_0=3
        else: 
            sigma_dscb_0=10
        #sigma_dscb = ROOT.RooRealVar("sigma_dscb", f"sigma_dscb_{mass}", 10, 0.1, 100)  # Increased upper limit
        sigma_dscb = ROOT.RooRealVar("sigma_dscb", f"sigma_dscb_{mass}", sigma_dscb_0, 0.1, 100)  
        alpha_left = ROOT.RooRealVar("alpha_left", f"alpha_left_{mass}", 1.5, 0.01, 10)
        n_left = ROOT.RooRealVar("n_left", f"n_left_{mass}", 3.0, 0.1, 10)
        alpha_right = ROOT.RooRealVar("alpha_right", f"alpha_right_{mass}", 1.5, 0.01, 10)
        n_right = ROOT.RooRealVar("n_right", f"n_right_{mass}", 3.0, 0.1, 10)
    
        # Define the DSCB PDF
    
        dscb = ROOT.RooCrystalBall("dscb", "Double-Sided Crystal Ball", mass_variable,
                                    mean, sigma_dscb, alpha_left, n_left,
                                    alpha_right, n_right)
        # Define fraction of Gaussian in the mixture
        frac_gaus = ROOT.RooRealVar("frac_gaus", f"frac_gaus_{mass}", 0.5, 0.2, 1.0) 

    gauss_dscb = ROOT.RooAddPdf("gauss_dscb", "Gaussian + DSCB", ROOT.RooArgList(gaussian, dscb), ROOT.RooArgList(frac_gaus))
    models_to_fit = [
        #(gaussian, [mean,sigma_gaus]),
        #(dscb, [mean,sigma_dscb,alpha_left,n_left,alpha_right,n_right]),
        (gauss_dscb, [mean,sigma_gaus,sigma_dscb,alpha_left,n_left,alpha_right,n_right,frac_gaus]),
    ]

    fit_results_sig = {} 
    for model, params in models_to_fit:
        print("model name:   ", model.GetName())
        fit_results_sig[str(model.GetName())] = model.fitTo(
            #sig_mc,
            sig_mc_binned,
            ROOT.RooFit.Range(fit_range_sig),
            #ROOT.RooFit.Minimizer("Minuit2", "minimize"),
            ROOT.RooFit.Minimizer("Minuit2", "Migrad"), # OK except 20, 25, 70
            ROOT.RooFit.SumW2Error(True),
            #ROOT.RooFit.Strategy(0), # FIXME
            #ROOT.RooFit.Strategy(1), # FIXME # OK except 20, 25, 70
            ROOT.RooFit.Strategy(2), # FIXME 
            ROOT.RooFit.PrintLevel(1),
            ROOT.RooFit.Save()
        )    
        for param in params:
            print("parameter being setConstant:  ", param)
            param.setConstant(True)

    os.makedirs(output_dir, exist_ok=True)
    f_out_sig = ROOT.TFile("%s/workspace_sig_MZp%s_%s.root" % (output_dir, mass, year), "RECREATE")
    w_sig = ROOT.RooWorkspace("workspace_sig", "workspace_sig")
    getattr(w_sig, "import")(gauss_dscb)
    getattr(w_sig, "import")(norm_sig)
    w_sig.Print()
    w_sig.Write()
    f_out_sig.Close()

    makeplot = True
    if makeplot:
        binning_sig = ROOT.RooFit.Binning(n_bins_sig,w3l_lo,w3l_hi)
        can = ROOT.TCanvas()
        #plot = massZ1.frame() 
        plot = mass_variable.frame()
        sig_mc.plotOn(plot, ROOT.RooFit.CutRange(fit_range_sig), binning_sig)
        for model, params in models_to_fit:
            model.plotOn(plot, ROOT.RooFit.Name(str(model.GetName())))
            if model.GetName()=='gauss_dscb':
                model.plotOn(plot, ROOT.RooFit.Components("gaussian"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name("gaussian"))
                model.plotOn(plot, ROOT.RooFit.Components("dscb"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name("dscb"))
        plot.Draw()
        leg = ROOT.TLegend(0.67, 0.6, 0.89, 0.85)


        for model, params in models_to_fit:
            #leg.AddEntry("Exponential", "Exponential", "L")
            if model.GetName()=='gauss_dscb':
                leg.AddEntry(plot.findObject("gauss_dscb"), "Gaussian + DSCB", "L")
                leg.AddEntry(plot.findObject("gaussian"), "Gaussian", "L")
                leg.AddEntry(plot.findObject("dscb"), "DSCB", "L")
            else:
                leg.AddEntry(str(model.GetName()), str(model.GetName()), "L")
        leg.Draw("Same")
        can.Update()
        #base_file_path = "%s/fits/%s/gauss_dscb/newWPs/discrete/mean/entries_Feb18/switch/pTL4_0/ws_fit_mc_sig_ZpM%s_%sbins_noZpMasscut_func" % (plot_dir, year, mass, n_bins_sig)
        #base_file_path = "%s/fits/%s/gauss_dscb/newWPs/discrete/mean/entries_Feb18/switch/pTL4_0/AMS/ws_fit_mc_sig_ZpM%s_%sbins_noZpMasscut_func" % (plot_dir, year, mass, n_bins_sig)
        #base_file_path = "%s/fits/%s/gauss_dscb/newWPs/discrete/mean/entries_Feb18/switch/pTL4_0/AMS/XSGen/ws_fit_mc_sig_ZpM%s_%sbins_noZpMasscut_func" % (plot_dir, year, mass, n_bins_sig)
        #base_file_path = "%s/fits/%s/gauss_dscb/newWPs/discrete/mean/entries_Feb18/switch/pTL4_0/AMS/XSGen/fixpDNNcut/ws_fit_mc_sig_ZpM%s_%sbins_noZpMasscut_func" % (plot_dir, year, mass, n_bins_sig)
        base_file_path = "%s/fits/%s/gauss_dscb/test/ws_fit_mc_sig_ZpM%s_%sbins_noZpMasscut_func" % (plot_dir, year, mass, n_bins_sig)

        directory = os.path.dirname(base_file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        source_file = os.path.expanduser("~/index.php")
    
        shutil.copy(source_file, directory)

        can.SaveAs(base_file_path + ".png")
        can.SaveAs(base_file_path + ".pdf")

    return norm_sig, sumw_mc, num_mc, pDNN_eff_sig_num, pDNN_eff_sig_sum, entries_noWt, fit_results_sig

def create_background_workspace(mass, year, output_dir,DNN_scores): 
    print(f"Creating background workspace for mass point: {mass}, year: {year}")

    # File paths
    #bkg_file_path = f"/eos/home-c/caruta/Zp_FinalTrees/Dec4/MiniTree_bkg_pDNN_{mass}.root"
    bkg_file_path = f"/eos/home-c/caruta/Zp_FinalTrees/Feb18/MiniTree_bkg_pDNN_{mass}.root"
    data_file_path = "/eos/cms/store/group/phys_muon/TagAndProbe/total_data_no_dupe.root"
#    score = DNN_scores[mass]
    score = 0.915 # NOTE fixing for smooth pDNN effs. proposal in sig. & bkg. from Caterina
    print("DNN_score:     ", score)
    w3l_sig_lo = mass - 0.02 * mass  # 2 sigma below mass
    w3l_sig_hi = mass + 0.02 * mass  # 2 sigma above mass
    w3l_lo = mass - 0.2 * mass       # 20% below mass
    w3l_hi = mass + 0.2 * mass       # 20% above mass
    #n_bins_bkg = 80 # orig
    n_bins_bkg = 20 # NOTE, for partial unblinding mode
    fit_range_bkg = "loSB,hiSB"
    if mass==4:
        # Exclude psi' resonance window [3.62, 3.75]
        w3l_siprime_lo = 3.62
        w3l_siprime_hi = 3.75
        # Exclude J/psi resonance window [3.2, 3.25]
        w3l_jpsi_lo, w3l_jpsi_hi = 3.2, 3.25
        fit_range_bkg = "loSB1,loSB2,hiSB"


    f_bkg = ROOT.TFile.Open(bkg_file_path, "READ")
    f_data = ROOT.TFile.Open(data_file_path, "READ")
    N_background = 0
    pDNN_eff_bkg = 0

    if not f_bkg or f_bkg.IsZombie():
        raise FileNotFoundError(f"Cannot open background ROOT file: {bkg_file_path}")
    if not f_data or f_data.IsZombie():
        raise FileNotFoundError(f"Cannot open data ROOT file: {data_file_path}")

    t_bkg = f_bkg.Get("passedEvents")

    print("mass:  ", mass)
    massZ1 = ROOT.RooRealVar("massZ1", "massZ1", w3l_lo, w3l_hi)
    massZ2 = ROOT.RooRealVar("massZ2", "massZ2", w3l_lo, w3l_hi)
    mass_variable = massZ2 if mass <= 25 else massZ1

    print("mass variable :  ",mass_variable)
    mass_variable.setBins(n_bins_bkg)
    DNN_score = ROOT.RooRealVar("DNN_score", "DNN_score", 0, 1)
    pTL4 = ROOT.RooRealVar("pTL4", "pTL4", 0,0,200)

    mass_variable.setRange("loSB", w3l_lo, w3l_sig_lo)
    mass_variable.setRange("hiSB", w3l_sig_hi, w3l_hi)
    mass_variable.setRange("full", w3l_lo, w3l_hi)
    if mass==4:
        #mass_variable.setRange("loSB1", w3l_lo, w3l_siprime_lo)
        mass_variable.setRange("loSB1", w3l_jpsi_hi, w3l_siprime_lo)
        mass_variable.setRange("loSB2", w3l_siprime_hi, w3l_sig_lo)

    arg_set = ROOT.RooArgSet(DNN_score, mass_variable, pTL4)
    mass_variable_name = mass_variable.GetName()
    cut_string = (f"((DNN_score > {score} && pTL4 == 0) && "
              f"(({mass_variable_name} >= {w3l_lo} && {mass_variable_name} <= {w3l_sig_lo}) || "
              f"({mass_variable_name} >= {w3l_sig_hi} && {mass_variable_name} <= {w3l_hi})))")


    cut_string_noDNN = (f"((pTL4 == 0) && ({mass_variable_name} >= {w3l_lo} && {mass_variable_name} <= {w3l_sig_lo}) || "
              f"({mass_variable_name} >= {w3l_sig_hi} && {mass_variable_name} <= {w3l_hi}))")
# excluding known resonances
    if mass==4:
        cut_string = (f"((DNN_score > {score} && pTL4 == 0) && "
                  f"(({mass_variable_name} >= {w3l_jpsi_hi} && {mass_variable_name} <= {w3l_siprime_lo}) || "
                  f"({mass_variable_name} >= {w3l_siprime_hi} && {mass_variable_name} <= {w3l_sig_lo}) || "
                  f"({mass_variable_name} >= {w3l_sig_hi} && {mass_variable_name} <= {w3l_hi})))")
        cut_string_noDNN = (f"((pTL4 == 0) && "
                  f"(({mass_variable_name} >= {w3l_jpsi_hi} && {mass_variable_name} <= {w3l_siprime_lo}) || "
                  f"({mass_variable_name} >= {w3l_siprime_hi} && {mass_variable_name} <= {w3l_sig_lo}) || "
                  f"({mass_variable_name} >= {w3l_sig_hi} && {mass_variable_name} <= {w3l_hi})))")
    if mass>=30:
        massZ2.setRange(0, 80)
        arg_set = ROOT.RooArgSet(DNN_score, mass_variable, pTL4, massZ2)
        cut_string = f"({cut_string} && (massZ2 < 9.0 | massZ2 > 11.0))"
        cut_string_noDNN = f"({cut_string_noDNN} && (massZ2 < 9.0 | massZ2 > 11.0))"


    print(f"Applying selection for background: {cut_string}")
    print(f"Applying selection for background (no DNN cut): {cut_string_noDNN}")

    bkg_data = ROOT.RooDataSet("bkg_data", "bkg_data", t_bkg,
                             arg_set, cut_string)
    N_background = bkg_data.numEntries()

    bkg_data_noDNN = ROOT.RooDataSet("bkg_data_noDNN", "bkg_data_noDNN", t_bkg,
                             arg_set, cut_string_noDNN)

    pDNN_eff_bkg = bkg_data.numEntries()/bkg_data_noDNN.numEntries()
    print("pDNN_eff_bkg:     ", pDNN_eff_bkg)
    bkg_data_hist = ROOT.RooDataHist("bkg_data_hist", "Background Data Histogram", ROOT.RooArgSet(mass_variable), bkg_data)

    data_obs = ROOT.RooDataSet("data_obs", "data_obs", t_bkg,
                             arg_set, cut_string)


    # Define models
    alpha = ROOT.RooRealVar("alpha", "alpha", -0.05, -0.2, 2)
    model_exp_bkg = ROOT.RooExponential("model_exp_bkg", "Exponential Background Model", mass_variable, alpha)

    poly_1 = ROOT.RooRealVar("poly_1", "T1 of Chebyshev Polynomial", 0.01, -4, 4)
    poly_2 = ROOT.RooRealVar("poly_2", "T2 of Chebyshev Polynomial", 0.01, -4, 4)
    poly_3 = ROOT.RooRealVar("poly_3", "T3 of Chebyshev Polynomial", 0.01, -4, 4)
    #model_poly_bkg = ROOT.RooChebychev("model_poly_bkg", "Chebyshev Polynomial Background Model", mass_variable, ROOT.RooArgList(poly_1, poly_2, poly_3)) # 3rd order
    #model_poly_bkg = ROOT.RooChebychev("model_poly_bkg", "Chebyshev Polynomial Background Model", mass_variable, ROOT.RooArgList(poly_1, poly_2)) # 2nd order
    model_poly_bkg = ROOT.RooChebychev("model_poly_bkg", "Chebyshev Polynomial Background Model", mass_variable, ROOT.RooArgList(poly_1)) # 1st order
    # Define coefficients for the power-law model
    beta = ROOT.RooRealVar("beta", "beta", -1, -5, 5)  
    
    # Define the power-law model
    model_powerlaw_bkg = ROOT.RooPower(
        "model_powerlaw_bkg",
        "1st Order Power Law Background Model",
        mass_variable,
        beta     
    ) 
    
    # Define coefficients for the linear model
    slope = ROOT.RooRealVar("slope", "slope", -0.01, -0.5, 1.5)  
    
    # Define the linear model
    model_linear_bkg = ROOT.RooPolynomial(
        "model_linear_bkg",
        "Linear Background Model",
        mass_variable,
        ROOT.RooArgList(slope)
    ) 

    # Define normalization coefficients for the combination (model_powerlaw_bkg and the model_linear_bkg)
    frac_powerlaw = ROOT.RooRealVar("frac_powerlaw", "Fraction of Power Law", 0.3, 0.0, 1.0)

    # Combine the power-law and linear models into a single model
    model_pow_bkg = ROOT.RooAddPdf(
        "model_pow_bkg",
        "Combined Power Law and Linear Background Model",
        ROOT.RooArgList(model_powerlaw_bkg, model_linear_bkg),
        ROOT.RooArgList(frac_powerlaw)
    )

    # Define the coefficients for the Bernstein polynomial
    coef0_bern1 = ROOT.RooRealVar("coef0_bern1", "Coefficient 0", 0.1, 0.0, 1.0)
    coef1_bern1 = ROOT.RooRealVar("coef1_bern1", "Coefficient 1", 0.2, 0.0, 1.0)
    coef0_bern2 = ROOT.RooRealVar("coef0_bern2", "Coefficient 0", 0.1, 0.0, 1.0)
#    coef1_bern2 = ROOT.RooRealVar("coef1_bern2", "Coefficient 1", 0.2, 0.0, 1.0)
    coef1_bern2 = ROOT.RooRealVar("coef1_bern2", "Coefficient 1", 0.2, -0.5, 0.5)
    coef2_bern2 = ROOT.RooRealVar("coef2_bern2", "Coefficient 2", 0.3, 0.0, 1.0)
    coef0_bern3 = ROOT.RooRealVar("coef0_bern3", "Coefficient 0", 0.1, 0.0, 1.0)
    coef1_bern3 = ROOT.RooRealVar("coef1_bern3", "Coefficient 1", 0.2, 0.0, 1.0)
    coef2_bern3 = ROOT.RooRealVar("coef2_bern3", "Coefficient 2", 0.3, 0.0, 1.0)
    coef3_bern3 = ROOT.RooRealVar("coef3_bern3", "Coefficient 3", 0.4, 0.0, 1.0)

    # Create the 1st-order Bernstein polynomial model
    model_bern1_bkg = ROOT.RooBernstein(
        "model_bern1_bkg",
        "1st Order Bernstein Polynomial Background Model",
        mass_variable,  # Variable to fit
        ROOT.RooArgList(coef0_bern1, coef1_bern1)  # Coefficients
    )

    # Create the 2nd-order Bernstein polynomial model
    model_bern2_bkg = ROOT.RooBernstein(
        "model_bern2_bkg",
        "2nd Order Bernstein Polynomial Background Model",
        mass_variable,  # Variable to fit
        ROOT.RooArgList(coef0_bern2, coef1_bern2, coef2_bern2)  # Coefficients
    )

    # Create the 3rd-order Bernstein polynomial model
    model_bern3_bkg = ROOT.RooBernstein(
        "model_bern3_bkg",
        "3rd Order Bernstein Polynomial Background Model",
        mass_variable,  # Variable to fit
        ROOT.RooArgList(coef0_bern3, coef1_bern3, coef2_bern3, coef3_bern3)  # Coefficients
    )


    laurent_coef1 = ROOT.RooRealVar("laurent_coef1", "Laurent Coefficient 1", 1.0, -5.0, 10.0)
    laurent_coef2 = ROOT.RooRealVar("laurent_coef2", "Laurent Coefficient 2", 1.0, -5.0, 10.0)
    laurent_formula = "(@1/@0) + (@2/(@0*@0))"  # i.e. (coef1/mass_variable + coef2/mass_variable^2)
    # Create the RooGenericPdf for the Laurent series
    model_laurent_bkg = ROOT.RooGenericPdf(
        "model_laurent_bkg",
        "Laurent Series Background Model",
        laurent_formula,
        ROOT.RooArgList(mass_variable, laurent_coef1, laurent_coef2)
    )

    models_to_fit = [
        (model_exp_bkg, [alpha]),
        #(model_poly_bkg, [poly_1, poly_2, poly_3]),
        (model_poly_bkg, [poly_1]),
#        (model_poly_bkg, [poly_1, poly_2]),
        (model_powerlaw_bkg, [beta]),
        (model_linear_bkg, [slope]),
#        (model_pow_bkg, [frac_powerlaw]),
        (model_bern1_bkg, [coef0_bern1, coef1_bern1]),
        (model_bern2_bkg, [coef0_bern2, coef1_bern2, coef2_bern2]),
        (model_bern3_bkg, [coef0_bern3, coef1_bern3, coef2_bern3, coef3_bern3]),
    #    (model_laurent_bkg, [laurent_coef1, laurent_coef2]),
    ]
    fit_results_bkg = {}
    for model, params in models_to_fit:
        print("model name:   ", model.GetName())
        fit_results_bkg[str(model.GetName())] = model.fitTo(
            bkg_data,
            ROOT.RooFit.Range(fit_range_bkg),
            ROOT.RooFit.Minimizer("Minuit2", "minimize"),
            ROOT.RooFit.SumW2Error(True),
            ROOT.RooFit.PrintLevel(-1),
            ROOT.RooFit.Save()
        )
        for param in params:
            param.setConstant(True)
    print("fit_results_bkg:     :",fit_results_bkg)
    print("fit_results_bkg[model_exp_bkg]:     :",fit_results_bkg["model_exp_bkg"])
    # RooMultiPdf
    pdf_index = ROOT.RooCategory("pdfindex_bkg", "Index of Pdf for Background")
    models = ROOT.RooArgList(model_exp_bkg, model_poly_bkg,model_powerlaw_bkg,model_linear_bkg,model_bern1_bkg,model_bern2_bkg,model_bern3_bkg)
    multipdf_bkg = ROOT.RooMultiPdf("multipdf_bkg", "MultiPdf for Background", pdf_index, models)

    # Normalization
    norm_bkg = ROOT.RooRealVar("multipdf_bkg_norm", "Number of background events", bkg_data.numEntries(), 0, 3 * bkg_data.numEntries())

    # Workspace
    workspace_data = ROOT.RooWorkspace("workspace_data", "Data Workspace")
    getattr(workspace_data, "import")(multipdf_bkg, ROOT.RooFit.RecycleConflictNodes())
    getattr(workspace_data, "import")(norm_bkg)
    getattr(workspace_data, "import")(bkg_data_hist)
    getattr(workspace_data, "import")(data_obs)

    os.makedirs(output_dir, exist_ok=True)
    #workspace_file = os.path.join(output_dir, f"workspace_data_MZp{mass}.root")
    workspace_file = os.path.join(output_dir, f"workspace_data_MZp%s_%s.root"%(mass,year))
    workspace_data.writeToFile(workspace_file)
    print(f"Workspace saved to {workspace_file}")

    makeplot = True 
    if makeplot:
        binning_bkg = ROOT.RooFit.Binning(n_bins_bkg, w3l_lo, w3l_hi)
        can = ROOT.TCanvas()
        plot = mass_variable.frame()
        
        bkg_data.plotOn(plot, binning_bkg,
                        ROOT.RooFit.MarkerColor(0), 
                        ROOT.RooFit.LineColor(0), 
                        ROOT.RooFit.FillColor(2),  
                        ROOT.RooFit.FillStyle(3001)
                       )    
        
        color = 2
        model_colors = []  # for colors for the models
        for model, params in models_to_fit:
            model.plotOn(plot, ROOT.RooFit.NormRange(fit_range_bkg),
                         ROOT.RooFit.Range(fit_range_bkg), 
                         ROOT.RooFit.LineColor(color),
                         ROOT.RooFit.Name(str(model.GetName()))
                        )    
            model_colors.append(color)  
            color += 1
        
        bkg_data.plotOn(plot, ROOT.RooFit.CutRange(fit_range_bkg), binning_bkg)
        
        plot.Draw()
    
        max_y = plot.GetMaximum()
    
        # Legend parameters
        legend_num_items = len(models_to_fit)
        legend_height = 0.05  
        total_legend_height = (legend_height * (legend_num_items // 3 + 1))  
        legend_margin = 0.02  
    
        # Calculate positions in the upper left area
        leg_x1 = 0.15
        leg_y1 = 0.85 - total_legend_height - legend_margin
        leg_x2 = 0.45  # Width for 3 columns
        leg_y2 = 0.85
    
        if leg_y1 < 0.1:  # not to go below zero or cross the border
            leg_y1 = 0.1
            leg_y2 = leg_y1 + total_legend_height
    
        leg = ROOT.TLegend(leg_x1, leg_y1, leg_x2, leg_y2)
        leg.SetFillColor(0) 
        leg.SetBorderSize(0)  
        leg.SetNColumns(3)  
        
        for idx, (model, params) in enumerate(models_to_fit):
            short_name = str(model.GetName()).replace("model_", "").replace("_bkg", "")
            leg.AddEntry(short_name, short_name, "L")  
        
        for idx, model_color in enumerate(model_colors):
            leg.GetListOfPrimitives().At(idx).SetLineColor(model_color)
        
        leg.Draw("Same")
    
        can.Update()
        
        #base_file_path = "%s/fits/%s/gauss_dscb/newWPs/discrete/mean/entries_Feb18/switch/pTL4_0/AMS/ws_fit_data_bkg_ZpM%s_%sbins_noZpMasscut_func" % (plot_dir, year, mass, n_bins_bkg)
        #base_file_path = "%s/fits/%s/gauss_dscb/newWPs/discrete/mean/entries_Feb18/switch/pTL4_0/AMS/XSGen/ws_fit_data_bkg_ZpM%s_%sbins_noZpMasscut_func" % (plot_dir, year, mass, n_bins_bkg)
        base_file_path = "%s/fits/%s/gauss_dscb/test/ws_fit_data_bkg_ZpM%s_%sbins_noZpMasscut_func" % (plot_dir, year, mass, n_bins_bkg)
        directory = os.path.dirname(base_file_path)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        can.SaveAs(base_file_path + ".png")
        can.SaveAs(base_file_path + ".pdf")
        
        return N_background, pDNN_eff_bkg, fit_results_bkg


