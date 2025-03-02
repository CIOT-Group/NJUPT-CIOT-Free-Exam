# import numpy as np
# import matplotlib.pyplot as plt
# import pylab
# # Though the following import is not directly being used, it is required
# # for 3D projection to work

# from sklearn.cluster import KMeans
# from sklearn import datasets

# #np.random.seed(5)

# iris = datasets.load_iris()
# X = iris.data
# y = iris.target

# estimators = [('k_means_iris_8', KMeans(n_clusters=8)),
#               ('k_means_iris_3', KMeans(n_clusters=3)),
#               ('k_means_iris_bad_init', KMeans(n_clusters=3, n_init=1,
#                                                init='random'))]

# labels_list=[]
# fignum = 1
# titles = ['8 clusters', '3 clusters', '3 clusters, bad initialization']
# for name, est in estimators:
#     fig = plt.figure(fignum, figsize=(4, 3))
#     #fig = pylab.figure(fignum, figsize=(4, 3))
#     ax = fig.add_subplot(111, projection='3d', elev=48, azim=134)
#     est.fit(X)
#     labels = est.labels_
#     labels_list.append(labels)

#     ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=labels.astype(float), edgecolor='k')#np.float in early numpy version

#     ax.xaxis.set_ticklabels([])
#     ax.yaxis.set_ticklabels([])
#     ax.zaxis.set_ticklabels([])
#     ax.set_xlabel('Petal width')
#     ax.set_ylabel('Sepal length')
#     ax.set_zlabel('Petal length')
#     ax.set_title(titles[fignum - 1])
#     ax.dist = 12
#     fignum = fignum + 1
#     plt.show()
#     #input()
    

# # Plot the ground truth
# fig = plt.figure(fignum, figsize=(4, 3))
# #fig = pylab.figure(fignum, figsize=(4, 3))
# ax = fig.add_subplot(111, projection='3d', elev=48, azim=134)

# for name, label in [('Setosa', 0),
#                     ('Versicolour', 1),
#                     ('Virginica', 2)]:
#     ax.text3D(X[y == label, 3].mean(),
#               X[y == label, 0].mean(),
#               X[y == label, 2].mean() + 2, name,
#               horizontalalignment='center',
#               bbox=dict(alpha=.2, edgecolor='w', facecolor='w'))
    
# # Reorder the labels to have colors matching the cluster results
# y = np.choose(y, [1, 2, 0]).astype(float)
# ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y, edgecolor='k')

# ax.xaxis.set_ticklabels([])
# ax.yaxis.set_ticklabels([])
# ax.zaxis.set_ticklabels([])
# ax.set_xlabel('Petal width')
# ax.set_ylabel('Sepal length')
# ax.set_zlabel('Petal length')
# ax.set_title('Ground Truth')
# ax.dist = 12

# plt.show()
# #input()
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

# Load the iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Estimators to test
estimators = [
    ('k_means_iris_8', KMeans(n_clusters=8)),
    ('k_means_iris_3', KMeans(n_clusters=3)),
    ('k_means_iris_bad_init', KMeans(n_clusters=3, n_init=1, init='random'))
]

labels_list = []
fignum = 1
titles = ['8 clusters', '3 clusters', '3 clusters, bad initialization']
metrics = []

# Evaluate each clustering result
for name, est in estimators:
    fig = plt.figure(fignum, figsize=(4, 3))
    ax = fig.add_subplot(111, projection='3d', elev=48, azim=134)
    est.fit(X)
    labels = est.labels_
    labels_list.append(labels)

    ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=labels.astype(float), edgecolor='k')
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])
    ax.set_xlabel('Petal width')
    ax.set_ylabel('Sepal length')
    ax.set_zlabel('Petal length')
    ax.set_title(titles[fignum - 1])
    ax.dist = 12
    fignum = fignum + 1
    plt.show()

    # Calculate evaluation metrics for the current clustering
    silhouette = silhouette_score(X, labels)  # Silhouette Score
    ch_score = calinski_harabasz_score(X, labels)  # Calinski-Harabasz Index
    db_score = davies_bouldin_score(X, labels)  # Davies-Bouldin Index

    metrics.append({
        'name': name,
        'silhouette_score': silhouette,
        'calinski_harabasz_score': ch_score,
        'davies_bouldin_score': db_score
    })

# Print the metrics for each clustering
for metric in metrics:
    print(f"Clustering: {metric['name']}")
    print(f"Silhouette Score: {metric['silhouette_score']:.4f}")
    print(f"Calinski-Harabasz Score: {metric['calinski_harabasz_score']:.4f}")
    print(f"Davies-Bouldin Score: {metric['davies_bouldin_score']:.4f}")
    print()

# Plot the ground truth
fig = plt.figure(fignum, figsize=(4, 3))
ax = fig.add_subplot(111, projection='3d', elev=48, azim=134)
for name, label in [('Setosa', 0), ('Versicolour', 1), ('Virginica', 2)]:
    ax.text3D(X[y == label, 3].mean(),
              X[y == label, 0].mean(),
              X[y == label, 2].mean() + 2, name,
              horizontalalignment='center',
              bbox=dict(alpha=.2, edgecolor='w', facecolor='w'))
    
y = np.choose(y, [1, 2, 0]).astype(float)
ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y, edgecolor='k')
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
ax.zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
ax.set_title('Ground Truth')
ax.dist = 12

plt.show()
