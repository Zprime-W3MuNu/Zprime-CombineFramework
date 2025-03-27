
mass=20
combine -M AsymptoticLimits datacards/datacard_MZp${mass}_2016.txt --run blind --freezeParameters xs_Zp,lumi,pdfindex_bkg --rMin 0.000000 --rMax 0.001 --rAbsAcc 0.000001 --rRelAcc 0.0001 -n M${mass}_stat --X-rtd MINIMIZER_freezeDisassociatedParams -v 3
