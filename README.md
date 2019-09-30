# weather_app
### A weather app for klaviyo

This is a newsletter app that allows someone to enter their email and location (which utilizes 
a drop down and auto-complete - with a list of the top 100 cities in the US).

We validate emails (with some regex) and store it in a postgresql database. It looks like a 
[python package exists](https://pypi.org/project/validate_email/) 
to check the validity of the email, but I wanted to limit the number of 
packages you would need to install to run thi

This also has a CLI program which allows a user to send an email to every email in the
data base. It gets the current and foretasted weather from [weatherbit.io](weatherbit.io) 
and makes a custom subject and body. The emails also include a gif randomly pulled 
from [giphy.com](giphy.com).

We have 3 different conditions Good, Bad, and Normal. 

* For the weather to be good it either has to be sunny out or 5 degrees warmer today 
  than it will be tomorrow.
  * We grab the current weather and the weather for the next 24 hours, then compare
    our current weather to the forecast 24 hours away. 
  * We also check to see if the weather code is either 800 or 801, the two codes that mean it 
    is sunny out
* For the weather to be bad it either has to be 5 degrees colder today than it is tomorrow, or
  be precipitating.
  * We grab the current weather and the weather for the next 24 hours, then compare
    our current weather to the last prediction  
  * We also check to see if the weather code is either between 200 and 624, the two codes 
    that mean it is precipitating out
* Otherwise, the weather is "Normal"

The body of the email includes the recipients location, the temperature, and the weather. We
just use the weather text sent by weatherbit.io in the body.

The CLI program loops through the unique cities contained in our database, this means we don't 
get weather for cities that we don't have a user for. Additionally, we only have to get the 
weather, gif, and build the majority of our email message once.

As an aside, Giphy's search is pretty terrible and the gifs we attach to the messages are 
tangentially related at best. But, that just makes the whole newsletter a bit more fun; right?

## Instillation etc.

1. Requirements
2. 