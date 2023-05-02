# Calculate covariance matrix of initial probability, cooccurrence, object count, value count

# Format of data:
# data[<object>][0] = <object> occurrence count
# data[<object>][1][<value>]["p"] = probability of <object>|isA|<value>
# data[<object>][1][<value>]["v"] = <value> occurrenxe count
# data[<object>][1][<value>]["co"] = <object> and <value> co-occurrenxe count

import math
import re

def create_dataset(filename):
    # Add probability data
    data = {}
    vocabulary = set()
    f = open(filename)

    for i in f:
        i = i.strip()
        i_split = i.split("|")
        object = i_split[-1]
        value = i_split[2].split(" ")[0]
        probability = float(i_split[0].split(":")[0])
        if object not in data: data[object] = [0, {value: {"p":probability}}]
        elif value not in data[object][1]: data[object][1][value] = {"p":probability}
        else: data[object][1][value]["p"] = probability # = {value: {"p":probability}}
        vocabulary.add(object)
        vocabulary.add(value)

    f.close()


    # Add cooccurrence data
    f = open("wikicooccurrence/wikimatrixrelatedtop20000")
    wordcount = {}
    counter = 0
    for i in f:
        row = i.split(",")
        key = row[0]
        counter += 1

        temp = int(row[1])
        if temp != 0: wordcount[key] = math.log(temp)
        
        if key not in vocabulary: continue

        # print("Cooccurrence gathering progress: " + str(counter) + " | " + "20000", end="\r", flush=True)

        count = row[1]
        for j in range(2, len(row), 2):
            val = int(row[j+1])
            if math.log(val) == 0: continue
            if key not in data: continue
            if row[j] not in data[key][1]: continue
            data[key][1][row[j]]["co"] = val #math.log(val)
            # data[key][row[j]]["co"] = math.log(val)

            if row[j] not in data: continue
            if key not in data[row[j]][1]: continue
            data[row[j]][1][key]["co"] = val #math.log(val)

    f.close()


    # Add object and value counts
    f = open("wikicooccurrence/important_words.txt")

    total = 0
    for i in f:
        i = i.strip()
        i = re.sub(" +", " ", i)
        i_split = i.split(" ")
        word = i_split[0].lower()
        count = int(i_split[4])

        if word not in vocabulary: continue
        if word in data:
            data[word][0] += count
            # total += 1

        for object in data:
            if word not in data[object][1]: continue
            total += 1
            data[object][1][word]["v"] = count

    # print(total)

    f.close()


    # Count how many rules have all required data (probability, object count, value count, object - value co-occurrence)
    count = 0
    temp = []
    for i in data:
        if data[i][0] == 0: continue
        for j in data[i][1]:
            if len(data[i][1][j]) == 3:
                count += 1
    # print(count)



    # Gather all relavant data into separate lists, this makes calculating covariance easier
    probabilities = []
    object_counts = []
    value_counts = []
    co_occurrence_counts = []
    objects = []
    values = []
    indexer = 0
    for i in data:
        if data[i][0] == 0: continue
        
        for j in data[i][1]:
            if len(data[i][1][j]) == 3:
                object_counts.append(data[i][0])
                value_counts.append(data[i][1][j]["v"])
                co_occurrence_counts.append(data[i][1][j]["co"])
                probabilities.append(data[i][1][j]["p"])
                objects.append(i)
                values.append(j)

    # print("COUNTS:::::")

    print("object, value, confidence, cooccurrence, object_count, value_count")
    for i in range(len(probabilities)):
        row = objects[i] + ", " + values[i] + ", " + str(probabilities[i]) + ", " + str(co_occurrence_counts[i]) + ", " + str(object_counts[i]) + ", " + str(value_counts[i])
        print(row)


# create_dataset("singularized/flipped/100k_flipped.txt")
create_dataset("flipped.txt")