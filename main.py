#IMPORTING JUMPAD
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import pyjokes
from datetime import timedelta
from time import strftime
import webbrowser
import subprocess
import urllib
import speech_recognition as sr
import pyttsx3
import pytz
import threading
import smtplib
from email.mime.text import MIMEText  
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import config
import remind
import bot
#---------------------------------------
SCOPES = ['https://www.googleapis.com/auth/calendar']
MONTHS = ["january","february"," march","april","may","june","july","august","september","october","november","december"]
DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
DAY_EXTENTIONS = ["rd","th","st","nd"]
WAKE = "hi everly"
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def get_audio():
    r =sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said=""
    
        try:
            said = r.recognize_google(audio)
            print("Me: " +said)
        except Exception as e:
            print("I couldn't hear you " + str(e))
            speak("I couldn't hear you")
    return said

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greetMe(): 
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        print("Everly :Hello and Good Morning! \n How are you doing today?")
        print("Happy \n Sad \n Joyful \n disappointed")

        speak("Hello! Good Morning! How are you doing today?")
    elif hour>=12 and hour<18:
        print("Everly: Hello and Good Afternoon! How are you doing today?")
        print("Happy \n Sad \n Joyful \n disappointed")

        speak("Hello and Good Afternoon! How are you doing today?")
    else:
        print("Everly: Hello and Good Evening! How are you doing today?")
        print("Happy \n Sad \n Joyful \n disappointed")

        speak("Hello and Good Evening! How are you doing today?")


def makeJoke():
    joke=pyjokes.get_joke(language='en', category= 'neutral')
    print("Everly:"+joke)
    speak("Here is a joke for you."+joke)

def givetime():
    current=strftime("%I:%M")
    print("Everly: Current time is" + " " + current)
    speak("Current time is" + current)

def giveDate():
    dateT=strftime("%B:%d:%A:%Y")
    print("Everly: Today's date is "+dateT)
    speak("Today's date is "+dateT)

def giveday():
    dateT=strftime("%A")
    print("Everly: Today is " + dateT)
    speak("Today is " + dateT)

def givemonth():
    dateT=strftime("%B")
    print( "Everly: "+ dateT)
    speak( dateT)

def openGmail(): 
        print("Everly: Opening Email Client")
        speak("Opening Email Client")
        url="https://mail.google.com/mail/u/0/#inbox"
        webbrowser.get().open(url)

def Gmail(said):
        search_term = said.split("from")[-1]
        url = "https://mail.google.com/mail/u/4/#search/" + search_term
        webbrowser.get().open(url)
        print("Everly: Here is what I found for " + search_term + "in gmail ")
        speak("Here is what I found for " + search_term + "in gmail")

def Drive(said): 
        print("What do you remember about file")
        speak("What do you remember about file")
        search_term = get_audio()
        url = "https://drive.google.com/drive/u/4/search?q=" + search_term
        webbrowser.get().open(url)
        print("Everly: Here is what I found for " + search_term + "in drive ")
        speak("Here is what I found for " + search_term + "in drive")

def Youtube(said): 
        search_term = said.split("for")[-1]
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        print("Everly: Here is what I found for " + search_term + "on youtube ")
        speak("Here is what I found for " + search_term + "on youtube")

def Google(said):
        search_term = said.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        print("Everly: Here is what I found for" + search_term + "on google")
        speak("Here is what I found for" + search_term + "on google")

def weather(said):
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        print("Everly: Here is what I found for on google")
        speak("Here is what I found for on google")

def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(day, service): #get your schedule for a particular date
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12)
                start_time = start_time + "pm"

            speak(event["summary"] + " at " + start_time)

def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:  
        year = year+1

    
    if month == -1 and day != -1:  
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  
        return datetime.date(month=month, day=day, year=year)

def create_event(said,service): 
    print("When do you have this event")
    speak("When do you have this event")
    text = get_audio().lower()
    date= get_date(text)
    print("what is the event")
    speak("what is the event")
    summary = get_audio().lower()
    start = date.isoformat()
    event_result = service.events().insert(calendarId='primary',
       body={
           "summary": summary,
           "description": '',
           "start": {"date": start, "timeZone": 'Asia/Kolkata'},
           "end": {"date": start, "timeZone": 'Asia/Kolkata'},
            }
                                          ).execute()
    print("Everly: Created event")
    speak("I have created this event")
    print("summary: ", event_result['summary'])
    print("starts on: ", event_result['start']['date'])
    speak(event_result["summary"]  + " on " + start)

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

def song(said):
        search_term = said.split("play")[-1]
        url="https://open.spotify.com/search/"+search_term
        webbrowser.get().open(url)
        print("Everly: playing song" + search_term + "on spotify ")
        speak(" playing song" + search_term + "on spotify ")

