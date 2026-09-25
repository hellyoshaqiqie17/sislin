%% =========================================================================
% LINEAR SYSTEMS FINAL PROJECT - MATLAB SIMULATION SCRIPT
% System: Aerostatic Suspension Compact Pneumatic Actuator (ASCPA)
% Reference Paper: Z. Yang et al., Mech. Syst. Signal Process., 2026.
% Model: Second-Order Linear Differential Equation:
%        m * y''(t) + c * y'(t) + k * y(t) = u(t)
% =========================================================================
clear; clc; close all;

%% 1. System Physical Parameters
m = 1.0;            % Total moving mass (kg)
c = 6.0;            % Equivalent viscous damping (N*s/m)
k = 25.0;           % Contact & pneumatic stiffness (N/m)

% Canonical parameters
wn = sqrt(k / m);              % Natural frequency (5.0 rad/s)
zeta = c / (2 * sqrt(k * m));   % Damping ratio (0.6)
wd = wn * sqrt(1 - zeta^2);    % Damped frequency (4.0 rad/s)
sigma = zeta * wn;             % Real decay rate (3.0 s^-1)
Kdc = 1.0 / k;                 % DC Gain (0.04 m/N)

fprintf('--- System Characteristics ---\n');
fprintf('Natural Frequency (wn): %.2f rad/s\n', wn);
fprintf('Damping Ratio (zeta):   %.2f\n', zeta);
fprintf('Damped Frequency (wd):  %.2f rad/s\n', wd);
fprintf('Decay Constant (sigma): %.2f s^-1\n', sigma);
fprintf('Poles:                  -%.1f +/- j%.1f\n', sigma, wd);

%% 2. Transfer Function Representation
s = tf('s');
G = 1 / (m * s^2 + c * s + k);
fprintf('\nTransfer Function G(s):\n');
G

%% 3. Impulse and Step Response (Problem 9)
t = linspace(0, 2.5, 1000);

% Analytical Impulse Response
h_analytical = (1 / (m * wd)) * exp(-sigma * t) .* sin(wd * t);

% Analytical Step Response
phi = acos(zeta);
y_step_analytical = Kdc * (1 - (exp(-sigma * t) ./ sqrt(1 - zeta^2)) .* sin(wd * t + phi));

% Metrics
tp = pi / wd;
OS = exp(-pi * zeta / sqrt(1 - zeta^2)) * 100;
ts = 4 / (zeta * wn);

fprintf('\n--- Step Response Metrics ---\n');
fprintf('Peak Time (tp):        %.4f s\n', tp);
fprintf('Percent Overshoot (%%):  %.2f %%\n', OS);
fprintf('Settling Time (ts, 2%%): %.4f s\n', ts);

figure('Name', 'Impulse and Step Responses', 'Position', [100 100 850 350]);
subplot(1, 2, 1);
plot(t, h_analytical, 'b-', 'LineWidth', 2); hold on;
plot(t, (1/(m*wd))*exp(-sigma*t), 'k--', 'LineWidth', 1);
plot(t, -(1/(m*wd))*exp(-sigma*t), 'k--', 'LineWidth', 1);
grid on; xlabel('Time (s)'); ylabel('h(t)');
title('Impulse Response'); legend('h(t)', 'Envelope', 'Location', 'NorthEast');

subplot(1, 2, 2);
plot(t, y_step_analytical, 'r-', 'LineWidth', 2); hold on;
yline(Kdc, 'k--', 'Steady State');
plot(tp, Kdc*(1 + exp(-pi*zeta/sqrt(1-zeta^2))), 'bo', 'MarkerSize', 8, 'LineWidth', 2);
grid on; xlabel('Time (s)'); ylabel('y(t) (m)');
title(sprintf('Step Response (%%OS = %.2f%%)', OS));

%% 4. Rectangular Pulse Response (Problem 5)
A = 1.0;            % Amplitude (N)
T_pulse = 1.0;      % Pulse duration (s)
t_pulse = linspace(0, 4.0, 1000);

