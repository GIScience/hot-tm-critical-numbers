# Critical Numbers

A GIScience Heidelberg project for the HOT Tasking Manager.


## Installation

### Requirements

Python 3

Following python packages and their dependences are required:
- click
    - creates beautiful command line interfaces
- requests
    - API Requests
- pygal
    - sexy charts
- geomet
    - GeoJSON to WKT conversion
- flask
    - Website
- flask-wtf
    - Website form handlich
- flask-bootstrap
    - Website style
- gunicorn
    - serve the website in production

Install requirements via setup.py (See Installtion Steps)


### Installation Steps

- Python 3.6 is required.
- Clone repository.
    - `git clone https://github.com/GIScience/hot-tm-critical-numbers.git`
- Change to CriticalNumbers directory
    - `cd hot-tm-critical-numbers/`
- Create and activate virtual environment
    - `python3 -m venv venv` (or use `virtualenv -p python3.6 venv`)
    - `source venv/bin/activate`
- Install via setup.py
    - `pip install .`


## Usage

Run `python -m cli serve` to serve the website on port 5000.
Until fixed the application will listen to `127.0.0.1:5000/critical_numbers/`.

<!--
### Basic Workflow

- Run `python cli.py add` to fetch statistical data of two default projects from HOT Tasking Manager API to your analysis.
- Run `python cli.py visualize` to get a example bar chart (.svg) of those projects.
- Run `python cli.py new` to start from scratch.
-->

## Deployment

For deployment you should not use the build in web server of Flask (eg. `flask.run()` which `cli serve` is relying upon).

Recommend deployment stack for this application is:
- Gunicorn (Application runner)
- Nginx Reverse Proxy

See official docs for more information: http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/

Or have a look at following tutorials: 
- http://exploreflask.com/en/latest/deployment.html
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux
