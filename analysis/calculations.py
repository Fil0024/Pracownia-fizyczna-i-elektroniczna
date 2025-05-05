import numpy as np
from scipy.optimize import curve_fit
from data_loader import load_data

def f_to_omega(f):
    """Hz -> rad/s"""
    return 2 * np.pi * f

def calc_transmission(df, U1='U_in', U2='U_out'):
    #Dodaje do df kolumnę T = Uwy/Uwe (transmitancję)
    df = df.copy()
    df['T'] = df[U2] / df[U1]
    return df

def T_function(omega, R, L, C, Rp):
    """
    Funkcja transmitancji
    """
    num = R
    den = np.sqrt((R + Rp)**2 + (omega*L - 1/(omega*C))**2)
    return num / den

def phi_function(omega, R, L, C, Rp):
    """
    Funkcja przesunięcia fazowego
    """
    return np.arctan((1 - omega**2 * L * C) / (omega*(R+Rp)*C))

def fit_T(omega, T_exp, R, C, p0=(1e-3, 10)):
    """
    Dopasowanie L i Rp do transmitancji.
    """
    def model(omega, L, Rp):
        return T_function(omega, R, L, C, Rp)

    popt, pcov = curve_fit(model, omega, T_exp, p0=p0)
    perr = np.sqrt(np.diag(pcov))
    return popt, perr


def fit_phi(omega, phi_exp, R, C, p0=(1e-3, 10)):
    """
    Dopasowanie L i Rp do przesunięcia fazowego.
    """
    def model(omega, L, Rp):
        return phi_function(omega, R, L, C, Rp)

    popt, pcov = curve_fit(model, omega, phi_exp, p0=p0)
    perr = np.sqrt(np.diag(pcov))
    return popt, perr

def calc_parameters(df, R, C):
    df = calc_transmission(df, U1='U_in', U2='U_out')

    omega   = f_to_omega(df['Freq'].to_numpy())
    T_exp   = df['T'].to_numpy()
    phi_exp = np.deg2rad(df['Phi'].to_numpy())

    (L_T, Rp_T),  (u_LT, u_RpT)  = fit_T(omega, T_exp,   R, C)
    (L_P, Rp_P),  (u_LP, u_RpP)  = fit_phi(omega, phi_exp, R, C)

    return {
        "L_T": L_T,
        "Rp_T": Rp_T,
        "u_LT": u_LT,
        "u_RpT": u_RpT,
        "L_P": L_P,
        "Rp_P": Rp_P,
        "u_LP": u_LP,
        "u_RpP": u_RpP
    }