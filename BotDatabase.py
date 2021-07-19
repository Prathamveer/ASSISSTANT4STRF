import pickle
import assist
import random

l1 =[" ","never","sometimes","most often","always"]
q =["Do you feel sad and depressed often?",
"Have you had a poor appetite or been overeating?",
"Do you feel tired No matter how much you sleep?",
"Do you feel scared without any good reason?",
"Do you find it difficult to relax?",
"Do you tend to over-react to situations?",
"Do you find it hard to calm down after something upset you?",
"Do you find it difficult to adapt to changes in your surrounding?",
"Do you feel that you have lost interest in just about everything?",
"Do you find it difficult to work up the initiative to do things?",
"Do you find it difficult to tolerate interruptions to what you are doing?",
"Do you seem to Not get any enjoyment out of the things you did?",
"Do you feel that life isn't worthwhile?",
"Do you have a feeling of shakiness often (eg, legs going to give way)?",
"Can you see something in the future to be hopeful about?",
"Do you find yourself in situations that make you so anxious that you were most relieved when they ended?",
"Do you seem to experience No positive feeling at all?",
"Do you experience breathing difficulty (eg, excessively rapid breathing, breathlessness in the absence of physical exertion)?",
"Do you feel your body or hands become sweaty even in the absence of high temperatures or physical exertion?",
"Do you have thoughts that you would be better off dead, or of hurting yourself?"]
a=['']

no_dep =["Everything is going to be fine!","sometimes even the wrong train takes us to the right station. You probably should grab a good book or Order some good food or may be watch some netflix.",]

mild_dep =["You should go out for a movie",
           "I think Jogging or walking might really help you to overcome this situation",
           "You might like listening to some music.",
           "You should try playing a team sport with your friends.",
           "You may love learning to play some musical instrument like guitar or piano",
           "Why don't you try gardening,Trust me its so much fun!!",
           "May be Go out swimming if you are a water baby",
           "How about Cooking or baking? You should definately try some amazing recipes.",]

ext_dep = ["Cheer up champ!! Sometimes its ok to be not ok! Nurture yourself with good nutrition, Depression can affect your appetite, You may not feel like eating at all, or sometimes might overeat!! If depression has affected your eating, you'll need to be extra mindful of getting the right nourishment, Proper nutrition can influence your mood and energy! So eat plenty of fruits and vegetables, and get regular meals! Even if you don't feel hungry, try to eat something light, like a piece of fruit, to keep you ", 
           "Hey!! You are not alone , its just a phase and its gonna pass, When you know, what's got you feeling blue and why, talk about it with a caring friend! Talking will release the feelings, Once you air out these thoughts, and feelings, you tend to look towards the bright side,, Feeling connected to friends and family,, can help you relieve depression, They might help you to fill the void!! or ekk baaat bolu??,  jab tum smile karta hain naa, toh essa lagta hain kee, keyaa maasst life hainn yaar!",
           "Bud may be its time to buckle up by involving in some activity. With depression, your creativity and sense of fun may seem blocked to you. Exercise your imagination by painting, drawing, doodling, sewing, writing, dancing or composing music, and you not only get those creative juices flowing, but you will also loosen up some positive emotions. “Ziinddaghie main teen cheezain kabhee underestimate nahi karna ! I, ME and MYSELF!!” You got this!!"]
comp ="DISCLAIMER: Please consult a doctor if you persist to feel the same for longer period of time.There is nothing wrong in taking some help, we all need it at some point of time in life. Look around life is beautiful bud!"          


def therapy():
  
  print("Choose the one that applies to you \nNever \nSometimes \nmost often \nalways")
  assist.speak("Choose the one that applies to you!!!! Never, Sometimes, most often, always ")

  with open('model_pickle','rb') as f:
      mod = pickle.load(f)
  
  for i in q :
      while True:  
        print(i)
        assist.speak(i)
        aa1= assist.get_audio()
        if aa1=="never" or aa1== "sometimes" or aa1 =="most often" or aa1=="always":
          a1 = l1.index(aa1)
          a.append(a1)
          break
        else:
          print("please try again.")
          assist.speak("please try again")

      if i==q[13]:
          pred = mod.predict([[a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12],a[13],0,0,0,0,0,0,0]])
          
          if pred==['No']:
            print("Looks like everything is GOOD")
            assist.speak("Looks like everything is GOOD")
            print("So now I have some suggestions you might like!")
            assist.speak("So now I have some suggestions you might like!")
            while True:
              show=random.choice(no_dep)
              print(show)
              assist.speak(show)
              print("Are you excited to do this?")
              assist.speak("Are you excited to do this?")
              ans = assist.get_audio().lower()
              if ans=="yes":
                exit()
          
          else:
            continue
    

  pred = mod.predict([[a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12],a[13],a[14],a[15],a[16],a[17],a[18],a[19],a[20]]])
  
  if pred == ['No']:
     print("You have symptoms of mild depression, but nothing to worry about, we can work it out together. ")
     assist.speak("You have symptoms of mild depression, but nothing to worry about, we can work it out together! ")
     print("So now I have some suggestions you might like!")
     assist.speak("So now I have some suggestions you might like!")
     while True:
      show=random.choice(mild_dep)
      print(show)
      assist.speak(show)
      print("Are you excited to do this?")
      assist.speak("Are you excited to do this?")
      ans = assist.get_audio().lower()
      if ans=="yes":
        exit()
  else:
    print("This is worrisome, but dont panic!")
    assist.speak("This is worrisome, but dont panic!")
    print("I have some suggestions you might like!")
    assist.speak("I have some suggestions you might like!")
    while True:
      show =random.choice(ext_dep)
      print(show + "\n" + comp)
      assist.speak(show)
      print("Are you excited to do this?")
      assist.speak("Are you excited to do this?")
      ans = assist.get_audio().lower()
      if ans=="yes":
          exit()

 

    
    
    