import csv

#def get_pDNN_cuts(file_path="/eos/user/c/caruta/Zp_FinalTrees/Feb18/pDNN_cuts_AMS.txt"):
def get_pDNN_cuts(file_path="/eos/user/c/caruta/Zp_FinalTrees/Feb18/pDNN_cuts_AMS_FullPrecision.txt"):
    pDNN_cuts = {}
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row or row[0].startswith("#"):  
                continue
            mass, cut = map(float, row)
            pDNN_cuts[int(mass)] = cut # NOTE, be vigilent for fractional mass points 
    return pDNN_cuts
