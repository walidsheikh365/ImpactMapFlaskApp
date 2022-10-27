import os
import numpy as np
import pandas as pd
import reverse_geocode as rg
from sqlalchemy import create_engine


def data_prep():
    """
    Add country names to dataset based on the coordinates with Reverse Geocode.

    Available at https://github.com/richardpenman/reverse_geocode.

    Notes:
        In venv reverse_geocode __init__.py, line 77 should be

        rows = csv.reader(open(local_filename, encoding="utf-8")),

        otherwise, the code raises an UnicodeDecodeError:

        UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position
        464: character maps to <undefined>

        Available at https://github.com/richardpenman/reverse_geocode/issues/2
    """
    cwd = os.getcwd()
    df = pd.read_csv(cwd + "\\meteorite_data.csv")

    # Working with NaNs is a hassle
    df.replace(np.nan, "na", inplace=True)

    # Create new column for countries and geolocations
    df["country"] = "na"

    # Get lon and lat of meteorites that has valid coordinates
    has_coords = df.loc[df["latitude"] != "na", ["latitude", "longitude"]]

    # Get ids of meteorites that has valid coordinates
    has_coords_id = list(df.loc[df["latitude"] != "na", "id"])

    # Create list of tuples of coordinates
    geolocs = list(has_coords[["latitude", "longitude"]].apply(tuple, axis=1))

    # Get regional data for the coordinates (list of dictionaries)
    country_data = rg.search(geolocs)

    # Get values for the key "country" from all dictionaries in the list
    countries = [val["country"] for val in country_data]

    # Create new dictionary for id (key) and country names (value)
    countries_dict = dict(zip(has_coords_id, countries))

    # Add country names to dataset
    df["country"] = df["id"].map(countries_dict)

    df.replace("na", np.nan, inplace=True)

    df.to_csv(cwd + "\\meteorite_data_with_countries.csv", index=False)

    return df


def create_meteorite_database():
    df = pd.read_csv("meteorite_data_with_countries.csv")

    engine = create_engine('sqlite:///meteorite_data.db')
    sqlite_connection = engine.connect()
    sqlite_table = "meteorite_data"

    df.to_sql(sqlite_table,
              sqlite_connection,
              if_exists="replace",
              index=False)


if __name__ == '__main__':
    data_prep()
    create_meteorite_database()
