1. Using weather code so I can get if it is sunny or cloudy or precipitating

2. Getting the next 24 hours of forecast data then getting the last forecasted hour 

3. I just copied a webpage with the top 100 cities by population into an excel work 
book then copied my desired column. I thought about building a little webscraper 
to keep the top 100 cities updated, but wasn't sure how I would handle people from 
a city that got booted from the top 100. Also, this took less time.

4. This requires psycopg2 version 2.8+

5. I utilized regex to check the email syntax. Full disclosure, I just copied 
one from the internet; but why reinvent the wheel? Also, i'm not sure what the 
different syntax requirements are for emails.

6. Giphy's search is admittedly terrible. The gifs are pretty much completely 
unrelated to the query tags.


Bonus things to add:
2. Testing