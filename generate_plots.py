"""
Script to generate all figures for the Linear Systems Project LaTeX Report
Based on MSSP 2026 Paper:
"Signal processing and force control for precision machining with grinding system
integrating an aerostatic suspension compact pneumatic actuator"
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set plot styling
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 13
plt.rcParams['lines.linewidth'] = 1.8
plt.rcParams['grid.alpha'] = 0.4
plt.rcParams['grid.linestyle'] = '--'

output_dir = 'figures'
os.makedirs(output_dir, exist_ok=True)

# System parameters:
# m = 1.0 kg, c = 6.0 N*s/m, k = 25.0 N/m
# G(s) = 1 / (s^2 + 6s + 25)
m = 1.0
c = 6.0
k = 25.0
wn = np.sqrt(k / m)      # 5.0 rad/s
zeta = c / (2 * np.sqrt(k * m))  # 0.6
wd = wn * np.sqrt(1 - zeta**2)   # 4.0 rad/s
sigma = zeta * wn        # 3.0 s^-1
Kdc = 1.0 / k            # 0.04 m/N

# ==============================================================================
# Fig 1: Schematic of ASCPA Grinding End-Effector System
# ==============================================================================
fig, ax = plt.subplots(figsize=(7, 3.8), dpi=300)
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 6)
ax.axis('off')

# Cylinder body
ax.add_patch(patches.Rectangle((0, 1.5), 6, 3, fill=True, facecolor='#EAECEE', edgecolor='#2C3E50', lw=2))
ax.text(3, 4.7, 'Aerostatic Cylinder Chamber ($P = 0.4$ MPa)', ha='center', va='center', fontweight='bold', color='#2C3E50')

# Piston inside
ax.add_patch(patches.Rectangle((2.2, 1.7), 1.6, 2.6, fill=True, facecolor='#3498DB', edgecolor='#1B4F72', lw=2))
ax.text(3.0, 3.0, 'Air-Bearing\nPiston\n($m = 1$ kg)', ha='center', va='center', color='white', fontweight='bold')

# Air film gap indication
ax.annotate('Air film ($h_0 = 30\,\mu$m)', xy=(3.0, 4.3), xytext=(3.0, 5.3),
            arrowprops=dict(facecolor='#E74C3C', shrink=0.08, width=1.5, headwidth=6),
            ha='center', fontweight='bold', color='#C0392B')
ax.annotate('', xy=(3.0, 1.7), xytext=(3.0, 0.7),
            arrowprops=dict(facecolor='#E74C3C', shrink=0.08, width=1.5, headwidth=6))
ax.text(3.0, 0.4, 'Non-contact Aerostatic Suspension ($\sigma_2 = 1.2$ N s/m)', ha='center', va='center', color='#C0392B', fontsize=9)

# Piston rod
ax.add_patch(patches.Rectangle((3.8, 2.6), 4.2, 0.8, fill=True, facecolor='#BDC3C7', edgecolor='#34495E', lw=1.5))

# Front cover air bearing
ax.add_patch(patches.Rectangle((5.5, 2.3), 1.0, 1.4, fill=True, facecolor='#F39C12', edgecolor='#B9770E', lw=1.5))
ax.text(6.0, 1.9, 'Air Bearing Guide', ha='center', va='center', fontsize=8, color='#B9770E', fontweight='bold')

# Grinding tool / head
ax.add_patch(patches.Circle((8.5, 3.0), 0.7, fill=True, facecolor='#E67E22', edgecolor='#935116', lw=2))
ax.text(8.5, 3.0, 'Grinding\nSpindle', ha='center', va='center', color='white', fontweight='bold', fontsize=8)

# Workpiece wall & contact spring/damper
ax.add_patch(patches.Rectangle((9.8, 1.0), 0.6, 4.0, fill=True, facecolor='#7F8C8D', edgecolor='#34495E', lw=2))
ax.text(10.1, 5.3, 'Workpiece', ha='center', va='center', fontweight='bold', color='#2C3E50')

# Contact spring
xs = np.linspace(8.5 + 0.7, 9.8, 100)
ys = 3.0 + 0.2 * np.sin(np.linspace(0, 8*np.pi, 100))
ax.plot(xs, ys, color='#2980B9', lw=2)
ax.text(9.5, 3.5, 'Contact $k = 25$ N/m', ha='center', fontsize=9, color='#2980B9', fontweight='bold')

# Pneumatic input force arrow
ax.annotate('', xy=(2.2, 3.0), xytext=(0.5, 3.0),
            arrowprops=dict(facecolor='#27AE60', edgecolor='#196F3D', shrink=0.05, width=3, headwidth=9))
ax.text(1.2, 3.5, 'Input Force $u(t)$\n$A_p \Delta P(t)$', ha='center', va='center', fontweight='bold', color='#196F3D')

# Displacement output
ax.annotate('', xy=(8.5, 1.8), xytext=(7.5, 1.8),
            arrowprops=dict(facecolor='#8E44AD', edgecolor='#5B2C6F', shrink=0.05, width=2, headwidth=7))
ax.text(8.0, 1.4, 'Output $y(t) = x(t)$', ha='center', va='center', fontweight='bold', color='#5B2C6F')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig1_system_schematic.png'), dpi=300)
plt.close()

# ==============================================================================
# Fig 2: Friction Characterization: ASCPA vs LFPA vs TPA (Table 2 of paper)
# ==============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)
v = np.linspace(0, 15, 500)  # mm/s

# Parameters from Table 2 in paper:
# TPA: Fc=15 N, Fs=18.45 N, vs=5 mm/s, sigma2=0.283 N*s/mm
# LFPA: Fc=5.4 N, Fs=8.7 N, vs=1.4 mm/s, sigma2=0.01 N*s/mm
# ASCPA: Fc=0.0777 N, Fs=0.0767 N, vs=0.01 mm/s, sigma2=0.0012 N*s/mm
f_tpa = (15 + (18.45 - 15) * np.exp(-(v/5.0)**2)) * (2/np.pi)*np.arctan(15*v) + 0.283 * v
f_lfpa = (5.4 + (8.7 - 5.4) * np.exp(-(v/1.4)**2)) * (2/np.pi)*np.arctan(15*v) + 0.01 * v
f_ascpa = (0.0777 + (0.0767 - 0.0777) * np.exp(-(v/0.01)**2)) * (2/np.pi)*np.arctan(15*v) + 0.0012 * v

ax.plot(v, f_tpa, label='TPA (Traditional Pneumatic Actuator)', color='#C0392B', lw=2.2)
ax.plot(v, f_lfpa, label='LFPA (Low-Friction Pneumatic Actuator)', color='#E67E22', lw=2.2, linestyle='--')
ax.plot(v, f_ascpa, label='ASCPA (Proposed Aerostatic Suspension)', color='#27AE60', lw=2.5)

ax.set_xlabel('Sliding Velocity $v$ (mm/s)', fontweight='bold')
ax.set_ylabel('Friction Force $f$ (N)', fontweight='bold')
ax.set_title('Experimental Friction Comparison (Table 2 of Reference Paper)', fontweight='bold')
ax.legend(frameon=True, loc='center right')
ax.grid(True)

# Inset zoom for ASCPA
ax_ins = ax.inset_axes([0.48, 0.15, 0.45, 0.35])
ax_ins.plot(v, f_ascpa, color='#27AE60', lw=2)
ax_ins.set_xlim(0, 15)
ax_ins.set_ylim(0, 0.12)
ax_ins.set_title('Zoom: ASCPA ($\ll 0.1$ N)', fontsize=9, fontweight='bold', color='#27AE60')
ax_ins.grid(True, linestyle=':')
ax_ins.set_xlabel('Velocity (mm/s)', fontsize=8)
ax_ins.set_ylabel('Friction (N)', fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig2_friction_comparison.png'), dpi=300)
plt.close()

# ==============================================================================
# Fig 3: s-Plane Pole-Zero Diagram
# ==============================================================================
fig, ax = plt.subplots(figsize=(5.5, 4.8), dpi=300)

ax.axhline(0, color='black', lw=1.2)
ax.axvline(0, color='black', lw=1.2)
ax.set_xlim(-6, 2)
ax.set_ylim(-6, 6)

# Shaded stable region
ax.axvspan(-6, 0, alpha=0.08, color='green', label='Stable Region ($\mathrm{Re}(s) < 0$)')

# Plot poles: s = -3 +/- j4
poles = [-3 + 4j, -3 - 4j]
ax.plot([p.real for p in poles], [p.imag for p in poles], 'rx', markersize=12, mew=3, label=r'Poles $p_{1,2} = -3 \pm j4$')

# Lines and annotations
for p in poles:
    ax.plot([0, p.real], [0, p.imag], 'b--', lw=1.2)
    ax.plot([p.real, p.real], [0, p.imag], 'gray', linestyle=':', lw=1)
    ax.plot([0, p.real], [p.imag, p.imag], 'gray', linestyle=':', lw=1)

# Annotate distances
ax.text(-3, -0.6, r'$-\sigma = -3$', ha='center', color='darkred', fontweight='bold')
ax.text(-0.3, 4.1, r'$+j\omega_d = +j4$', ha='right', color='darkblue', fontweight='bold')
ax.text(-0.3, -4.1, r'$-j\omega_d = -j4$', ha='right', color='darkblue', fontweight='bold')

# Damping radius arc
theta = np.linspace(0, 2*np.pi, 200)
ax.plot(5*np.cos(theta), 5*np.sin(theta), 'k:', lw=1, alpha=0.6)
ax.text(-1.3, 2.3, r'$\omega_n = 5$ rad/s', color='purple', fontweight='bold')

# Angle theta arc
th = np.linspace(np.pi, np.pi - np.arccos(0.6), 50)
ax.plot(1.5*np.cos(th), 1.5*np.sin(th), 'm-', lw=1.5)
ax.text(-1.8, 0.4, r'$\theta = 53.1^\circ$', color='m', fontweight='bold')

ax.set_xlabel(r'Real Axis $\sigma$ ($\mathrm{s}^{-1}$)', fontweight='bold')
ax.set_ylabel(r'Imaginary Axis $j\omega$ ($\mathrm{rad/s}$)', fontweight='bold')
ax.set_title(r'$s$-Plane Pole-Zero Constellation', fontweight='bold')
ax.grid(True)
ax.legend(frameon=True, loc='upper left')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig3_splane_pole_zero.png'), dpi=300)
plt.close()

# ==============================================================================
# Fig 4: Frequency Response / Bode Plot of G(jw)
# ==============================================================================
fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(6.5, 5.0), sharex=True, dpi=300)

w = np.logspace(-1, 2, 500)
s = 1j * w
G = 1.0 / (s**2 + 6*s + 25)
mag_dB = 20 * np.log10(np.abs(G))
phase_deg = np.unwrap(np.angle(G)) * 180 / np.pi

# Resonant metrics
wr = wn * np.sqrt(1 - 2*zeta**2)  # 5 * sqrt(0.28) = 2.646 rad/s
Mr = 1.0 / (2 * zeta * np.sqrt(1 - zeta**2) * k)  # 1 / (2*0.6*0.8*25) = 1/24 = 0.04167
Mr_dB = 20 * np.log10(Mr)

# Magnitude
ax_mag.semilogx(w, mag_dB, color='#2980B9', lw=2.2, label=r'$|G(j\omega)|$')
ax_mag.plot(wr, Mr_dB, 'ro', markersize=7, label=f'Resonant Peak: $\omega_r = {wr:.2f}$ rad/s, $M_r = {Mr_dB:.2f}$ dB')
ax_mag.axhline(20*np.log10(Kdc), color='gray', linestyle=':', label=f'DC Gain $K_{{dc}} = {20*np.log10(Kdc):.2f}$ dB')
ax_mag.set_ylabel('Magnitude (dB)', fontweight='bold')
ax_mag.set_title(r'Frequency Response $G(j\omega) = \frac{1}{(25 - \omega^2) + j6\omega}$', fontweight='bold')
ax_mag.grid(True, which='both')
ax_mag.legend(frameon=True, loc='lower left')

# Phase
ax_phase.semilogx(w, phase_deg, color='#C0392B', lw=2.2, label=r'$\angle G(j\omega)$')
ax_phase.axhline(-90, color='gray', linestyle=':', label=r'$-90^\circ$ at $\omega_n = 5$ rad/s')
ax_phase.axvline(wn, color='purple', linestyle='--', alpha=0.7)
ax_phase.set_xlabel(r'Frequency $\omega$ (rad/s)', fontweight='bold')
ax_phase.set_ylabel('Phase (deg)', fontweight='bold')
ax_phase.set_yticks([0, -45, -90, -135, -180])
ax_phase.grid(True, which='both')
ax_phase.legend(frameon=True, loc='lower left')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig4_frequency_bode.png'), dpi=300)
plt.close()

# ==============================================================================
# Fig 5: Rectangular Pulse Response in Time Domain (Multiple Pulse Widths)
# ==============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)
t = np.linspace(0, 4.0, 1000)

def step_resp(time_arr):
    res = np.zeros_like(time_arr)
    pos = time_arr >= 0
    t_pos = time_arr[pos]
    res[pos] = Kdc * (1.0 - np.exp(-3*t_pos) * (np.cos(4*t_pos) + 0.75 * np.sin(4*t_pos)))
    return res

for T, col, ls in zip([0.5, 1.0, 2.0], ['#2980B9', '#27AE60', '#E67E22'], ['-', '--', '-.']):
    # u(t) = A [u(t) - u(t-T)]
    u_t = np.where((t >= 0) & (t <= T), 1.0, 0.0)
    y_t = step_resp(t) - step_resp(t - T)
    ax.plot(t, y_t, label=f'Output $y(t)$ ($T = {T}$ s)', color=col, linestyle=ls, lw=2)

ax.plot(t, np.where((t >= 0) & (t <= 1.0), 0.04, 0.0), 'k:', lw=1.5, label='Input $u(t) / k$ ($T=1$ s scaled)')

ax.set_xlabel('Time $t$ (s)', fontweight='bold')
ax.set_ylabel('Displacement $y(t)$ (m)', fontweight='bold')
ax.set_title('Single Rectangular Pulse Response ($A = 1$ N)', fontweight='bold')
ax.grid(True)
ax.legend(frameon=True, loc='upper right')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig5_pulse_responses.png'), dpi=300)
plt.close()

# ==============================================================================
# Fig 6: CTFT Spectrum of Rectangular Pulse Input and Output
# ==============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)

w_spec = np.linspace(0.01, 30, 1000)
T_pulse = 1.0
U_jw = np.abs(np.sinc(w_spec * T_pulse / (2 * np.pi)) * T_pulse)
G_jw = 1.0 / np.sqrt((25 - w_spec**2)**2 + 36 * w_spec**2)
Y_jw = U_jw * G_jw

ax.plot(w_spec, U_jw, label=r'Input Spectrum $|U(j\omega)|$ (Sinc)', color='#7F8C8D', lw=1.8, linestyle='--')
ax.plot(w_spec, G_jw / G_jw[0], label=r'Normalized System $|G(j\omega)| / G(0)$', color='#2980B9', lw=1.8, linestyle=':')
ax.plot(w_spec, Y_jw / Y_jw[0], label=r'Normalized Output Spectrum $|Y(j\omega)| / Y(0)$', color='#C0392B', lw=2.3)

ax.set_xlabel(r'Frequency $\omega$ (rad/s)', fontweight='bold')
ax.set_ylabel('Normalized Magnitude', fontweight='bold')
ax.set_title(r'Continuous-Time Fourier Transform Spectrum ($T = 1.0$ s)', fontweight='bold')
ax.grid(True)
ax.legend(frameon=True, loc='upper right')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig6_pulse_spectrum.png'), dpi=300)
plt.close()

# ==============================================================================
# Fig 7: Fourier Series Representation of Rectangular Pulse Input
# ==============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)

T0 = 4.0
T_w = 1.0
w0 = 2 * np.pi / T0
t_fs = np.linspace(-0.5, 4.5, 1000)
u_exact = np.where((t_fs % T0 >= 0) & (t_fs % T0 <= T_w), 1.0, 0.0)

ax.plot(t_fs, u_exact, 'k-', lw=2.5, label='Exact Periodic Pulse $u(t)$')

colors = ['#E74C3C', '#F39C12', '#27AE60', '#2980B9']
for N, col in zip([1, 3, 7, 25], colors):
    u_approx = np.full_like(t_fs, T_w / T0)
    for n in range(1, N + 1):
        an = (2.0 / (n * np.pi)) * np.sin(n * w0 * T_w / 2.0) * np.cos(n * w0 * T_w / 2.0) # a_n
        # Actually: c_n = (1/T0) int_0^T e^{-j n w0 t} dt = (1/T0) (1 - e^{-j n w0 T}) / (j n w0)
        # u(t) = a0 + sum an cos(n w0 t) + bn sin(n w0 t)
        an = (1.0 / (n * np.pi)) * np.sin(n * w0 * T_w)
        bn = (2.0 / (n * np.pi)) * (np.sin(n * w0 * T_w / 2.0))**2
        u_approx += an * np.cos(n * w0 * t_fs) + bn * np.sin(n * w0 * t_fs)
    ax.plot(t_fs, u_approx, label=f'Fourier Series $N = {N}$', color=col, lw=1.5)

ax.set_xlabel('Time $t$ (s)', fontweight='bold')
ax.set_ylabel('Amplitude $u(t)$ (N)', fontweight='bold')
ax.set_title('Fourier Series Approximation of Input (Gibbs Phenomenon)', fontweight='bold')
ax.grid(True)
ax.legend(frameon=True, loc='upper right')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig7_fourier_series_input.png'), dpi=300)
plt.close()

# ==============================================================================
# Fig 8: Fourier Series Output and NMSE Convergence
# ==============================================================================
fig, (ax_resp, ax_err) = plt.subplots(1, 2, figsize=(9.5, 4.0), dpi=300)

# Steady-state periodic output
def periodic_output_exact(time_arr, periods=10):
    y = np.zeros_like(time_arr)
    for p in range(-periods, 1):
        t_shift = time_arr - p * T0
        y += step_resp(t_shift) - step_resp(t_shift - T_w)
    return y

t_out = np.linspace(0, T0, 500)
y_exact = periodic_output_exact(t_out)

ax_resp.plot(t_out, y_exact, 'k-', lw=2.5, label='Exact Steady-State $y(t)$')

Ns = [1, 3, 7, 15]
nmse_list = []
N_all = list(range(1, 31))

for n_harm in N_all:
    y_approx = np.full_like(t_out, (T_w / T0) * Kdc)
    for n in range(1, n_harm + 1):
        an = (1.0 / (n * np.pi)) * np.sin(n * w0 * T_w)
        bn = (2.0 / (n * np.pi)) * (np.sin(n * w0 * T_w / 2.0))**2
        cn = 0.5 * (an - 1j * bn)
        
        # Multiply by G(j n w0)
        s_n = 1j * n * w0
        G_n = 1.0 / (s_n**2 + 6*s_n + 25)
        dn = cn * G_n
        
        # Real harmonic: 2 * Re(dn * exp(j n w0 t))
        y_approx += 2 * np.real(dn * np.exp(1j * n * w0 * t_out))
    
    nmse = np.sum((y_exact - y_approx)**2) / np.sum(y_exact**2) * 100
    nmse_list.append(nmse)
    
    if n_harm in Ns:
        ax_resp.plot(t_out, y_approx, label=f'Fourier $N = {n_harm}$', lw=1.6)

ax_resp.set_xlabel('Time $t$ (s)', fontweight='bold')
ax_resp.set_ylabel('Displacement $y(t)$ (m)', fontweight='bold')
ax_resp.set_title('Output Fourier Approximation', fontweight='bold')
ax_resp.grid(True)
ax_resp.legend(frameon=True, loc='upper right')

# NMSE error plot
ax_err.semilogy(N_all, nmse_list, 'ro-', lw=1.8, markersize=5, label='Output NMSE (%)')
ax_err.axhline(1.0, color='gray', linestyle='--', label='1% Error Threshold')
ax_err.set_xlabel('Number of Harmonics $N$', fontweight='bold')
ax_err.set_ylabel('Normalized Mean Square Error (%)', fontweight='bold')
ax_err.set_title('Reconstruction Convergence Rate', fontweight='bold')
ax_err.grid(True, which='both')
ax_err.legend(frameon=True, loc='upper right')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig8_fourier_series_output.png'), dpi=300)
plt.close()

# ==============================================================================
# Fig 9: Impulse and Step Responses with Performance Markers
# ==============================================================================
fig, (ax_imp, ax_step) = plt.subplots(1, 2, figsize=(9.5, 4.0), dpi=300)

t_eval = np.linspace(0, 2.5, 1000)

# Impulse response
h_t = 0.25 * np.exp(-3*t_eval) * np.sin(4*t_eval)
envelope = 0.25 * np.exp(-3*t_eval)

ax_imp.plot(t_eval, h_t, color='#2980B9', lw=2.2, label=r'$h(t) = 0.25 e^{-3t}\sin(4t)$')
ax_imp.plot(t_eval, envelope, 'k--', lw=1.2, label=r'$\pm 0.25 e^{-3t}$ Envelope')
ax_imp.plot(t_eval, -envelope, 'k--', lw=1.2)
ax_imp.axhline(0, color='black', lw=0.8)
ax_imp.set_xlabel('Time $t$ (s)', fontweight='bold')
ax_imp.set_ylabel('Impulse Response $h(t)$', fontweight='bold')
ax_imp.set_title('Impulse Response (Time Domain)', fontweight='bold')
ax_imp.grid(True)
ax_imp.legend(frameon=True, loc='upper right')

# Step response
y_step_eval = step_resp(t_eval)
y_final = Kdc
tp = np.pi / 4.0
ymax = Kdc * (1 + np.exp(-3*np.pi/4.0))

ax_step.plot(t_eval, y_step_eval, color='#C0392B', lw=2.2, label=r'$y_{step}(t)$')
ax_step.axhline(y_final, color='black', linestyle='--', label=f'Steady State $y_{{ss}} = {y_final:.2f}$ m')
ax_step.plot(tp, ymax, 'bo', markersize=7, label=f'Peak: $t_p = {tp:.3f}$ s, $y_{{max}} = {ymax:.4f}$ m')

# Settling bounds (2%)
ax_step.axhline(y_final * 1.02, color='green', linestyle=':', alpha=0.7, label='$\pm 2\%$ Settling Band')
ax_step.axhline(y_final * 0.98, color='green', linestyle=':', alpha=0.7)
ax_step.axvline(4.0 / 3.0, color='purple', linestyle='--', alpha=0.7, label=r'Settling Time $t_s \approx 1.33$ s')

ax_step.set_xlabel('Time $t$ (s)', fontweight='bold')
ax_step.set_ylabel('Displacement $y(t)$ (m)', fontweight='bold')
ax_step.set_title('Step Response (%OS = 9.48%)', fontweight='bold')
ax_step.grid(True)
ax_step.legend(frameon=True, loc='lower right', fontsize=8.5)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig9_impulse_step_response.png'), dpi=300)
plt.close()

print('All 9 figures successfully generated and saved to figures/')
