# C12_TreeTypesMapping

This repo contains Python scripts to obtain and filter reference data from GBIF including the
[pyproject.toml](pyproject.toml) to setup the necessary Python environment with [uv](https://docs.astral.sh/uv/).

The TreeSat dataset used for the prototype can be obtained at https://zenodo.org/records/6780578.

The original TempCNN base model for time-series classification is available at https://github.com/charlotte-pel/temporalCNN

Sentinel-2 time-series can be retrieved via CDSE (https://documentation.dataspace.copernicus.eu/APIs/OData.html).

For training, we used all Sentinel-2 scenes for three reference years (+- 3 months) from October 2019 till 
March 2023 with a maximum cloud cover of 80%. After cloud masking the time-series was resampled to regular
10-day intervals using linear interpolation. Inference was performed for the reference year 2021.



