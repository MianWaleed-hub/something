import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
class Models():
    def __init__(self):
        pass
    def convert(self,x):
        if (x < 0):
            return 'negative'
        elif x == 0:
            return 'neutral'
        else:
            return 'positive'

    def sentiment_analysis(self,sentiment):
        cont_len=len(sentiment)
        sentiment = re.sub('[^ A-Za-z]+', ' ', sentiment)
        sid = SentimentIntensityAnalyzer()
        sentiment=sid.polarity_scores(sentiment)
        cont_sent=self.convert(sentiment['compound'])
        cont_pol=sentiment['compound']
        return cont_len,cont_sent,cont_pol

    def ohe(self,cont_sent):
        if(cont_sent == 'negative'):
            sent_neg=1
            sent_neut=0
            sent_pos=0
        elif(cont_sent =="positive"):
            sent_neg=0
            sent_neut=0
            sent_pos=1
        else:
            sent_neg=0
            sent_neut=1
            sent_pos=0
        return sent_neg,sent_neut,sent_pos

    def predict_market(self,day,month,year,open,high,low,volume,sentiment):
        df=pd.read_csv('data.csv')
        cont_len,cont_sent,cont_pol= self.sentiment_analysis(sentiment)
        sent_neg,sent_neut,sent_pos=self.ohe(cont_sent)
        print(cont_len,cont_sent,cont_pol)
        print(sent_neg,sent_neut,sent_pos) 

        X=df[['date_year','date_month','date_day', 'open','high','low','volume','cont_len','cont_pol','sent_neg','sent_neu','sent_pos']]
        Y=df["close"]
        X_train,_, y_train,_ = train_test_split(X, Y, test_size = 0.3, random_state = 0)
        smodel = LogisticRegression()
        smodel.fit(X_train,y_train)
        return smodel.predict([[int(day),int(month),int(year),float(open),float(high),float(low),float(volume),int(cont_len),int(cont_pol),int(sent_neg),int(sent_neut),int(sent_pos)]])[0]

