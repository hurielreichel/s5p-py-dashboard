#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

suppressPackageStartupMessages(library(shiny))
suppressPackageStartupMessages(library(shinythemes))
suppressPackageStartupMessages(library(openeo))
suppressPackageStartupMessages(library(raster))
suppressPackageStartupMessages(library(sf))
suppressPackageStartupMessages(library(geojsonsf))
suppressPackageStartupMessages(library(rjson))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(rnaturalearth))
suppressPackageStartupMessages(library(gifski))
suppressPackageStartupMessages(library(magick))
suppressPackageStartupMessages(library(ggvis))
suppressPackageStartupMessages(library(leaflet))
suppressPackageStartupMessages(library(dplyr))

con = connect(host = "https://openeo.cloud")

# login
login()

# Define UI
ui <- suppressWarnings({fluidPage(

    theme = shinytheme("darkly"),

    navbarPage(


      title = "SENTINEL 5P (TROPOMI) DATA ANALYSER",
      id = "navbar",

      # Page1, used as a welcome landing page with descriptions and redirecting features for the user
      tabPanel( title = "Home", value = "tab1",
                mainPanel(

                  h1("Welcome to SENTINEL 5P data analyser"),
                  h4("Here you may find three different framework to deeply look into SENTINEL 5P NO2 data.
                              There are three frameworks free for you to use:
                                 the Time-Series Analyser, the Map Maker and the Spacetime Animation one.
                                 \n
                                 With the first one, you should be able to plot a time-series with mean
                                 and maximum values of specified regions given a certain time extent.

                                 The second framework is set to make you able to plot a map of the data in
                                 a specific region (country) and given snapshot.

                                 The third one, finally,
                                 will allow you to create an animated GIF of maps in a certain region and
                                 time gap."),

                  tags$img(src = "img.png")

                )

      ), # end Page1

    # Application title
    tabPanel( title = "Time-Series Analyser", value = "tab2",

    # Sidebar with a slider input for number of bins
    sidebarLayout(
        sidebarPanel(

          checkboxInput("terrascope", "Tick to use Terrascope instead of Sentinel Hub", TRUE),

          numericInput("w", "xmin (EPSG:4326)", 10.35, min = 0, step = .01),
          numericInput("s", "ymin (EPSG:4326)", 46.10, min = 0, step = .01),
          numericInput("e", "xmax (EPSG:4326)", 12.55, min = 0, step = .01),
          numericInput("n", "ymax (EPSG:4326)", 47.13, min = 0, step = .01),

          # dynamic bbox
          leafletOutput("mymap"),

          # Select time gap
          dateRangeInput("date1date2", "Select timeframe", start = "2019-01-01", end = "2019-12-31",
                         min = "2019-01-01", max = "2020-12-31", startview =  "year", weekstart = "1"),

          numericInput("cloud", "cloud cover to be considered? (0 to 1 - 0.5 is recommended)", 0.5, min = 0, max = 1, step = .1),

          #submit button
          actionButton(inputId = "data1", label = icon("rocket")),
        ),

        # Show a plot of the time series
        mainPanel(
           plotOutput("timeseries")
        )
      )
    ),

    tabPanel( title = "Map Maker", value = "tab3",
              sidebarLayout(
                sidebarPanel(

                  checkboxInput("terrascope", "Tick to use Terrascope in spite of Sentinel Hub", TRUE),

                  textInput("country", "Country Name as in rnaturalearth package", value = 'switzerland'),

                  # Select time gap
                  dateRangeInput("datedate12", "Select timeframe for interpolation only", start = "2018-01-01", end = "2021-12-31",
                                 min = "2018-01-01", max = "2021-12-31", startview =  "year", weekstart = "1"),

                  dateInput("date", "Select date for the plot", min = "2018-01-01", max = "2021-12-31", startview =  "year", weekstart = "1"),

                  numericInput("cloud", "cloud cover to be considered? (0 to 1 - 0.5 is recommended)", 0.5, min = 0, max = 1, step = .1),

                  #submit button
                  actionButton(inputId = "data2", label = icon("rocket")),
                ),

                # Show a plot of the generated distribution
                mainPanel(
                  plotOutput("mapmaker")
                )
                ) #sidebar
              ),#tabpanel

    tabPanel(title = "Spacetime Animation", value = "tab4",
             sidebarLayout(
               sidebarPanel(

                 checkboxInput("terrascope", "Tick to use Terrascope in spite of Sentinel Hub", TRUE),

                 textInput("country2", "Country Name as in rnaturalearth package", value = 'switzerland'),

                 #numericInput("w", "Bounding Box West coord. (EPSG:4326)", 6.09, min = 0, step = .01),
                 #numericInput("s", "Bounding Box South coord. (EPSG:4326)", 46.15, min = 0, step = .01),
                 #numericInput("e", "Bounding Box East coord. (EPSG:4326)", 6.99, min = 0, step = .01),
                 #numericInput("n", "Bounding Box North coord. (EPSG:4326)", 46.57, min = 0, step = .01),

                 # Select time gap
                 dateRangeInput("datedate122", "Select timeframe for interpolation only", start = "2020-06-01", end = "2020-06-15",
                                min = "2018-01-01", max = "2021-12-31", startview =  "year", weekstart = "1"),

                 numericInput("cloud3", "cloud cover to be considered? (0 to 1 - 0.5 is recommended)", 0.5, min = 0, max = 1, step = .1),

                 numericInput("delay", "animation speed time in fraction of a second (0.1 to 1)", 0.3, min = 0.1, max = 1, step = .1),

                 #submit button
                 actionButton(inputId = "data3", label = icon("rocket")),
               ),

               # Show a plot of the generated distribution
               mainPanel(
                 plotOutput("animation")
                        )
        ) #sidebar
      )#tabpanel
    )#navbar
  )#fluidpage

}) #suppressWarning
# server
server <- function(input, output) {

  # Time Series ----------------------------------------------------------------
  # plot bbox
  output$mymap <- renderLeaflet({
    coords_df = data.frame(lon = c(input$w, input$e), lat = c(input$s, input$n)) %>%
      st_as_sf(coords = c("lon", "lat"), crs = 4326) %>%
      st_bbox() %>%
      st_as_sfc

    lon = coords_df %>% st_centroid() %>% st_coordinates() %>% as_tibble() %>%
      pull(X) %>% unlist() %>% as.numeric()

    lat = coords_df %>% st_centroid() %>% st_coordinates() %>% as_tibble() %>%
      pull(Y) %>% unlist() %>% as.numeric()

    leaflet(coords_df) %>%
      addTiles(group = "OpenStreetMap") %>%
      setView(lng = lon, lat = lat, zoom = 20) %>%
      fitBounds(input$w, input$s, input$e, input$n) %>%
      addPolygons(data = coords_df)

  })

    output$timeseries <- renderPlot({

      if (input$data1 == 0) return()

      input$data1
      input$terrascope

      w = input$w
      s = input$s
      e = input$e
      n = input$n
      date1 = input$date1date2[1]
      date2 = input$date1date2[2]
      if (input$terrascope == FALSE){cloud = input$cloud}

      print(date1)
      print(date2)

      # Collections
      collections = list_collections()

      # Processes
      processes = list_processes()

      # User defined process
      p = processes()

      if (input$terrascope == TRUE){
        print("using terrascope")
        # acquire data for the extent
        datacube = p$load_collection(
          id = "TERRASCOPE_S5P_L3_NO2_TD_V1",
          spatial_extent = list(west = w, south = s, east = e, north = n),
          temporal_extent=c(date1, date2),
          bands=c("NO2")
        )
      }else{
        print("using sentinelhub")
        # acquire data for the extent
        datacube_no2 = p$load_collection(
          id = "SENTINEL_5P_L2",
          spatial_extent = list(west = w, south = s, east = e, north = n),
          temporal_extent=c(date1, date2),
          bands=c("NO2")
        )

        datacube = p$load_collection(
          id = "SENTINEL_5P_L2",
          spatial_extent = list(west = w, south = s, east = e, north = n),
          temporal_extent=c(date1, date2),
          bands=c("CLOUD_FRACTION")
        )

        # 10km x 10km grid : may be optional
        # datacube = p$resample_spatial(
        #   data = datacube, resolution = 10/111
        # )
        #
        # datacube_no2 = p$resample_spatial(
        #   data = datacube_no2, resolution = 10/111
        # )

        # mask for cloud cover
        threshold_ <- function(data, context) {

          threshold <- p$gte(data[1], cloud)
          return(threshold)
        }

        # apply the threshold to the cube
        cloud_threshold <- p$apply(data = datacube, process = threshold_)

        # mask the cloud cover with the calculated mask
        datacube <- p$mask(datacube_no2, cloud_threshold)
      }

      # interpolate where nodata
      interpolate = function(data,context) {
        return(p$array_interpolate_linear(data = data))
      }

      datacube = p$apply_dimension(process = interpolate,
                                   data = datacube, dimension = "t"
      )

      # moving average UDF - create another datacube
      udf = "Python"
      if (udf == "R"){
        ma <- function(data, context){
          p$run_udf(data = data, udf = readr::read_file("src/udf.py"),
                    runtime = "Python"
          )
        }
      } else{
        ma <- function(data, context){
          p$run_udf(data = data, udf = readr::read_file("src/py-udf.py"),
                    runtime = "Python"
          )
        }
      }

      datacube_ma = p$apply_dimension(process = ma,
                                      data = datacube, dimension = "t"
      )

      # compress spatial dimension
      lon = c(w, e)
      lat = c(s, n)

      bbox_df = data.frame(lon, lat)

      pol = st_polygon(
        list(
          cbind(
            bbox_df$lon[c(1,2,2,1,1)],
            bbox_df$lat[c(1,1,2,2,1)])
        )
      )
      polygons = st_sfc(pol, crs=4326)
      polygons = st_sf(polygons)

      # add any attribute as a workaround
      polygons$anAttribute <- 4

      # aggregate spatially
      datacube_mean <- p$aggregate_spatial(data = datacube, reducer = function(data, context) { p$mean(data) }, geometries = polygons)
      datacube_max <- p$aggregate_spatial(data = datacube, reducer = function(data, context) { p$max(data) }, geometries = polygons)
      datacube_ma <- p$aggregate_spatial(data = datacube_ma, reducer = function(data, context) { p$mean(data) }, geometries = polygons)

      # graph results
      if ( (((e-w)+(n-s)) * 111) < 1000 ){

        tryCatch({

          # submit mean
          print("Trying synchronous process")
          graph = suppressWarnings(as(datacube_mean,"Graph"))
          suppressWarnings(compute_result(graph = graph, output_file = "data/time-series-mean.json"))
          print("mean time series stored")

          # submit max
          graph = suppressWarnings(as(datacube_max,"Graph"))
          suppressWarnings(compute_result(graph = graph, output_file = "data/time-series-max.json"))
          print("max time series stored")

          # submit moving average
          graph = suppressWarnings(as(datacube_ma,"Graph"))
          suppressWarnings(compute_result(graph = graph, output_file = "data/time-series-ma.json"))
          print("moving average time series stored")

          # read json - add save option
          ts_mean = fromJSON(file = "data/time-series-mean.json")
          ts_max = fromJSON(file = "data/time-series-max.json")
          ts_ma = fromJSON(file = "data/time-series-ma.json")
          print("time series read")

        }, error = function(e) {

          message(e)
          print("Synchronous process failed : queuing computation...")
          print("it may take a while... \n")
          formats = list_file_formats()

          # submit mean
          result = p$save_result(data = datacube_mean,
                                 format = formats$output$JSON)
          job = create_job(graph=result, title = "time-series-mean")
          start_job(job = job)
          jobs = list_jobs()
          while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

            print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
            Sys.sleep(60)

            jobs = list_jobs()

            if (jobs[[job$id]]$status == 'finished'){

              print("downloading results")

              download_results(job = job$id, folder = "data/")
            }

            if (jobs[[job$id]]$status == 'error') {

              stop("Error in the backend")
              break

            }
          }

          ts_mean = fromJSON(file = "data/timeseries.json")
          print("mean time series read")

          # submit max
          result = p$save_result(data = datacube_max,
                                 format = formats$output$JSON)
          job = create_job(graph=result, title = "time-series-max")
          start_job(job = job)
          jobs = list_jobs()
          while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

            print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
            Sys.sleep(60)

            jobs = list_jobs()
            if (jobs[[job$id]]$status == 'finished'){

              download_results(job = job$id, folder = "data/")
            }

            if (jobs[[job$id]]$status == 'error') {

              stop("Error in the backend")

              break
            }
          }

          ts_max = fromJSON(file = "data/timeseries.json")
          print("max time series read")

          # submit moving average
          result = p$save_result(data = datacube_ma,
                                 format = formats$output$JSON)
          job = create_job(graph=result, title = "time-series-ma")
          start_job(job = job)
          jobs = list_jobs()
          while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

            print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
            Sys.sleep(60)

            jobs = list_jobs()
            if (jobs[[job$id]]$status == 'finished'){

              download_results(job = job$id, folder = "data/")
            }

            if (jobs[[job$id]]$status == 'error') {

              stop("Error in the backend")

              break
            }
          }

          ts_ma = fromJSON(file = "data/timeseries.json")
          print("moving average time series read")

        }, warning = function(w) {

          message(e)
          print("Synchronous process failed : queuing computation... \n")
          print("it may take a while... \n")
          formats = list_file_formats()

          # submit mean
          result = p$save_result(data = datacube_mean,
                                 format = formats$output$JSON)
          job = create_job(graph=result, title = "time-series-mean")
          start_job(job = job)
          jobs = list_jobs()
          while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

            print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
            Sys.sleep(60)

            jobs = list_jobs()

            if (jobs[[job$id]]$status == 'finished'){

              print("downloading results")

              download_results(job = job$id, folder = "data/")
            }

            if (jobs[[job$id]]$status == 'error') {

              stop("Error in the backend")
              break

            }
          }

          ts_mean = fromJSON(file = "data/timeseries.json")
          print("mean time series read")

          # submit max
          result = p$save_result(data = datacube_max,
                                 format = formats$output$JSON)
          job = create_job(graph=result, title = "time-series-max")
          start_job(job = job)
          jobs = list_jobs()
          while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

            print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
            Sys.sleep(60)

            jobs = list_jobs()
            if (jobs[[job$id]]$status == 'finished'){
              Rplot
              download_results(job = job$id, folder = "data/")
            }

            if (jobs[[job$id]]$status == 'error') {

              stop("Error in the backend")

              break
            }
          }

          ts_max = fromJSON(file = "data/timeseries.json")
          print("max time series read")

          # submit moving average
          result = p$save_result(data = datacube_ma,
                                 format = formats$output$JSON)
          job = create_job(graph=result, title = "time-series-ma")
          start_job(job = job)
          jobs = list_jobs()
          while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

            print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
            Sys.sleep(60)

            jobs = list_jobs()
            if (jobs[[job$id]]$status == 'finished'){

              download_results(job = job$id, folder = "data/")
            }

            if (jobs[[job$id]]$status == 'error') {

              stop("Error in the backend")

              break
            }
          }

          ts_ma = fromJSON(file = "data/timeseries.json")
          print("moving average time series read")
        })

      }else{

        print("queuing computation... \n")
        print("it may take a while... \n")
        formats = list_file_formats()

        # submit mean
        result = p$save_result(data = datacube_mean,
                               format = formats$output$JSON)
        job = create_job(graph=result, title = "time-series-mean")
        start_job(job = job)
        while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

          print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
          Sys.sleep(60)

          if (jobs[[job$id]]$status == 'finished'){

            print("downloading results")
            download_results(job = job$id, folder = "data/")
            break
          }

          if (jobs[[job$id]]$status == 'finished') {

            print('error!')
            break

          }
        }

        ts_mean = fromJSON(file = "data/timeseries.json")
        print("mean time series read")
        print(ts_mean)

        # submit max
        result = p$save_result(data = datacube_max,
                               format = formats$output$JSON)
        job = create_job(graph=result, title = "time-series-max")
        start_job(job = job)
        jobs = list_jobs()
        while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

          print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
          Sys.sleep(60)

          jobs = list_jobs()
          if (jobs[[job$id]]$status == 'finished'){

            download_results(job = job$id, folder = "data/")
          }

          if (jobs[[job$id]]$status == 'error') {

            print('error!')
            break

          }}
        ts_max = fromJSON(file = "data/timeseries.json")
        print("max time series read")
        print(ts_max)

        # submit moving average
        result = p$save_result(data = datacube_ma,
                               format = formats$output$JSON)
        job = create_job(graph=result, title = "time-series-ma")
        start_job(job = job)
        jobs = list_jobs()
        while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

          print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
          Sys.sleep(60)

          jobs = list_jobs()
          if (jobs[[job$id]]$status == 'finished'){

            download_results(job = job$id, folder = "data/")
          }

          if (jobs[[job$id]]$status == 'error') {

            stop("Error in the backend")

            break
          }
        }

        ts_ma = fromJSON(file = "data/timeseries.json")
        print("moving average time series read")
        print(ts_ma)
      }

      #no2 mean
      no2 = list(range(length(ts_mean)))
      for (i in 1:length(ts_mean)){
        no2[i] = ts_mean[[i]]
      }

      # no2 max
      no2_max = list(range(length(ts_max)))
      for (i in 1:length(ts_max)){
        no2_max[i] = ts_max[[i]]
      }

      # no2 ma
      no2_ma = list(range(length(ts_ma)))
      for (i in 1:length(ts_ma)){
        no2_ma[i] = ts_ma[[i]]
      }

      no2 = unlist(no2)
      no2_max = unlist(no2_max)
      no2_ma = unlist(no2_ma)
      # if (input$terrascope == TRUE){no2_ma = no2_ma/10}
      time = seq(as.Date(date1), by = "days", length.out=length(no2))
      no2_k = ksmooth(time(time),no2,'normal',bandwidth=3)
      time = seq(as.Date(date1), as.Date(date2), length.out=length(no2_k$x))

      scientific_notation <- function(l) {

        l <- format(l, scientific = TRUE)
        l <- gsub("^(.*)e", "'\\1'e", l)
        l <- gsub("e", "%*%10^", l)
        parse(text=l)
      }

      # plotting
      if (e <= 12.55 & w >= 10.35 & n <= 47.13 & s >= 46.10 &
          as.Date(date1) >= as.Date("2018-12-14") &
          as.Date(date2) <= as.Date("2021-12-31")){

        print("adding local data to the plot")

        library(readxl)
        library(dplyr)
        library(xts)
        library(treasuryTR)

        df = read_excel("rshiny_NO2_TM75_2017-2022.xlsx")
        df = df %>% slice(5:n()) %>% dplyr::select(2:ncol(df))

        df = as.data.frame(df)
        date = as.POSIXct(seq(0,3600*24*nrow(df)-1,by=24*3600), origin="2017-01-01")
        df$date = as.Date(date)
        xts_df = tibble_to_xts(df)
        storage.mode(xts_df) = "integer"

        # interpolate
        xts_df = na.approx(xts_df)
        xts_df = na.omit(xts_df)
        ##xts_df %>% head()

        # aggregate
        agg = cbind(xts_df, rowMeans(xts_df))

        # convert to comparable scale
        if (input$terrascope == FALSE){agg = agg * 10e-7 * 3
        }else{agg = agg / 10}

        #agg %>% head()

        # filter by date
        filtered = agg[paste0(date1, "/", date2)]

        local_dt <- as.vector(filtered$rowMeans.xts_df.)
        time = c(time,
                 seq(as.Date(date1), as.Date(date2), length.out=length(no2)),
                 seq(as.Date(date1), as.Date(date2), length.out=length(no2_max)),
                 seq(as.Date(date1), as.Date(date2), length.out=length(no2_ma)),
                 seq(as.Date(date1), as.Date(date2), length.out=length(local_dt)))

        # to data frame
        data = c(no2_k$y, no2, no2_max, no2_ma, local_dt)
        group = c(rep("smoothed", length(no2_k$y)),
                  rep("raw", length(no2)),
                  rep("maximum", length(no2_max)),
                  rep("moving average", length(no2_ma)),
                  rep("local", length(local_dt)))

      } else{

        print("no local data in the desired area")

        time = c(time,
                 seq(as.Date(date1), as.Date(date2), length.out=length(no2)),
                 seq(as.Date(date1), as.Date(date2), length.out=length(no2_max)),
                 seq(as.Date(date1), as.Date(date2), length.out=length(no2_ma)))

        data = c(no2_k$y, no2, no2_max, no2_ma)
        group = c(rep("smoothed", length(no2_k$y)),
                  rep("raw", length(no2)),
                  rep("maximum", length(no2_max)),
                  rep("moving average", length(no2_ma)))
      }

      df = data.frame(time, data, group)

      #png('time-series-no2.png')
      ggplot(df, aes(x=time, y=data, group = group, col = group, linetype = group)) +
        geom_line() +
        scale_y_continuous(labels=scientific_notation) +
        theme(legend.position="top") +
        theme(legend.title = element_blank())+
        xlab("Time") + ylab("Tropospheric NO2 Vertical Column (molec/cm²)")
      #dev.off()

    })

    # Map Maker ----------------------------------------------------------------

      output$mapmaker <- renderPlot({

        if (input$data2 == 0) return()

        input$data2
        input$terrascope

        # user inputs
        country = input$country
        date1 = input$datedate12[1]
        date2 = input$datedate12[2]
        if (input$terrascope == FALSE){cloud = input$cloud}
        date = input$date

        print(date1)
        print(date2)
        print(date)

        # Collections
        collections = list_collections()

        # Processes
        processes = list_processes()

        # User defined process
        p = processes()

        # extract bbox
        country_sf = ne_countries(country = country, returnclass = "sf", scale = 'large')
        w = st_bbox(country_sf)[1]
        s = st_bbox(country_sf)[2]
        e = st_bbox(country_sf)[3]
        n = st_bbox(country_sf)[4]

        if (input$terrascope == TRUE){
          print("using terrascope")
          datacube = p$load_collection(
            id = "TERRASCOPE_S5P_L3_NO2_TD_V1",
            spatial_extent = list(west = w, south = s, east = e, north = n),
            temporal_extent=c(date1, date2),
            bands=c("NO2")
          )
        }else{
          print("using sentinelhub")
          # acquire data for the extent
          datacube_no2 = p$load_collection(
            id = "SENTINEL_5P_L2",
            spatial_extent = list(west = w, south = s, east = e, north = n),
            temporal_extent=c(date1, date2),
            bands=c("NO2")
          )

          datacube = p$load_collection(
            id = "SENTINEL_5P_L2",
            spatial_extent = list(west = w, south = s, east = e, north = n),
            temporal_extent=c(date1, date2),
            bands=c("CLOUD_FRACTION")
          )

          # # 10km x 10km grid : may be optional
          # datacube = p$resample_spatial(
          #   data = datacube, resolution = 10/111
          # )
          #
          # datacube_no2 = p$resample_spatial(
          #   data = datacube_no2, resolution = 10/111
          # )

          # mask for cloud cover
          threshold_ <- function(data, context) {

            threshold <- p$gte(data[1], cloud)
            return(threshold)
          }

          # apply the threshold to the cube
          cloud_threshold <- p$apply(data = datacube, process = threshold_)

          # mask the cloud cover with the calculated mask
          datacube <- p$mask(datacube_no2, cloud_threshold)

        }

        # interpolate where nodata
        interpolate = function(data,context) {
          return(p$array_interpolate_linear(data = data))
        }

        datacube = p$apply_dimension(process = interpolate,
                                     data = datacube, dimension = "t"
        )

        ## filter
        datacube_map = p$filter_temporal(
          data = datacube, extent = c(date, date)
        )

        print("Queuing computation... ")
        print("it may take a while... ")
        formats = list_file_formats()
        result = p$save_result(data = datacube_map,
                               format = formats$output$GTiff)
        job = create_job(graph=result, title = 'one-snapshot-raster')
        start_job(job = job)
        jobs = list_jobs()
        while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' ){

          print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
          Sys.sleep(30)

          jobs = list_jobs()

          if (jobs[[job$id]]$status == 'finished' | jobs[[job$id]]$status == 'error' ){

            break

          }
        }
        if (jobs[[job$id]]$status == 'error'){stop("Error in the backend")}
        files = list.files(path = "data/", pattern="\\.tif$")
        for (i in 1:length(files)){
          if (file.exists(paste0("data/", files[i]))) {
            try(file.remove(paste0("data/", files[i])))
          }
        }

        print("downloading results")
        download_results(job = job$id, folder = "data/")
        Sys.sleep(3)
        file = list.files(path = "data/", pattern = "\\.tif$")
        rst = mask(raster(paste0("data/", file)), country_sf)
        print(rst)

        #png(paste0('data/', country, date, '.png'))
        par(mar = c())
        plot(
          rst,
          col = hcl.colors(100, palette = "inferno", alpha = NULL, rev = FALSE, fixup = TRUE),
          main = paste0('Tropospheric NO2 Vertical Column (molec/cm²)','\n', country, ' (', date, ')'),
          axes = FALSE
        )
        plot(st_geometry(country_sf), add = T, type = 'l', lwd = 5)
        #dev.off()

      }) # renderplot

      # Spacetime animation ----------------------------------------------------

      output$animation <- renderImage({

        filename <- normalizePath(
          file.path('./image',
             paste('spacetime-animation',
                    '.gif', sep='')))

        if (input$data3 == 0) return()

        input$data3
        input$terrascope

        # Collections
        collections = list_collections()

        # Processes
        processes = list_processes()

        # User defined process
        p = processes()

        # user inputs
        country = input$country2
        ## time extent
        date1 = input$datedate122[1]
        date2 = input$datedate122[2]
        ## cloud cover value (>=)
        if (input$terrascope == FALSE){cloud = input$cloud3}
        ##delay for spacetime animation
        delay = input$delay

        # extract bbox
        country_sf = ne_countries(country = country, returnclass = "sf", scale = 'large')
        w = st_bbox(country_sf)[1]
        s = st_bbox(country_sf)[2]
        e = st_bbox(country_sf)[3]
        n = st_bbox(country_sf)[4]

        if (input$terrascope == TRUE){
          print("using terrascope")
          datacube = p$load_collection(
            id = "TERRASCOPE_S5P_L3_NO2_TD_V1",
            spatial_extent = list(west = w, south = s, east = e, north = n),
            temporal_extent=c(date1, date2),
            bands=c("NO2")
          )
        }else{

          print("using sentinelhub")
          # acquire data for the extent
          datacube_no2 = p$load_collection(
            id = "SENTINEL_5P_L2",
            spatial_extent = list(west = w, south = s, east = e, north = n),
            temporal_extent=c(date1, date2),
            bands=c("NO2")
          )

          datacube = p$load_collection(
            id = "SENTINEL_5P_L2",
            spatial_extent = list(west = w, south = s, east = e, north = n),
            temporal_extent=c(date1, date2),
            bands=c("CLOUD_FRACTION")
          )

          # # 10km x 10km grid : may be optional
          # datacube = p$resample_spatial(
          #   data = datacube, resolution = 10/111
          # )
          #
          # datacube_no2 = p$resample_spatial(
          #   data = datacube_no2, resolution = 10/111
          # )

          # mask for cloud cover
          threshold_ <- function(data, context) {

            threshold <- p$gte(data[1], value)
            return(threshold)
          }

          # apply the threshold to the cube
          cloud_threshold <- p$apply(data = datacube, process = threshold_)

          # mask the cloud cover with the calculated mask
          datacube <- p$mask(datacube_no2, cloud_threshold)
        }

        # interpolate where nodata
        interpolate = function(data,context) {
          return(p$array_interpolate_linear(data = data))
        }

        datacube = p$apply_dimension(process = interpolate,
                                     data = datacube, dimension = "t"
        )

        print("queuing computation...")
        print("it may take a while...")
        formats = list_file_formats()
        result = p$save_result(data = datacube,
                               format = formats$output$GeoTiff)
        job = create_job(graph=result, title = "time-animation-tif")
        start_job(job = job)
        jobs = list_jobs()
        while (jobs[[job$id]]$status == 'running' | jobs[[job$id]]$status == 'queued' | jobs[[job$id]]$status == 'created' | jobs[[job$id]]$status == 'downloading results' ){

          print(paste0('this may take a moment, your process is ', jobs[[job$id]]$status))
          Sys.sleep(60)

          jobs = list_jobs()
          if (jobs[[job$id]]$status == 'finished' | jobs[[job$id]]$status == 'error'){

            break

          }
        }
        if (jobs[[job$id]]$status == 'error'){stop("Error in the backend")}
        files = list.files(path = "data/")
          for (i in 1:length(files)){
            if (file.exists(paste0("data/", files[i]))) {
              file.remove(paste0("data/", files[i]))
            }
          }

        print("downloading results")
        download_results(job = job$id, folder = "data/")

        pal <- hcl.colors(11, palette = "Red-Yellow", alpha = NULL, rev = TRUE, fixup = TRUE)
        files = list.files('data/')
        files = paste0('data/', files)
        dates = sub('data/openEO_', '', files)
        dates = sub('Z.tif', '', dates)
        filepath = tempdir()

        min = c()
        max = c()
        for (i in 1:length(files)){
          min[i] = hist(raster(files[i]))$breaks[1]
          max[i] = hist(raster(files[i]))$breaks[length(hist(raster(files[i]))$breaks)]
        }
        min_v = min(min)
        max_v = max(max)
        for (i in 1:length(files)){

          if (length(files) < 10){

            png(paste0(filepath, '/', as.character(0), as.character(i),'.png'), width = 800)
            plot(mask(raster(files[i]), country_sf), col = pal,
                 axes = FALSE,
                 breaks = seq(min_v, max_v, 0.1*max_v),
                 main = dates[i])
            plot(st_geometry(country_sf), add = T, type = 'l', lwd = 5)
            dev.off()

          } else{

            png(paste0(filepath, '/', as.character(i),'.png'), width = 800)
            plot(mask(raster(files[i]), country_sf), col = pal,
                 axes = FALSE,
                 breaks = seq(min_v, max_v, 0.1*max_v),
                 main = dates[i])
            plot(st_geometry(country_sf), add = T, type = 'l', lwd = 5)
            dev.off()

          }}

        png_files = list.files(filepath)
        png_files = paste0(filepath, '/', png_files)
        gifski(png_files = png_files, gif_file = filename,
               delay = delay,
               progress = T)
        #showGIF <- function(fn) system(paste("display",fn))
        #showGIF("spacetime-animation.gif")
        list(src = filename)
        }, deleteFile = FALSE) #renderplot
  } # function server
# Run the application
shinyApp(ui = ui, server = server)
