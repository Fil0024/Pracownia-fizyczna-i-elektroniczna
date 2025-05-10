import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import calculations as calc

def visualise_data(data,  results, R, C, path_figures, name, x_axis = 'omega'):
    omega = data[x_axis].to_numpy()
    T_exp = data['U_out'] / data['U_in']
    phi_exp = np.deg2rad(data['Phi'])

    plt.figure()
    plt.scatter(omega, T_exp, label='Measured', color='blue')
    plt.plot(omega, calc.T_function(omega, R, results['L_T'], C, results['Rp_T']), label='Fit', color='red')
    plt.xlabel(r'Częstość sygnału $\omega$ (rad/s)')
    plt.ylabel('Transmitancja')
    plt.legend()
    plt.grid()
    plt.savefig(f"{path_figures}/transmittance_{name}.pdf")
    plt.close()

    plt.figure()
    plt.scatter(omega, phi_exp, label='Measured', color='blue')
    plt.plot(omega, calc.phi_function(omega, R, results['L_P'], C, results['Rp_P']), label='Fit', color='red')
    plt.xlabel(r'Częstość sygnału $\omega$ (rad/s)')
    plt.ylabel('Przesunięcie fazowe (rad)')
    plt.legend()
    plt.grid()
    plt.savefig(f"{path_figures}/phase_shift_{name}.pdf")
    plt.close()