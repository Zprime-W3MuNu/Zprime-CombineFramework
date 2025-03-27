import ast 
import re

#def update_norms(mass, norm_sig, sumw=None, num=None, bkg_norm=None, xs_mass=None, pDNN_eff_bkg=None, pDNN_eff_sig_num=None, pDNN_eff_sig_sum=None):
def update_norms(mass, norm_sig, sumw=None, num=None, bkg_norm=None, xs_mass=None, pDNN_eff_bkg=None, pDNN_eff_sig_num=None, pDNN_eff_sig_sum=None, entries_noWt=None):
    # Update norms.py
    norms_file = "norms.py"

    try:
        with open(norms_file, "r") as f:
            content = f.read()

        data = {}
        exec(content, {}, data)
        sig_norms = data.get("sig_norms", {}) 
        sig_sumw = data.get("sig_sumw", {}) 
        sig_num = data.get("sig_num", {}) 
        bkg_norms = data.get("bkg_norms", {}) 
        xs_mass_dict = data.get("xs_mass", {}) 
        pDNN_eff_bkg_dict = data.get("pDNN_eff_bkg", {}) 
        pDNN_eff_sig_num_dict = data.get("pDNN_eff_sig_num", {}) 
        pDNN_eff_sig_sum_dict = data.get("pDNN_eff_sig_sum", {}) 
        entries_noWt_dict = data.get("entries_noWt", {}) 
    except (FileNotFoundError, SyntaxError, ValueError):
        sig_norms = {}
        sig_sumw = {}
        sig_num = {}
        bkg_norms = {}
        xs_mass_dict = {}
        pDNN_eff_bkg_dict = {}
        pDNN_eff_sig_num_dict = {}
        pDNN_eff_sig_sum_dict = {}
        entries_noWt_dict = {}

    sig_norms[mass] = norm_sig
    if sumw is not None:
        sig_sumw[mass] = sumw
    if num is not None:
        sig_num[mass] = num 
    if bkg_norm is not None:
        bkg_norms[mass] = bkg_norm
    if xs_mass is not None:
        xs_mass_dict[mass] = xs_mass
    if pDNN_eff_bkg is not None:
        pDNN_eff_bkg_dict[mass] = pDNN_eff_bkg
    if pDNN_eff_sig_num is not None:
        pDNN_eff_sig_num_dict[mass] = pDNN_eff_sig_num
    if pDNN_eff_sig_sum is not None:
        pDNN_eff_sig_sum_dict[mass] = pDNN_eff_sig_sum
    if entries_noWt is not None:
        entries_noWt_dict[mass] = entries_noWt

    with open(norms_file, "w") as f:
        f.write("sig_norms = {\n")
        for m, n in sig_norms.items():
            f.write(f"    {m}: {n},\n")
        f.write("}\n")

        f.write("sig_sumw = {\n")
        for m, s in sig_sumw.items():
            f.write(f"    {m}: {s},\n")
        f.write("}\n")

        f.write("sig_num = {\n")
        for m, n in sig_num.items():
            f.write(f"    {m}: {n},\n")
        f.write("}\n")

        f.write("bkg_norms = {\n")
        for m, b in bkg_norms.items():
            f.write(f"    {m}: {b},\n")
        f.write("}\n")

        f.write("xs_mass = {\n")
        for m, x in xs_mass_dict.items():
            f.write(f"    {m}: {x},\n")
        f.write("}\n")

        f.write("pDNN_eff_bkg = {\n")
        for m, p in pDNN_eff_bkg_dict.items():
            f.write(f"    {m}: {p},\n")
        f.write("}\n")

        f.write("pDNN_eff_sig_num = {\n")
        for m, p in pDNN_eff_sig_num_dict.items():
            f.write(f"    {m}: {p},\n")
        f.write("}\n")

        f.write("pDNN_eff_sig_sum = {\n")
        for m, p in pDNN_eff_sig_sum_dict.items():
            f.write(f"    {m}: {p},\n")
        f.write("}\n")

        f.write("entries_noWt = {\n")
        for m, p in entries_noWt_dict.items():
            f.write(f"    {m}: {p},\n")
        f.write("}\n")

