myWorkspace=load('mysignal')

fs=myWorkspace.fs()
period=1/fs
x=(myWorkspace.x())
t=(myWorkspace.t())


subplot(1,3,1)
plot(t,x)
xlabel('time')
ylabel('signal')

y = fft(x);             %discrete fourier transform

n = length(x);          % number of samples
f = (0:n-1)*(fs/n);     % frequency range
power = abs(y).^2/n;    % power of the DFT
subplot(1,3,2)
plot(f,power)
xlabel('Frequency')
ylabel('Power')

y0 = fftshift(y);         % shift y values
f0 = (-n/2:n/2-1)*(fs/n); % 0-centered frequency range
power0 = abs(y0).^2/n;    % 0-centered power

subplot(1,3,3)

plot(f0,power0)
xlabel('Frequency')
ylabel('Power')