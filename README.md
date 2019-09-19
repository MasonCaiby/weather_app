# weather_app
A weather app for klaviyo

create a newsletter sign up page that allows someone to enter their email address and choose their location from a list of the top 100 cities in the US by population. The interface should be pleasant to use and leverage a technique such as autocompletion for hinted location selection.

Once the user submits their information and it's validated, it should be stored in a database and a confirmation message or page should be displayed. Keep in mind, the same email address should only be allowed to sign up once.

CLI program to send a personalized email to each email address in the list. For each recipient, the script should fetch the current weather for that recipient's location in an efficient manner and compare that to the forecasted weather forecast to personalize the subject of the email based on conditions.

If it's nice outside, either sunny or 5 degrees warmer than tomorrow’s forecasted temperature for that location, the email's subject should be "It's nice out! Enjoy a discount on us." Otherwise, if it's not so nice out, either precipitating or 5 degrees cooler than tomorrow’s forecasted temperature, the subject should be "Not so nice out? That's okay, enjoy a discount on us." If the weather doesn't meet either of those conditions, the email subject should read simply "Enjoy a discount on us." In all cases the email should be sent to the recipient's entered email address and come from your email address.

To look up a recipient's weather by their location, you can use the free Weatherbit.io API, OpenWeatherMap API, or Dark Sky API. Weather data is also available from these APIs or other sources. Feel free to document any design decisions you make for the weather calculation based on the data source and retention you pick.

The body of the email can be formatted however you like. It should contain a readable version of the recipient's location along with the current temperature and weather. For example, "55 degrees, sunny." (For extra flair, you could include an image or animated GIF of the current weather.)

1. Create a DataBase to store user information - email and location
2. Website that allows users to enter email address and choose their location from the top 100 cities in the US by population. Use autocompletion.
3. Confirm users information and display confirmation message. Addresses should be unique
4. CLI program to send an email to each address on the list.
    1. Needs to get current and tomorrow's weather for their location from: free Weatherbit.io API, OpenWeatherMap API, or Dark Sky API
    2. Subject:
        1. Nice out (sunny or 5 degrees warmer than tomorrow's forecasted temp): "It's nice out! Enjoy a discount on us."
        2. Not Nice out (percipitating or 5 degrees cooler than tomorrow): "Not so nice out? That's okay, enjoy a discount on us."
        3. Otherwise "Enjoy a discount on us."
    3. Body: contain a readable version of the recipient's location along with the current temperature and weather. For example, "55 degrees, sunny." (For extra flair, you could include an image or animated GIF of the current weather.)
    4. Should come from my email and go to theirs.
    