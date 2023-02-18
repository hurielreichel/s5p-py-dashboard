# Load required packages
from pathlib import Path
from shiny import App, render, ui
import openeo

# openeo connection and authentication 
# https://open-eo.github.io/openeo-python-client/auth.html
## In Linux terminal :
## openeo-auth oidc-auth openeo.cloud
con = openeo.connect("openeo.cloud")
# con.authenticate_oidc_device(store_refresh_token=True)

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
            ui.output_plot("plot_s")
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
      )
    )
  )


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"

www_dir = Path(__file__).parent / "WWW"
app = App(app_ui, server, static_assets=www_dir)
