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
    labels = ["supposability", "co-occurrence", "object importance", "value importance"]

    # Generate eigen pairs
    eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]
    for i in range(len(eig_pairs)):
        eig_pairs[i] = (eig_pairs[i][0], eig_pairs[i][1], labels[i])
        print(eig_pairs[i])

    # Eigenvalues in order
    sorted_labels = []
    eig_pairs.sort(key=lambda x: x[0], reverse=True)
    print('Eigenvalues in descending order:')
    for i in eig_pairs:
        print(i)
        sorted_labels.append(i[2])


    # Explained variance
    tot = sum(eig_vals)
    var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
    cum_var_exp = np.cumsum(var_exp)


    with plt.style.context('seaborn-whitegrid'):
        plt.figure(figsize=(6, 4))

        plt.bar(sorted_labels, var_exp, alpha=0.5, align='center',
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




    plt.show()



# pca("singularized/flipped/100k_cooccurrence_data.txt")
pca("data.txt")