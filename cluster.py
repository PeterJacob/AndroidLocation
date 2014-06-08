import matplotlib.pyplot as plt
import numpy as np
import lxml
from pykml import parser
from sklearn.cluster import MeanShift


# Read data from file
with open('./rawData/31_maart.kml') as f:
    doc = parser.parse(f)

raw = doc.xpath("//gx:Track/*/text()",namespaces={'gx':'http://www.google.com/kml/ext/2.2'})
cords_raw = raw[2::2]


# Create an array of the coordinates
cords = list()
for c in cords_raw:
    lng, lat, _ = c.split(' ')
    lat, lng    = float(lat), float(lng)
    cords.append([lat,lng])

cords = np.array(cords)


# Plot the cords
plt.figure()
plt.plot(cords[:,1], cords[:,0], ':ko')
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.ylabel("Latitude")
plt.xlabel("Longitude")
plt.savefig("cords.eps", bbox_inches='tight')
plt.close()


# Compute clusters
ms = MeanShift(bandwidth=0.0003)
ms.fit(cords)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters = len(labels_unique)


# Print the clusters
print("number of data points : %d" % len(cords))
print("number of clusters : %d" % n_clusters)

for nr, (lat, lng) in enumerate(cluster_centers):
    print("Cluster %d, # of points: %d, loc=(%f, %f)" % (nr, np.sum(labels==nr), lat, lng))
