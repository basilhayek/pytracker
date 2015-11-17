# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 14:57:27 2015

@author: bhayek
"""

import pandas as pd

PARETO = 0.8


def get_pareto(df_in, value_column):
    df = df_in.copy()
    df = add_pareto(df, value_column)
    df = df[df['pareto'] == 1]
    return df


def add_pareto(df, value_column):
    # Sort the dataframe, and create a new index for access
    df = df.sort(columns=value_column, ascending=False).reset_index()

    total = df[value_column].sum()
    df['cum_sum'] = df[value_column].cumsum()
    df['cum_perc'] = df.cum_sum / total

    # Mark the columns that get us to to 80% of time spent that has been
    # tracked
    df['pareto'] = 1 * (df['cum_perc'] <= PARETO)

    # Mark the rows at the boundary
    df_less = df['cum_perc'] <= PARETO
    df_more = df['cum_perc'] >= PARETO

    # It's possible that no rows are below the Pareto threshold (first item
    # becomes the Pareto set)
    if df_less.sum() == 0:
        df.loc[0, ('pareto')] = 1
    else:
        idx_less = df.ix[df_less, 'cum_perc'].idxmax()
        idx_more = df.ix[df_more, 'cum_perc'].idxmin()
        df.ix[idx_less:idx_more, 'pareto'] = 1

    # Return to original sort order
    df = df.set_index('index')
    df = df.sort()

    return df


def test():
    df = pd.DataFrame.from_items([('label', ['a', 'b', 'c', 'd', 'e']),
                                  ('value', [2, 2, 2, 3, 2])])
    print add_pareto(df, 'value')
#    print get_pareto(df, 'value')


if __name__ == '__main__':
    test()
