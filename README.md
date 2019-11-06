# TrendWithSNS
This project is graduation project.

We want to predict the trend on social media through analyzing the changes of number of likes, followers and retweets.
First, we try to process this project with using data during 2019 LCK (Korean LOL contest). We collected the number of likes, followers and retweets on each LOL progame team's twitter account which participated in 2019 LCK.
And also we collected the time the event (ex. destroy the turret, get killed, ...etc) occured in every game during 2019 LCK.

## Local Env

##### Python 3.7

##### Google Colab

##### InfluxDB 1.4

> For influxDB 8086 port used

## Setup

##### Set up the InfluxDB configuration file

> Open /etc/influxdb/influxdb.conf and look for 'http'. Uncomment 'auth-enabled' and change the value from false to true (default is false)

##### Start InfluxDB on Server

> /etc/rc.d/init.d/influxdb start

##### twitter API

> reference this documnet. (https://developer.twitter.com/en/docs)

#### Clone this repository

> ```git clone https://github.com/chojpsh1/TrendWithSNS.git```

## Analysis

#### Datasets

> We saved the dataset collected in InfluxDB in the 'TrendWithSNS/Trend_analysis/data' directory.

#### trend_analysis.py
> First, check the dataset is downloaded correctly.

> By default, we assume our basic directory is 'TrendWithSNS/Trend_analysis'.

- To analyze the trend with SNS,

> ```python trend_analysis.py```

## Python codes

##### influxDB_python.py

> Here datas will be written into the connected InfluxDB. This project call this module to insert collected data to DB.

##### user_timeline.py

> This project requires two arguments. One is the account of being collected and the other is id of tweet which is the start of collecting.
> This program gets information of total number of likes, followers and retweets with using twitter API.

#### total_analysis.ipynb

> This is a quick glance at how the team's SNS information is analyzed. 
>We analyzed the information of eight teams participating in the 2019 LCK.

> We used Google colab as the environment for running this program. But you must save the collected data to google drive and reset it for your path.

#### trend_analysis.py

> This program was run in a cmd.exe window and pops up a visualization of the analysis information of eight teams.

> We then visualized the eight teams in order of the highest icreasing rate of 'likes' per minute. After showing this, we also visualized it by considering the followers of each team account.
