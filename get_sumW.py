import os

# /eos/home-c/caruta/Zp_FinalTrees/sumW_sgn/sumW_2016pre/
def get_sumW_for_mass_point(mass_point):
    #eras = ["-2016", "2016", "2017", "2018"]
    eras = ["2016pre", "2016post", "2017", "2018"]
    total_sumW = 0.0
    
    for era in eras:
        #filename = f"sumW/{era}/Wto3l_M{mass_point}.txt"
        filename = f"/eos/home-c/caruta/Zp_FinalTrees/sumW_sgn//sumW_{era}/Wto3l_M{mass_point}.txt"
        
        try:
            with open(filename, 'r') as file:
                content = file.read().strip()
                sumW = float(content)  # Convert to float
                print("mass_point:   ", mass_point ,"   era:   ",era,"     sumW:   ",sumW)
                total_sumW += sumW
        except FileNotFoundError:
            print(f"Warning: File '{filename}' not found. Skipping this era.")
        except ValueError:
            print(f"Warning: Could not convert content of '{filename}' to a float. Skipping this era.")
        except Exception as e:
            print(f"An unexpected error occurred with file '{filename}': {e}")
    
    return total_sumW

#mass_point = 60
#total_sumW_value = get_sumW_for_mass_point(mass_point)

