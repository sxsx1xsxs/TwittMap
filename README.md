# TwittMap
A web app using AWS Cloud Service for 2017 Fall Cloud Computing & Big Data class.

## API Description
| Title| TODO |
|---|---|
| URL | http://flask-es.us-east-1.elasticbeanstalk.com/keyword/\<keyword>/size/\<size> |
| URL Params | **Required**: <br> \<keyword>, \<size>=[integer] <br>**Example**: http://flask-es.us-east-1.elasticbeanstalk.com/keyword/trump/size/10 |
| Data Params | {u : {"coordiantes" : [integer, integer], "text" : [string],     "id" : [integer]}} <br> **Example**: {"coordinates": [-48.76708459542083, -94.    37075012624818], "text": "RT @ostfale: @thehill Keep #Trump busy with tweets     and let\u2019s people like Tillerson do the job", "id": 919623369988898816}     |
