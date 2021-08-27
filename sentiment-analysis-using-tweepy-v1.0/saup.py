from textblob.blob import TextBlob
import tweepy
import cred
import textblob
import matplotlib.pyplot as plt
from tkinter import *
# make a connection
# this function will setup a connection with twitter API and do authentication
def authenticateTwitterAPI(con_key,con_secret):
    try:
        # create a auth instance
        auth = tweepy.AppAuthHandler(consumer_key=con_key,consumer_secret=con_secret)
        # WE ARE USING OAUTH2 ,HENCE NO ACCESS TOKEN OR ACCESS KEY IS REQUIRED
        # then create an API instance
        api = tweepy.API(auth)
        return api
    except:
        return False

# search a term using twitter API and get the result
# This function will search a specific term using API.search and do pagination with cursor
def searchInTwitter(api,searchTerm,tweetNo):
    try:
        return tweepy.Cursor(api.search, q=searchTerm).items(tweetNo)
    except:
        return False

# analyze using text blob
def analyzeText(tweets):
    pos = neg = neut = 0
    for tweet in tweets:
        # print(tweet.text)
        blob = TextBlob(tweet.text)
        # print(blob)
        for sentence in blob.sentences:
            pol = sentence.sentiment.polarity
            # print(pol)
            if(pol==0):
                neut+=1
            elif (pol>0):
                pos+=1
            else:
                neg+=1
    # return the analysis result
    return neut,pos,neg


# show the result
def showResult(analyzedData,searchTerm):
    labels = ["Neutral","Positive","Negetive"]
    data = list(analyzedData)
    # print(data)
    expld = [0,0,0]
    expld[data.index(max(data))] = 0.1
    plt.axis("equal")
    plt.pie(data,labels=labels,radius=1,autopct="%0.2f%%",explode=expld)
    plt.title(f"What people are thinking about {searchTerm} in Twitter")
    plt.show()

# function for initiating the analysis
def startAnalysis():
    try:
        searchTerm = st.get()
        tweetCount = int(tc.get())
    except:
        label3['text'] = "Oops! Something went wrong!"
    # now make the connection
    api = authenticateTwitterAPI(cred.API_KEY,cred.API_SECRET)
    # search
    if(api!=False):
        tweets = searchInTwitter(api,searchTerm,tweetCount)
        data = analyzeText(tweets)
        showResult(data,searchTerm)
    else:
        label3['text'] = "Oops! Something went wrong!"
        


# Driver code
if __name__ == "__main__":

    # making window instance
    root = Tk()
    root.geometry("400x400")
    root.title("Sentiment Analysis Program")
    # taking user input
    label1 = Label(root,text="Enter any term to analyze :",padx=20,pady=20)
    label2 = Label(root,text="Enter the number of tweets to perform analysis :",padx=20,pady=20)
    label3 = Label(root,text=" ",padx=30,pady=30)
    st = Entry(root)
    tc = Entry(root)
    label1.pack()
    st.pack()
    label2.pack()
    tc.pack()
    anlsBtn = Button(root,text="Analyze",command=startAnalysis,padx=10,pady=10)
    anlsBtn.pack(padx=20,pady=20)
    label3.pack()
    root.mainloop()