def loc(said):
        search_term = said.split("is")[-1]
        url="https://www.google.com/maps/place/"+search_term
        webbrowser.get().open(url)
        print("Everly: showing " + search_term +" on google maps ")
        speak("showing " + search_term + "on google maps")

def send_mail():
    print("whom do you want to send?")
    speak("whom do you want to send? Enter the id")
    send_to=input()
    print("what is the subject?")
    speak("what is the subject?")
    sub = get_audio()
    print("what is the message?")
    speak("what is the message?")
    m = get_audio()
    EMAIL=config.EMAIL
    PASSWORD=config.PASSWORD
    server.login(EMAIL,PASSWORD)

    message=MIMEText(m)
    message["From"]=EMAIL
    message["To"]=send_to
    message["Subject"]=sub

    server.sendmail(EMAIL,send_to,message.as_string())

    print("Mail is successfully sent")
    speak("Mail is successfully sent")

def news():
  site = 'https://news.google.com/news/rss'
  op = urlopen(site) 
  rd = op.read() 
  op.close()   
  sp_page = soup(rd,'xml') 
  news_list = sp_page.find_all('item')    
  n=[]
  for news in news_list :
   n.append(news.title.text)

  for i in range(6):
    print(n[i])
    speak(n[i])
    speak("!!")

SERVICE = authenticate_google()
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

def chat():
    while True:
            print("Listening")
            text = get_audio().lower()
            if "hello" in text:
                    print("Hello! I am everly your personal voice assistant, How may i help you?")
                    speak("Hello! I am everly your personal voice assistant, How may i help you?")
            elif "what is your name" in text:
                    print("My name is Everly")
                    speak("My name is Everly")
            elif "are you a robot" in text:
                    print("Yes, I am a robot and That makes it ideal for keeping things you share with me private.")
                    speak("Yes, I am a robot and That makes it ideal for keeping things you share with me private.")
            elif "are you a human" in text:
                    speak("Nope, I am a robot. That makes it ideal for keeping things you share with me private.")
            elif "who are you" in text or "define yourself" in text: 
                    speak ("Hello, I am Everly. Your personal Assistant. I am here to make your life easier. You can command me to perform various tasks")
                    print("Hello, I am Everly. Your personal Assistant. I am here to make your life easier. You can command me to perform various tasks")
            elif "who made you" in text or "created you" in text: 
                  print("I have been created by a group of amazing humans.")
                  speak("I have been created by a group of amazing humans.")
            elif "joke" in text:
                    makeJoke()
            elif "time" in text:
                    givetime()
            elif "date" in text:
                    giveDate()
            elif "day" in text:
                    giveday()
            elif "month" in text:
                    givemonth()
            elif "gmail" in text and 'from' not in text:
                    openGmail()  
            elif "youtube" in text:
                    Youtube(text)
            elif "search for" in text and 'YouTube' not in text:
                    Google(text)
            elif "weather" in text:
                    weather(text)
            elif "mail from" in text:
                    Gmail(text)  
            elif "drive" in text:
                    Drive(text)   
            elif "what do i have" in text or "do i have plans" in text or "am i busy" in text:
                date = get_date(text)
                get_events(date, SERVICE)
            elif "make a note" in text or "write this down" in text or "remember this" in text:
                speak("What would you like me to write down? ")
                print("What would you like me to write down? ")
                write_down = get_audio()
                note(write_down)
                speak(" I've made a note of that.")
                print(" I've made a note of that.")
            elif "add event"in text:
                    create_event(text,SERVICE)
            elif "send mail" in text:
                send_mail()       
            elif "add reminder" in text:
                remind.add_remind()
            elif "reminders for today" in text:
                remind.read_reminder()
            elif "play" in text:
                song(text)
            elif "where is" in text:
                loc(text)
            elif "news" in text:
                print("Some of the latest news are")
                speak("Some of the latest news are")
                news()
            elif "sad" in text or "disappointed" in text:
               print("I want to know how you feel today? Could you please answer few questions for me? \n (YES/NO)")
               speak("I want to know how you feel today!!!!! Could you please answer few questions for me? Please reply with yes or no")
               res = get_audio().lower()
               if res == "yes":
                  bot.therapy()
               else:
                   print("Ok! Everything will be fine")
                   speak("Ok! Everything will be fine")
                   break
            elif "happy" in text or "joyfull" in text:
                print("I am glad to know that! Have a good day . I can do some tasks for you if you want!")
                speak("I am glad to know that! Have a good day . I can do some tasks for you if you want!")
            elif "quit" in text or "bye" in text or "exit" in text:
                    speak("I could continue more, but ok byee")
                    print("I could continue more, but ok byee")
                    exit()
            
def main():
    print("Start")
    text = get_audio().lower()
    if text.count(WAKE) > 0:
      greetMe()
      while True:
        chat()
    
   
if __name__ == '__main__':
   main()

   
