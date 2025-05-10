import numpy as np
from sympy import symbols, diff, solve, sqrt, N
from scipy.optimize import curve_fit
from data_loader import load_data

def calc_transmission(df):
    #Dodaje do df kolumnę T = Uwy/Uwe (transmitancję)
    df = df.copy()
    df['T'] = df['U_out'] / df['U_in']
    df['u_T'] = df['T'] * np.sqrt((df['u_Uout'] / df['U_out'])**2 + (df['u_Uin'] / df['U_in'])**2)
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
    num = 1 - omega**2 * L * C
    den = omega*(R+Rp)*C
    return np.arctan2(num, den)

def fit_T(omega, T_exp, u_T_exp, R, C, p0=(1e-3, 20)):
    """
    Dopasowanie L i Rp do transmitancji.
    """
    def model(omega, L, Rp):
        return T_function(omega, R, L, C, Rp)

    popt, pcov = curve_fit(model, omega, T_exp, p0=p0)
    perr = np.sqrt(np.diag(pcov))

    residuals = (T_exp - model(omega, *popt)) / u_T_exp
    chi2 = np.sum(residuals**2)
    dof = len(omega) - len(popt)   # N - p
    chi2_red = chi2 / dof

    return popt, perr, chi2_red


def fit_phi(omega, phi_exp, u_phi_exp, R, C, p0=(1e-3, 30)):
    """
    Dopasowanie L i Rp do przesunięcia fazowego.
    """
    def model(omega, L, Rp):
        return phi_function(omega, R, L, C, Rp)

    popt, pcov = curve_fit(model, omega, phi_exp, p0=p0)
    perr = np.sqrt(np.diag(pcov))

    residuals = (phi_exp - model(omega, *popt)) / u_phi_exp
    chi2 = np.sum(residuals**2)
    dof = len(omega) - len(popt)
    chi2_red = chi2 / dof

    return popt, perr, chi2_red

def calc_parameters(df, R, C):
    df = calc_transmission(df)
    omega = df['omega'].to_numpy()

    T_exp, u_T_exp   = df['T'].to_numpy(), df['u_T'].to_numpy()
    phi_exp, u_phi_exp = np.pi*df['Phi'].to_numpy()/180, df['u_Phi'].to_numpy()*np.pi/180

    (L_T, Rp_T),  (u_LT, u_RpT), chi2_red_T  = fit_T(omega, T_exp, u_T_exp,   R, C)
    (L_P, Rp_P),  (u_LP, u_RpP), chi2_red_P  = fit_phi(omega, phi_exp, u_phi_exp, R, C)

    return {
        "L_T": L_T,
        "Rp_T": Rp_T,
        "u_LT": u_LT,
        "u_RpT": u_RpT,
        "chi2_red_T": chi2_red_T,
        "L_P": L_P,
        "Rp_P": Rp_P,
        "u_LP": u_LP,
        "u_RpP": u_RpP,
        "chi2_red_P": chi2_red_P
    }
    

def calc_resonance_and_bandwidth(R, L, C, Rp):
    x = symbols('x', real=True, positive=True)

    T = R / sqrt((R + Rp)**2 + (x*L - 1/(x*C))**2)

    dT = diff(T, x)
    crit_pts = solve(dT, x)

    crit_real = [pt for pt in crit_pts if pt.is_real and pt > 0]

    crit_vals = [float(N(T.subs(x, pt))) for pt in crit_real]

    idx_max = crit_vals.index(max(crit_vals))
    x_res = float(N(crit_real[idx_max]))        
    T_max = crit_vals[idx_max]             

    cutoff_level = T_max / (2**0.5)
    eq = T - cutoff_level
    cut_sols = solve(eq, x)

    cut_real = [sol for sol in cut_sols if sol.is_real and sol > 0]

    cut_vals = sorted([float(N(sol)) for sol in cut_real])

    if len(cut_vals) >= 2:
        bandwidth = cut_vals[-1] - cut_vals[0]
    else:
        bandwidth = None
        
    theoretical_x_res = 1 / (sqrt(L * C))

    theoretical_Rp = 1/T_max * ( R - T_max * R)

    return x_res, bandwidth, theoretical_x_res, T_max, theoretical_Rp
    