# FastAPI application demo
>:star: For background, check out the first ~7 chapters of the `FastAPI` [tutorial](https://fastapi.tiangolo.com/tutorial/).
>
>:star: Read about `pydantic` model-based validation [here](https://docs.pydantic.dev/latest/concepts/models/)
>
>:star: Read the `# comments` in `app.py` to see how the application is set up and how the `pydantic` models are used.

## Setup :wrench:
- build a conda environment from `environment.yml` (this is just the `snap-geo` environment with `fastapi` added)
```
conda env create -f environment.yml
```
- start the application in `dev` mode like so:
```
fastapi dev app.py
```

## OpenAPI JSON schema 📖
This is automagically generated from the code itself:
- http://127.0.0.1:8000/openapi.json

Which allows documentation to be automagically generated from that schema. It comes in two flavors:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc


## Demo of query validation :zap:

Right now, queries just return messages to test if `pydantic` parameter validation worked. No data is fetched yet.

#### Good queries :white_check_mark:
- Request the "about" page at the root
    - http://localhost:8000/about/

- Request the "about" page, but specify a service category. The query uses a `GET` parameter to specify a service category.
    - http://localhost:8000/about/?service_category=atmosphere

- Request data for an atmospheric variable. The query uses `GET` parameters to specify variable, location, year range, and format. Notice that if we do not specify the format, we see the default in the message.
    - http://localhost:8000/data/atmosphere/?variable=t2&lat=64.5&lon=-147.7&start_year=1990&end_year=2020
    - http://localhost:8000/data/atmosphere/?variable=t2&lat=64.5&lon=-147.7&start_year=1990&end_year=2020&format=csv
- What happens if we request multiple variables?
    - We allow lists in the `variable` field of the `AtmosphereDataParameters` class, and define allowable list of  `Literal` items in the class variable `AtmosphereDataParameters.variable`. So this query works, but note that we must use two separate `GET` requests for `variable`:
        - http://localhost:8000/data/atmosphere/?variable=t2&variable=clt&lat=64.5&lon=-147.7&start_year=1990&end_year=2020

#### Bad queries :x:
- What happens if we are missing a required `GET` parameter, or specify an invalid choice?
    - bad `service category`...
        - http://localhost:8000/about/?service_category=atmospheric
    - missing `end_year`...
        - http://localhost:8000/data/atmosphere/?variable=t2&lat=64.5&lon=-147.7&start_year=1990
    - bad `end_year`...
        - http://localhost:8000/data/atmosphere/?variable=t2&lat=64.5&lon=-147.7&start_year=1990&end_year=2120
    - Including a non-allowable `variable` in the list...
        - http://localhost:8000/data/hydrosphere/?variable=pr&variable=foo&lat=64.5&lon=-147.7&start_year=1990&end_year=2020
    - Using years in the wrong order...
        - http://localhost:8000/data/hydrosphere/?variable=pr&lat=64.5&lon=-147.7&start_year=1990&end_year=1980
    - Trying to use `location`, `lat`, and `lon` parameters all at once...
        - http://localhost:8000/data/hydrosphere/?variable=pr&lat=64.5&lon=-147.7&start_year=1990&end_year=2020&location=AK1

- What happens if we add extra parameters to the request?
    - We specifically forbid this in the `GeneralDataParameters` parent model, and so extra parameters will raise an error.
        - http://localhost:8000/data/hydrosphere/?variable=pr&lat=64.5&lon=-147.7&start_year=1990&end_year=2020&foo=bar


# Metadata Catalog Rant :open_file_folder:
> This app has **no 1:1 relationship between endpoints and coverages**! Requests focus on the variable and location.

In order for us to direct these requests towards our resources, we need some easily searchable record of our holdings. One way of accomplishing this is to build a metadata catalog. 

The goal is to have a **single, structured, authoritative record** of the data that we want to expose via the API that can answer the question: _"Is there any data available to fulfill this request?"_

Ideally, the metadata catalog should be:

>- **populated programmatically directly from our holdings** (_via Rasdaman [get capabilities](https://zeus.snap.uaf.edu/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities) and [describe coverage](https://zeus.snap.uaf.edu/rasdaman/ows?&SERVICE=WCS&VERSION=2.1.0&REQUEST=DescribeCoverage&COVERAGEID=cmip6_monthly&outputType=GeneralGridCoverage) requests?_)
> - **populated on-the-fly to immediately reflect changes in our holdings**
> - **structured to allow search of any validated request**

This of course relies on there being rich metadata in the holdings themselves! Coverages may have to be re-ingested to improve **metadata uniformity** (_i.e., use the same metadata schema for every coverage_) and possibly **data uniformity** (_e.g., use the same axis id's and datatypes for time, variables, etc._) 

#### The holy grail :trophy:
- **add / subtract / update data in our holdings without revising the API codebase or documentation**

This demo uses a metadata catalog mockup (in `catalog.py`) where the highest levels of organization are the `service_category` and `variable`. Using those parameters, requests can be validated against the metadata catalog without hard-coding any constraints in `app.py`. In other words, the metadata catalog items can be updated and the valid parameter ranges adjusted to the datasets without touching `app.py`,  so long as the catalog structure is static.

This setup should dramatically reduce effort in bringing new resources online (or taking old ones offline), and reduce the overall number of endpoints in the API. In a way, the effort would be transferred to the maintenance of coverage metadata instead.

As for documentation, we can see how having the application translated into the OpenAPI JSON schema allows for automatic generation of API documentation pages. We could consider building our HTML documentation directly from the application's OpenAPI JSON schema in a similar way, which would also reduce effort when we update our holdings. 
