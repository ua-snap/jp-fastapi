# metadata catalog mockup
data_locations = {
    "all": ["AK1", "AK2", "AK3", "AK4", "AK5", "AK6", "AK7", "AK8", "AK9", "AK10"],
    "default": None,
}

data_formats = {
    "all": ["json", "csv", "netcdf", "geotiff"],
    "default": "json",
}

data_catalog = {
    "service_category": {
        "atmosphere": {
            "variable": {
                "t2": {
                    "name": "air temperature at 2m",
                    "source": {
                        "era5": {
                            "coverage_id": "era5_monthly",
                            "units": "K",
                            "start_year": 1950,
                            "end_year": 2020,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip6": {
                            "coverage_id": "cmip6_monthly",
                            "units": "C",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
                "t10": {
                    "name": "air temperature at 10m",
                    "source": {
                        "era5": {
                            "coverage_id": "era5_monthly",
                            "units": "K",
                            "start_year": 1950,
                            "end_year": 2020,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip6": {
                            "coverage_id": "cmip6_monthly",
                            "units": "C",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
                "clt": {
                    "name": "cloud cover",
                    "source": {
                        "era5": {
                            "coverage_id": "era5_monthly",
                            "units": "%",
                            "start_year": 1950,
                            "end_year": 2020,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip6": {
                            "coverage_id": "cmip6_monthly",
                            "units": "%",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
                "dw": {
                    "name": "deep winter days",
                    "source": {
                        "cmip5": {
                            "coverage_id": "cmip5_indicators",
                            "units": "days",
                            "start_year": 1950,
                            "end_year": 2020,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "yearly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip6": {
                            "coverage_id": "cmip6_indicators",
                            "units": "days",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "yearly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
            },
        },
        "hydrosphere": {
            "variable": {
                "pr": {
                    "name": "precipitation",
                    "source": {
                        "era5": {
                            "coverage_id": "era5_monthly",
                            "units": "kg m-2 s-1",
                            "start_year": 1950,
                            "end_year": 2020,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip5": {
                            "coverage_id": "cmip5_monthly",
                            "units": "kg m-2 s-1",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip6": {
                            "coverage_id": "cmip6_monthly",
                            "units": "kg m-2 s-1",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
                "swe": {
                    "name": "snow water equivalent",
                    "source": {
                        "era5": {
                            "coverage_id": "era5_monthly",
                            "units": "kg m-2",
                            "start_year": 1950,
                            "end_year": 2020,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip5": {
                            "coverage_id": "cmip5_monthly",
                            "units": "kg m-2",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip6": {
                            "coverage_id": "cmip6_monthly",
                            "units": "kg m-2",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "ncar": {
                            "coverage_id": "ncar_monthly",
                            "units": "kg m-2",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
                "rx1day": {
                    "name": "maximum 1-day precipitation",
                    "source": {
                        "cmip5": {
                            "coverage_id": "cmip5_indicators",
                            "units": "mm",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip6": {
                            "coverage_id": "cmip6_indicators",
                            "units": "mm",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
                "rx5day": {
                    "name": "maximum 5-day precipitation",
                    "source": {
                        "cmip5": {
                            "coverage_id": "cmip5_indicators",
                            "units": "mm",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip6": {
                            "coverage_id": "cmip6_indicators",
                            "units": "mm",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
            },
        },
        "biosphere": {
            "variable": {
                "flam": {
                    "name": "flammability",
                    "source": {
                        "alfresco": {
                            "coverage_id": "flammability",
                            "units": "index",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "yearly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
                "veg": {
                    "name": "vegetation",
                    "source": {
                        "alfresco": {
                            "coverage_id": "vegetation_yearly",
                            "units": "categorical",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "yearly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
                "beetles": {
                    "name": "beetles",
                    "source": {
                        "alfresco": {
                            "coverage_id": "beetle_risk",
                            "units": "index",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "yearly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
            },
        },
        "cryosphere": {
            "variable": {
                "siconc": {
                    "name": "sea ice concentration",
                    "source": {
                        "cmip5": {
                            "coverage_id": "cmip5_monthly",
                            "units": "%",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                        "cmip6": {
                            "coverage_id": "cmip6_monthly",
                            "units": "%",
                            "start_year": 1950,
                            "end_year": 2100,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "monthly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
            },
        },
        "anthroposphere": {
            "variable": {
                "population": {
                    "name": "population",
                    "source": {
                        "census": {
                            "coverage_id": "demographics",
                            "units": "count",
                            "start_year": 2020,
                            "end_year": 2020,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "yearly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
                "pct_minority": {
                    "name": "percentage of minorities",
                    "source": {
                        "census": {
                            "coverage_id": "demographics",
                            "units": "%",
                            "start_year": 2020,
                            "end_year": 2020,
                            "bbox": [-180, 50, 180, 90],
                            "frequency": "yearly",
                            "citation": "https://doi.org/10.XXXXXXX",
                        },
                    },
                },
            },
        },
    },
}
