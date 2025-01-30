from typing import Annotated, Literal, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel, model_validator, field_validator, conint, confloat
from pydantic_core.core_schema import FieldValidationInfo


# local
from util import (
    mockup_message,
    validate_parameters_against_catalog,
    fetch_data_using_catalog,
    package_data,
)

app = FastAPI()

# The pydantic models below are used to validate the query parameters for each route.
# They check for sane values for each parameter, and provide default values where appropriate.
# They only check that the request is well-formed.
# The lists used in the models could come directly from the metadata catalog and be populated programmatically.
# *** They do not check for data availability! ***
# Data availability is checked within each route using the pre-validated parameters from these base models.


class AboutParameters(BaseModel):
    model_config = {"extra": "forbid"}
    service_category: (
        Literal[
            "atmosphere", "hydrosphere", "biosphere", "cryosphere", "anthroposphere"
        ]
        | None
    ) = None


class AtmosphereDataParameters(BaseModel):
    # model_config = {"extra": "forbid"}
    variable: Literal["t2", "t10", "clt", "dw"] = ...
    source: Literal["cmip5", "cmip6", "cmip7"] = ...
    lat: confloat(ge=50, le=90) = ...
    lon: confloat(ge=-180, le=180) = ...
    start_year: conint(ge=1950, le=2100) = ...
    end_year: conint(ge=1950, le=2100) = ...
    format: Literal["json", "csv", "netcdf", "geotiff"] = "json"


class HydrosphereDataParameters(BaseModel):
    model_config = {"extra": "forbid"}
    variable: Literal["pr", "swe", "rx1day", "rx5day"] = ...
    # source: Literal["cmip5", "cmip6", "cmip7"] = ...
    source: list[str] = ...
    # lat: confloat(ge=50, le=90) = ...
    # lon: confloat(ge=-180, le=180) = ...
    location: Literal["AK1", "AK2", "AK3"] | None = None
    lat: confloat(ge=50, le=90) | None = None
    lon: confloat(ge=-180, le=180) | None = None
    start_year: conint(ge=1950, le=2100) = ...
    end_year: conint(ge=1950, le=2100) = ...
    format: Literal["json", "csv", "netcdf", "geotiff"] = "json"

    @field_validator("source")
    def validate_option(cls, v):
        allowable_sources = ["cmip5", "cmip6", "cmip7"]
        if not all(item in allowable_sources for item in v):
            raise ValueError(f"Source must be in {allowable_sources}.")
        return v

    @model_validator(mode="after")
    def validate_years(self):
        if not self.start_year < self.end_year:
            raise ValueError("Start year must be less than end year.")
        return self

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


class BiosphereDataParameters(BaseModel):
    model_config = {"extra": "forbid"}
    variable: Literal["flam", "veg", "beetles"] = ...
    source: Literal["era5", "cmip5"] = ...
    lat: confloat(ge=50, le=90) = ...
    lon: confloat(ge=-180, le=180) = ...
    start_year: conint(ge=1950, le=2100) = ...
    end_year: conint(ge=1950, le=2100) = ...
    format: Literal["json", "csv", "netcdf", "geotiff"] = "json"


class CryosphereDataParameters(BaseModel):
    model_config = {"extra": "forbid"}
    variable: Literal["siconc", "slie"] = ...
    source: Literal["cmip5", "cmip6", "cmip7"] = ...
    lat: confloat(ge=50, le=90) = ...
    lon: confloat(ge=-180, le=180) = ...
    start_year: conint(ge=1950, le=2100) = ...
    end_year: conint(ge=1950, le=2100) = ...
    format: Literal["json", "csv", "netcdf", "geotiff"] = "json"


class AnthroposphereDataParameters(BaseModel):
    model_config = {"extra": "forbid"}
    variable: Literal["population", "pct_minority"] = ...
    location: Literal["AK1", "AK2", "AK3"] = ...
    format: Literal["json", "csv", "netcdf", "geotiff"] = "json"


@app.get("/about/")
def root(parameters: Annotated[AboutParameters, Query()]):
    """
    Returns a description of the API. Optionally, returns descriptions of service categories from user-specified parameters.
    """
    return mockup_message(parameters, "about")


@app.get("/data/atmosphere/")
def root(parameters: Annotated[AtmosphereDataParameters, Query()]):
    """
    Validates request parameters against the metadata catalog.
    Fetches, packages, and returns atmospheric data from user-specified parameters.
    """
    catalog_subset = validate_parameters_against_catalog(parameters)
    data = fetch_data_using_catalog(parameters, catalog_subset)
    packaged_data = package_data("atmosphere", data, parameters.format)

    # return packaged_data
    return mockup_message(parameters, "atmosphere")


@app.get("/data/hydrosphere/")
def root(parameters: Annotated[HydrosphereDataParameters, Query()]):
    """
    Validates request parameters against the metadata catalog.
    Fetches, packages, and returns hydrologic data from user-specified parameters.
    """
    catalog_subset = validate_parameters_against_catalog(parameters)
    data = fetch_data_using_catalog(parameters, catalog_subset)
    packaged_data = package_data("atmosphere", data, parameters.format)

    # return packaged_data
    return mockup_message(parameters, "hydrosphere")


@app.get("/data/biosphere/")
def root(parameters: Annotated[BiosphereDataParameters, Query()]):
    """
    Validates request parameters against the metadata catalog.
    Fetches, packages, and returns biological data from user-specified parameters.
    """
    catalog_subset = validate_parameters_against_catalog(parameters)
    data = fetch_data_using_catalog(parameters, catalog_subset)
    packaged_data = package_data("atmosphere", data, parameters.format)

    # return packaged_data
    return mockup_message(parameters, "biosphere")


@app.get("/data/cryosphere/")
def root(parameters: Annotated[CryosphereDataParameters, Query()]):
    """
    Validates request parameters against the metadata catalog.
    Fetches, packages, and returns cryospheric data from user-specified parameters.
    """
    catalog_subset = validate_parameters_against_catalog(parameters)
    data = fetch_data_using_catalog(parameters, catalog_subset)
    packaged_data = package_data("atmosphere", data, parameters.format)

    # return packaged_data
    return mockup_message(parameters, "cryosphere")


@app.get("/data/anthroposphere/")
def root(parameters: Annotated[AnthroposphereDataParameters, Query()]):
    """
    Validates request parameters against the metadata catalog.
    Fetches, packages, and returns anthropological data from user-specified parameters.
    """
    catalog_subset = validate_parameters_against_catalog(parameters)
    data = fetch_data_using_catalog(parameters, catalog_subset)
    packaged_data = package_data("atmosphere", data, parameters.format)

    # return packaged_data
    return mockup_message(parameters, "anthroposphere")
