"""Module for common preprocessing tasks."""
import time
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# TODO: acertar docustrings
# TODO: drop_by
# TODO: apply_custom_item_level (escolher axis)
class Prep(object):
    """Preprocessing / preparing data.

    Attributes:
        data (pandas DataFrame): dataframe with all transformations

    """

    def __init__(self, df: pd.DataFrame):
        """Create new object.
        
        Args:
            - df (DataFrame): a pandas dataframe to performs preprocessing tasks.
            Al tasks are performed on a copy of this DataFrame

        """
        self._data = df.copy()

    @property
    def df(self):
        """Get the actual version of modified df."""
        return self._data.copy()

    @df.setter
    def df(self, df):
        """Set a new dataframe to be modified."""
        self._data = df.copy()
        return self
        
    def apply_custom(self, fn, args={}):
        """Apply a custom function to the dataframe.
        
        Args:
            - fn: custom function to apply. Should receive the dataframe and returns the modified dataframe

        Returns:
            self

        """
        self._data = fn(self._data, **args)
        return self

    def drop_nulls(self, cols: list = None):
        """Drop all rows with nulls.

        Args:
            - cols (list): list of columns or None to all dataframe 

        Returns:
            self

        """
        if cols == None:
            self._data.dropna(inplace=True)
        else:
            cols = [c for c in cols if c in self._data.columns]
            self._data.dropna(subset=cols, inplace=True)
        return self

    def drop_not_nulls(self, cols: list):
        """Drop all rows with not null values for each column in cols.

        Args:
            - cols (list): list of columns
        
        Returns:
            self

        """
        cols = [c for c in cols if c in self._data.columns]
        for col in cols:
            self._data = self._data[self._data[col].isnull()]
        return self

    def drop_cols(self, cols: list):
        """Drop all listed columns.

        Args:
            - cols (list): list of cols to drop

        Returns:
            self

        """
        cols = [c for c in cols if c in self._data.columns]
        for col in cols:
            self._data.drop(col, axis=1, inplace=True)
        return self

    def bool_to_int(self, cols: list):
        """Transform bool into 1 and 0.
        
        Args:
            - cols (list): list of cols to transform

        Returns:
            Self

        """
        if cols == None:
            self._data.applymap(lambda x: 1 if x else 0)
        else:
            cols = [c for c in cols if c in self._data.columns]
            for col in cols:
                self._data[col] = self._data[col].apply(lambda x: 1 if x else 0)
        return self

    # TODO: Salvar label encoder em pickle
    def encode(self, cols: list):
        """Encode categorical vars into numeric ones.

        Args:
            - cols (list): list of columns to encode

        Returns:
            Self

        """
        l_e = LabelEncoder()
        cols = [c for c in cols if c in self._data.columns]
        for col in cols:
            self._data[col].fillna('N/A-ENC', inplace=True)
            self._data[col] = l_e.fit_transform(self._data[col])
        return self

    def fill_null_with(self, val, cols=None):
        """Fill all null with a same value.

        Args:
            - val: can be `mean` to replace null with the mean of the columns
            or any value to put in place of nulls.
            - cols (list): list of columns or None to all dataframe 

        Returns:
            self

        """
        if cols == None:
            self._data.fillna(val, inplace=True)
        else:
            cols = [c for c in cols if c in self._data.columns]
            if isinstance(val, str):
                if val == 'mean':
                    for col in cols:
                        self._data[col].fillna((self._data[col].mean()),
                                            inplace=True)
                else:
                    for col in cols:
                        self._data[col].fillna(val, inplace=True)
            else:
                for col in cols:
                    self._data[col].fillna(val, inplace=True)

        return self

    def dummify(self, columns: list, drop_first: bool = True):
        """Create dummies for selected columns

        Args:
            columns (list): list of columns to dummify
            drop_first (bool, optional): select if the first class will be dropped. Defaults to True

        Returns:
            pd.DataFrame
        """
        for col in columns:
            dummy = pd.get_dummies(self._data[col], drop_first=drop_first)
            self._data = pd.concat([self._data, dummy], axis=1)

        self._data.drop(columns, axis=1, inplace=True)
        return self

    def col_2_time(self, columns: list):
        """Summary

        Args:
            columns (list): Description

        Returns:
            pd.DataFrame: Description
        """
        for column in columns:
            self._data[column] = pd.to_datetime(self._data[column])
        return self

    def time_2_float(self, columns: list):
        """Summary

        Args:
            columns (list): Description

        Returns:
            pd.DataFrame: Description
        """
        for column in columns:
            self._data[column] = self._data[column].apply(
                lambda x: time.mktime(x.timetuple()))
        return self


# TODO:
# unit test: testar se modifica o dataframe original nos metodos acima,
# ou seja, criar assert para verificar se os objetos são diferentes mesmo com o mesmo valor

# Separar colunas numericas de colunas categóricas (describe separa colunas numéricas)
# aplicar por padrão a função dummify na lista de colunas categóricas
# aplicar por padrão a função scale nas colunas numéricas
# criar properties pra isso ???

# cria coluna baseado em calculo de outras ???

# preencher null com média de outras colunas
