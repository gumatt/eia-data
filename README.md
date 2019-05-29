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

## Requirements: 

Python 3.7.x

and environment variables used in plotly.sign_on(username, key):
PLOTLY_USERNAME (plotly account username for authentication)
PLOTLY_KEY (API Key)

