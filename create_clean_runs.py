import json
from tqdm import tqdm
import os
import pandas as pd
from tqdm import tqdm

def create_df(run, metric):
    metric_dict = match(run['metrics'], metric)
    df = pd.DataFrame(metric_dict['values'])
#     print(df.columns)
    df.columns = ['start', 'end', metric]
    return df

def match(metrics, wanted_metric):
    """
    Get correct metric dictionary from list of 
    metric dictionaries in run['metrics']
    
    Returns: metric: entire dictionary
    """
    for metric in metrics:
        if metric['type'] == wanted_metric:
            return metric

def create_df(run, metric):
    """
    Convert json dict to DataFrame for single metric
    and rename columns to avoid clash in future merge
    
    Returns: DataFrame with columns [start, end, <metric>]
    """
    metric_dict = match(run['metrics'], metric)
    df = pd.DataFrame(metric_dict['values'])
#     print(df.columns)
    df.columns = ['start', 'end', metric]
    return df


def create_metric_df(filename):
    """
    Create metric dataframe for single run, given filename 
    of run json file from API.
    
    If run is less detailed, distance, speed and a few other metrics
    are still gathered without location data.
    
    Returns: run dataframe with all available metrics
    """
    run = json.load(open(filename))
    distance_df = create_df(run, 'distance')
    if "longitude" in run["metric_types"]:
        longitude_df = create_df(run, 'longitude')
        latitude_df = create_df(run, 'latitude')
        location_df = pd.merge(longitude_df,
                           latitude_df,
                           on = "end")[1:]
        run_df = pd.merge(distance_df, location_df, on = "end", how = "right")
        bad_data = False
        main_metric = "longitude"
    else:
        bad_data = True
        run_df = distance_df
        main_metric = "distance"
    metrics =  run["metric_types"]
    for metric in ["distance", "latitude", "longitude"]:
        if metric in metrics:
            metrics.remove(metric)
    for metric in metrics:
        metrics_df = create_df(run, metric)
        run_df = pd.merge(metrics_df, run_df, how = "outer", on = "end")
        run_df = run_df.sort_values("end")
        run_df[metric] = run_df[metric].fillna(method="bfill").fillna(method="ffill")
    run_df = run_df.dropna(subset=[main_metric])
    del run_df["start_x"]
    del run_df['start_y']
    run_df["end"] = (run_df.end - run_df.end.min())/1000
    run_df.speed = 3600 * run_df.distance/run_df.end.diff()
    if bad_data:
        run_df.speed = run_df.speed.rolling(5, min_periods=1).mean()
    
    run_df.set_index("end", inplace=True)
    return run_df




def create_all_dfs(input_path, output_path):
    """
    Run create_metric_df on all runs contained in 
    a folder and write them to output folder
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    files = os.listdir(input_path)
    for file in tqdm(files, unit="runs"):
#         print(file)
        try:
            run_df = create_metric_df(os.path.join(input_path, file))
            run_id = file.split(".")[0]
            run_df.to_csv(os.path.join(output_path, f"{run_id}.csv"))
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
	create_all_dfs("run_details", "clean_runs")
    