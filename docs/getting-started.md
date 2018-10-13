Getting started
===============

## Installation

You can install **ML Belt** using pip:

```
pip install ml_belt
```

## Preprocessing:

All you need to do is import [`Prep`](prep.html) class, create a new object passing a pandas DataFrame, so you can chain some steps of pre-processing that will be applied over the result of antecessor.

At the end your modified DataFrame will be in `data` attribute.


```python
from ml_belt.prep import Prep
import pandas as pd

def custom_fn(df):
    '''Do some modifications on df and return it.'''
    return df

# Prep needs a pandas dataframe
prep_df = Prep(pd.read_csv('data.csv')) \
    .drop_nulls(['col1', 'col2']) \
    .bool_to_int(['col3']) \
    .drop_cols(['nosense_col1', 'nosense_col2']) \
    .fill_null_with('mean', ['col_with_nulls', 'another_coll_with_nulls']) \
    .fill_null_with(-1, ['col_with_nulls2', 'col_with_nulls3']) \
    .apply_custom(custon_fn) \
    .drop_nulls()

# Now you have a modified df 
# with all steps above
df = prep_df.df
df.to_csv('data_prep.csv')
```