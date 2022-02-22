% Cmpe362 Hw2 Ömer Faruk Özdemir Question 1

f0=25
t=(0:0.001:0.12)

plotPart0=0.5
plotPart1= 2/j/j/pi/pi/1/1* exp(j*2*pi*f0*t*1)
plotPart3= 2/j/j/pi/pi/3/3* exp(j*2*pi*f0*t*3)
plotPart5= 2/j/j/pi/pi/5/5* exp(j*2*pi*f0*t*5)
plotPart7= 2/j/j/pi/pi/7/7* exp(j*2*pi*f0*t*7)
plotPart9= 2/j/j/pi/pi/9/9* exp(j*2*pi*f0*t*9)
mirrorplotPart1= 2/j/j/pi/pi/-1/-1* exp(j*2*pi*f0*t*-1)
mirrorplotPart3= 2/j/j/pi/pi/-3/-3* exp(j*2*pi*f0*t*-3)
mirrorplotPart5= 2/j/j/pi/pi/-5/-5* exp(j*2*pi*f0*t*-5)
mirrorplotPart7= 2/j/j/pi/pi/-7/-7* exp(j*2*pi*f0*t*-7)
mirrorplotPart9= 2/j/j/pi/pi/-9/-9* exp(j*2*pi*f0*t*-9)

y1=(plotPart0+plotPart1+plotPart3+mirrorplotPart1+mirrorplotPart3)
y=(plotPart0+plotPart1+plotPart3+plotPart5+plotPart7+plotPart9+mirrorplotPart1+mirrorplotPart3+mirrorplotPart5+mirrorplotPart7+mirrorplotPart9)
figure(1)
subplot(1,3,1)
plot(t,y1)
title('Sum of harmonics until 3th')

subplot(1,3,2)
plot(t,y)
title('Sum Of Harmonics Until 9th')


t = 0:0.001:.12;
T = 0.04;
fs = 1 / T0;
sawtoothWave = (sawtooth(fs * 2 * pi * t, 0.5) + 1) / 2;

subplot(1, 3, 3);
plot(t, sawtoothWave);
title("Sawtooth Wave")

figure(2)

y = fft(sawtoothWave) / length(t);             %discrete fourier transform
y2 = fftshift(y);

n = length(t);              % number of samples
f = (0:n-1)*(fs/n);         % frequency range
f0 = (-n/2:n/2-1)*(fs/n); % 0-centered frequency range

plot(f0,y2)
title("Sawtooth Wave Frequency Spectrum")
xlabel("Frequency")
ylabel("Value")