# Data API v2

This repo is designed to explore the data API using a different organizational schema that asserts the primacy of the variable (as opposed to the coverage) in API requests. New features in this application include a metadata catalog, an `about` endpoint that describes data resources, and a `data` endpoint used to request data from an immutable set of service categories.

### Why v2?

#### Background:
Our current endpoints (table below) are a mix of dataset titles (`cmip6`, `alfresco`, `gipl`...), variable names (`permafrost`, `temperature`, `beetles`, ...), spatial units (`boundary`, `places`, `point`, ...), applications (`eds`, `ncr`, ...). What at first glance appears as a hierarchical organizational scheme is actually not. Current service categories are really just synonyms for their data source (usually a Rasdaman coverage) and similar variable data can be found under multiple service categories. In general, request parameterization is inconsistent. Request parameters are specified via the route URL, but sometimes they are selected using additional `GET` parameters.

#### Table of v1 endpoints by route
|route|endpoint|GET parameters|
|--------|-------|-------|
|`boundary.py`|`boundary/area/<var_id>`||
|`vectordata.py`|`places/<type>`|`format`|
|`vectordata.py`|`places/search/<lat>/<lon>`||
|`cmip6.py`|`cmip6/point/<lat>/<lon>`|`format`, `vars`|
|`cmip6.py`|`cmip6/point/<lat>/<lon>/<start_year>/<end_year>`|`format`, `vars`|
|`hydrology.py`|`hydrology/point/<lat>/<lon>`|`format`, `summarize`, `community`, `preview`|
|`hydrology.py`|`eds/hydrology/<lat>/<lon>`|`summarize`, `preview`|
|`hydrology.py`|`eds/hydrology/point/<lat>/<lon>`|`summarize`, `preview`|
|`snow.py`|`eds/snow/<lat>/<lon>`|`summarize`, `preview`|
|`snow.py`|`snow/snowfallequivalent/<lat>/<lon>`|`format`, `summarize`, `community`, `preview`|
|`demographics.py`|`demographics/<community>`|`format`|
|`fire.py`|`fire/point/<lat>/<lon>`||
|`elevation.py`|`elevation/point/<lat>/<lon>`||
|`elevation.py`|`elevation/area/<var_id>`||
|`indicators.py`|`indicators/cmip6/point/<lat>/<lon>`|`format`, `summarize`, `community`|
|`indicators.py`|`indicators/base/point/<lat>/<lon>`|`format`, `community`|
|`indicators.py`|`indicators/base/area/<var_id>`|`format`, `community`|
|`degree_days.py`|`degree_days/<var_ep>/<lat>/<lon>`||
|`degree_days.py`|`degree_days/<var_ep>/<lat>/<lon>/<start_year>/<end_year>`||
|`degree_days.py`|`eds/degree_days/<var_ep>/<lat>/<lon>`||
|`ecoregions.py`|`ecoregions/point/<lat>/<lon>`||
|`permafrost.py`|`permafrost/point/gipl/<lat>/<lon>`||
|`permafrost.py`|`permafrost/point/gipl/<lat>/<lon>/<start_year>/<end_year>`||
|`permafrost.py`|`permafrost/point/<lat>/<lon>`||
|`permafrost.py`|`eds/permafrost/<lat>/<lon>`||
|`permafrost.py`|`ncr/permafrost/point/<lat>/<lon>`||
|`beetles.py`|`beetles/point/<lat>/<lon>`||
|`beetles.py`|`beetles/area/<var_id>`||
|`landfastice.py`|`landfastice/point/<lat>/<lon>`||
|`wet_days_per_year.py`|`wet_days_per_year/<horp>/point/<lat>/<lon>`||
|`wet_days_per_year.py`|`wet_days_per_year/<horp>/point/<lat>/<lon>/<start_year>/<end_year>`||
|`wet_days_per_year.py`|`mmm/wet_days_per_year/<horp>/point/<lat>/<lon>`||
|`wet_days_per_year.py`|`mmm/wet_days_per_year/<horp>/point/<lat>/<lon>/<start_year>/<end_year>`||
|`wet_days_per_year.py`|`eds/wet_days_per_year/point/<lat>/<lon>`||
|`eds.py`|`eds/all/<lat>/<lon>`||
|`seaice.py`|`seaice/point/<lat>/<lon>`||
|`taspr.py`|`eds/temperature/<lat>/<lon>`||
|`taspr.py`|`eds/precipitation/<lat>/<lon>`||
|`taspr.py`|`<var_ep>/<lat>/<lon>`||
|`taspr.py`|`<var_ep>/<month>/<lat>/<lon>`||
|`taspr.py`|`<var_ep>/<lat>/<lon>/<start_year>/<end_year>`||
|`taspr.py`|`<var_ep>/<month>/<lat>/<lon>/<start_year>/<end_year>`||
|`taspr.py`|`tas2km/point/<lat>/<lon>`||
|`taspr.py`|`temperature/point/<lat>/<lon>`||
|`taspr.py`|`precipitation/point/<lat>/<lon>`||
|`taspr.py`|`taspr/point/<lat>/<lon>`||
|`taspr.py`|`temperature/area/<var_id>`||
|`taspr.py`|`precipitation/area/<var_id>`||
|`taspr.py`|`taspr/area/<var_id>`||
|`taspr.py`|`precipitation/frequency/point/<lat>/<lon>`||
|`alfresco.py`|`alfresco/<var_ep>/local/<lat>/<lon>`||
|`alfresco.py`|`alfresco/<var_ep>/area/<var_id>`||

