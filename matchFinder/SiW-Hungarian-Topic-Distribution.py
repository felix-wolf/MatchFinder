#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import logging
import numpy as np
import pandas as pd
import scipy.optimize
import argparse

#########################################################################
#########################################################################
#########################################################################
# User defined settings

parser = argparse.ArgumentParser(description='Perform assignement optimisation')
parser.add_argument("input", type=Path, default=Path("poll.csv"), help="Input csv exported from bitpoll")
parser.add_argument("--assignment-limit", "--l", type=int, default=1, help="How many people may be accepted simultaneously?")
parser.add_argument("--number-choices", "--c", type=int, default=3, help="How many choices does each person have?")
parser.add_argument("--allow-na", "--n", action='store_true', help="Set true, if not every topic must get an assignment (assignments are then set to np.infty by default)")

args = parser.parse_args()
#args = parser.parse_args("test_poll.csv --assignment-limit 10 --number-choices 4".split())

# path to csv exported from bitpoll
input_file = args.input
# how often may a person be assigned to a topic (use assignment_limit = 1 for a 1:1 assignment)
assignment_limit = args.assignment_limit
# how many choices does each student have (bitpoll schema should comply to Stimme-x)
number_of_choices = args.number_choices
# set na values to infty, so that they get least priority my hungarian method
na_value = np.infty
# set true, if not each "topic" needs to be selected or decided. If false and if a student does not apply number_of_choices many choices, they are dropped
allow_na = args.allow_na


#########################################################################
#########################################################################
#########################################################################
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)
_logger.info("Process input file {}".format(input_file))

# read data
assert input_file.exists()
df=pd.read_csv(str(input_file))

#########################################################################
#########################################################################
#########################################################################

# cleanse data and perform sanity checks
# 1 column with name, check if no na there if not allowed
if allow_na:
    expected_na_cardinality = len(df.columns) - 1 - number_of_choices
else:
    expected_na_cardinality = 0

assert number_of_choices < na_value

# check if each name is an unique identifier
df_duplicates = df[df.duplicated(subset=["Name"], keep='last')]
if not df_duplicates.empty:
    _logger.warning("Found duplicates:\n{}\nOnly last entry will be processed\n".format(df_duplicates["Name"]))
    df.drop_duplicates(subset=["Name"], keep='last', inplace=True, ignore_index=True)

# check if each choice is unique (e.g. not more than one Stimme-1)
to_be_dropped = []
for i in range(len(df)):
    if not df.loc[i].is_unique:
        #_logger.error("Selection of user {} is invalid, dropping row (each selection may only be used once)".format(df.loc[i]["Name"]))
        to_be_dropped.append(i)
#df.drop(to_be_dropped, inplace=True)

na_cardinality = df.isna().sum(axis=1)
for name in df[na_cardinality != expected_na_cardinality]["Name"]:
    pass
    #_logger.error("Selection of user {} is invalid, dropping row (expected na: {}, found na: {})".format(name, expected_na_cardinality, na_cardinality))
#df=df[na_cardinality == expected_na_cardinality]


# In[ ]:


#df.replace([np.NAN, "Drittwahl", "Zweitwahl", "Erstwahl"],[100, 3, 2, 1], inplace=True)
df.replace([np.NAN, "Sechstwahl", "Fünftwahl", "Viertwahl", "Drittwahl", "Zweitwahl", "Erstwahl"],[na_value, 6, 5, 4, 3, 2, 1], inplace=True)
weights = ["Stimme-" + str(i) for i in range(1, number_of_choices + 1)] + [np.NAN]
replacement = list(range(1, number_of_choices + 1)) + [na_value]
#df.replace(stimmen, replacement)

# adjust input according to global limit
# if multiple people may be assigned the same topic, this can be handled by duplicating those topics
repeated_df = np.repeat(df.iloc[:,1:].to_numpy(), assignment_limit, axis=1)
repeated_columns = np.repeat(df.columns[1:].to_numpy(), assignment_limit)


# In[ ]:


# Perform hungarian method to get optimum fit
row_ind, col_ind = scipy.optimize.linear_sum_assignment(repeated_df)
names = df["Name"].reset_index(drop=True)
topics = pd.DataFrame(repeated_columns[col_ind])
choices = pd.DataFrame(repeated_df[row_ind,col_ind])

output = pd.concat([names, choices, topics],axis=1)
output.columns=["Name","Weight","Selection"]

# Visualise topic distribution
_logger.info(output)
for choice_weight in range(1, number_of_choices + 1):
    _logger.info("Assigned choice {}: \t{}".format(choice_weight, np.sum(output["Weight"] == choice_weight)))
_logger.info("Nat 1 auf luck-check : \t{}".format(np.sum(output["Weight"] == na_value)))

