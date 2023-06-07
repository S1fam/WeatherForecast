import streamlit as st
import plotly.express as px
from backend import get_data

st.title("Weather Forecast for the Next Days")

place = st.text_input(label="Place:")

days = st.slider('Forecast Days', min_value=1, max_value=5, value=1,
                 help="Select the amount of day to be forecasted")

option = st.selectbox('Select data to view', ('Temperature', 'Sky'))

st.subheader(f"{option} for the next {days} days in {place}")

place_exists = False

if place:  # only when user enters place
    try:
        filtered_data = get_data(place, days)
        place_exists = True
    except KeyError:
        st.info("We dont have information for your selected place")
        place_exists = False

if option == "Temperature" and place_exists:
    temperatures = [dict_of_data['main']['temp'] - 273.15 for dict_of_data in filtered_data]
    dates = [dict_of_data['dt_txt'] for dict_of_data in filtered_data]
    figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
    # x is an array of data (could be a list)
    st.plotly_chart(figure)
    # gets a figure object which we can get from plotting library (plotly)

if option == "Sky" and place_exists:  # Clear, Clouds, Rain, Snow
    images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
              "Rain": "images/rain.png", "Snow": "images/snow.png"}
    sky_conditions = [dict_of_weather['weather'][0]['main'] for dict_of_weather in filtered_data]
    st.image([images[weather_condition] for weather_condition in sky_conditions], width=100)

    times = []
    for item in filtered_data:
        times.append(item['dt_txt'])

    st.info("Times:")
    st.write(times)
