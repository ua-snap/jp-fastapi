from typing import Annotated, ClassVar, Literal, List
from fastapi import FastAPI, Query, UploadFile
from pydantic import BaseModel, model_validator, conint, confloat
from pathlib import Path

# local
from catalog import data_locations, data_formats, data_catalog
from util import get_metadata, check_for_data_and_package_it, mockup_message


#############################################################################################################
# APP
########################################################################################################################

# Here we set up the app and its metadata
# The metadata is used to generate the OpenAPI documentation

description = """
Query climate data from **Scenarios Network for Alaska and Arctic Planning** (SNAP) holdings 

## Service Categories

You can get data about these topics:
* **Atmosphere**
* **Hydrosphere**
* **Biosphere**
* **Cryosphere**
* **Anthroposphere**

## Request Parameters

You can query data by:

* **Variable** 
* **Time Range**
* **Geographic Location** _(by location ID or coordinates)_
"""

tags_metadata = [
    {
        "name": "about",
        "description": "Get information about the API and its service categories.",
        "externalDocs": {
            "description": "Read about SNAP's API",
            "url": "https://earthmaps.io/",
        },
    },
    {
        "name": "data",
        "description": "Request data from SNAP's holdings.",
        "externalDocs": {
            "description": "Read tutorials on data access",
            "url": "https://arcticdatascience.org/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app = FastAPI(
    title="SNAP API",
    summary=None,
    description=description,
    version="2.0",
    terms_of_service=None,
    contact={
        "name": "SNAP Team",
        "url": "https://uaf-snap.org/contact/",
        "email": "uaf-snap-data-tools@alaska.edu",
    },
    license_info={
        "name": "Creative Commons",
        "url": "https://creativecommons.org/licenses/by/4.0/",
    },
)

############################################################################################################
# MODELS
############################################################################################################

### Pydantic Models:
# Here "model" is in the sense of pydantic models, not climate data models!
# The pydantic models below are used to validate the query parameters for each route.
# They are used to check for sane values for each parameter, and provide default values where appropriate.
# They are used to check that the request is well-formed and is within the general bounds of our holdings.
# The metadata in the models comes directly from a metadata catalog, which would be populated programmatically (TBD).
# Ideally, this app would not need to be updated when the metadata changes, as long as the structure remains the same.

### Parent models: AboutParameters and GeneralDataParameters
# These are general models that contain fields common to all "/about/" and "/data/" requests
# They are used to validate certain request parameters that will be inherited by the child models

### Child models: AtmosphereDataParameters, HydrosphereDataParameters, BiosphereDataParameters, CryosphereDataParameters, AnthroposphereDataParameters
# These are models that contain fields specific to each service category
# Child models inherit all fields from the parent models

### Class Variables:
# Here "variable" is in the sense of python variables, not climate data variables!
# These can be defined by ranges in the metadata catalog, or hardcoded into the app
# They get passed to the model fields to create choice lists for validation

### Model Fields:
# These are the actual fields used in the request GET parameters.
# We define the data types, if they are required/optional, and provide defaults if appropriate
# If using class variables choice lists defined by the metadata catalog,
# model fields can be responsive to changes in the metadata catalog without the app needing to be updated


class AboutParameters(BaseModel, extra="forbid"):
    # Class Variables:
    service_categories: ClassVar[list] = list(data_catalog["service_category"].keys())
    # Model Fields:
    service_category: Literal[tuple(service_categories)] | None = None


class GeneralDataParameters(BaseModel, extra="forbid"):
    # Class Variables:
    locations: ClassVar[dict] = data_locations
    formats: ClassVar[dict] = data_formats
    # Model Fields:
    location: List[Literal[tuple(locations["all"])]] | None = locations["default"]
    format: Literal[(tuple(formats["all"]))] = formats["default"]
    lat: confloat(ge=-90, le=90) | None = None
    lon: confloat(ge=-180, le=180) | None = None

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

    # Non-general validation functions (for fields that may be specific to child model)
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


class AtmosphereDataParameters(GeneralDataParameters):
    # Class Variables:
    variables: ClassVar[list] = data_catalog["service_category"]["atmosphere"][
        "variable"
    ]
    # apply function to get metadata from the catalog using the service category and variable(s)
    metadata: ClassVar[tuple] = get_metadata("atmosphere", variables, data_catalog)
    first_year: ClassVar[int] = metadata["first_year"]
    last_year: ClassVar[int] = metadata["last_year"]

    # Model Fields:
    variable: List[Literal[tuple(variables)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class HydrosphereDataParameters(GeneralDataParameters):
    # Class Variables:
    variables: ClassVar[list] = data_catalog["service_category"]["hydrosphere"][
        "variable"
    ]
    metadata: ClassVar[tuple] = get_metadata("hydrosphere", variables, data_catalog)
    first_year: ClassVar[int] = metadata["first_year"]
    last_year: ClassVar[int] = metadata["last_year"]

    # Model Fields:
    variable: List[Literal[tuple(variables)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class BiosphereDataParameters(GeneralDataParameters):
    # Class Variables:
    variables: ClassVar[list] = data_catalog["service_category"]["biosphere"][
        "variable"
    ]
    metadata: ClassVar[tuple] = get_metadata("biosphere", variables, data_catalog)
    first_year: ClassVar[int] = metadata["first_year"]
    last_year: ClassVar[int] = metadata["last_year"]

    # Model Fields:
    variable: List[Literal[tuple(variables)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class CryosphereDataParameters(GeneralDataParameters):
    # Class Variables:
    variables: ClassVar[list] = data_catalog["service_category"]["cryosphere"][
        "variable"
    ]
    metadata: ClassVar[tuple] = get_metadata("cryosphere", variables, data_catalog)
    first_year: ClassVar[int] = metadata["first_year"]
    last_year: ClassVar[int] = metadata["last_year"]

    # Model Fields:
    variable: List[Literal[tuple(variables)]] = ...
    start_year: conint(ge=first_year, le=last_year) = ...
    end_year: conint(ge=first_year, le=last_year) = ...


class AnthroposphereDataParameters(GeneralDataParameters):
    # Class Variables:
    variables: ClassVar[list] = data_catalog["service_category"]["anthroposphere"][
        "variable"
    ]
    # Model Fields:
    variable: List[Literal[tuple(variables)]] = ...


############################################################################################################
# ROUTES
############################################################################################################

# These routes will validate the request parameters against the ranges in the metadata catalog and return a mockup message.
# They would also fetch, package, and return any data that matches user-specified parameters (TBD).


@app.get("/about/", tags=["about"])
def root(parameters: Annotated[AboutParameters, Query()]):
    """
    Returns a description of the API. Optionally, returns descriptions of service categories from user-specified parameters.
    """
    return mockup_message(parameters, "about")


@app.get("/data/atmosphere/", tags=["data"])
def root(parameters: Annotated[AtmosphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("atmosphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "atmosphere")


@app.get("/data/hydrosphere/", tags=["data"])
def root(parameters: Annotated[HydrosphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("hydrosphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "hydrosphere")


@app.get("/data/biosphere/", tags=["data"])
def root(parameters: Annotated[BiosphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("biosphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "biosphere")


@app.get("/data/cryosphere/", tags=["data"])
def root(parameters: Annotated[CryosphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("cryosphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "cryosphere")


@app.get("/data/anthroposphere/", tags=["data"])
def root(parameters: Annotated[AnthroposphereDataParameters, Query()]):
    packaged_data = check_for_data_and_package_it("anthroposphere", parameters)
    # return packaged_data # not implemented yet
    return mockup_message(parameters, "anthroposphere")


############################################################################################################
# FILE UPLOAD
############################################################################################################

# This route will allow a file upload and return a mockup message with information about the file.
# This upload would be the first step in a BYO-polygon scenario where data is summarized within a user polygon.


@app.post("/uploadfile/")
async def create_upload_file(file_upload: UploadFile):
    data = await file_upload.read()
    if Path("uploads") is not None:
        Path("uploads").mkdir(parents=True, exist_ok=True)

    save_path = Path("uploads") / file_upload.filename
    with open(save_path, "wb") as f:
        f.write(data)
    # return the file name and size in MB
    return {
        "filename": file_upload.filename,
        "size": f"{len(data) / 1024 / 1024:.2f} MB",
        "message": "File uploaded successfully!",
    }
