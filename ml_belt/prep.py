"""Module for common preprocessing tasks."""
import time
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# TODO: acertar docustrings
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
        self.data = df.copy()

    # TODO: organizar a exibição / docstring
    def info(self):
        """Summary
        """
        # Configura para exibir a quantidade de nulls em um dataset grande
        # utilizando a função .info())
        print(self.data.set_option('max_info_rows', self.data.shape[0] + 1))
        print('Shape:')
        print(self.data.shape, '\n')
        print('Info:')
        print(self.data.info())
        print('Shape:')
        print(self.data.describe())
        print('Head ... Tail:')
        print(self.data.head())
        print(self.data.tail())
        print('Columns:')
        print(self.data.columns)
        print('Null count:')
        print(self.data.isnull().sum())
        return self

    def apply_custom(self, fn, filtered: False):
        """Apply a custom function to the dataframe.
        
        Args:
            - fn: custom function to apply. Should receive the dataframe and returns the modified dataframe

        Returns:
            self

        """
        self.data = fn(self.data)
        return self

    def drop_nulls(self, cols: list = None):
        """Drop all rows with nulls.

        Args:
            - cols (list): list of columns or None to all dataframe 

        Returns:
            self

        """
        if cols == None:
            self.data.dropna(inplace=True)
        else:
            cols = [c for c in cols if c in self.data.columns]
            self.data.dropna(subset=cols, inplace=True)
        return self

    def drop_not_nulls(self, cols: list):
        """Drop all rows with not null values for each column in cols.

        Args:
            - cols (list): list of columns
        
        Returns:
            self

        """
        cols = [c for c in cols if c in self.data.columns]
        for col in cols:
            self.data = self.data[self.data[col].isnull()]
        return self

    def drop_cols(self, cols: list):
        """Drop all listed columns.

        Args:
            - cols (list): list of cols to drop

        Returns:
            self

        """
        cols = [c for c in cols if c in self.data.columns]
        for col in cols:
            self.data.drop(col, axis=1, inplace=True)
        return self

    def bool_to_int(self, cols: list):
        """Transform bool into 1 and 0.
        
        Args:
            - cols (list): list of cols to transform

        Returns:
            Self

        """
        if cols == None:
            self.data.applymap(lambda x: 1 if x else 0)
        else:
            cols = [c for c in cols if c in self.data.columns]
            for col in cols:
                self.data[col] = self.data[col].apply(lambda x: 1 if x else 0)
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
        cols = [c for c in cols if c in self.data.columns]
        for col in cols:
            self.data[col].fillna('N/A-ENC', inplace=True)
            self.data[col] = l_e.fit_transform(self.data[col])
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
            self.data.fillna(val, inplace=True)
        else:
            cols = [c for c in cols if c in self.data.columns]
            if isinstance(val, str):
                if val == 'mean':
                    for col in cols:
                        self.data[col].fillna((self.data[col].mean()),
                                            inplace=True)
                else:
                    for col in cols:
                        self.data[col].fillna(val, inplace=True)
            else:
                for col in cols:
                    self.data[col].fillna(val, inplace=True)

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
            dummy = pd.get_dummies(self.data[col], drop_first=drop_first)
            self.data = pd.concat([self.data, dummy], axis=1)

        self.data.drop(columns, axis=1, inplace=True)
        return self

    def col_2_time(self, columns: list):
        """Summary

        Args:
            columns (list): Description

        Returns:
            pd.DataFrame: Description
        """
        for column in columns:
            self.data[column] = pd.to_datetime(self.data[column])
        return self

    def time_2_float(self, columns: list):
        """Summary

        Args:
            columns (list): Description

        Returns:
            pd.DataFrame: Description
        """
        for column in columns:
            self.data[column] = self.data[column].apply(
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
