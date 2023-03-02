# Load required packages
from pathlib import Path
from shiny import App, render, ui
import openeo
import json
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# openeo connection and authentication 
# https://open-eo.github.io/openeo-python-client/auth.html
## In Linux terminal :
## openeo-auth oidc-auth openeo.cloud
con = openeo.connect("openeo.cloud")
con.authenticate_oidc()

# Define User Interface
app_ui = ui.page_fluid(
  
  # Title of App
  ui.panel_title("SENTINEL 5P (TROPOMI) DATA ANALYSER"),
  
  # Define that we're working with a shiny with different tabs
  ui.navset_tab(
        # Tab1 : Home Screen
        ui.nav("Home", 
        
        # Some informative text
        ui.h1("Welcome to SENTINEL 5P data analyser"),
        ui.h4("Here you may find three different framework to deeply look into SENTINEL 5P NO2 data. "),
        ui.h4("There are three frameworks free for you to use:"),
        ui.h4("the Time-Series Analyser, the Map Maker and the Spacetime Animation one."),
        
        # logo from WWU, ESA and openEO 
        ui.img(src="img.png")
        ), #end of nav
        
        # Tab2 : Time Series Analyser
        ui.nav("Time-Series Analyser", 
        
        # This tab has both a sidebar and panel
        ui.layout_sidebar(
        
          # Define Sidebar Inputs
          ui.panel_sidebar(
            
            # Bounding Box
            ui.input_numeric("w", "xmin (EPSG:4326)", 10.35, min = 0, step = .01),
            ui.input_numeric("s", "ymin (EPSG:4326)", 46.10, min = 0, step = .01),
            ui.input_numeric("e", "xmax (EPSG:4326)", 12.55, min = 0, step = .01),
            ui.input_numeric("n", "ymax (EPSG:4326)", 47.13, min = 0, step = .01),
            
            # Temporal Filter
            ui.input_date_range("date1date2", "Select timeframe", start = "2019-01-01", end = "2019-12-31",
                         min = "2019-01-01", max = "2020-12-31", startview =  "year", weekstart = "1"),
                         
            # Cloud Cover 
            ui.input_numeric("cloud", "cloud cover to be considered? (0 to 1 - 0.5 is recommended)", 0.5, min = 0, max = 1, step = .1),

            # Submit Button
            ui.input_action_button("data1", "Submit")
            
          ),
          # Time Series Plot
          ui.panel_main(
            ui.output_plot("plot_ts")
          ),
        ),
      ),
      
      ui.nav("Map Maker", 
      # This tab has both a sidebar and panel
        ui.layout_sidebar(
        
          # Define Sidebar Inputs
          ui.panel_sidebar(
            
            # Bounding Box
            ui.input_numeric("w", "xmin (EPSG:4326)", 10.35, min = 0, step = .01),
            ui.input_numeric("s", "ymin (EPSG:4326)", 46.10, min = 0, step = .01),
            ui.input_numeric("e", "xmax (EPSG:4326)", 12.55, min = 0, step = .01),
            ui.input_numeric("n", "ymax (EPSG:4326)", 47.13, min = 0, step = .01),
            
            # Temporal Filter
            ui.input_date_range("date1date2", "Select timeframe", start = "2019-01-01", end = "2019-12-31",
                         min = "2019-01-01", max = "2020-12-31", startview =  "year", weekstart = "1"),
                         
            # Cloud Cover 
            ui.input_numeric("cloud", "cloud cover to be considered? (0 to 1 - 0.5 is recommended)", 0.5, min = 0, max = 1, step = .1),

            # Submit Button
            ui.input_action_button("data2", "Submit")
            
          ),
          # Time Series Plot
          ui.panel_main(
            ui.output_plot("plot_map")
          ),
        ),
      ),
      
       ui.nav("Spacetime Animation", 
      # This tab has both a sidebar and panel
        ui.layout_sidebar(
        
          # Define Sidebar Inputs
          ui.panel_sidebar(
            
            # Bounding Box
            ui.input_numeric("w", "xmin (EPSG:4326)", 10.35, min = 0, step = .01),
            ui.input_numeric("s", "ymin (EPSG:4326)", 46.10, min = 0, step = .01),
            ui.input_numeric("e", "xmax (EPSG:4326)", 12.55, min = 0, step = .01),
            ui.input_numeric("n", "ymax (EPSG:4326)", 47.13, min = 0, step = .01),
            
            # Temporal Filter
            ui.input_date_range("date1date2", "Select timeframe", start = "2019-01-01", end = "2019-12-31",
                         min = "2019-01-01", max = "2020-12-31", startview =  "year", weekstart = "1"),
                         
            # Cloud Cover 
            ui.input_numeric("cloud", "cloud cover to be considered? (0 to 1 - 0.5 is recommended)", 0.5, min = 0, max = 1, step = .1),

            # Cloud Cover 
            ui.input_numeric("delay", "animation speed time in fraction of a second (0.1 to 1)", 0.3, min = 0.1, max = 1, step = .1),
            # Submit Button
            ui.input_action_button("data3", "Submit")
            
          ),
          # Time Series Plot
          ui.panel_main(
            ui.output_plot("plot_animation")
          ),
        ),
      )
    )
  )


