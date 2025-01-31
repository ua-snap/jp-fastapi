from typing import Annotated, ClassVar, Literal, List
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel, model_validator, conint, confloat

# from pydantic_core.core_schema import FieldValidationInfo

# local
from util import mockup_message, check_for_data_and_package_it

app = FastAPI()


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
    service_category: (
        Literal[
            "atmosphere", "hydrosphere", "biosphere", "cryosphere", "anthroposphere"
        ]
        | None
    ) = None


class GeneralDataParameters(BaseModel, extra="forbid"):
    # these class variables will be specific to ranges in the metadata catalog
    # they get passed to the fields below as a choice list for validation
    locations: ClassVar[list] = ["AK1", "AK2", "AK3", "AK4", "AK5"]
    formats: ClassVar[list] = ["json", "csv", "netcdf", "geotiff"]

    # these are the actual fields that are common to all data requests
    # we define the data types, whether they are required/optional, and provide defaults if appropriate
    location: List[Literal[tuple(locations)]] | None = None
    lat: confloat(ge=-90, le=90) | None = None
    lon: confloat(ge=-180, le=180) | None = None
    format: Literal[(tuple(formats))] = "json"

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
    variables: ClassVar[list] = ["t2", "t10", "clt", "dw"]
    sources: ClassVar[list] = ["era5", "cmip5", "cmip6", "cmip7"]
    first_year: ClassVar[int] = 1950
    last_year: ClassVar[int] = 2100

    # these are the actual fields that can be in the request for this service category
    # we define the data types, whether they are required/optional, and provide defaults if appropriate
    # the ellipsis (...) means the field is required
    variable: List[Literal[tuple(variables)]] = ...
    source: List[Literal[tuple(sources)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class HydrosphereDataParameters(GeneralDataParameters):
    variables: ClassVar[list] = ["pr", "swe", "rx1day", "rx5day"]
    sources: ClassVar[list] = ["era5", "cmip5", "cmip6", "cmip7"]
    first_year: ClassVar[int] = 1950
    last_year: ClassVar[int] = 2100

    variable: List[Literal[tuple(variables)]] = ...
    source: List[Literal[tuple(sources)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class BiosphereDataParameters(GeneralDataParameters):
    variables: ClassVar[list] = ["flam", "veg", "beetles"]
    sources: ClassVar[list] = ["era5", "cmip5", "cmip6", "cmip7"]
    first_year: ClassVar[int] = 1950
    last_year: ClassVar[int] = 2100

    variable: List[Literal[tuple(variables)]] = ...
    source: List[Literal[tuple(sources)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class CryosphereDataParameters(GeneralDataParameters):
    variables: ClassVar[list] = ["siconc", "slie"]
    sources: ClassVar[list] = ["era5", "cmip5", "cmip6", "cmip7"]
    first_year: ClassVar[int] = 1950
    last_year: ClassVar[int] = 2100

    variable: List[Literal[tuple(variables)]] = ...
    source: List[Literal[tuple(sources)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class AnthroposphereDataParameters(GeneralDataParameters):
    variables: ClassVar[list] = ["population", "pct_minority"]

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
