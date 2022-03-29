# -*- coding: utf-8 -*-
"""HW2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jIoyNkFsb8I614fYhgnd5DHc3QXUpcKR
"""

# the package needed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score, mean_squared_error

# Load data and transform "weedDay" to the type of "date".
df = pd.read_csv('/content/drive/MyDrive/HW2 regression dataset.csv', parse_dates= ['weekDay'])
df.head()

# "weekDay" columm has included all the time informtion so we drop the rows offering duplicated information.
df.drop(columns = ['observation','weeknumber','month','year'], inplace = True)

# type transforming
df['trustad'] = df['trustad'].astype('bool')

# calculate the boundary of "Seasonality" according to "eq_volum"
watershed = (df['eq_volum'].quantile(.75) - df['eq_volum'].quantile(.25))*1.5 + df['eq_volum'].quantile(.75)
print('watershed line:' + str(watershed))
df['season'] = 0
df.loc[df.loc[:,'eq_volum'] >= watershed, 'season'] = 1

# type transforming
df['season'] = df['season'].astype('bool')
print("date type: " + str(df.dtypes))

# Min Max Mean SD
description = df.apply((np.min,np.max,np.mean,np.std)) 

# round to keep concise
description = round(description, 2)

# mapping index
description.index = ['min', 'max', 'mean', 'sd']

# show summary statistics
description

# Plot
df_eq_volum_trending =df.pivot_table(index =df['weekDay'].dt.year, columns = df['weekDay'].dt.isocalendar().week, values = 'eq_volum').transpose()
sns.relplot(data = df_eq_volum_trending, kind = 'line');
plt.xlabel('Week');
plt.ylabel('EQ Volumn of Brand C');
plt.title('the Trendings of EQ volumn of Brand C');

# Plot
sns.relplot(kind = 'line', data = df[['price_c','price_e','price_p']]);
plt.ylabel('Price');
plt.xlabel('Observed Week');
plt.title('the Trending of each Brand');

# Plot
sns.relplot(kind = 'line', data = df, x = df.index, y = 'disacv_c', hue = df['weekDay'].dt.year);
plt.xlabel('Observed Week');
plt.ylabel('Brand C %ACV * % Discount');
plt.title('the Changing of Brand C %ACV * % Discount');

# Plot
sns.relplot(kind = 'line', data = df[['tvgrp_c','tvgrp_u']]);
plt.title('TV GRPs of Brand C & U');
plt.ylabel('Times');
plt.xlabel('Observed Week');

# Plot
sns.relplot(kind = 'line', data = df, x = df['weekDay'].dt.isocalendar().week, y = 'trustad', hue = df['weekDay'].dt.year, palette = ['red','yellow','green','black']);
plt.xlabel('Week');
plt.title('Theme of Brand C TV advertising focused on the message “Trusted');

# X-Y plot
sns.pairplot(kind = 'reg', data = df, x_vars=['disacv_c', 'bonusacv', 'price_c','price_e','price_p'], y_vars = 'eq_volum');
sns.pairplot(kind = 'reg',data = df, x_vars=['tvgrp_c','tvgrp_u', 'trustad', 'itemstor', 'walmart'], y_vars = 'eq_volum');
sns.pairplot(kind = 'reg',data = df, x_vars=['fsi_holi','fsi_non','fsi_comp',"season"], y_vars = 'eq_volum');

# Correlation between eq_volum and other variables
print(df.corr().iloc[:,0])

# All the correlations
df.iloc[:,2:].corr()

# Visualize the all the correlations
sns.heatmap(df.iloc[:,2:].corr(), cmap="RdBu");
plt.title('Correlation Visualization');

# Log-Transform
df['eq_volum'] = np.log(df['eq_volum'])

# Model including 10 variables
mod10 = ols('eq_volum ~ disacv_c + season + price_c + price_p + tvgrp_c + trustad + fsi_holi + fsi_non + fsi_comp + itemstor', data = df).fit()
print(mod10.summary())

# Model including 7 variables
mod7 = ols('eq_volum ~ disacv_c + season  + tvgrp_c + trustad + fsi_holi + fsi_comp + itemstor', data = df).fit()
print(mod7.summary())

# Linearity and moscedasticity of errors check
sns.relplot(kind = 'scatter', data = df, \
            x = mod7.predict(df), y = mod7.resid)
plt.axhline(y=0, color='r', linestyle='-')
print("        Correlation: " \
      + str(mod7.predict(df).corr(mod7.resid)))
plt.title('Linearity and moscedasticity of errors check');

# Normality of errors
sns.histplot(data = mod7.resid, bins = 15, kde=True, stat = 'percent')
print('     mean: ' + str(round(mod7.resid.mean(),2)))
print('     median: ' + str(round(np.median(mod7.resid),2)))
plt.title('Normality of errors');

# The comparsion between the actual and predict values.
plt.plot(mod7.predict(df), label = 'predict');
plt.plot(df['eq_volum'], label = 'actual');
plt.legend();
plt.title('The comparsion between the actual and predict values');

# The model fitted from 150 rows.
mod7_150 = ols('eq_volum ~ disacv_c + season  + tvgrp_c + trustad + fsi_holi + fsi_comp + itemstor', data = df.iloc[:150,:]).fit()
print(mod7_150.summary())

y_pre_150 = mod7_150.predict(df.iloc[:150,:])

#Overfitting Check
print('MSE for Train set: ' + str(mean_squared_error(df.iloc[:150,:]['eq_volum'], y_pre_150)))
print('MSE for Test set:  ' + str(mean_squared_error(df['eq_volum'].iloc[150:], mod7_150.predict(df.iloc[150:,:]))))

# The comparison between the last 29 weeks
plt.plot(mod7_150.predict(df.iloc[150:,:]), color = 'red', label = 'Predict');
plt.plot(df['eq_volum'].iloc[150:], label = 'Actual');
plt.legend();
plt.title('The comparison between the last 29 weeks');

pred = pd.DataFrame({'season': [1, 1],
                    'trustad':[1, 0],
                    'disacv_c':[9.2, 9.2],
                    'tvgrp_c':[0, 0],
                    'fsi_holi':[0, 0],
                    'fsi_comp':[0, 0],
                    'itemstor':[8.5, 8.5]})

eq_volum_pred = round(np.exp(mod7.predict(pred)),2)
eq_volum_pred.index = ['with trusted ad','without trusted ad']
print(eq_volum_pred)
print('The difference between "with trusted ad" and "without trusted ad" is {}'.format(round(eq_volum_pred[0] - eq_volum_pred[1],2)))

eq_volum_pred[0]