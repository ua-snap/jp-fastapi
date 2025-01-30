# import a metadata catalog... this could take many formats
catalog = {"metadata": {}}


def validate_parameters_against_catalog(parameters, catalog=catalog):
    """
    Validates the parameters against the metadata catalog to ensure at least some data exists for the given parameters.
    This function should be a simple database search to see if any data exists for combinations of the parameters.
    Returns a subset of the catalog, which could be empty.
    """
    # do something to subset the catalog using parameters
    catalog_subset = catalog
    return catalog_subset


def fetch_data_using_catalog(parameters, catalog_subset):
    """
    Fetches data using coverage info from the metadata catalog and given parameters.
    This function will probably call other subfunctions to create WCPS queries to fetch the data.
    """
    # perform data fetching operations using parameters and catalog_subset
    data = {"data": {}}
    return data


def package_data(service_category, data, format):
    """
    Packages the data into a format specified by the user.
    Allows different packaging options for different service categories.
    """
    # perform data packaging operations using service_category, data, and format parameters
    packaged_data = {"packaged_data": {}}
    return packaged_data


def mockup_message(parameters, route):
    """
    Helps to create a message for the API. This is just a mockup! The actual app will return actual data :)
    """
    params = list(parameters.model_fields.keys())

    if route == "about":
        message = f"This is a root endpoint. You have requested a general description of the API. "
        if parameters.service_category is not None:
            message += f"You have requested more information about a service category ({parameters.service_category}), and the service category you requested is valid."
        return {"message": message}

    else:
        message = f"You have requested {route} data using the following parameters: "
        if "variable" in params:
            message += f"Variable: {parameters.variable} | "
        if "source" in params:
            message += f"Source: {parameters.source} | "
        if "lat" in params:
            message += f"Latitude: {parameters.lat} | "
        if "lon" in params:
            message += f"Longitude: {parameters.lon} | "
        if "location" in params:
            message += f"Location: {parameters.location} | "
        if "start_year" in params:
            message += f"Start Year: {parameters.start_year} | "
        if "end_year" in params:
            message += f"End Year: {parameters.end_year}"
        if "format" in params:
            message += f" | Format: {parameters.format}"

    return {"message": message}
