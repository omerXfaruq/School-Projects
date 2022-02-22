% Cmpe362 Hw2 Ömer Faruk Özdemir Question 3

[y1,fs1] = audioread('./clean_testset_wav/p232_028.wav'); %y=sampled data and Fs is the sampling rate
[y2,fs2] = audioread('./noisy_testset_wav/p232_028.wav'); %y=sampled data and Fs is the sampling rate

figure(1)
subplot(3,1,1)
plot(y1)
title('Clean Audio')

subplot(3,1,2)
plot(y2)
title('Noisy Audio')

subplot(3,1,3)
plot(y2-y1)
title('Difference')

x=y2+delayseq(y2,1)+delayseq(y2,2)+delayseq(y2,3)+delayseq(y2,4)+delayseq(y2,5)+delayseq(y2,6)+delayseq(y2,7)+delayseq(y2,8)+delayseq(y2,9)+delayseq(y2,10) ...
    +delayseq(y2,11)+delayseq(y2,12)+delayseq(y2,13)+delayseq(y2,14)+delayseq(y2,15)+delayseq(y2,16)+delayseq(y2,17)+delayseq(y2,18)+delayseq(y2,19)+delayseq(y2,20) ...
    +delayseq(y2,21)+delayseq(y2,22)+delayseq(y2,23)+delayseq(y2,24)+delayseq(y2,25)+delayseq(y2,26)+delayseq(y2,27)+delayseq(y2,28)+delayseq(y2,29)

x=x/30

figure(2)
subplot(3,1,1)
plot(x)
title('Filtered Audio')
subplot(3,1,2)
plot(y1)
title('Clean Audio')
subplot(3,1,3)
plot(y2)
title('Noisy Audio')

audiowrite("outputOfMyCode.wav",x,fs1)

figure(3)

subplot(2,1,1)
plot(y2-y1)
title('Noisy-Clean Difference')
subplot(2,1,2)
plot(x-y1)
title('Filtered-Clean Difference')


figure(4)
subplot(3,1,1)

n=length(y1)                         % number of samples
z = fft(y1) / n           %discrete fourier transform
z2 = fftshift(z);

f = (0:n-1)*(fs1/n);         % frequency range
f0 = (-n/2:n/2-1)*(fs1/n); % 0-centered frequency range

plot(f0,z2)
title("Clean Wave Frequency Spectrum")
xlabel("Frequency")
ylabel("Value")

subplot(3,1,2)

n=length(y2)                         % number of samples
z = fft(y2) / n           %discrete fourier transform
z2 = fftshift(z);

f = (0:n-1)*(fs2/n);         % frequency range
f0 = (-n/2:n/2-1)*(fs2/n); % 0-centered frequency range

plot(f0,z2)
title("Noisy Wave Frequency Spectrum")
xlabel("Frequency")
ylabel("Value")


subplot(3,1,3)

n=length(x)                         % number of samples
z = fft(x) / n           %discrete fourier transform
z2 = fftshift(z);

f = (0:n-1)*(fs1/n);         % frequency range
f0 = (-n/2:n/2-1)*(fs1/n); % 0-centered frequency range

plot(f0,z2)
title("Filtered Wave Frequency Spectrum")
xlabel("Frequency")
ylabel("Value")

