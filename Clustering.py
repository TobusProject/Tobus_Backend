from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import pandas as pd
import matplotlib.pyplot as plt
import csv
from collections import defaultdict

df = pd.read_csv("../SourceData/Google/clustering.csv")
df = df.dropna()
method_list = ("average", "centroid", "complete", "median", "single", "ward", "weighted")
label = []

section = df["SectionNum"]
df = df.drop("SectionNum",axis = 1)

from sklearn.preprocessing import MinMaxScaler
minmaxsc = MinMaxScaler()
X = df.loc[:,"v_Mean":"Jam"]
X = minmaxsc.fit_transform(X)
df.loc[:,"v_Mean":"Jam"] = X

# df = df.drop("v_Mean",axis=1)
for s in section:
    label.append(s)
    
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=8)
kmeans.fit(df)
df["label"] = kmeans.labels_
lstcp = kmeans.labels_

sns.scatterplot(data=df,x = "v_Mean" ,y='Jam',hue = "label")

plt.xlim(-0.5, 1.5)
plt.ylim(-0.5, 1.5)
plt.savefig("Cluster_kmeans.png")

for i in range(len(label)):
    wrt = label[i],lstcp[i]
    print(wrt)