"""
Predicting the salary of employees
==================================

The `employee salaries <https://catalog.data.gov/dataset/employee-salaries-2016>`_
dataset contains information
about annual salaries (year 2016) for more than 9,000 employees of the 
Montgomery County (Maryland, US). In this example, we are interested
in predicting the column *Current Annual Salary*
depending on a mix of clean columns and a dirty column.
We choose to benchmark different categorical encodings for
the dirty column *Employee Position Title*, that contains
dirty categorical data.

"""

################################################################################
# Data Importing and preprocessing
# --------------------------------
#
# We first download the dataset:
from dirty_cat.datasets import fetch_employee_salaries
employee_salaries = fetch_employee_salaries()
print(employee_salaries['DESCR'])


################################################################################
# Then we load it:
import pandas as pd
df = employee_salaries['data']

################################################################################
# Now, let's carry out some basic preprocessing:
df['Date First Hired'] = pd.to_datetime(df['date_first_hired'])
df['Year First Hired'] = df['Date First Hired'].apply(lambda x: x.year)
# drop rows with NaN in gender
df.dropna(subset=['gender'], inplace=True)

target_column = 'Current Annual Salary'
y = df[target_column].values.ravel()

#########################################################################
# Choosing columns
# -----------------
# For categorical columns that are supposed to be clean, it is "safe" to
# use one hot encoding to transform them:

clean_columns = {
    'gender': 'one-hot',
    'department_name': 'one-hot',
    'assignment_category': 'one-hot',
    'Year First Hired': 'numerical'}

#########################################################################
# We then choose the categorical encoding methods we want to benchmark
# and the dirty categorical variable:

encoding_methods = ['one-hot', 'target', 'similarity', 'minhash']
dirty_column = 'employee_position_title'
#########################################################################


#########################################################################
# Creating a learning pipeline
# ----------------------------
# The encoders for both clean and dirty data are first imported:

from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OneHotEncoder
from dirty_cat import SimilarityEncoder, TargetEncoder, MinHashEncoder

encoders_dict = {
    'one-hot': OneHotEncoder(handle_unknown='ignore', sparse=False),
    'similarity': SimilarityEncoder(similarity='ngram'),
    'target': TargetEncoder(handle_unknown='ignore'),
    'minhash': MinHashEncoder(n_components=10, ngram_range=(2, 4),
                              hashing='fast', minmax_hash=False),
    'numerical': FunctionTransformer(None)}

# We then create a function that takes one key of our ``encoders_dict``,
# returns a pipeline object with the associated encoder,
# as well as a Scaler and a RidgeCV regressor:

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def make_pipeline(encoding_method):
    # static transformers from the other columns
    transformers = [(enc + '_' + col, encoders_dict[enc], [col])
                    for col, enc in clean_columns.items()]
    # adding the encoded column
    transformers += [(encoding_method, encoders_dict[encoding_method],
                      [dirty_column])]
    pipeline = Pipeline([
        # Use ColumnTransformer to combine the features
        ('union', ColumnTransformer(
            transformers=transformers,
            remainder='drop')),
        ('scaler', StandardScaler(with_mean=False)),
        ('clf', RidgeCV())
    ])
    return pipeline


#########################################################################
# Fitting each encoding methods with a RidgeCV
# --------------------------------------------
# Eventually, we loop over the different encoding methods,
# instantiate each time a new pipeline, fit it
# and store the returned cross-validation score:
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold, cross_val_score
import numpy as np

all_scores = dict()

cv = KFold(n_splits=5, random_state=12, shuffle=True)
scoring = 'r2'
for method in encoding_methods:
    pipeline = make_pipeline(method)
    scores = cross_val_score(pipeline, df, y, cv=cv, scoring=scoring)
    print('{} encoding'.format(method))
    print('{} score:  mean: {:.3f}; std: {:.3f}\n'.format(
        scoring, np.mean(scores), np.std(scores)))
    all_scores[method] = scores

#########################################################################
# Plotting the results
# --------------------
# Finally, we plot the scores on a boxplot:
# We notice that the MinHashEncoder performs poorly compared to other encoding
# methods. There are two reasons for that: the MinHashEncoder performs better
# with tree-based models than linear models (see example 03), and the
# low-dimensionality of encodings (increasing n_components improves
# performances.

import seaborn
import matplotlib.pyplot as plt
plt.figure(figsize=(4, 3))
ax = seaborn.boxplot(data=pd.DataFrame(all_scores), orient='h')
plt.ylabel('Encoding', size=20)
plt.xlabel('Prediction accuracy     ', size=20)
plt.yticks(size=20)
plt.tight_layout()



