# -*- coding: utf-8 -*-
"""coursework_2_v_01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bl2KYBbWwXz9VGH7FOJE3U7TKPcnzRrk
"""

import pandas as pd
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

"""##Dataset loading"""

df_spot=pd.read_excel("/content/drive/MyDrive/Datasets/sunspot_data.xlsx",sheet_name="spots1981-2017")
df_spot.drop(columns=["Unknown_var"],inplace=True)

df_spot.sample(5)

df_spot.info()

"""##checking null values"""

df_spot.isna().sum()

"""#Dropped null values from date and time column because want to convert these values into date time format with null values can't convert it"""

df_spot.dropna(subset=["Date","Time"],inplace=True)

df_spot.isna().sum()

"""##creating copy of dataset to play with"""

df_spot_copy=df_spot.copy()

"""to convert Date into datetime format first the date column is listed as float so changed it into into int to remove trailing zero then converted it into str to remove first two charachters of ID"""

df_spot_copy['Date']=df_spot_copy['Date'].astype(int)

df_spot_copy['Date']=df_spot_copy['Date'].astype(str)

df_spot_copy['Date']=df_spot_copy['Date'].str[2:]

df_spot_copy.sample(5)

"""used to_datetime function to convert it into date format"""

df_spot_copy['Date']=pd.to_datetime(df_spot_copy['Date'],format="%y%m%d",errors='coerce')

df_spot_copy.sample(5)

"""now have to convert time column into time format"""

df_spot_copy['Time'].info()

"""it's also listed as float so have to convert it into int then str"""

df_spot_copy['Time']=df_spot_copy['Time'].astype(int)

df_spot_copy.sample(5)

df_spot_copy['Time'].info()

"""now we can see it's in the integer format next step is to convert it into str"""

df_spot_copy['Time']=df_spot_copy['Time'].astype(str)

df_spot_copy.sample(5)

df_spot_copy['Time'].info()

df_spot_copy['Time']=pd.to_datetime(df_spot_copy['Time'],format="%H%M",errors="coerce").dt.time

df_spot_copy.sample(5)

df_spot_copy.isna().sum()

df_spot_copy.info()

df_spot_copy['Number of sunspots'].unique()

plt.figure(figsize=(28,6))
plt.plot(df_spot_copy['Date'],df_spot_copy['Number of sunspots'])
plt.xlabel("Years")
plt.ylabel("Xray_flux")
#plt.yscale("log")

"""we can clearly see the 11 year solar cycle solar minimum and solar maximum

---
this also verifes our asumption from flares data set where we see high xray flux around 2002 which is the solar maximum time

---
Can you visually identify a pattern of sunspots that are most likely to
produce significant flares?

---

i think this graph here and the other graph in flare dataset answer this question when the number of sunspot is high, they are producing X class or M class flares we can see this through these two graphs


"""

start_date=pd.to_datetime("1996-01-01")
end_date=pd.to_datetime("2008-12-01")
filtered_df = df_spot_copy[(df_spot_copy['Date'] >= start_date) & (df_spot_copy['Date'] <= end_date)]

filtered_df.sample(5)

plt.figure(figsize=(20,8))
plt.plot(filtered_df['Date'],filtered_df['Number of sunspots'])
plt.xlabel("Years")
plt.ylabel("number of Spots")
#plt.yscale("log")

"""complete solar cycle start from 1996 end at 2008"""

df_spot_copy_1=df_spot_copy.copy()

df_spot_copy_1.set_index('Date', inplace=True)

df_spot_copy_1.head()

monthly_mean = df_spot_copy_1['Number of sunspots'].resample('M').mean()
monthly_mean

plt.figure(figsize=(28,6))
plt.plot(monthly_mean.index, monthly_mean, label='Monthly Mean Sunspots', linestyle='-', color='blue')
plt.ylabel("sunspots number mean")
plt.xlabel("years")
plt.title("Monthly mean number of Sunspots")

df_spot_copy.to_csv("/content/drive/MyDrive/Datasets/sunspot_dataset_v1.csv",index=False)

"""###Model for Sunspot Prediction"""

#copy of data set
model_df=df_spot_copy.copy()

model_df.head()

"""##Cleaning dataset for model building"""

model_df.drop(columns=["Time","Location","Mount Wilson Class","individual date","regional date","station_number","observartories","Region_number"],inplace=True)

model_df.head()

model_df.isna().sum()

"""dropping rows with null values in region number and date and filling the null values of number of sunspots, length , area with the mean of that"""

model_df.dropna(subset=["Date"],inplace=True)

model_df['Number of sunspots']=model_df['Number of sunspots'].fillna(model_df['Number of sunspots'].mean())
model_df['length']=model_df['length'].fillna(model_df['length'].mean())
model_df['area']=model_df['area'].fillna(model_df['area'].mean())

model_df.isna().sum()

"""#transformation of McIntosh_class"""

model_df[['Class0', 'Class1', 'Class2',"Class3"]] = model_df['McIntosh_class'].str.split('', expand=True).iloc[:, 1:5]
model_df.head()

model_df.drop(columns=["Class0","McIntosh_class"],inplace=True)

class_1={"A":0.10,"H":0.15,"B":0.30,"C":0.45,"D":0.60,"E":0.75,"F":0.90}
class_2={"X":0,"R":0.10,"S":0.30,"A":0.50,"H":0.70,"K":0.90}
class_3={"X":0,"O":0.10,"C":0.90,"I":0.50}

