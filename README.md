# Probabilistic-classification-knowledge-base

Code used for generating the probabilistic classification knowledge base

In order to generate new probabilistic classification rules, run the programs in the order in which they are listed below.

## 1. Gathering data

In order to extract rules from another knowledge base, run the *convertFrom* function within the **convert.py** script.
This function takes in 4 arguments.
1. Name of the knowledge base file, from which suitable rules will be extracted
2. *keyes*= list of keyewords, used to extract rules related to scelected topics (leave this list empty, to extract all suitable rules)
3. *whitelist*= list of whitelisted strings used for detecting suitable rules, rules not containing a string from this list are excluded from further processing
4. *blackilst*= any rule which contains a string in this list will be excluded from the result

Change the values of these arguments in order to extract the rules you find useful.
Once you are satisfied with the results of this step, pipe the result to a text file, using the following command *convert.py > rules.txt*

## 2. Singularizing and combining data

In order to increase the plausibility of the confidences calculated in later steps, run the *singularize_object* function within the **singularize.py** script.
The input of this function is a list of file names. add the names of the files created in the previous step into this list and run the code in order to lemmatize and singularize the *object* and *value* words within the rules extracted in the previous step. Similarly to the previous step, pipe the result into a new file like so: *singularize.py > singulars.txt*

## 3. Fliping the singularized rules

In order to convert the singularized rules into probabilistic classification rules, run the function *flip* within the **flip.py** script.
as its input it takes the name of the file which contains the singularized rules. Similarly to previous steps again, provide the function with the correct arguments and pipe the results into a new file like so: *flip.py > flipped.txt*

## 4. Extract co-occurrence and word importance data

In this step a dataset containing the confidences created in the previous step, as well as co-occurrence data from Wikipedia and word importances are created.
This data will later be used for pca and calculating improved confidences.

Simply run the *create_dataset* function within the **flipped_to_dataset.py** script with the name of the file created in the previous step. pipe the result into a new file, *flipped_to_dataset.py > data.txt*

## 5. PCA

**This step is optional**

In this step principal component analysis is performed, run the *pca* function within the **pca.py** script.

## 6. Improving confidences

Within the **formula_validation.py** script, change the arguments of the *read_data* function to reflect the name of the file created in the fourth step.

Then change the first argument of the *ajust_confidence* function to the file name of the flipped rules, created in the third step, and the second argument of this function to the file name of the new knowledge base that will be created as a result of running this function.

The *read_data* function gathers the necessary data for calculating new confidences.
The *ajust_confidence* function uses the gathered data to calculate new confidences, evaluates the result and writes the rules with new confidences to a file.

Within *ajust_confidence*, define a new function, *apply_data* this function defines the formula used to calculate the new confidences.

There are two methods for applying formulas to the data, so two ways to define the *apply_data* function

1. def apply_data(data, index, c, co, o, v) return data[0][index] * c
2. def apply_data(data, index): return data[0][index]

The first method can be applied as follows: *calc_rec(test_set, apply_data)*. The *calc_rec* function recursively modifies the variables *c, co, o, v* to apply multiplyers to the data.

The second method can be applied as follows: *calc_static(test_set, apply_data)* here the weights can be applied manually, and the formula is applied only once.

In order to speed up processing time, the *write_to_file* argument of the *ajust_confidences* function can be set to False. This will prevent the program from writing the rules to a file, reducing the time required to run the program.
