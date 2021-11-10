"""
This file contains all the helper functions that is used across the app
"""

import pandas
import streamlit as st
import pandas_profiling

from streamlit_pandas_profiling import st_profile_report


def assertType(default, test, conditions=None):
    if isinstance(test, default):
        if conditions is not None:
            if test in conditions:
                return True
            else:
                raise AssertionError(f'{test} is not one of the accepted parameter {conditions}')
        else:
            return True
    else:
        raise AssertionError(f'{type(test)} is not the same as {type(default)}. Try again.')


def printDataFrame(data: pandas.DataFrame, verbose_level: int, advanced: bool,
                   extract_from: str or None = None):
    """
    Takes in a Pandas DataFrame and prints out the DataFrame in Streamlit

    Parameter
    ----------
    data:                               Pandas DataFrame or Series object
    extract_from:                       Name of column to extract data from
    verbose_level:                      The number of rows of data to display
    advanced:                           Conduct Advanced Analysis on the DataFrame
    dtm:                                Special processing for DTMs
    ----------
    """

    if verbose_level != 0:
        try:
            if extract_from is not None:
                st.dataframe(data[[extract_from]].head(verbose_level), height=600, width=800)
            else:
                st.dataframe(data.head(verbose_level), height=600, width=800)
        except RuntimeError:
            st.warning('Warning: Size of DataFrame is too large. Defaulting to 10 data points...')
            st.dataframe(data.head(10), height=600, width=800)
        except KeyError:
            st.error(f'Error: DataFrame Column with value {extract_from} does not exist. Try again.')
        except Exception as ex:
            st.error(f'Error: {ex}')
        else:
            if advanced:
                if extract_from is not None:
                    with st.expander('Advanced Profile Report'):
                        st_profile_report(data[[extract_from]].profile_report(
                            explorative=True,
                            minimal=True))
                else:
                    with st.expander('Advanced Profile Report'):
                        st_profile_report(data.profile_report(
                            explorative=True,
                            minimal=True))
    else:
        try:
            if extract_from is not None:
                st.dataframe(data[[extract_from]], height=600, width=800)
            else:
                st.dataframe(data, height=600, width=800)
        except RuntimeError:
            st.warning('Warning: Size of DataFrame is too large. Defaulting to 10 data points...')
            st.dataframe(data.head(10), height=600, width=800)
        except KeyError:
            st.error(f'Error: DataFrame Column with value {extract_from} does not exist. Try again.')
        except Exception as ex:
            st.error(f'Error: {ex}')
        else:
            if advanced:
                if extract_from is not None:
                    with st.expander('Advanced Profile Report'):
                        st_profile_report(data[[extract_from]].profile_report(
                            explorative=True,
                            minimal=True))
                else:
                    with st.expander('Advanced Profile Report'):
                        st_profile_report(data.profile_report(
                            explorative=True,
                            minimal=True))
