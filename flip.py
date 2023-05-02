from collections import defaultdict


def def_value():
    return 0

def lst():
    return defaultdict(def_value)


def flip(fileName):
      
    tails = defaultdict(def_value) # Mitu korda saba element andmestikus esineb

    counts = defaultdict(lst) # Iga saba elemendi kohta: mitu korda on mingi pea antud sabaga seostatud
    
    f = open(fileName)

    kolmik = []
    try:
        for i in f:
            kolmik = i.strip("\n").split("|")
            tails[kolmik[2]] += 1
            counts[kolmik[2]][kolmik[0]] += 1
    except:
        print("ERROR")
        print("Err, while processing: " + str(kolmik))
    
    # print(counts)

    f.close()

    f = open(fileName)

    kolmik = []
    error_index = 0
    try:
        for i in f:
            error_index += 1
            kolmik = i.strip("\n").split("|")
            
            # antud pea sabaga seostamiste arv andmestikus / saba esinemiste arv andmestikus
            probability = counts[kolmik[2]][kolmik[0]] / tails[kolmik[2]]
            print(str(probability) + ": X|" + kolmik[1] + "|" + kolmik[2] + " => X|isA|" + kolmik[0])

        f.close()
    except:
        print("ERROR")
        print("Err, while handling: " + str(kolmik) + " index: " + str(error_index) + " / " + str(error_index * 2))

# flip("converted/wheels_n_wings.txt")
# flip("converted/50k.txt")
# flip("converted/vehicles.txt")

# flip("singularized/50k.txt")
# flip("singularized/vehicles.txt")
# flip("singularized/wheels_n_wings.txt")

# flip("singularized/100k.txt")
flip("singulars.txt")