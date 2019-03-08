import matplotlib.pyplot as plt
import json as j

labels = []
values = []

d = j.loads(open('switches_markov_uses.txt').read().replace('\n',''))
s = sorted(d.items(), key=lambda x: x[1])

for v in s:
    labels.append(v[0])
    values.append(v[1])

plt.bar([i for i in range(len(values))],values)
plt.xticks([i for i in range(len(values))],labels,rotation="vertical",fontsize=5)

plt.show()
