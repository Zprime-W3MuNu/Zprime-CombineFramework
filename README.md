# Zprime-CombineFramework

## Instructions for for setting up and running W->3mu nu shape analysis
After logging into the ```lxplus9``` account, following steps can be followed:
## 1. Setup 
```
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v10.1.0
scramv1 b clean; scramv1 b
git clone https://github.com/Zprime-W3MuNu/Zprime-CombineFramework.git
cd Zprime-CombineFramework
```

## 2. Add weights to root files
After navigating to the ```Zprime-CombineFramework``` directory, weights to the ```known``` MC signal samples can be added by the following:
```
python3 add_weight_branch_ent.py
```

## 3. Producing the workspaces and saving the yields

Output from the previous step is used to run the following module:
```
python3 createZPworkspace_knownMC.py
```
This module also saves the signal and background fit plots at a path on ```eos```. 
## 3. Producing the datacards
```
python3 generate_cards_Feb18.py
```
Above module creates datacards with the signal yields produced at the previous step.

## 4. Extracting the expected limits
To for all knwon mass points, do:
```
sh extract_limits_knownMC.sh
```
Limits are saved in output files.
## 5. Extracting the prefit and postfit norms
Those can be obtained by:
```
sh extract_prepostfit_norms_knownMC.sh
```
Above script saves the plots at a path on ```eos``` and values in the output files. 


