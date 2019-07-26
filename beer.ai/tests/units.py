"""Identify if columns of data in the recipes are within expected ranges."""

import argparse
import pandas as pd

function_map = {}

def register(s):
    """Register a function based on its decorator as a state function or a regular function"""
    def inner(f):
        function_map[s] = f
        return f
    return inner


@register("efficiency")
def efficiency(core, ing):
    """Check if efficiency exists and is between 0 and 1"""
    print("Efficiency exists?")
    n_na = core["efficiency"].isna().sum()
    n_exist = len(core) - n_na
    print(f"----{n_exist} exist, {n_na} NaNs.")
    print("Efficiency between 0-1?")
    col = core["efficiency"].dropna()
    n_good = ((col <= 1)&(col > 0)).sum()
    n_bad = ((col > 1)|(col <= 0)).sum()
    print(f"----{n_good} good, {n_bad} out of range.")


@register("boilbatch")
def boil_batch(core, ing):
    """Check which recipes have neither of boil/batch size, or have both <= 0."""
    print("Boil/batch exist?")
    one_exists = (~core["boil_size"].isna() & ~core["batch_size"].isna()).sum()
    neither_exists = len(core) - one_exists
    print(f"----{one_exists} has at least one, {neither_exists} has neither.")
    bad_values = ((core["boil_size"] <= 0) & (core["batch_size"] <= 0)).sum()
    print(f"----{bad_values} have batch/boil <= 0.")


def main(functions=[]):

    if functions == []:
        functions = function_map.values()

    with pd.HDFStore("../all_recipes.h5","r") as store:
        core = store.select("core", where="index < 1000")
        ing = store.select("ingredients", where="index < 1000")

    for func in functions:
        func(core, ing)


def make_args():
    parser = argparse.ArgumentParser(
            description="Script to check if different data columns are in expected ranges."
            )
    # Add arguments for each runnable function?
    return parser

if __name__=="__main__":
    parser = make_args()
    args = parser.parse_args()
    main()
