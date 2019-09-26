from database import grab_data
import smtplib
import requests
import psycopg2
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_prediction(city, api_key):
    # code: 800 or 801 == good
    # code: 200-624 or 900 == bad

    get_url = f"https://api.weatherbit.io/v2.0/current?city={city}&key={api_key}"
    current_weather = requests.get(get_url).json().get('data')[0]
    current_temp = current_weather.get('temp')
    current_code = int(current_weather.get('weather').get('code'))
    current_weather = current_weather.get('weather').get('description')

    body = f"It is currently {current_temp} degrees C outside and {current_weather} in {city}."

    forecast_url = f"https://api.weatherbit.io/v2.0/forecast/hourly?city={city}&key={api_key}&hours=24"
    forecast = requests.get(forecast_url).json()['data']
    next_day = forecast[-1]
    tomorrow_temp = next_day['temp']

    #print(f"current_temp: {current_temp}, current_code: {current_code}, tomorrow_temp: {tomorrow_temp}")

    if (current_temp - tomorrow_temp >= 5) or (current_code==800) or (current_code==801):
        subject = "It's nice out! Enjoy a discount on us."
    elif (current_temp - tomorrow_temp <= -5) or (200<=current_code<=624) or (current_code==900):
        subject = "Not so nice out? That's okay, enjoy a discount on us."
    else:
        subject = "Enjoy a discount on us."

    return body, subject


def send_email(from_email, password, to_email, body, subject, img=False):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msgHtml = MIMEText(body, 'html')
    msg.attach(msgHtml)

    server = smtplib.SMTP('smtp.gmail.com', 587)  # port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.close()


def email_blast(data):
    con = psycopg2.connect(dbname='weather_app',
                           user=data['database_user'],
                           host='',
                           password=data['database_password'])

    cur = con.cursor()
    cur.execute("""Select distinct(city) from recipients;""")
    cities = cur.fetchall()

    for city in cities:
        city = city[0]
        body, subject = get_prediction(city, data['weather_api_key'])

        email_query = f"Select email from recipients where city = '{city}';"
        cur.execute(email_query)
        emails = cur.fetchall()
        for email in emails:
            email = email[0]

            try:
                send_email(data['from_email'], data['email_password'], email, body, subject)
            except smtplib.SMTPRecipientsRefused:
                print(f'{email} is not a valid email')


if __name__ == "__main__":
    data, DATABASE_URI = grab_data()
    email_blast(data)