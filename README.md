# MLM-Geo

MLM-Geo is a web application based on two main tasks: information retrieval and location estimation. Currently, the application receives as input an image and performs both tasks. Regarding location estimation, the top 10 predicted locations are displayed on the map. While for the information retrieval task, the top 10 visually similar human settlement entities from [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) are returned. MLM-Geo also provides the current news taking place in any of the retrieved entities using [EventRegistry](https://eventregistry.org/)!

MLM-Geo is built on top of the MLM dataset. In particular an extension of it with 7 more languages. For more details about MLM dataset click [here](http://cleopatra.ijs.si/goal-mlm/)!

MLM-Geo is currently online and you can give it a try [here](http://cleopatra.ijs.si/mlm-demo/)! More details on how to use it are present by clicking the info button on the page.

## Run MLM-Geo locally:
### Requirements and Setup
Python version >= 3.7

PyTorch version = 1.5.1

``` bash
# clone the repository
git clone https://github.com/GOALCLEOPATRA/MLM_Geo.git
cd MLM_Geo
pip install -r requirements.txt
```

### Download Checkpoints and dataset files
For working with MLM-Geo locally you will need to download the model checkpoints and dataset files. Checkpoints should be placed under the models' directory in a folder named checkpoints. While all other files should be placed under a folder named data.

Link for the checkpoints and dataset files will be provided soon!

### Run server
We serve MLM-Geo using [Waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/) pure-Python WSGI server. After having all the checkpoints and dataset files you can simply run:
``` bash
# run waitress server
python waitress_server.py
```
This should run MLM-Geo in the following address [0.0.0.0:9000](0.0.0.0:9000).

## Live API
A live API is provided alongside the application. More details on how to access it will come soon!
