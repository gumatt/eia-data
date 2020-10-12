## Introduction

This project uses data procuced each week by the EIA to product 5-year trend charts for certain petroleum statistics.  

The conifg file eia_config.py defines key configuration options:

```python
source_urls = [
    'http://ir.eia.gov/wpsr/psw01.xls',
    'http://ir.eia.gov/wpsr/psw02.xls',
    'http://www.eia.gov/dnav/pet/hist_xls/W_EPC0_SAX_YCUOK_MBBLw.xls',
    'http://www.eia.gov/dnav/pet/xls/PET_SUM_SNDW_DCUS_NUS_W.xls'
]

charts = [
    {
        'name': 'Chart1',
        'title': 'Commercial Crude Oil Stocks<br />(Millions of Barrels)<br />Week Ending ',
        'data_file': 'psw01.xls',
        'data_sheet': 'Data 1',
        'data_id': 'WCESTUS1',
        'chart_type': 'MultiYearWeeklyDataTrendChart',
        'num_years': 5,
        'timeframe_unit': 'Year',
        'data_scale_factor': 0.001,
        'auto_open': False,
    },
    ...
```
Note: the ```data_file``` parameter for a chart must be the last component of an existing url in ```source_urls``` 

## Deployment

The project is maintained on GitHub at https://github.com/gumatt/eia-data.  The repo is linked to a Google Source Repository, which is, in turn, linked to a Google Cloud Function project.  Pushing code to github repo, forces a sync to google, and the cloud function uses the new code. 

NOTE:  currently there is not automated testing, and quality logic in the deployment!!

## Usage

To update the charts that appear in the powerhousetl.com/eia-data section of the Powerhouse website, initiate the eia-charts cloud function (can be triggered with a call to https://us-central1-eia-charts.cloudfunctions.net/eia-charts).  

To add/modify the charts simply edit the eia_config.py file and push the change to github.

| config param        | description                                                       |
| ------------------- | ----------------------------------------------------------------- |
| name:               | the name of the chart for (not used in chart rendering)           |
| title:              | html text for chart title (the chart date will be appended to this title when rendered)|
| data_file:          | the filename of the excel doc with the source data to use for the chart |
| data_id:            | the column sourcekey (usually row 2 in each source file) identifier for the data to use for the chart |
| chart_type:         | MultiYearWeeklyDataTrendChart is the only valid value at this point |
| num_years:          | the number of years to show in the chart |
| timeframe_unit:     | This is the unit of time used in the legend to describe the max, min and avg lines in a MultiYear chart |
| data_scale_factor:  | multiplicative factor to apply to the raw data to scale for presentation in the chart |
| auto_open:          | open the chart in the browser when finished -- set to True for testing; default and production value should be False |
| yaxis_name:         | title to use on the y-axis in the chart; default is 'Millions' |



## Requirements: 

Python 3.7.x

and environment variables used in plotly.sign_on(username, key):
PLOTLY_USERNAME (plotly account username for authentication)
PLOTLY_KEY (API Key)

## TODOs


|        |                            |
|------- | -------------------------- |
| TODO:  | Set up cron triggering for 10:31am and 1:01pm ET Wednesdays; and 11:01am and 1:01pm Thursdays (the Thursday triggers cover the weeks when the EIA data is published on Thursdays -- usually after a 3 day weekend)|