def map_class_1(class_1_value):
    return class_1.get(class_1_value, pd.NA)

def map_class_2(class_2_value):
    return class_2.get(class_2_value, pd.NA)

def map_class_3(class_3_value):
    return class_3.get(class_3_value, pd.NA)

model_df["numeric_class_1"]=model_df['Class1'].apply(map_class_1)
model_df["numeric_class_2"]=model_df['Class2'].apply(map_class_2)
model_df["numeric_class_3"]=model_df['Class3'].apply(map_class_3)

model_df.sample(5)

"""#cleaning this transformed dataset"""

model_df.isna().sum()

model_df.dropna(subset=["numeric_class_1","numeric_class_2","numeric_class_3"],inplace=True)

model_df.isna().sum()

model_df.drop(columns=["Class1","Class2","Class3"],inplace=True)

model_df.head()

plt.figure(figsize=(28,6))
plt.plot(model_df['Date'],model_df["Number of sunspots"])

model_df.shape

filtered_df=model_df[model_df['Date']>="2001-12-01"]

plt.figure(figsize=(28,6))
plt.plot(filtered_df['Date'],filtered_df["Number of sunspots"])

filtered_df.shape

model_df.head()

model_df["Month"]=model_df['Date'].dt.to_period('M')

mean_value=model_df.groupby("Month")["Number of sunspots"].mean().reset_index()
mean_value

mean_value.info()

mean_value.isnull().sum()

mean_value['Number of sunspots'].shape

mean_value['Month'].shape

"""####Monthly Mean number of sunspots"""

monthly_mean = df_spot_copy_1['Number of sunspots'].resample('M').mean()

X=monthly_mean.values
y=monthly_mean.index

print(X.shape)
print(y.shape)

print(type(X))

df = pd.DataFrame({"date": y, "value": X})
df = df.set_index("date")

df["month"] = df.index.month
df["day_of_week"] = df.index.dayofweek
df["lag_1"] = df["value"].shift(1)  # Lag feature (example)

df.head()

plt.figure(figsize=(28,6))
plt.plot(df.index,df['value'])

df.isna().sum()

df.dropna(inplace=True)

df.isna().sum()

"""##XGBoost Regressor


"""

X = df.drop("value", axis=1)  # Features
y = df["value"]  # Target variable

X_train=X.iloc[0:240,0:5]
X_test=X.iloc[241:,0:5]

y_train=y.iloc[0:240]
y_test=y.iloc[241:]

#from sklearn.model_selection import train_test_split

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

import xgboost as xgb
model = xgb.XGBRegressor(n_estimators=110, max_depth=2, learning_rate=0.1, early_stopping_rounds=3)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)])

from sklearn.metrics import mean_absolute_error
predictions = model.predict(X_test)

# Evaluate performance
mae = mean_absolute_error(y_test, predictions)
print("MAE:", mae)

plt.figure(figsize=(28,6))
plt.plot(df.index,df['value'],label="Actual",linestyle="dotted")
plt.plot(X_test.index,predictions,label="predicted",linestyle="-")
plt.title("Predictions by XgBoost")
plt.legend()

"""###Linear Regression"""

from sklearn.linear_model import LinearRegression
model = LinearRegression()

# Fit the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, predictions)
print(f'Mean absolute Error: {mae}')

plt.figure(figsize=(28,6))
plt.plot(df.index,df['value'],label="Actual",linestyle="dotted")
plt.plot(X_test.index,predictions,label="predicted",linestyle="-")
plt.title("Predictions by Linear Regression")
plt.legend()

"""##Random Forest Regressor"""

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Fit the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
print(f'Mean absolute Error: {mae}')

plt.figure(figsize=(28,6))
plt.plot(df.index,df['value'],label="Actual",linestyle="dotted")
plt.plot(X_test.index,predictions,label="predicted",linestyle="-")
plt.title("Predictions by Random Forest Regressor")
plt.legend()

"""##DecisionTreeRegressor"""

from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor(random_state=42)

# Fit the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean absolute Error: {mae}')

plt.figure(figsize=(28,6))
plt.plot(df.index,df['value'],label="Actual",linestyle="dotted")
plt.plot(X_test.index,predictions,label="predicted",linestyle="-")
plt.title("Predictions by DecisionTreeRegressor")
plt.legend()

"""##Gradient Boosting Regressor:"""

from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)

# Fit the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean absolute Error: {mae}')

plt.figure(figsize=(28,6))
plt.plot(df.index,df['value'],label="Actual",linestyle="dotted")
plt.plot(X_test.index,predictions,label="predicted",linestyle="-")
plt.title("Predictions by Gradient Boosting Regressor")
plt.legend()

"""This is giving best results

##Support Vector Regression (SVR):
"""

from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize the Support Vector Regressor model
model = SVR(kernel='rbf', C=1.0, epsilon=0.1)

# Fit the model on the training data
model.fit(X_train_scaled, y_train)

# Make predictions on the test data
predictions = model.predict(X_test_scaled)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean absolute Error: {mae}')

plt.figure(figsize=(28,6))
plt.plot(df.index,df['value'],label="Actual",linestyle="dotted")
plt.plot(X_test.index,predictions,label="predicted",linestyle="-")
plt.title("Predictions by Support Vector Regression (SVR)")
plt.legend()

"""filtered_df['Date'],filtered_df['Number of sunspots']"""