"""Summary
"""
import pandas as pd
import seaborn as sb


class Plot(object):

    """Summary

    Attributes:
        data (TYPE): Description
    """

    def __init__(self, df: pd.DataFrame):
        """Summary

        Args:
            df (pd.DataFrame): Description
        """
        self.data = df

    def bar_sum(self, col, pallete: str = 'hls'):
        """Summary

        Args:
            col (TYPE): Description
            pallete (str, optional): Description
        """
        sb.countplot(x=col, data=self.data, palette=pallete)

    def box(self, col_x, col_y, pallete: str = 'hls'):
        """Summary

        Args:
            col_x (TYPE): Description
            col_y (TYPE): Description
            pallete (str, optional): Description
        """
        sb.boxplot(x=col_x, y=col_y, data=self.data, palette=pallete)

    def independency(self):
        """Summary
        """
        sb.heatmap(self.data.corr())
