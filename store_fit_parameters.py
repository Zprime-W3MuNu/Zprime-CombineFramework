import json
import os

def load_fit_parameters(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as file:
                data = file.read()
                if data.strip():  
                    namespace = {}
                    exec(data, {}, namespace)
                    return namespace.get("fit_parameters", {})
        except Exception as e:
            print(f"Warning: Failed to load {file_name}. Starting fresh. Error: {e}")
    return {}

def save_fit_parameters(fit_parameters, file_name):
    with open(file_name, "w") as file:
        file.write("fit_parameters = ")
        json.dump(fit_parameters, file, indent=4)


def store_fit_parameters(existing_dict, fit_result, model_name, mass_point, params_list):
    mass_point_str = str(mass_point)

    if mass_point_str not in existing_dict:
        existing_dict[mass_point_str] = {}

    if model_name not in existing_dict[mass_point_str]:
        existing_dict[mass_point_str][model_name] = {}

    # Update parameters
    for param in params_list:
        param_name = param.GetName()
        existing_dict[mass_point_str][model_name][param_name] = { 
            "value": param.getVal(),
            "error": param.getError()
        }

    return existing_dict

