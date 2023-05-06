from collections import defaultdict
import numpy as np
from sklearn.preprocessing import StandardScaler
import numpy as np
from numpy.linalg import norm
from sklearn.preprocessing import minmax_scale
import math
from pattern.text.en import singularize
from nltk.stem.wordnet import WordNetLemmatizer

def def_nr():
    return -1

def def_value():
    return defaultdict(def_nr)

def read_data(filename):
    f = open(filename)

    objects = []
    values = []
    confidences = []
    cooccurrences = []
    object_counts = []
    value_counts = []
    vocabulary = set()
    relations = {}

    verification_data = defaultdict(def_value)
    evaluation_data = []

    f.readline()
    for i in f:
        i = i.strip()
        i_split = i.split(", ")

        objects.append(i_split[0])
        values.append(i_split[1])
        confidences.append(float(i_split[2]))
        cooccurrences.append(int(i_split[3]))
        object_counts.append(int(i_split[4]))
        value_counts.append(int(i_split[5]))
        vocabulary.add(i_split[0])
        vocabulary.add(i_split[1])
        if i_split[0] not in relations:
            relations[i_split[0]] = [i_split[1]]
        else:
            relations[i_split[0]].append(i_split[1])
        # relations[singularize(WordNetLemmatizer().lemmatize(i_split[0]))] = singularize(WordNetLemmatizer().lemmatize(i_split[1]))

    f.close()

    f = open("double_words.csv")
    f.readline()
    for row in f:
        row = row.strip()
        split_row = row.split(",")
        word1 = singularize(WordNetLemmatizer().lemmatize(split_row[0]))
        word2 = singularize(WordNetLemmatizer().lemmatize(split_row[1]))
        if word1 in relations:
            if word2 in relations[word1]:
                verification_data[word1][split_row[1]] = float(split_row[2])
        elif word2 in relations:
            if word1 in relations[word2]:
                verification_data[word2][word1] = float(split_row[2])
    
    f.close()

    for i in range(len(objects)):
        # print(verification_data[objects[i]][values[i]])
        evaluation_data.append(verification_data[objects[i]][values[i]])
    

    return objects, values, confidences, cooccurrences, object_counts, value_counts, evaluation_data


def remove_zero_rows(a, b):
    A = []
    B = []

    for i in range(len(a)):
        if b[i] == -1:
            continue
        A.append(a[i])
        B.append(b[i])

    return A, B

global last_similarity
global last_confs
global _c, _co, _o, _v
last  = -1
last_confs = []



def i_sqrt_cos(confidences, verification):
    temp = 0
    for i in range(len(confidences)):
        temp += math.sqrt(confidences[i] * verification[i])
    return temp / (math.sqrt(sum(confidences)) * math.sqrt(sum(verification)))


def evaluate(confidences, verification):
    global last, last_confs
    # define two lists or array
    A = np.array(confidences)
    B = np.array(verification)

    A, B = remove_zero_rows(A, B)
    # compute cosine similarity
    # cosine = np.dot(A,B)/(norm(A)*norm(B))
    cosine = i_sqrt_cos(A, B)
    if cosine > last:
        last_confs = confidences
        last = cosine
    return cosine



def formula(data, c, co, o, v, apply_data):
    global _c, _co, _o, _v
    ajusted_confidences = []
    for i in range(len(data[0])):
        ajusted_confidences.append(apply_data(data, i, c, co, o, v))
    ajusted_confidences = minmax_scale(ajusted_confidences)
    return ajusted_confidences



def calc_rec(data, apply_data):
    return calc_c(data, 1, 1, 1, 1, 5, -1, apply_data)



def calc_c(data, c, co, o, v, depth, best, apply_data):
    if depth == 0:
        return best, c, co, o, v
    else:
        ajusted_confidences = formula(data, c, co, o, v, apply_data)
        similarity = evaluate(ajusted_confidences, verification_data)
        
        global last, _c, _co, _o, _v
        if similarity >= last:
            _c = c
            _co = co
            _o = o
            _v = o

        best, c, co, o, v = calc_co(data, c, co, o, v, depth, best, apply_data)
        best1, c1, co1, o1, v1 = calc_c(data, c * 2, co, o, v, depth-1, similarity, apply_data)
        best2, c2, co2, o2, v2 = calc_c(data, c / 1.5, co, o, v, depth-1, similarity, apply_data)

        if best1 > best2:
            return best1, c1, co1, o1, v1
        else:
            return best2, c2, co2, o2, v2
        

