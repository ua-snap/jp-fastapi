from typing import Annotated, ClassVar, Literal, List
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel, model_validator, conint, confloat

# from pydantic_core.core_schema import FieldValidationInfo

# local
from catalog import data_locations, data_formats, data_catalog
from util import mockup_message, check_for_data_and_package_it

app = FastAPI()

############################################################################################################
# FUNCTIONS
############################################################################################################


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


############################################################################################################
# MODELS
############################################################################################################


# The pydantic models below are used to validate the query parameters for each route.
# They check for sane values for each parameter, and provide default values where appropriate.
# They only check that the request is well-formed. They do not check for data availability.
# The metadata in the child models would come directly from a metadata catalog, populated programmatically.
# Data availability will be checked within each route after validation from parent and child data models.


# Parent models for the about endpoint and all data endpoints
# These are general models that contain fields common to all about / data requests
# They are used to validate the request parameters before passing them to the child models


class AboutParameters(BaseModel, extra="forbid"):
    # these class variables will be specific to ranges in the metadata catalog
    # they get passed to the fields below as a choice list for validation
    service_categories: ClassVar[list] = list(data_catalog["service_category"].keys())

    service_category: Literal[tuple(service_categories)] | None = None


class GeneralDataParameters(BaseModel, extra="forbid"):
    # these class variables will be specific to ranges in the metadata catalog
    # they get passed to the fields below as a choice list for validation
    locations: ClassVar[dict] = data_locations
    formats: ClassVar[dict] = data_formats

    # these are the actual fields that are common to all data requests
    # we define the data types, whether they are required/optional, and provide defaults if appropriate
    location: List[Literal[tuple(locations["all"])]] | None = locations["default"]
    lat: confloat(ge=-90, le=90) | None = None
    lon: confloat(ge=-180, le=180) | None = None
    format: Literal[(tuple(formats["all"]))] = formats["default"]

    # General validation functions (for fields that are in the parent model)
    @model_validator(mode="after")
    def validate_lat_lon(self):
        if self.location is None and self.lat is None:
            raise ValueError("Either location or both lat & lon must be provided.")
        if self.location is None and self.lon is None:
            raise ValueError("Either location or both lat & lon must be provided.")
        if self.location is not None and (self.lat is not None or self.lon is not None):
            raise ValueError(
                "Can only request location or lat & lon, cannot request both."
            )
        return self

    # Non-general validation functions (fields may be specific to child model)
    # these functions need to check for the existence of the fields before running using hasattr()
    @model_validator(mode="after")
    def validate_years(cls, self):
        if not hasattr(self, "start_year") or not hasattr(self, "end_year"):
            return self
        else:
            if not self.start_year < self.end_year:
                raise ValueError("Start year must be before end year.")
            if not cls.first_year <= self.start_year <= cls.last_year:
                raise ValueError(
                    f"Start year must be between {cls.first_year} and {cls.last_year}."
                )
            if not cls.first_year <= self.end_year <= cls.last_year:
                raise ValueError(
                    f"End year must be between {cls.first_year} and {cls.last_year}."
                )
            return self


# Child models for each service category, with specific fields and data for validation functions


class AtmosphereDataParameters(GeneralDataParameters):
    # these class variables will be specific to ranges in the metadata catalog
    # they get passed to the fields below as a choice list for validation
    variables: ClassVar[list] = data_catalog["service_category"]["atmosphere"][
        "variable"
    ]

    metadata: ClassVar[tuple] = get_metadata("atmosphere", variables, data_catalog)

    sources: ClassVar[list] = metadata["sources"]
    first_year: ClassVar[int] = metadata["first_year"]
    last_year: ClassVar[int] = metadata["last_year"]

    # these are the actual fields that can be in the request for this service category
    # we define the data types, whether they are required/optional, and provide defaults if appropriate
    # the ellipsis (...) means the field is required
    variable: List[Literal[tuple(variables)]] = ...
    source: List[Literal[tuple(sources)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class HydrosphereDataParameters(GeneralDataParameters):
    variables: ClassVar[list] = data_catalog["service_category"]["hydrosphere"][
        "variable"
    ]

    metadata: ClassVar[tuple] = get_metadata("hydrosphere", variables, data_catalog)

    sources: ClassVar[list] = metadata["sources"]
    first_year: ClassVar[int] = metadata["first_year"]
    last_year: ClassVar[int] = metadata["last_year"]

    variable: List[Literal[tuple(variables)]] = ...
    source: List[Literal[tuple(sources)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class BiosphereDataParameters(GeneralDataParameters):
    variables: ClassVar[list] = data_catalog["service_category"]["biosphere"][
        "variable"
    ]

    metadata: ClassVar[tuple] = get_metadata("biosphere", variables, data_catalog)

    sources: ClassVar[list] = metadata["sources"]
    first_year: ClassVar[int] = metadata["first_year"]
    last_year: ClassVar[int] = metadata["last_year"]

    variable: List[Literal[tuple(variables)]] = ...
    source: List[Literal[tuple(sources)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class CryosphereDataParameters(GeneralDataParameters):
    variables: ClassVar[list] = data_catalog["service_category"]["cryosphere"][
        "variable"
    ]

    metadata: ClassVar[tuple] = get_metadata("cryosphere", variables, data_catalog)

    sources: ClassVar[list] = metadata["sources"]
    first_year: ClassVar[int] = metadata["first_year"]
    last_year: ClassVar[int] = metadata["last_year"]

    variable: List[Literal[tuple(variables)]] = ...
    source: List[Literal[tuple(sources)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class AnthroposphereDataParameters(GeneralDataParameters):
    variables: ClassVar[list] = data_catalog["service_category"]["anthroposphere"][
        "variable"
    ]

    variable: List[Literal[tuple(variables)]] = ...


############################################################################################################
# ROUTES
############################################################################################################

# These routes are used to validate the request parameters and return a mockup message.
# In practice, these would validates request parameters against the metadata catalog.
# and fetch, package, and return atmospheric data that match user-specified parameters.


@app.get("/about/")
def root(parameters: Annotated[AboutParameters, Query()]):
    """
    Returns a description of the API. Optionally, returns descriptions of service categories from user-specified parameters.
    """
    return mockup_message(parameters, "about")


@app.get("/data/atmosphere/")
def root(parameters: Annotated[AtmosphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("atmosphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "atmosphere")


@app.get("/data/hydrosphere/")
def root(parameters: Annotated[HydrosphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("hydrosphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "hydrosphere")


@app.get("/data/biosphere/")
def root(parameters: Annotated[BiosphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("biosphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "biosphere")


@app.get("/data/cryosphere/")
def root(parameters: Annotated[CryosphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("cryosphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "cryosphere")


@app.get("/data/anthroposphere/")
def root(parameters: Annotated[AnthroposphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("anthroposphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "anthroposphere")
