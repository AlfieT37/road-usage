# Road Usage Analysis 
### *SIoT coursework* - 13/01/2020
#### By Alfie Thompson

## WebApp address
Available at: https://road-usage-siot.herokuapp.com/
## Presentation video
Available at: 

## Introduction
##### Information about the study
This study spans over two weeks of data collection, with 16,600 samples. Future development of the study would
generate data that is useful for road planning and smart cities, who could redirect traffic based upon real data.
*For more information, contact me* - [Via email](mailto:alfiethompson37@gmail.com) *(alfiethompson37@gmail.com)*

##### Web app
This web app was coded in python using the in Dash: "A productive Python framework for building web applications". 
The web app is hosted for free via Heroku and, through its linkage to Github, is able to automatically rebuild when 
new data is generated. This would occur on a daily basis as the study continued.

*For more information:*
* Visit the Dash [documentation](https://dash.plot.ly/)
* Visit Heroku's [Website](https://www.heroku.com/)
* Visit Openweather's [Website](https://openweathermap.org/)

## Instructions
This Github repository is made up of a mix of data, python files and prerequisites for the web app. Provided below is
a guide to these files.

It is necessary to install CV2 ([Guide](https://www.pyimagesearch.com/opencv-tutorials-resources-guides/)) and Skimage ([Guide](https://scikit-image.org/docs/dev/install.html)) in order to run iot functions. In addition, images need to be downloaded and paths  for image files updated to run analysis. *A full analysis of all datapoints and images takes approximately 2 hours*.

#### Guide
* **Important**
  * **Car Counter** is used by the Remote Sensor Module to generate the data
  * **App** file containing web app code
  * **iot functions** primary file for data processing

* **Initialisation**
  * **idea** contains data required for the app to function.
  * **pycache** contains files that have been complied into bytecode by the interpreter.
  * **venv** contains data for the virtual environment used throught the creation of the web app
  * **gitignore** is used to tell the app to ignore certain file types.
  * **Procfile** contains crucial information for the web app so Heroku can specify a server to run the app
  * **Requirements** contains full list of packages used for web app
  * **Setup** contains setup data

* **Data**
  * **data_export** this is the file that outputs after the first round of dataprocessing
  * **data_export2** same as above but with additional points dropped
  * **data csv** is raw data directly from the Remote Sensor Module
  * **data detector csv** processed data looking at detection errors
  * **data temp csv** processed data looking at temperature
  * **data time csv** processed data looking at time
  * **data totals csv** processed data looking at total numbers of each vehicle
  * **data uncertain csv** processed data looking at vehicles that have not been identified
  * **data weather pct** processed data looking the percentage of vehicle types in each weather type
  * **data week csv** processed data looking at days of the week

