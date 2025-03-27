#!/bin/bash

mass_points=(2 4 5 15 20 25 30 35 40 45 50 55 60 65 70)
#mass_points=(65) # 5 15 20 25 30 35 40 45 50 55 60 65 70)
for mass in "${mass_points[@]}"; do
  mass_formatted=$(printf "%.2f" $mass)
  datacard="datacards/datacard_MZp${mass}_2016.txt"  
  if [[ -f $datacard ]]; then
    echo "Running combine FitDiagnostics for mass point $mass_formatted..."
    echo "combine -M FitDiagnostics $datacard -n M${mass_formatted}_discrete --cminDefaultMinimizerStrategy=0 --X-rtd MINIMIZER_freezeDisassociatedParams --saveNormalizations --plots --saveShapes -t -1  -m $mass --saveWorkspace"
    combine -M FitDiagnostics $datacard -n M${mass_formatted}_discrete --cminDefaultMinimizerStrategy=0 --X-rtd MINIMIZER_freezeDisassociatedParams --saveNormalizations --plots --saveShapes -t -1  -m $mass --saveWorkspace
  else
    echo "Datacard $datacard not found, skipping mass point $mass_formatted."
  fi  
  mv "covariance_fit_s.png" "covariance_fit_s_${mass}.png"
  mv "covariance_fit_b.png" "covariance_fit_b_${mass}.png"
done

first_letter=$(whoami | cut -c1)
username=$(whoami)
user="${first_letter}/${username}"
out_dir="/eos/user/${user}/www/Wto3l/fits/comb/test/"
mkdir -p "$out_dir"
rsync -av *png $out_dir
cp /afs/cern.ch/user/t/tjavaid/public/index.php $out_dir 
rm *fit*png

output_file="prefit_postfit_norms_knownMC.py"

echo "preFit_postFit_Norms = {" > "$output_file"

output_csv="prefit_postfit_norms_knownMC.csv"

echo "mass,ZpToMuMu_Prefit,ZpToMuMu_SBFit,bkg_Prefit,bkg_SBFit" > "$output_csv"


for mass in "${mass_points[@]}"; do
  mass_formatted=$(printf "%.2f" $mass)
  
  file_FitDiagnostics="fitDiagnosticsM${mass_formatted}_discrete.root"

  if [[ -f $file_FitDiagnostics ]]; then
    echo "Running combine FitDiagnostics for mass point $mass_formatted..."
    
    python3 ../HiggsAnalysis/CombinedLimit/test/mlfitNormsToText.py $file_FitDiagnostics > temp_output.txt

    zp_line=$(grep "ZpToMuMu" temp_output.txt | head -1)
    bkg_line=$(grep " bkg " temp_output.txt | head -1)

    zp_prefit=$(echo $zp_line | awk '{print $3}')
    zp_sbfit=$(echo $zp_line | awk '{print $4}')
    bkg_prefit=$(echo $bkg_line | awk '{print $3}')
    bkg_sbfit=$(echo $bkg_line | awk '{print $4}')

    if [[ -n $zp_prefit && -n $zp_sbfit && -n $bkg_prefit && -n $bkg_sbfit ]]; then
      echo "    $mass_formatted: {" >> "$output_file"
      echo "        \"ZpToMuMu\": {\"Pre-fit\": $zp_prefit, \"S+B Fit\": $zp_sbfit}," >> "$output_file"
      echo "        \"bkg\": {\"Pre-fit\": $bkg_prefit, \"S+B Fit\": $bkg_sbfit}" >> "$output_file"
      echo "    }," >> "$output_file"
      echo "$mass_formatted,$zp_prefit,$zp_sbfit,$bkg_prefit,$bkg_sbfit" >> "$output_csv"
    else
      echo "Failed to parse results for mass $mass_formatted"
    fi  
  else
    echo "FitDiagnostics file $file_FitDiagnostics not found, skipping mass point $mass_formatted."
  fi  
done

echo "}" >> "$output_file"

rm -f temp_output.txt

echo "Pre-fit and post-fit norms saved in $output_file and in $output_csv"








