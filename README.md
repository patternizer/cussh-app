![image](https://github.com/patternizer/cussh-app/blob/main/figures/cussh-cities-logo.png)
![image](https://github.com/patternizer/cussh-app/blob/main/figures/cussh-cities-map.png)
![image](https://github.com/patternizer/cussh-app/blob/main/figures/tas_SSPs_with_historical_bias_adjusted-London.png)

# cussh-app

Python codebase for CUSSH project dashboard. The dashboard HTML code has been adapted to mirror the climate indicator manager dashboard code [climind v0.1](https://github.com/jjk-code-otter/climate-indicator-manager) written by John Kennedy. ISIMIP historical and SSP1-2.6 and SSP3-7.0 climate model runs for climate extreme indices and heat stress indicators derived from CMIP6 global climate projections are from [C3S CDS](https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-extreme-indices-cmip6). CMIP6 historical and SSP1-2.6 and SSP3-7.0 yearly mean and total accumulated precipitation are calculated from CMIP6 projections at [C3S CDS](https://cds.climate.copernicus.eu/cdsapp#!/dataset/projections-cmip6). The ISIMIP temperature variable historical reference data has been calculated from JRA-55 and the precipitation variable historical reference data has been calculated from GPCC-FDD by Ian Harris at CRU/UEA. The CMIP6 observed temperature and precipitation historical reference data is from CRU-TS 3.26 by Ian Harris at CRU/UEA. All data was regridded to 0.5 degrees using CDO and 30-yr averages for key epoches have been calculated for each variable. The multi-model mean and 90% confidence interval bounds are smoothed with a 30-yr Gaussian filter.

## Contents

* `dashboard.html` - html landing page and city selector
* `[city].html` - html code displaying all variables and associated statistical tables for a selection of CUSSH cities [].

The first step is to clone the latest cussh-app code and step into the check out directory: 

    $ git clone https://github.com/patternizer/cussh-app.git
    $ cd cussh-app

### Usage

The code was tested locally for the Firefox and Chrome browsers on a Linux box.

    $ firefox dashboard.html
    
Observations and projection source data extracted from C3S CDS are available on request.

## License

The code is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Michael Taylor](michael.a.taylor@uea.ac.uk)


