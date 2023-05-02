# code from https://sebastianraschka.com/Articles/2015_pca_in_3_steps.html#covariance-matrix

import numpy as np
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt

def pca(filename):
    # Read confidence, coocccurrence, object count and value count from data
    probabilities = []
    object_counts = []
    value_counts = []
    co_occurrence_counts = []

    f = open(filename)
    f.readline()
    for i in f:
        i = i.strip()
        i_split = i.split(", ")
        probabilities.append(float(i_split[2]))
        co_occurrence_counts.append(float(i_split[3]))
        object_counts.append(float(i_split[4]))
        value_counts.append(float(i_split[5]))

    # print(len(probabilities))
    # print(len(object_counts))
    # print(len(value_counts))
    # print(len(co_occurrence_counts))




    # Standardize data
    scaler = StandardScaler()
    sets = np.array([probabilities, co_occurrence_counts, object_counts, value_counts])
    standardized_data = scaler.fit_transform(sets.T).T

    # print(standardized_data[0][:10])
    # Calculate covariance matrix
    covariance_matrix = np.cov(standardized_data)

    # Calculate eigen vectors, eigen values
    eig_vals, eig_vecs = np.linalg.eig(covariance_matrix)

    # Generate eigen pairs
    eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

    # Eigenvalues in order
    eig_pairs.sort(key=lambda x: x[0], reverse=True)
    print('Eigenvalues in descending order:')
    for i in eig_pairs:
        print(i[0])


    # Explained variance
    tot = sum(eig_vals)
    var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
    cum_var_exp = np.cumsum(var_exp)


    with plt.style.context('seaborn-whitegrid'):
        plt.figure(figsize=(6, 4))

        plt.bar(range(4), var_exp, alpha=0.5, align='center',
                label='individual explained variance')
        plt.step(range(4), cum_var_exp, where='mid',
                label='cumulative explained variance')
        plt.ylabel('Explained variance ratio')
        plt.xlabel('Principal components')
        plt.legend(loc='best')
        plt.tight_layout()
        # plt.show()

    matrix_w = np.hstack((eig_pairs[0][1].reshape(4,1),
                        eig_pairs[1][1].reshape(4,1)))




    print('Covariance matrix \n%s' %covariance_matrix)


    # Projection onto new feature space
    Y = standardized_data.T.dot(matrix_w).T
    print(len(Y))
    print(len(Y[0]))

    with plt.style.context('seaborn-whitegrid'):
        plt.figure(figsize=(6, 4))
        plt.scatter(Y[0], Y[1])
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.legend(loc='lower center')
        plt.tight_layout()
        plt.show()



# pca("singularized/flipped/100k_cooccurrence_data.txt")
pca("data.txt")