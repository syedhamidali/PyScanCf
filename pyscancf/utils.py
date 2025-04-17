"""
Utilities for parsing sweeps
Author: @syedhamidali
"""


def parse_fields(ds):
    """
    Parse and extract metadata and data from variables in a NetCDF dataset.

    Parameters
    ----------
    ds : netCDF4.Dataset
        A NetCDF dataset containing radar data and metadata.

    Returns
    -------
    variable_data : dict
        A dictionary containing variable names as keys and their associated
        metadata and data as values. Each value is a dictionary containing the
        following key-value pairs:
        - 'data': The variable's data as a NumPy array.
        - Other variable attributes as key-value pairs.

    Notes
    -----
    This function parses and extracts metadata and data from variables within a
    NetCDF dataset. It focuses on variables with two or more dimensions and
    retrieves the variable's data along with its attributes. The extracted
    information is stored in a dictionary for further analysis and processing.

    """
    variable_data = {}
    for var_name, var in ds.variables.items():
        if len(var.dimensions) >= 2:
            # Get the variable's data
            data = var[:]
            attrs = {}
            # Get the variable's attributes using the get_variable_attrs function
            for attr_name in var.ncattrs():
                attrs[attr_name] = var.getncattr(attr_name)
            attrs["data"] = data
            # Store the attributes dictionary for the variable
            variable_data[var_name] = attrs
    return variable_data
