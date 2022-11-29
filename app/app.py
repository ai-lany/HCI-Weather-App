from flask import Flask
import requests
import json
import streamlit as st
import pandas as pd
import numpy as np
import utils
import os

API_KEY = '5ae705c7-4dbf-4eba-ae61-183c137c4400'
COUNTRIES_URL = 'https://api.airvisual.com/v2/countries?key={}'.format(API_KEY)



@st.cache
def getCountries():
    response = requests.get(COUNTRIES_URL).json()
    print(response)
    return response

@st.cache
def getStates(country):
    STATES_URL = 'https://api.airvisual.com/v2/states?country={}&key={}'.format(country,API_KEY)
    response = requests.get(STATES_URL).json()
    print(response)
    return response

@st.cache
def getCities(country, state):
    CITY_URL = 'https://api.airvisual.com/v2/cities?state={}&country={}&key={}'.format(state,country,API_KEY)
    print(CITY_URL)
    response = requests.get(CITY_URL).json()
    return response

@st.cache
def getAirQuality(country, state, city):
    AIRQUALITY_URL = 'https://api.airvisual.com/v2/city?city={}&state={}&country={}&key={}'.format(city, state, country, API_KEY)
    response = requests.get(AIRQUALITY_URL).json()
    return response


def getDataFromFile(fileName):
    f = open(fileName)
    return json.load(f)


st.title('Air Quality')

COUNTRIES = getCountries()
Countries = list[dict[str,str]]
if COUNTRIES['status'] != 'success':
    COUNTRIES = getDataFromFile('countries.JSON')
COUNTRIES_LIST:Countries = COUNTRIES['data']  

country =  st.selectbox(
            'Country',
            [c['country'] for c in COUNTRIES_LIST]
        )

STATES = getStates(country)
if STATES['status'] == 'success':
    state =  st.selectbox(
                'State',
                [s['state'] for s in STATES['data']]
            )
    CITIES = getCities(country, state)
    if CITIES['status'] == 'success':
        city = st.selectbox(
                'City',
                [c['city'] for c in CITIES['data']]
            )
        airQuality = getAirQuality(country, state, city)
        coordinates = airQuality['data']['location']['coordinates']
        utils.map_creator(coordinates[0],coordinates[1])
