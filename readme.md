# Dashboard Filter Change Management

Identify references to dashboard filters with specific default values. This is intended to help retire old/obsolete references to old fields or default values. In the future, this repo will also include functions that allow you to find and replace default filter values.

### Prerequisites

This script relies on the new Looker [Python SDK](https://github.com/looker-open-source/sdk-codegen/tree/master/python), which requires Python 3.6+.


### Getting started

* Clone this repo, and configure a file called `looker.ini` in the same directory as the two Python scripts. Follow the instructions [here](https://github.com/looker-open-source/sdk-codegen/tree/master/python#configuring-the-sdk) for more detail on how to structure the `.ini` file. The docs also describe how to use environment variables for API authentication if you so prefer.
* Install all Python dependencies in `requirements.txt`

### Usage

``` Arguments:
  -h, --help            show this help message and exit
  --default_value DEFAULT_VALUE, -v DEFAULT_VALUE
                        The default filter value to search for. Required.
  --dimension DIMENSION, -d DIMENSION
                        The fully qualified dimension name. e.g., 'products.brand'. Optional.
```

To run the script, run the following:

```
python dashboard_filter_change_management.py  -v "{default value}"
```

This will return a CSV with dashboard metadata about every reference to the supplied default value. This includes, dashboard id, dashboard title, and dimension.

If you'd like to hone in on a specific dimension, you can optionally supply a dimension argument, like so:

```
python dashboard_filter_change_management.py -d "{fully qualified dimension}" -v "{default value}"
```

This will narrow the result set to specific pairs of default values and filter dimensions.

#### A note on performance

Dashboard filter metadata can only be collected iteratively on a dahboard by dashboard basis. As a result, this script can take a long time to run on Looker instances with many dashboards. 