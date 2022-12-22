import unittest
import pandas as pd
import argparse
import pathlib
import sys

"""
This script tests whether two datasets resulting from the priority places calculation
are equal across all individual values.

The columns expected in each of the two comparison dataframes are as follows:

['domain_supermarket_proximity', 
 'domain_supermarket_accessibility',
 'domain_ecommerce_access', 
 'domain_socio_demographic',
 'domain_nonsupermarket_proximity', 
 'domain_food_for_families',
 'domain_fuel_poverty', 
 'country', 
 'country_denominator', 
 'combined',
 'domain_supermarket_proximity_decile',
 'domain_supermarket_accessibility_decile',
 'domain_ecommerce_access_decile', 
 'domain_socio_demographic_decile',
 'domain_nonsupermarket_proximity_decile',
 'domain_food_for_families_decile', 
 'domain_fuel_poverty_decile',
 'domain_domain_ecommerce_access_decile'
 'combined_decile']
"""

def ppfi_derivation_test(args):
    
    reference = pd.read_csv(args.reference_filepath)
    if 'geocode' in reference.columns:
        reference.index=reference.geo_code
        reference.drop('geo_code', axis=1, inplace=True)
    
    new = pd.read_csv(args.newly_derived_filepath)
    if 'geocode' in new.columns:
        new.index=new.geo_code
        new.drop('geo_code', axis=1, inplace=True)
    
    equal_test = reference.merge(new, left_index=True, right_index=True)
    
    col_number = 0
    distinct_records = []
    for col_number in range(18):
        col1 = equal_test.columns[col_number]
        col2 = col1.replace('_x', '_y')
        #print(col1, 42618 - ((equal_test.loc[:, col1] == equal_test.loc[:,col2]) | (equal_test.loc[:, col1].isna() & equal_test.loc[:, col2].isna())).sum())
        distinct_records.append(
            42618 - ((equal_test.loc[:, col1] == equal_test.loc[:,col2]) | (equal_test.loc[:, col1].isna() & equal_test.loc[:, col2].isna())).sum()
        )
    
    if sum(distinct_records) == 0:
        print('Reference and new are the same')
    else:
        print('Reference and new are different')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-ref", "--reference_filepath", action='store', help="Reference version of the dataset", type=pathlib.Path)
    parser.add_argument("-new", "--newly_derived_filepath", action='store', help="Newly derived filepath", type=pathlib.Path)
    args = parser.parse_args(sys.argv[1:])
    ppfi_derivation_test(args)
    