def calc_co(data, c, co, o, v, depth, best, aply_data):
    if depth == 0:
        return best, c, co, o, v
    else:
        ajusted_confidences = formula(data, c, co, o, v, aply_data)
        similarity = evaluate(ajusted_confidences, verification_data)

        global last, _c, _co, _o, _v
        if similarity >= last:
            _c = c
            _co = co
            _o = o
            _v = o

        best, c, co, o, v = calc_o(data, c, co, o, v, depth, best, aply_data)
        best1, c1, co1, o1, v1 = calc_co(data, c, co * 2, o, v, depth-1, similarity, aply_data)
        best2, c2, co2, o2, v2 = calc_co(data, c, co / 1.5, o, v, depth-1, similarity, aply_data)

        if best1 > best2:
            return best1, c1, co1, o1, v1
        else:
            return best2, c2, co2, o2, v2

def calc_o(data, c, co, o, v, depth, best, aply_data):
    if depth == 0:
        return best, c, co, o, v
    else:
        ajusted_confidences = formula(data, c, co, o, v, aply_data)
        similarity = evaluate(ajusted_confidences, verification_data)

        global last, _c, _co, _o, _v
        if similarity >= last:
            _c = c
            _co = co
            _o = o
            _v = o

        best, c, co, o, v = calc_v(data, c, co, o, v, depth, best, aply_data)
        best1, c1, co1, o1, v1 = calc_o(data, c, co, o * 2, v, depth-1, similarity, aply_data)
        best2, c2, co2, o2, v2 = calc_o(data, c, co, o / 1.5, v, depth-1, similarity, aply_data)

        if best1 > best2:
            return best1, c1, co1, o1, v1
        else:
            return best2, c2, co2, o2, v2
        
def calc_v(data, c, co, o, v, depth, best, apply_data):
    if depth == 0:
        return best, c, co, o, v
    else:
        ajusted_confidences = formula(data, c, co, o, v, apply_data)
        similarity = evaluate(ajusted_confidences, verification_data)

        global last, _c, _co, _o, _v
        if similarity >= last:
            _c = c
            _co = co
            _o = o
            _v = o

        best1, c1, co1, o1, v1 = calc_v(data, c, co, o, v * 2, depth-1, similarity, apply_data)
        best2, c2, co2, o2, v2 = calc_v(data, c, co, o, v / 1.5, depth-1, similarity, apply_data)

        if best1 > best2:
            return best1, c1, co1, o1, v1
        else:
            return best2, c2, co2, o2, v2


def calc_static(data, apply_data):
    ajdjusted_confidences = []
    for i in range(len(data[0])):
        ajdjusted_confidences.append(apply_data(data, i))
    ajdjusted_confidences = minmax_scale(ajdjusted_confidences, (0, 1))
    similarity = evaluate(ajdjusted_confidences, verification_data)
    return similarity