def server(input, output, session):
    @output
    @render.plot
    def plot_ts():
      
      # Define the Spatial Extent
      extent = { # Münster
        "type": "Polygon",
        "coordinates": [[
          [input.w(), input.n()],
          [input.e(), input.n()],
          [input.e(), input.s()],
          [input.w(), input.s()],
          [input.w(), input.n()]
          ]]
          }
          
      # Build the Datacube    
      datacube = con.load_collection(
        "TERRASCOPE_S5P_L3_NO2_TD_V1",
        spatial_extent = extent,
        temporal_extent = [input.date1date2()[0], input.date1date2()[1]]
        )
        
      # mask for cloud cover
      #   threshold_ <- function(data, context) {
      # 
      #     threshold <- p$gte(data[1], cloud)
      #     return(threshold)
      #   }
      # 
      #   # apply the threshold to the cube
      #   cloud_threshold <- p$apply(data = datacube, process = threshold_)
      # 
      #   # mask the cloud cover with the calculated mask
      #   datacube <- p$mask(datacube_no2, cloud_threshold)
      # }
      # 
      
      # Fill Gaps
      datacube = datacube.apply_dimension(dimension = "t", process = "array_interpolate_linear")
      
      # Moving Average Window
      moving_average_window = 31
      
      with open('ma.py', 'r') as file:
        udf_file = file.read()
        
      udf = openeo.UDF(udf_file.format(n = moving_average_window))
      datacube_ma = datacube.apply_dimension(dimension = "t", process = udf)
      
      # Timeseries as JSON
      print("Processing and Downloading Results...")
      
      ## Mean as Aggregator
      datacube_mean = datacube.aggregate_spatial(geometries = extent, reducer = "mean")
      datacube_mean = datacube_mean.download("data/time-series-mean.json")
      
      ## Max as Aggregator
      datacube_max = datacube.aggregate_spatial(geometries = extent, reducer = "max")
      datacube_max = datacube_max.download("data/time-series-max.json")
      
      ## Mean as Aggregator for Moving Average Data Cube
      datacube_ma = datacube_ma.aggregate_spatial(geometries = extent, reducer = "mean")
      datacube_ma = datacube_ma.download("data/time-series-ma.json")
      
      # Read in JSONs
      with open("data/time-series-mean.json", "r") as f:
        ts_mean = json.load(f)
      print("mean time series read")
      
      with open("data/time-series-max.json", "r") as f:
        ts_max = json.load(f)
      print("max time series read")

      with open("data/time-series-ma.json", "r") as f:
        ts_ma = json.load(f)
      print("ma time series read")

      ts_df = pd.DataFrame.from_dict(ts_mean, orient='index', columns=['Mean']).reset_index()
      ts_df.columns = ['Date', 'Mean']
      ts_df['Mean'] = ts_df['Mean'].str.get(0)
     
      ts_max_df = pd.DataFrame.from_dict(ts_max, orient='index', columns=['Max']).reset_index()
      ts_max_df.columns = ['Date', 'Max']
      ts_df['Max'] = ts_max_df['Max'].str.get(0) 
      
      ts_ma_df = pd.DataFrame.from_dict(ts_ma, orient='index', columns=['MA']).reset_index()
      ts_ma_df.columns = ['Date', 'MA']
      ts_df['MA'] = ts_ma_df['MA'].str.get(0)
      
      # convert 'Date' column to datetime dtype
      ts_df['Date'] = pd.to_datetime(ts_df['Date'])
      
      # set 'Date' column as index
      ts_df.set_index('Date', inplace=True)
      
      # Time Series Smoothing
      ts_df['Smooth'] = ts_df['Mean'].rolling(31).mean()

      # plot time series for each column
      fig, ax = plt.subplots(figsize=(8, 5))
      ts_df.plot(ax=ax)
      ax.set_xlabel('Time')
      ax.set_ylabel('Value')
      ax.set_title('NO2 Time Series from SENTINEL 5P')
      # plt.show()
      
      return fig
      
          
www_dir = Path(__file__).parent / "WWW"
app = App(app_ui, server, static_assets=www_dir)
