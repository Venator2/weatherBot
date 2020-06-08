import requests


class Weather():
    def weather_data(self, query):
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?' +
                         query+'&appid=ac7c75b9937a495021393024d0a90c44&units=metric')
        return r.json()

    def out_temp(self, result):
        temp = "{}'s temperature : {}°C ".format(
            result['name'], result['main']['temp'])
        wind = "Wind speed:{} m/s".format(result['wind']['speed'])
        weather = "Weather:{}".format(result['weather'][0]['main'])
        desc = "Description:{}".format(result['weather'][0]['description'])

        message = "\n".join([temp, wind, weather, desc])
        return message

    def temp(self, lat, lon):
        query = 'lat='+lat+'&lon='+lon
        data = self.weather_data(query)
        return self.out_temp(data)


w = Weather()
