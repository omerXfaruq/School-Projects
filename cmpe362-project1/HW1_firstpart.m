%Ömer Faruk Özdemir 2016400048
%Cmpe362 Hw1
disp("Hello There")
t=(-2:0.01:2)
%y7=t .* sin(2*pi*t)
%subplot(5,2,7)
%plot(t,y7)


y1=sin(2*pi*t)
y2= sin(2*pi*10*t)
y3=10*sin(2*pi*t)
y4= sin(2*pi*t)+10
y5= sin(2*pi*(t-0.5))
y6= 10*sin(2*pi*10*t)
y7=t.*sin(2*pi*t)
y8= (sin(2*pi*t)./t)
y9= y1+y2+y3+y4+y5+y6+y7+y8

figure(1)
subplot(5,2,1)
plot(t,y1)

subplot(5,2,2)
plot(t,y2)

subplot(5,2,3)
plot(t,y3)

subplot(5,2,4)
plot(t,y4)

subplot(5,2,5)
plot(t,y5)

subplot(5,2,6)
plot(t,y6)

subplot(5,2,7)
plot(t,y7)

subplot(5,2,8)
plot(t,y8)

subplot(5,2,9)
plot(t,y9)


%Finished plots
%Problem 2

z=randn(401,1)*0.1
z=z'
y10= z, y11 = z+t , y12= z+y1, y13= z.*y1, y14=t.*sin(2*pi*z), 
y15= sin(2*pi*(t+z)), y16= z.*y2, y17= sin(2*pi*(t+10*z)), y18=y1./z 
y19= y11+y12+y13+y14+y15+y16+y17+y18

figure(2)
subplot(5,2,1)
plot(t,y10)

subplot(5,2,2)
plot(t,y11)

subplot(5,2,3)
plot(t,y12)

subplot(5,2,4)
plot(t,y13)

subplot(5,2,5)
plot(t,y14)

subplot(5,2,6)
plot(t,y15)

subplot(5,2,7)
plot(t,y16)

subplot(5,2,8)
plot(t,y17)

subplot(5,2,9)
plot(t,y18)

subplot(5,2,10)
plot(t,y19)

%Problem 3

z=rand(401,1)*0.1
z=z'
y20= z, y21 = z+t , y22= z+y1, y23= z.*y1, y24=t.*sin(2*pi*z), 
y25= sin(2*pi*(t+z)), y26= z.*y2, y27= sin(2*pi.*(t+10*z)), y28=y1./z 
y29= y21+y22+y23+y24+y25+y26+y27+y28
figure(3)
subplot(5,2,1)
plot(t,y20)

subplot(5,2,2)
plot(t,y21)

subplot(5,2,3)
plot(t,y22)

subplot(5,2,4)
plot(t,y23)

subplot(5,2,5)
plot(t,y24)

subplot(5,2,6)
plot(t,y25)

subplot(5,2,7)
plot(t,y26)

subplot(5,2,8)
plot(t,y27)

subplot(5,2,9)
plot(t,y28)

subplot(5,2,10)
plot(t,y29)

%Problem 4

r1=sqrt(1).*randn(5000,1)
r2=sqrt(8).*randn(5000,1)
r3=sqrt(64).*randn(5000,1)
r4=sqrt(256).*randn(5000,1)
figure(4)
subplot(2,2,1)
hist(r1)
subplot(2,2,2)
hist(r2)
subplot(2,2,3)
hist(r3)
subplot(2,2,4)
hist(r4)

%Problem 5 

r6=10+ sqrt(1).*randn(5000,1)
r7=20+ sqrt(4).*randn(5000,1)
r8=-10 + sqrt(1).*randn(5000,1)
r9=-20 + sqrt(4).*randn(5000,1)
figure(5)
subplot(2,2,1)
hist(r6)
subplot(2,2,2)
hist(r7)
subplot(2,2,3)
hist(r8)
subplot(2,2,4)
hist(r9)

%Problem 6

r11=-4 + 8.*rand(5000,1)
r21=-20+ 40.*rand(5000,1)
figure(6)
subplot(2,2,1)
hist(r11)
subplot(2,2,2)
hist(r21)

