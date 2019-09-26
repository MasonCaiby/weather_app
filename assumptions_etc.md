1. Using weather code so I can get if it is sunny or cloudy or precipitating
2. Getting the next 24 hours of forecast data then getting the last forecasted hour 
3. I just copied a webpage with the top 100 cities by population into an excel work book then copied my desired column. I thought about building a little webscraper to keep the top 100 cities updated, but wasn't sure how I would handle people from a city that got booted from the top 100.
4. This requires psycopg2 version 2.8+
5. I implemented a basic regex to check the email syntax. It looks like a [python package exists](https://pypi.org/project/validate_email/) to check the validity of the email, but I wanted to limit the number of packages you would need to install to run this.
6. 