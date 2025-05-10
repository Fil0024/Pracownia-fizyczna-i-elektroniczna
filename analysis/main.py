import calculations as calc
from data_loader import load_data, base_dir
from visualisation import visualise_data
import numpy as np

path_in1 = 'data/pkt4.csv'
path_in2 = 'data/pkt5.csv'
path_figures = 'raport/figures'
path_results = 'analysis/results.txt'

path_results = base_dir()/path_results
path_figures = base_dir()/path_figures

R1 = 506        # Ohm
R2 = 50.2        # Ohm
C = 1e-9      # F

def show_results(data,  R, C, name='no_name'):
    data['omega'] = 2 * np.pi * data['Freq']
    data['u_Uin'] = data['U_in'] * 0.03 / np.sqrt(3)
    data['u_Uout'] = data['U_out'] * 0.03 / np.sqrt(3)
    data['u_Phi'] = data['Phi'] * 0.03 / np.sqrt(3)
    results = calc.calc_parameters(data, R, C)
    exp_resonance1, exp_bandwidth1, theoretical_resonance1, exp_transmitance_rez, Theoretical_Rp  = calc.calc_resonance_and_bandwidth(R1, results['L_T'], C, results['Rp_T'])

    
    with open(path_results, 'a') as f:
        f.write("Results for "+name+":\n")
        f.write(f"L_T = {results['L_T']:.6f} +- {results['u_LT']:.6f} H\n")
        f.write(f"Rp_T = {results['Rp_T']:.4f} +- {results['u_RpT']:.4f} Ohm\n")
        f.write(f"L_P = {results['L_P']:.6f} +- {results['u_LP']:.6f} H\n")
        f.write(f"Rp_P = {results['Rp_P']:.4f} +- {results['u_RpP']:.4f} Ohm\n")
        f.write(f"chi2_red_T = {results['chi2_red_T']:.4f}\n")
        f.write(f"chi2_red_P = {results['chi2_red_P']:.4f}\n")
        f.write(f"Experimental resonance frequency (omega0) = {exp_resonance1:.4f} 1/s \n")
        f.write(f"Experimental resonance transmitance (Trez) = {exp_transmitance_rez:.4f} \n")
        f.write(f"Theoretical Rp = {Theoretical_Rp:.4f} Ohm \n")
        f.write(f"Theoretical resonance frequency (omega0) = {theoretical_resonance1:.4f} 1/s \n")
        f.write(f"Experimental bandwidth (delta_omega) = {exp_bandwidth1:.4f} 1/s \n\n")

    visualise_data(data, results, R, C, path_figures, name=name)


if __name__ == "__main__":
    with open(path_results, 'w') as f:
        f.write("")

    data1 = load_data(path_in1)
    data2 = load_data(path_in2)

    show_results(data1, R1, C, name='pkt4')
    show_results(data2, R2, C, name='pkt5')

    print("Results saved to", path_results)
    print("Figures saved to", path_figures)
