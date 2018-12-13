"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import requests


@route('/', method='GET')
def index():
    return template("chatbot.html")


count = 0


def hello(strg):
    global count
    count += 1
    # return "Hello {0}! How are you".format(strg)


def shout(msg):
    scream = msg.split("!")
    return 'Stop shouting! anyways, "{0}" is not worth screaming about!'.format(scream[0])


def question(msg):
    qstn = msg.split("?")
    return "I'm sorry I don't think I can reveal that kind of information. However, I think " \
           "Ilana knows '{0}', BUT remember YOU DIDN'T HEAR IT FROM ME! ".format(qstn[0])


def coding():
    return "no more CODING talk! How does that make you feel? "


def joke():
    r = requests.get('https://geek-jokes.sameerkumar.website/api')
    return r.text


def weather():
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?q=London&APPID=e1185ea30127a965cc653a5a4aa33689')
    weather_obj = json.loads(r.text)
    weather_list = weather_obj['list']
    first_list = weather_list[0]
    main_weather = first_list['main']
    temp = main_weather['temp']
    humidity = main_weather['humidity']

    return "The weather in london is now {0} Kelvin and {1}% humid".format(temp, humidity)


def response(strg):
    code = ["python", "java", " c ", "code", "html", "css", "function", "media query", "visual studios", "debug"]
    msg = strg.lower()
    global count
    if count == 0:
        return hello(strg)
    elif "!" in msg:
        return shout(msg)
    elif "?" in msg:
        return question(msg)
    elif any(word in msg for word in code):
        return coding()
    elif "joke" in msg:
        return joke()
    elif "weather" in msg:
        return weather()
    else:
        return msg


def emotion(strg):
    emotions = ("afraid", "bored", "confused", "crying", "dancing", "dog",
                "excited", "giggling", "heartbroke", "inlove", "laughing",
                "money", "no", "ok", "takeoff", "waiting")
    msg = strg.lower()
    for word in emotions:
        if word in msg:
            return word

    else:
        return "excited"


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": emotion(user_message), "msg": response(user_message)})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
