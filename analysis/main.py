import calculations as calc
from data_loader import load_data
from visualisation import visualise_data
import numpy as np

path_in1 = 'dane/pkt4.csv'
path_in2 = 'dane/pkt5.csv'
path_figures = 'raport/figures'
path_results = 'analiza/results.txt'

R1 = 510        # Ohm
R2 = 50        # Ohm
C = 1e-9      # F

data1 = load_data(path_in1)
data2 = load_data(path_in2)

# Calculate parameters
results1 = calc.calc_parameters(data1, R1, C)
results2 = calc.calc_parameters(data2, R2, C)


# Save results to a text file
with open(path_results, 'w') as f:
    f.write("Results for pkt4.csv:\n")
    f.write(f"L_T = {results1['L_T']:.4f} +- {results1['u_LT']:.4f}\n")
    f.write(f"Rp_T = {results1['Rp_T']:.4f} +- {results1['u_RpT']:.4f}\n")
    f.write(f"L_P = {results1['L_P']:.4f} +- {results1['u_LP']:.4f}\n")
    f.write(f"Rp_P = {results1['Rp_P']:.4f} +- {results1['u_RpP']:.4f}\n\n")

    f.write("Results for pkt5.csv:\n")
    f.write(f"L_T = {results2['L_T']:.4f} +- {results2['u_LT']:.4f}\n")
    f.write(f"Rp_T = {results2['Rp_T']:.4f} +- {results2['u_RpT']:.4f}\n")
    f.write(f"L_P = {results2['L_P']:.4f} +- {results2['u_LP']:.4f}\n")
    f.write(f"Rp_P = {results2['Rp_P']:.4f} +- {results2['u_RpP']:.4f}\n")

visualise_data(data1, results1, R1, C, path_figures, 'pkt4')
visualise_data(data2, results2, R2, C, path_figures, 'pkt5')
print("Results saved to", path_results)
print("Figures saved to", path_figures)