This already feels a little unweildy. But looking ahead a few years, imagine we have brought a lot more data into our holdings, and imagine we have 4x as many endpoints in our current API. Wouldn't this start to resemble a data junk drawer? Say a user wants data for precipitation. How do they know which endpoint to look in? Are we just relying on service category names to guide them there, and are the service category names descriptive enough? 

## The general proposal
>- Develop a set of service categories that **will not change** when adding additional datasets
>- Reduce endpoints to **< 10 service categories**, and field all other request parameters via `GET`
>- Use a **1:many variable-to-dataset** model instead of a 1:1 endpoint-to-coverage model.
>- Focus on **adding rich metadata** used by an application instead of adding complexity to an application.

### Proposed Service Categories
Data endpoints would be limited to 5 service categories (`atmosphere`, `hydrosphere`, `biosphere`, `cryosphere`, and `anthroposphere`) plus an additional endpoint for geospatial data (`geospatial` - not explored in this repo yet). These categories are intended to be immutable meaning they should be able to incorporate variables from any forseeable new datasets without adding new categories. They are intended to quickly direct the user to their desired variable. An additional `about` endpoint would serve information about service categories, variables, etc.

>- **DATA**
>    - **Atmosphere**
>       - Air temperature, Cloud cover, ...
>    - **Biosphere**
>       - Land Cover, Flammability, Spruce Beetles, ...
>    - **Hydrosphere**
>       - Precipitation, Runoff, Snow, ...
>    - **Cryosphere**
>       - Sea Ice, Landfast Sea Ice, ...
>    - **Anthroposphere**
>       - Demographics, ...
>    - **Geospatial**
>       - Point, Polygon, Line, ...
>
>- **ABOUT**
>    - Atmosphere, Biosphere, Hydrosphere, Cryosphere, Anthroposphere
>        - `<service_category_variables>` 

### The house party metaphor

To further explore the difference between v1 and the proposed v2, let's have some house parties. Imagine that we are the host, inviting some guests over for a house party...

#### v1 party
>Host: _"I got all the beverages, and put them in easily accessible places for guests to find. I'll make documents describing where to find all the different beverages, and explicit instructions on how to get them. When the guests arrive, they can review all the documents and go find the beverages they want."_

>Guest: _“I want soda...but first I need to read about all the places where soda could be, and read about the different flavors of soda available. I must read well, or I might not know about all the places that have soda, or I might not know about all the flavors that are available. I’ll make trips to each place to get the exact soda flavors I want.”_

#### v2 party
>Guest: _“I want soda...I'll simply ask the host for soda.”_

>Host: _“Here is all the soda I have from various locations in the house. I have many flavors available for you. Enjoy!”_

This difference may seem subtle, but represents a large change in the user experience and a large change in our data management. In v1, we give the guest a large map or menu and hope they find the soda they want. In v2, we let the user ask for the thing they want (soda) and then either a) tell them what soda we have and let them further refine their choice, or b) give them all the soda we have.  

![image](https://github.com/user-attachments/assets/68ebc214-beb4-4da4-a9c4-fe24b22670b3)

### v2 Goals:
The goals of reconfiguring the organization scheme of the API would be to:
>- reduce complexity in documentation and user experience
>- implement universal functions that operate identically in every service category
>- develop a proper testing suite
>- reduce effort when we add / subtract / update data & its corresponding documentation
>- prepare to use the API in an AI/LLM context

