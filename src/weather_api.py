from database import Database
from giphy import get_gif
import smtplib
import requests
import psycopg2
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_prediction(city, api_key):
    """ Grabs the current weather and the forecasted weather from weatherbit's api.
        I determine if it is nice or not (e.g. precipitating or sunny) based on the weather code.
        This let me have the least logic of the 3 options I saw from their API."""

    get_url = f"https://api.weatherbit.io/v2.0/current?city={city}&key={api_key}&units=i"
    current_weather = requests.get(get_url).json().get('data')[0]
    current_temp = current_weather.get('temp') # used to get subject and for the body

    current_code = int(current_weather.get('weather').get('code')) # used to get the subject
    # code: 800 or 801 == good
    # code: 200-624 or 900 == bad

    current_weather = current_weather.get('weather').get('description') # used for the body and for giphy

    body = f'It is currently {current_temp} degrees F outside and {current_weather} in {city}.'

    forecast_url = f"https://api.weatherbit.io/v2.0/forecast/hourly?city={city}&key={api_key}&hours=24&units=i"
    forecast = requests.get(forecast_url).json()['data']
    next_day = forecast[-1] # I get 24 hours of forecast data, then get the last one in the list, so 24 hours later
    tomorrow_temp = next_day['temp']

    #print(f"current_temp: {current_temp}, current_code: {current_code}, tomorrow_temp: {tomorrow_temp}")

    if (current_temp - tomorrow_temp >= 5) or (current_code == 800) or (current_code==801):
        subject = "It's nice out! Enjoy a discount on us."
    elif (current_temp - tomorrow_temp <= -5) or (200 <= current_code <= 624) or (current_code==900):
        subject = "Not so nice out? That's okay, enjoy a discount on us."
    else:
        subject = "Enjoy a discount on us."

    return body, subject, current_weather


def send_email(from_email, password, to_email, msg):
    """ This send a prebuilt message to the given email address."""
    msg['To'] = to_email

    server = smtplib.SMTP('smtp.gmail.com', 587)  # port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.close()


def build_msg(from_email, body, subject, img=False):
    """ Builds an email message that can be re-used for all users in a certain city. This way we don't have to build a
        message for each user."""

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email

    # check to see if there is an image, if so, attach it.
    if img:
        # add this to the body so the image appears in the body, not as an attachement
        body = body+ '<br><img src="cid:image1">'

        with open(img, 'rb') as img_open:
            img_email = img_open.read()
            msg_img = MIMEImage(img_email, 'jpg')
            msg_img.add_header('Content-ID', '<image1>')
            msg_img.add_header('Content-Disposition', 'inline', filename=img)
            msg.attach(msg_img)

    msg_html = MIMEText(body, 'html')
    msg.attach(msg_html)

    return msg


def email_blast(database):
    """ Sends an email to all users in the database, personalized for their city."""

    con = psycopg2.connect(dbname='weather_app',
                           user=database.data['database_user'],
                           host='',
                           password=database.data['database_password'])

    cur = con.cursor()
    cur.execute("""Select distinct(city) from recipients;""")
    cities = cur.fetchall()

    # loop by city, so we aren't remaking anything for multiple people in a city.
    for city in cities:
        city = city[0]  # city comes as a tuple
        body, subject, current_weather = get_prediction(city, database.data['weather_api_key'])

        email_query = f"Select email from recipients where city = '{city}';"
        cur.execute(email_query)
        emails = cur.fetchall()

        # check to see if we can connect to giphy
        if database.data.get('giphy_api_key'):
            file = get_gif(database.data, current_weather)
            msg = build_msg(database.data['from_email'], body, subject, img=file)
        else:
            msg = build_msg(database.data['from_email'], body, subject)

        for email in emails:
            email = email[0]

            try:
                send_email(database.data['from_email'], database.data['email_password'], email, msg)
                print(f'sent email to {email}')
            # in case the email doesn't go through, don't want to break the app
            except smtplib.SMTPRecipientsRefused:
                print(f'{email} is not a valid email')


if __name__ == "__main__":
    database = Database()
    email_blast(database)
