from pattern.text.en import singularize
from nltk.stem.porter import *
from nltk.stem.wordnet import WordNetLemmatizer


def singularize_object(files):

    stemmer = PorterStemmer()
    
    for filename in files:
        f = open(filename)

        for i in f:
            kolmik = i.split("|")
            # singular = stemmer.stem(kolmik[0].strip("\n"))
            singular_object = singularize(kolmik[0].strip("\n"))
            singular_object = WordNetLemmatizer().lemmatize(singular_object)
            # singular_object = kolmik[0].strip("\n")

            singular_value = singularize(kolmik[2].strip("\n"))
            singular_value = WordNetLemmatizer().lemmatize(singular_value)
            # singular_value = kolmik[2].strip("\n")
            print(singular_object + "|" + kolmik[1] + "|" + singular_value)
        
        f.close()     


# singularize_object(["converted/50k.txt", "converted/q50k.txt"])
# singularize_object("converted/vehicles.txt")
# singularize_object("converted/wheels_n_wings.txt")
singularize_object(["rules.txt", "rules2.txt"])
