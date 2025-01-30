# demo a FastAPI application
>:star: For background, check out the first ~7 chapters of the `FastAPI` [tutorial](https://fastapi.tiangolo.com/tutorial/).
>
>:star: Read more about `pydantic` validation [here](https://docs.pydantic.dev/latest/concepts/models/)

## Setup :wrench:
- build a conda environment from `environment.yml` (this is just the `snap-geo` environment with `fastapi` added)
- start the application in `dev` mode like so:
```
fastapi dev app.py
```

## Endpoint documentation :book:
This is automagically generated from the code itself, in two flavors...
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## OpenAPI JSON schema :zap:
This is also automagically generated from the code itself.
- http://127.0.0.1:8000/openapi.json


## Demo of query validation

Right now, these queries just return messages to prove that `pydantic` parameter validation worked or did not work. No data is fetched yet. This is to demonstrate that the app can easily validate requests to make sure they are well-formed and that the parameters are sane.

### Good queries :white_check_mark:
- Request the "about" page at the root
    - http://localhost:8000/about/

- Request the "about" page, but specify a service category. The query uses a `GET` parameter to specify a service category.
    - http://localhost:8000/about/?service_category=atmosphere

- Request data for an atmospheric variable. The query uses `GET` parameters to specify variable, source, location, and year range, and format. Notice that if we do not specify the format, we see the default in the message.
    - http://localhost:8000/data/atmosphere/?variable=t2&source=cmip6&lat=64.5&lon=-147.7&start_year=1990&end_year=2020
    - http://localhost:8000/data/atmosphere/?variable=t2&source=cmip6&lat=64.5&lon=-147.7&start_year=1990&end_year=2020&format=csv
- What happens if we request multiple sources?
    - For the atmospheric data, this doesn't work as expected because we do not allow lists in the `AtmosphereDataParameters.source` object. So the query works, but looking at the return, we only get the first source (they are listed alphabetically by default, so we get CMIP5 instead of CMIP6, even thought CMIP6 is first in the request).
        - http://localhost:8000/data/atmosphere/?variable=t2&source=cmip6&source=cmip5&lat=64.5&lon=-147.7&start_year=1990&end_year=2020
    - For the hydrologic data, we _do_ allow lists in the `HydrosphereDataParameters.source` object, and so our return shows a list of sources.
        - http://localhost:8000/data/hydrosphere/?variable=pr&source=cmip6&source=cmip5&lat=64.5&lon=-147.7&start_year=1990&end_year=2020

### Bad queries :x:
- What happens if we are missing a required `GET` parameter, or specify an invalid choice?
    - bad `service category`...
        - http://localhost:8000/about/?service_category=atmospheric
    - missing `end_year`...
        - http://localhost:8000/data/atmosphere/?variable=t2&source=cmip6&lat=64.5&lon=-147.7&start_year=1990
    - bad `end_year`...
        - http://localhost:8000/data/atmosphere/?variable=t2&source=cmip6&lat=64.5&lon=-147.7&start_year=1990&end_year=2120

 - The `HydrosphereDataParameters` model features a second validation layer which ensures that all items in the list for the `source` parameter are allowable. There's also some additional validation in the `HydrosphereDataParameters` model to make sure `start year` is before `end year`, and that the request includes either a `lat` & `lon` pair or a `location`, but not both. The error type and messages here are custom, but are packaged by the app in the same way as the errors above.
    - Including a non-allowable `source` in the list...
        - http://localhost:8000/data/hydrosphere/?variable=pr&source=cmip4&source=cmip5&lat=64.5&lon=-147.7&start_year=1990&end_year=2020
    - Using years in the wrong order...
        - http://localhost:8000/data/hydrosphere/?variable=pr&source=cmip6&source=cmip5&lat=64.5&lon=-147.7&start_year=1990&end_year=1980
    - Trying to use `location`, `lat`, and `lon` parameters all at once...
        - http://localhost:8000/data/hydrosphere/?variable=pr&source=cmip6&source=cmip5&lat=64.5&lon=-147.7&start_year=1990&end_year=2020&location=AK1

- What happens if we add extra parameters to the request?
    - For the atmospheric data, this is OK because we don't specifically forbid this in the `AtmosphereDataParameters` model.
        - http://localhost:8000/data/atmosphere/?variable=t2&source=cmip6&lat=64.5&lon=-147.7&start_year=1990&end_year=2020&foo=bar
    - For the hydrologic data, we specifically forbid this in the `HydrosphereDataParameters` model, and so extra parameters will raise an error.
        - http://localhost:8000/data/hydrosphere/?variable=pr&source=cmip6&lat=64.5&lon=-147.7&start_year=1990&end_year=2020&foo=bar


## Proposed Metadata Catalog :open_file_folder:
This is referenced in `util.py`, but is not implemented yet. 

Once the main `app.py` validates a request to make sure it is sane, we need to use the request parameters to search our holdings for relevant data. Without a 1:1 relationship between endpoints and coverages, we need a searchable record - one that does not rely on manual population of lookup tables to direct requests towards resources.

 >One way of accomplishing this is to build a metadata catalog. The catalog could take many formats, but the goal is to have a **single, structured, authoritative source of the data that we want to expose via the API**, with enough information to answer the question: _"Is there any data available to fulfill this request?"_

Ideally, the metadata catalog should be:

- populated programmatically directly from our holdings
    - _parse Rasdaman [get capabilities](https://zeus.snap.uaf.edu/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities) and [describe coverage](https://zeus.snap.uaf.edu/rasdaman/ows?&SERVICE=WCS&VERSION=2.1.0&REQUEST=DescribeCoverage&COVERAGEID=cmip6_monthly&outputType=GeneralGridCoverage) requests into a more searchable database structure?_
- populated on-the-fly to immediately reflect changes in our holdings
- have a level of detail granular enough to allow search of any validated request

This of course relies on there being rich metadata in the holdings themselves! Coverages may have to be re-ingested to improve metadata uniformity (i.e., use the same metadata schema for every coverage) and possibly data uniformity (e.g., use the same axis id's and datatypes for time, variables, etc.) 

#### The holy grail :trophy:
- **addition/deletion of data to our holdings without revising the API codebase or documentation**
