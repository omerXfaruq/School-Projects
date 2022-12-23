from matplotlib import pyplot as plt

f = open('EnergyEfficiency.log','r')
lines = f.readlines()
values = []
for line in lines:
    words = line.split(',')
    values.append(float(words[0]))

plt.plot(values)
plt.xlabel("Iteration")
plt.ylabel("Normalized Geomean EDP")
plt.show()