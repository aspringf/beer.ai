""" Clean recipe quantities
This script cleans the quantitative features of a homebrew recipe DataFrame:
* Recipe features (eg. efficiency, boil size, batch size)
* Ingredient features (eg. ferm quantity, hop quantity)

It loads an HDFStore file containing a DataFrame of recipes.
It saves a second HDFStore file with _cleaned_qty appended to the name.
"""

import argparse
import pandas as pd

# List of columns with quantities to clean
COLS_QTY_CORE = ['batch_size', 'boil_size', 'boil_time', 'efficiency']
COLS_QTY_INGRED = ['ferm_amount', 'ferm_color', 'ferm_yield', 
'hop_amount', 'hop_alpha', 'hop_time',
'yeast_amount', 'yeast_attenuation',
'misc_time']
COLS_LOAD = {'core': COLS_QTY_CORE, 'ingredients': COLS_QTY_INGRED}

def load_df(hdf_key):
    """ (str) -> DataFrame
    Load the recipe DataFrame from the HDF."""
    if hdf_key not in COLS_LOAD:
        print('This key is not HDF. Options: {}'.format(COLS_LOAD.keys()))
        return 
    
    with pd.HDFStore(args.filename, "r") as store:
        df = store.select(hdf_key, columns=COLS_LOAD[hdf_key], where='index<{}'.format(args.num_recipes))
        
    print('Loaded {} DataFrame: {} rows.'.format(hdf_key, df.shape[0]))
    return df     
    
def make_arg_parser():
    """Create and return argument parser."""

    parser = argparse.ArgumentParser(
        description="Script to run through beer data and map differently spelled "
            "or referenced ingredients to a standard name."
    )

    parser.add_argument(
        "-f",
        "--filename",
        default="all_recipes.h5",
        help="path of HDF file containing ingredients. Default is "
            "'all_recipes.h5' in current directory."
    )
    
    parser.add_argument(
        "-n",
        "--num_recipes",
        type=int,
        default=1000,
        help="The number of recipes to clean."
    )


    return parser


if __name__ == "__main__":
    parser = make_arg_parser()
    args = parser.parse_args()
    
    # Load HDF to clean
    df_core = load_df('core')
    df_ing = load_df('ingredients')
    
    # Make changes, column by column
    #   First: efficiency
    
    # Write changes
    #   Write DF as new HDFStore
    

