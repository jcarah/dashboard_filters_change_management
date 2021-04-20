
import looker_sdk # pip install looker_sdk
from pprint import pprint
import csv
import argparse

config_file = "looker.ini"
sdk = looker_sdk.init31(config_file)

def get_all_dashboards():
    dashboards = sdk.all_dashboards(
        fields="id,title"
    )
    return dashboards

def get_dashboard_filters(dashboard_id):
    dashboard_filters = sdk.dashboard_dashboard_filters(
        str(dashboard_id), 
        fields="id,title,type,explore,model,dimension,default_value"
    )
    return dashboard_filters

def parse_dashboard_filters(
        dashboard_title,
        dashboard_id,
        dashboard_filter,
        dashboard_filter_id,
        default_value,
        dimension = None
    ):
    if dashboard_filter.default_value is None:
        dashboard_filter.default_value = ''
    if(
        default_value.lower() in dashboard_filter.default_value.lower()
        and (
                dashboard_filter.dimension == dimension
                or dimension is None
        )
    ):
        return(
            {
                "dashboard_id": dashboard_id,
                "dashboard_title": dashboard_title,
                "dashboard_filter_id": dashboard_filter.id,
                "filter_type": dashboard_filter.type,
                "model": dashboard_filter.model,
                "explore": dashboard_filter.explore,
                "dimension": dashboard_filter.dimension,
                "default_value": dashboard_filter.default_value
            }
        )
    else:
        pass

def write_output_to_csv(output, output_csv_name):
    try:
        with open(output_csv_name, "w") as csvfile:
            writer = csv.DictWriter(
                csvfile,
               fieldnames=list(output[0].keys())
            )
            writer.writeheader()
            for data in output:
                writer.writerow(data)
        print(f"Dashboard filter information outputed to {output_csv_name}")
    except IOError:
        print("I/O error")

def main():
    parser = argparse.ArgumentParser(
        description="Find dashboard filters that are tied to a specific dimension and have specific default arguement.")
    parser.add_argument("--default_value","-v", type=str, required=True,
                        help="The default filter value to search for. Required.")
    parser.add_argument("--dimension", "-d", type=str,required=False,
                        help="The fully qualified dimension name. e.g., 'products.brand'. Optional.")
    args = parser.parse_args()
    dimension = args.dimension
    default_value = args.default_value
    output = []
    dashboards = get_all_dashboards()
    for dashboard in dashboards:
        print(f"Getting filters for dashboard {dashboard.id}")
        try:
            dashboard_filters = get_dashboard_filters(dashboard.id)
            for dashboard_filter in dashboard_filters:
                filter_metadata = parse_dashboard_filters(
                    dashboard.title,
                    dashboard.id,
                    dashboard_filter,
                    dashboard_filter.id,
                    default_value,
                    dimension
                )
                if filter_metadata is not None:
                    output.append(filter_metadata)
                else:
                    pass
        except Exception as e:
            print(f"Error: {e}")
            print("Skipping")
            pass
    pprint(output)
    write_output_to_csv(output, 'dashboard_filters.csv')

main()
