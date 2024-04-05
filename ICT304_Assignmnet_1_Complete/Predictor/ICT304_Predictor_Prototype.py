#THINGS TO BE INCLUDED IN FINAL VERSION
    #adding new items handled correctly (currently not handled so training and predicting wont work with items with no sale history)
    #averaging data from month over days in month (this should hopefully make the model mor accurate but may cause issues in prediction)
    #normalising (may inprove accuracy but may also impact the predictions)
    #paramater tuning (increase accuracy of model)

#CURRENT ISSUES
    #daily predictions are way out
    #current adding of days has many 0 qty and jumps to high tens when there was data present in the origional dataframe (throwing out the model)
    #testing currently not working in this format (but working in original .ipyn file)

    
    
#imports not sure if needed in both functions so just gonna put them here for now (change as needed)
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error
import calendar
import datetime
import pickle

def train():
    try:
        #create variables
        dfList=[]
        splitY=[]
        dateRange = []
        extendedSplit = []
        models = []
        fitted = []
    
        #reads csv (may want to change to passed csv not sure how you want to do it)
        df = pd.read_csv("invoices_tester.csv")
        df.drop(columns=['itemName', 'itemDesc'], errors='ignore', inplace=True)
    
        #sets date invoiced as index then removes column
        df.index = pd.to_datetime(df['dateInvoiced'])
        df.drop(columns=['dateInvoiced'], inplace=True)
        df.index = pd.DatetimeIndex(df.index).to_period('D')
    
        #gets all item IDs
        items = df['itemID'].unique()

        #splits df into array of dataframes based off item ID
        for ID in items:
            temp = df[df['itemID'] == ID].copy()
            dfList.append(temp)
    
        #extracts the item QTY from each df in array
        for item in dfList:
            splitY.append(item[['itemQTY']])
    
        #gets range of dates for each item df
        for split in splitY:
            dateRange.append(pd.date_range(start=split.index[0].to_timestamp(), end=split.index[-1].to_timestamp()))
    
        #converts ranges to dataframe
        for ranges in dateRange:
            extended_split_data = pd.DataFrame(index=pd.concat([pd.Series(ranges)]))
            extendedSplit.append(extended_split_data)
    
        #adds corrosponding item QTY or 0 if no matching found
        for i, split in enumerate(extendedSplit):
            for index in split.index:
                # Check if the index exists in the itemQTY dataframe
                if index in splitY[i].index:
                    split.loc[index, 'itemQTY'] = splitY[i].loc[index].values[0]
                else:
                    split.loc[index, 'itemQTY'] = 0
    
        #creates model and adds it to array with 
        for split in extendedSplit:
            split.index = pd.DatetimeIndex(split.index).to_period('D')
            model = SARIMAX(split, order=(10, 0, 0), trend='ct')
            models.append(model)
            fitted.append(model.fit())
    
        #saves fitted for predict
        with open('fitted.pkl', 'wb') as f:
            pickle.dump(fitted, f)
    
        #saves items for predict
        with open('items.pkl', 'wb') as f:
            pickle.dump(items, f)
        
        return True
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def predict():
    try:
        #create variables
        forecast = []
        holderFore = []
        collected = []
        i=0
        
        #loads fitted that was saved
        with open('fitted.pkl', 'rb') as f:
        fitted = pickle.load(f)
        
        #loads items that was saved
        with open('items.pkl', 'rb') as f:
        items = pickle.load(f)
        
        #getting the qty forecast from fitted models
        for fit in fitted:
            forecast.append(fit.forecast(steps=30))
            
        #combine the days into prediction for 1 month
        for fore in forecast:
            holderPred = 0
            for pred in fore:
                holderPred += pred
            holderFore.append(round(holderPred))
            i += 1
        
        #combines item ID and combined predictions into an array
        for item, holderPred in zip(items, holderFore):
            collected.append([item, holderPred])
        
        #returns array
        return collected
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None