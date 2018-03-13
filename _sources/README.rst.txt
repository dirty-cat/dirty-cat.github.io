dirty_cat
=========

dirty_cat is a Python module for machine-learning on dirty categorical variables.


Installation
------------

Dependencies
~~~~~~~~~~~~

dirty_cat requires:

- Python (>= 2.7 or >= 3.4)
- NumPy (>= 1.8.2)
- SciPy (>= 0.13.3)
- scikit-learn ()


User installation
~~~~~~~~~~~~~~~~~

If you already have a working installation of NumPy and SciPy,
the easiest way to install dirty_cat is using ``pip`` ::

    pip install -U ...

Documentation
-------------

preprocessing.categorical_encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* One-hot encoding
* Ordinal encoding
* Similarity encoding:
    + levenshtein-ratio
    + jaro-winkler
    + ngram 
* Target encoding
* N-gram based encoders:
    + 'ngram-count',
    + 'ngram-presence',
    + 'ngram-tfidf'





Citation
~~~~~~~~

If you use this module in a scientific publication, please cite the following:
(coming soon :))
