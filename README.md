# Probabilistic-classification-knowledge-base

This repository contains the code and datasets used for the thesis **Creating probabilistic classification rules from existing knowledge bases**. The probabilistic classification knowledge base assessed in the thesis is available in the file **flipped_adjustedd.txt**

The rules within this knowledge base contain probabilistic classification rules in the following form.

    0.0:  X|property|value => X|isA|object

The number preceeding the rules is the supposability value used for comparing the plausibilities of similar rules.

# Clone code and data, using git Large File Storage (lfs)

**Install git lfs and use the following command to clone the repository.**

    git lfs clone git@github.com:RenetRamman/Probabilistic-classification-knowledge-base.git ramman/

**Move to the cloned directory.**

    cd ramman
 

**install required packages, if not already installed**

libmysqlclient-dev is a dependency for pattern

    pip3 install numpy
    sudo apt-get install libmysqlclient-dev
    pip3 install pattern 


# Use

This repository contains all of the datasets and scripts required to create the rules that were assessed within the thesis. The **flipped_adjusted.txt** knowledge base of probabilistic classification rules can be created from the start by executing the fllowing commands within the cloned repository in the order in which they are listed below.

    python ./convert.py cnet_50k.js -b "// class element" --whitelist "// " > rules.txt
    python ./convert.py quasi_50k.js -b "// class element" --whitelist "// " > rules2.txt
    python ./singularize.py rules.txt rules2.txt > singulars.txt
    python ./flip.py singulars.txt > flipped.txt
    python ./flipped_to_dataset.py flipped.txt > data.txt
    python ./calculate_supposability.py flipped.txt -d data.txt -v > flipped_adjusted.txt



## Short explanation of the code
### 1. Gathering data

In order to extract rules from another knowledge base, **convert.py** script.
This function takes in 3 arguments.
1. Name of the knowledge base file, from which suitable rules will be extracted
2. *whitelist*= list of whitelisted strings used for detecting suitable rules, rules not containing a string from this list are excluded from further processing
3. *blackilst*= any rule which contains a string in this list will be excluded from the result

Change the values of these arguments in order to extract the rules you find useful.
Once you are satisfied with the results of this step, pipe the result to a text file, using the following command

    python ./convert.py cnet_50k.js -b "// class element" --whitelist "// " > rules.txt
    python ./convert.py quasi_50k.js -b "// class element" --whitelist "// " > rules2.txt

### 2. Singularizing and combining data

In order to increase the plausibility of the supposability values calculated in later steps, run the **singularize.py** script.
The input of this function is a list of file names. add the names of the files created in the previous step into this list and run the code in order to lemmatize and singularize the *object* and *value* words within the rules extracted in the previous step. Similarly to the previous step, pipe the result into a new file

    python ./singularize.py rules.txt rules2.txt > singulars.txt

### 3. Fliping the singularized rules

In order to convert the singularized rules into probabilistic classification rules, run the **flip.py** script.
as its input it takes the name of the file which contains the singularized rules. Similarly to previous steps again, provide the function with the correct arguments and pipe the results into a new file

    python ./flip.py singulars.txt > flipped.txt

### 4. Extract co-occurrence and word importance data

In this step a dataset containing the supposability values created in the previous step, as well as co-occurrence data from wikimatrixrelatedtop20000 and word importances from importantwords.txt is created.
This data will later be used for pincipal component analysis (pca) and for calculating improved supposability values.

Simply run the **flipped_to_dataset.py** script with the name of the file created in the previous step. pipe the result into a new file, 

    python ./flipped_to_dataset.py flipped.txt > data.txt

### 5. PCA

**This step is optional**

In this step principal component analysis is performed.


### 6. Improving confidences

Calculate more plausible supposability values for the probabilistic classification rules created in step 3 by running the **calculate_supposability.py** script.

The *read_data* function gathers the necessary data for calculating new confidences.
The *ajust_confidence* function uses the gathered data to calculate new confidences, evaluates the result and writes the rules with new confidences to a file.

Within *ajust_confidence*, by modifying the function, *apply_data* the formula used for calculating supposability values can be changed.

There are two methods for applying formulas to the data, so two ways to define the *apply_data* function

1. def apply_data(data, index, c, co, o, v) return data[0][index] * c
2. def apply_data(data, index): return data[0][index]

The first method can be applied as follows: *calc_rec(test_set, apply_data)*. The *calc_rec* function recursively modifies the variables *c, co, o, v* to apply multiplyers to the data.

The second method can be applied as follows: *calc_static(test_set, apply_data)* here the weights can be applied manually, and the formula is applied only once, thus reducing the programs excecution time.

The **-verboose** argument. If this argument is provided when running the **calculate_supposability.py** script, the calculated supposability values are added to the probabilistic classification rules and printed ot the output. If this argument is not provided, only the ISC similarity to the validation data from double_words.csv dataset will be printed to reduce the programs excecution time.

Run the following command

    python ./calculate_supposability.py flipped.txt -d data.txt -v > flipped_adjusted.txt

## References

**double_words.csv**

Download link: https://wordnorms.com/

**cnet_50k.js**

Download link: http://turing.cs.ttu.ee/~Tanel.Tammet/cnet_50k.js

**quasi_50k.js**

Download link: http://turing.cs.ttu.ee/~Tanel.Tammet/quasi_50k.js

**wikimatrixrelatedtop20000 and importantwords.txt**

Download link:    http://turing.cs.ttu.ee/~Tanel.Tammet/wikicooccurrence.tar.gz
