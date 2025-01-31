from catalog import data_catalog


def validate_parameters_against_catalog(parameters, catalog=data_catalog):
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
    # perform data packaging operations using service_category, data, and format parameter
    packaged_data = {"packaged_data": {}}
    return packaged_data


def check_for_data_and_package_it(service_category, parameters):
    catalog_subset = validate_parameters_against_catalog(parameters)
    data = fetch_data_using_catalog(parameters, catalog_subset)
    packaged_data = package_data(parameters, service_category, data)
    return packaged_data


def get_metadata(service_category, variable_list, data_catalog=data_catalog):
    all_variable_sources = []
    all_variable_start_years = []
    all_variable_end_years = []

    for variable in variable_list:
        all_variable_sources.extend(
            data_catalog["service_category"][service_category]["variable"][variable][
                "source"
            ].keys()
        )
        for source in data_catalog["service_category"][service_category]["variable"][
            variable
        ]["source"].keys():
            all_variable_start_years.append(
                data_catalog["service_category"][service_category]["variable"][
                    variable
                ]["source"][source]["start_year"]
            )
            all_variable_end_years.append(
                data_catalog["service_category"][service_category]["variable"][
                    variable
                ]["source"][source]["end_year"]
            )

    return {
        "sources": all_variable_sources,
        "first_year": min(all_variable_start_years),
        "last_year": max(all_variable_end_years),
    }


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
            message += f"Variable(s): {parameters.variable} | "
        if "source" in params:
            message += f"Source(s): {parameters.source} | "
        if "lat" in params:
            if parameters.lat is not None:
                message += f"Latitude: {parameters.lat} | "
        if "lon" in params:
            if parameters.lon is not None:
                message += f"Longitude: {parameters.lon} | "
        if "location" in params:
            if parameters.location is not None:
                message += f"Location: {parameters.location} | "
        if "start_year" in params:
            message += f"Start Year: {parameters.start_year} | "
        if "end_year" in params:
            message += f"End Year: {parameters.end_year}"
        if "format" in params:
            message += f" | Format: {parameters.format}"

    return {"message": message}
