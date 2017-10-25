# TwittMap
A web app using AWS Cloud Service for 2017 Fall Cloud Computing & Big Data class.

## API Description
| Title| TODO |

|---|---|

| URL | http://flask-es.us-east-1.elasticbeanstalk.com/keyword/\<keyword>/size/\<size> |

| URL Params | **Required**: <br> \<keyword>, \<size>=[integer] <br>**Example**: http://flask-es.us-east-1.elasticbeanstalk.com/keyword/trump/size/10 |

| Data Params | {u : {"coordiantes" : [integer, integer], "text" : [string],     "id" : [integer]}} <br> **Example**: {"coordinates": [-48.76708459542083, -94.    37075012624818], "text": "RT @ostfale: @thehill Keep #Trump busy with tweets     and let\u2019s people like Tillerson do the job", "id": 919623369988898816}     |

|---|---|

| URL | http://flask-es.us-east-1.elasticbeanstalk.com/distance/\<distance>/lat/\<lat>/lon/\<lon> |

| URL Params | **Required**: <br> \<distance> <br> \<lat>=[float]: latitude + 90.0 <br> \<lon>=[float]: longitude + 180.0 <br>**Example**: <br>http://flask-es.us-east-1.elasticbeanstalk.com/distance/1200/lat/160.0/lon/140.0|


## Front End URL
http://flask-env.pptffrafzq.us-east-1.elasticbeanstalk.com

## Contributor
* [Yi Zhang](https://github.com/sxsx1xsxs)
* [Zhijian Jiang](https://github.com/ZhijianJiang)

## Acknowledgement
* [Kaimao Yang](https://github.com/ReggieYang)