y_pulse = zeros(size(t_pulse));
for i = 1:length(t_pulse)
    ti = t_pulse(i);
    y1 = 0; y2 = 0;
    if ti >= 0
        y1 = Kdc * (1 - (exp(-sigma*ti)/sqrt(1-zeta^2)) * sin(wd*ti + phi));
    end
    if ti >= T_pulse
        t_shift = ti - T_pulse;
        y2 = Kdc * (1 - (exp(-sigma*t_shift)/sqrt(1-zeta^2)) * sin(wd*t_shift + phi));
    end
    y_pulse(i) = A * (y1 - y2);
end

figure('Name', 'Rectangular Pulse Response', 'Position', [150 150 600 350]);
plot(t_pulse, y_pulse, 'g-', 'LineWidth', 2); hold on;
u_pulse = double(t_pulse >= 0 & t_pulse <= T_pulse) * Kdc;
plot(t_pulse, u_pulse, 'k:', 'LineWidth', 1.5);
grid on; xlabel('Time (s)'); ylabel('Displacement (m)');
title(sprintf('Rectangular Pulse Response (T = %.1f s)', T_pulse));
legend('Output y(t)', 'Input u(t)/k', 'Location', 'NorthEast');

%% 5. Fourier Series Representation (Problem 6)
T0 = 4.0;                   % Fundamental period (s)
w0 = 2 * pi / T0;           % Fundamental angular frequency (rad/s)
t_fs = linspace(0, T0, 1000);

% Compute Fourier Series approximations for N = 1, 3, 7, 25
harmonics = [1, 3, 7, 25];
figure('Name', 'Fourier Series Approximation', 'Position', [200 200 850 350]);

subplot(1, 2, 1);
u_exact = double(t_fs <= T_pulse);
plot(t_fs, u_exact, 'k-', 'LineWidth', 2.5); hold on;
for N = harmonics
    u_approx = ones(size(t_fs)) * (T_pulse / T0);
    for n = 1:N
        an = (1 / (n * pi)) * sin(n * w0 * T_pulse);
        bn = (2 / (n * pi)) * (sin(n * w0 * T_pulse / 2))^2;
        u_approx = u_approx + an * cos(n * w0 * t_fs) + bn * sin(n * w0 * t_fs);
    end
    plot(t_fs, u_approx, 'LineWidth', 1.5);
end
grid on; xlabel('Time (s)'); ylabel('Input Amplitude');
title('Input Fourier Series (Gibbs Phenomenon)');
legend('Exact', 'N=1', 'N=3', 'N=7', 'N=25', 'Location', 'NorthEast');

subplot(1, 2, 2);
for N = harmonics
    y_approx = ones(size(t_fs)) * (T_pulse / T0) * Kdc;
    for n = 1:N
        an = (1 / (n * pi)) * sin(n * w0 * T_pulse);
        bn = (2 / (n * pi)) * (sin(n * w0 * T_pulse / 2))^2;
        cn = 0.5 * (an - 1j * bn);
        sn = 1j * n * w0;
        Gn = 1 / (m * sn^2 + c * sn + k);
        dn = cn * Gn;
        y_approx = y_approx + 2 * real(dn * exp(1j * n * w0 * t_fs));
    end
    plot(t_fs, y_approx, 'LineWidth', 1.5); hold on;
end
grid on; xlabel('Time (s)'); ylabel('Output Displacement (m)');
title('Output Fourier Series (Fast Convergence)');
legend('N=1', 'N=3', 'N=7', 'N=25', 'Location', 'NorthEast');

%% 6. Bode and Pole-Zero Diagram (Problems 7 & 8)
figure('Name', 'Bode and Pole-Zero', 'Position', [250 250 800 400]);
subplot(1, 2, 1);
pzmap(G); grid on;
title('s-Plane Pole-Zero Constellation');

subplot(1, 2, 2);
bode(G); grid on;
title('System Frequency Response G(j\omega)');