def adjust_supposability(in_file, out_file, confidences, cooccurrences, object_counts, value_counts, write_to_file=False):
    global last, last_confs

    # Standardize data
    scaler = StandardScaler()
    sets = np.array([confidences, cooccurrences, object_counts, value_counts])
    standardized_data = scaler.fit_transform(sets.T).T
    standardized_confidences = np.asarray(confidences).T
    standardized_cooccurrences = minmax_scale(scaler.fit_transform(np.array([cooccurrences]).T).T[0], (-1, 1))
    # standardized_object_counts = scaler.fit_transform(np.array([object_counts, object_counts]).T).T[0]
    standardized_object_counts = np.asarray(object_counts).T
    standardized_value_counts = np.asarray(value_counts).T

    # test_set = np.array([confidences, standardized_cooccurrences, standardized_object_counts, standardized_value_counts])
    test_set = [standardized_confidences, standardized_cooccurrences, standardized_object_counts, standardized_value_counts]
    # test_set = [verification_data, verification_data, verification_data, verification_data]

    # print(type(formula(np.array([[1,2],[3,4],[4,5]]), 1, 1, 1, 1)))

    # cos similarity: 0.47699561773379756 improver sqrt cos similarity: 0.7516661505980545
    # def apply_data(data, index): return data[0][index]

    # 0.0 -> 19552
    # SIMILARITY: 0.9310175695129416
    # def apply_data(data, index, c, co, o, v): return (data[0][index] * c) + (data[1][index] * co) + (data[2][index] * o) + (data[3][index] * v)

    # 0.0 -> 19591
    # SIMILARITY: 0.8997583915043091
    # def apply_data(input_data, index, c, co, o, v): return (input_data[0][index]) + (input_data[1][index] * 0.55)

    # 0.0 -> 19661
    # SIMILARITY: 0.8747814814665604
    # 1.3333333333333333
    # 37.925925925925924
    # 7.822642576269847e-06
    # 7.822642576269847e-06
    # def apply_data(data, index, c, co, o, v): return ((data[0][index] * c) + (data[1][index] * co))

    # 0.2 -> 12234
    # SIMILARITY: 0.9184217454544548
    # 2.6666666666666665
    # 0.6242950769699741
    # 8081.738699121823
    # 8081.738699121823
    # def apply_data(data, index, c, co, o, v): return ((data[0][index] * c) + (data[1][index] * co)) / ((1 + (data[2][index] * o)))
    
    # 0.1 -> 12383
    # SIMILARITY: 0.8225215179248376
    # 0.19753086419753085
    # 202.2716049382716
    # 1.030142232265988e-06
    # 1.030142232265988e-06
    # def apply_data(data, index, c, co, o, v): return ((data[0][index] * c) - (data[1][index] * co)) * ((1 / (data[3][index] * v)))

    # 0.3 -> 6400
    # SIMILARITY: 0.9108460423811375
    # 1
    # 0.6666666666666666
    # 0.1316872427983539
    # 0.1316872427983539
    # def apply_data(data, index, c, co, o, v): return ((data[0][index] * c) + ((data[1][index] * co) * (1 / ( (math.log(data[2][index]) * o ) / ( math.log(data[3][index]) *v ) ) ) ) )


    # 0.0 -> 13223
    # SIMILARITY: 0.8112071150308376
    # def apply_data(data, index): return ((data[0][index]) - (data[1][index] * 0.05)) / ((1 / math.log(data[3][index]) * 0.65))

    ### 0.1 -> 8584
    # SIMILARITY: 0.8867583999175119
    # def apply_data(data, index): return ((data[0][index]) + (data[1][index] * 0.3)) / (math.log(data[3][index]))

    ### 0.1 -> 8584 
    # SIMILARITY: 0.8867583999175119
    # def apply_data(data, index): return ((data[0][index]) + (data[1][index] * 0.3)) / (math.log(data[3][index]) * 0.8)

    ### 0.1 -> 5610
    # SIMILARITY: 0.8925113258199749
    # def apply_data(data, index): return ((data[0][index]) + (data[1][index] * 0.4)) * ((1 / math.log(data[3][index])) * 0.5)

    ### 0.3 -> 6283
    # SIMILARITY: 0.9108321059750986
    # def apply_data(data, index): return ((data[0][index]) + (data[1][index] * (1 / (math.log(data[2][index]) / math.log(data[3][index])) ) ) )

    ####### 0.4 -> 0.6688
    # SIMILARITY: 0.9095063342895561
    def apply_data(data, index): return ((data[0][index]) + (data[1][index] * (1 / ( (math.log(data[2][index]) * 0.5 ) / ( math.log(data[3][index])  ) ) ) ) )

    # 0.0 16319
    # SIMILARITY: 0.8904347680069572
    # def apply_data(data, index): return (data[0][index]) + (((math.log(data[3][index]) * 0.35))) * (data[1][index] * 0.05)

    # def apply_data(data, index): return (data[0][index])


    calc_static(test_set, apply_data)
    # calc_rec(test_set, apply_data)


    # print("Evaluation:")
    # print(evaluate(verification_data, verification_data))

    print("SIMILARITY: " + str(last))
    print(len(last_confs))
    print(last_confs[:10])
    print(min(last_confs))
    print(max(last_confs))

    count = 0
    for number in verification_data:
        if number != -1:
            count += 1
    print(count)
    # print(_c)
    # print(_co)
    # print(_o)
    # print(_v)


    if write_to_file:
        f = open(in_file)
        g = open(out_file, "w")

        index = 0
        for i in f:
            found = False
            i = i.strip()
            i_split = i.split("|")
            object = i_split[-1]
            value = i_split[2].split(" ")[0]
            conf = float(i_split[0].split(":")[0])
            for j in range(len(objects)):
                if object != objects[j]: continue
                if value != values[j]: continue
                if conf != confidences[j]: continue
                g.write(str(last_confs[j]) + ": " + i.split(":")[1] + "\n")

                

        f.close()
        g.close()

    






objects, values, confidences, cooccurrences, object_counts, value_counts, verification_data = read_data("data.txt")

adjust_supposability("flipped.txt", "flipped_adjusted.txt", confidences, cooccurrences, object_counts, value_counts, True)




