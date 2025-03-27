#!/bin/bash

output_script="expected_limits_discrete_knownMC.py"
echo "limits = {" > $output_script

echo "    'full_limits': {" >> $output_script
mass_points=(2 4 5 15 20 25 30 35 40 45 50 55 60 65 70)

for mass in "${mass_points[@]}"; do
    echo "Processing mass point: $mass"

  mass_formatted=$(printf "%.2f" $mass)
  datacard="datacards/datacard_MZp${mass}_2016.txt"

  if [[ -f $datacard ]]; then
    echo "Running combine for mass point $mass_formatted..."
    result_full=$(combine -M AsymptoticLimits "$datacard" --run blind --rMin 0.000000 --rMax 0.001 --rAbsAcc 0.000001 --rRelAcc 0.0001 -n M${mass})
#    if [[ "$mass" == "2" || "$mass" == "4" || "$mass" == "5" || "$mass" == "15" || "$mass" == "20" || "$mass" == "25" ]]; then
#        result_full=$(combine -M AsymptoticLimits "$datacard" --run blind --setParameterRanges r=1e-5,1)
#    else
#        result_full=$(combine -M AsymptoticLimits "$datacard" --run blind)
#    fi

    expected_50_full=$(echo "$result_full" | grep "Expected 50.0%:" | awk '{print $5}')

    if [[ ! -z $expected_50_full ]]; then
      echo "        $mass_formatted: $expected_50_full," >> $output_script
    else
      echo "Warning: No 50.0% expected limit found for mass point $mass_formatted (full limits)."
    fi
  else
    echo "Datacard $datacard not found, skipping mass point $mass_formatted."
  fi

done

echo "    }," >> $output_script

echo "    'stat_only_limits': {" >> $output_script

# for statistical-only limits

for mass in "${mass_points[@]}"; do
  # Format the mass point with two decimal places
  mass_formatted=$(printf "%.2f" $mass)
  datacard="datacards/datacard_MZp${mass}_2016.txt"
  if [[ -f $datacard ]]; then
    echo "Running combine for mass point $mass_formatted with stat-only limits..."

    # Stat-only limits (freeze all nuisances)
    #result_stat=$(combine -M AsymptoticLimits "$datacard" --run blind --freezeParameters all)  
    #result_stat=$(combine -M AsymptoticLimits "$datacard" --run blind --freezeParameters xs_Zp,lumi,pdfindex_bkg --rMin 0.000000 --rMax 0.001 --rAbsAcc 0.000001 --rRelAcc 0.0001  -n M${mass}_stat)
    result_stat=$(combine -M AsymptoticLimits "$datacard" --run blind --freezeParameters xs_Zp,lumi,pdfindex_bkg --rMin 0.000000 --rMax 0.001 --rAbsAcc 0.000001 --rRelAcc 0.0001  -n M${mass}_stat --X-rtd MINIMIZER_freezeDisassociatedParams)
    expected_50_stat=$(echo "$result_stat" | grep "Expected 50.0%:" | awk '{print $5}')

    if [[ ! -z $expected_50_stat ]]; then
      echo "        $mass_formatted: $expected_50_stat," >> $output_script
    else
      echo "Warning: No 50.0% expected limit found for mass point $mass_formatted (stat-only limits)."
    fi
  else
    echo "Datacard $datacard not found, skipping mass point $mass_formatted."
  fi

done

echo "    }" >> $output_script
echo "}" >> $output_script

echo "Results stored in $output_script."

