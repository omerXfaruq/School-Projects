% Cmpe362 Hw2 Ömer Faruk Özdemir Question 2

frequency1=12
frequency2=15
t = 0:1/frequency1:5;                      % 10 second span time vector
y1=sin(frequency1*2*pi*t);
y2= cos(frequency2*2*pi*t);

x=y1+y2

fs=10
Ts = 1/fs;
ts = 0:1/fs:10;
xresampled = cos(2*pi*frequency1*ts);
xreconstructed = zeros(1,length(t)); %preallocating for speed
samples = length(ts);
for i = 1:1:length(t)
    for n = 1:1:samples
        xreconstructed(i) = xreconstructed(i) + xresampled(n)*sinc(2*fs*ts(i)-n);
        
    end
end
figure(1)
subplot(3,2,1)
plot(t,x)
%hold on
%stem(ts,xresampled)
subplot(3,2,2)
plot(t,xreconstructed)
title("Undersampling")
xres1=xreconstructed

fs=30           %Nyquist rate is fmax*2
Ts = 1/fs;
ts = 0:1/fs:10;
xresampled = cos(2*pi*frequency1*ts);
xreconstructed = zeros(1,length(t)); %preallocating for speed
samples = length(ts);
for i = 1:1:length(t)
    for n = 1:1:samples
        xreconstructed(i) = xreconstructed(i) + xresampled(n)*sinc(2*fs*ts(i)-n);
        
    end
end
subplot(3,2,3)
plot(t,x)
%hold on
%stem(ts,xresampled)
subplot(3,2,4)
plot(t,xreconstructed)
title("Nyquist Sampling")
xres2=xreconstructed


fs=50
Ts = 1/fs;
ts = 0:1/fs:10;
xresampled = cos(2*pi*frequency1*ts);
xreconstructed = zeros(1,length(t)); %preallocating for speed
samples = length(ts);
for i = 1:1:length(t)
    for n = 1:1:samples
        xreconstructed(i) = xreconstructed(i) + xresampled(n)*sinc(2*fs*ts(i)-n);
    end
end
subplot(3,2,5)
plot(t,x)
%hold on
%stem(ts,xresampled)
subplot(3,2,6)
plot(t,xreconstructed)
title("Oversampling")
xres3=xreconstructed


figure(2)

subplot(3,1,1)
hold on
plot(xres1)
plot(x)
hold off
title("Undersampling")

subplot(3,1,2)
hold on
plot(xres2)
plot(x)
hold off
title("Nyquist sampling")

subplot(3,1,3)
hold on
plot(xres3)
plot(x)
hold off
title("Oversampling")
