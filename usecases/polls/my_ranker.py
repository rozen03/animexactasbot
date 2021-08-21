import numpy as np
import pandas as pd
import scipy as sp
from rankit import Ranker
from rankit.Ranker.matrix_build import fast_colley_build


class MyColleyRanker(Ranker.ColleyRanker):
    def rank(self, table):
        """Calculate the rank and rating with specified parameters.

        this subclass fixes some shitty bug i don't want to overthink

        Parameters
        ----------
        table: Table
            The record table to be ranked, should be a Table object.

        Returns
        -------
        pandas.DataFrame, with column ['name', 'rating', 'rank']
        """
        drawMargin = self.drawMargin
        data = table.table[['hidx', 'vidx', 'hscore', 'vscore', 'weight']]

        idx = data.iloc[:, :2]
        score = data.iloc[:, 2:]
        C, b = fast_colley_build(np.require(idx, dtype=np.int32), np.require(score, dtype=np.float64),
                                 table.itemnum, drawMargin)

        rating = sp.linalg.solve(C, b)
        self.rating = pd.DataFrame({
                "iidx": np.arange(table.itemnum, dtype=np.int),
                "rating": rating})

        return self._showcase(table, False)
