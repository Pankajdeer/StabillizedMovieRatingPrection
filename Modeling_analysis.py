# -*- coding: utf-8 -*-
"""PythonCourseProject.ipynb

Automatically generated by Colaboratory.


## Importing libraries
"""



# Importing Libraries
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sn

pip install factor_analyzer

# PCA and Factor analysis libraries
from sklearn.decomposition import PCA as pca
from sklearn.decomposition import FactorAnalysis as fact
from sklearn import preprocessing
from factor_analyzer import FactorAnalyzer

# importing Slearn libraries for neural network modeling
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import metrics

# importing libraries for Multiple Regression using sklearn and 
from sklearn.linear_model import LinearRegression

# Regression alternative to sklearn: Using stats model library
import statsmodels.formula.api as smf

#imporing libraries for regres
import scipy.stats as sts
from scipy.stats.stats import pearsonr

#importing data for modeling analysis
data1_movies = pd.read_csv("/content/IMDB.csv")

data1_movies.head()

# columns in the data
data1_movies.columns

#dataset dimension
data1_movies.shape

#Exploraoty Data Analysis
#initial summary of the data
data1_movies.describe().T

#understanding the data type of the data
data1_movies.info()

#checking for missing values
data1_movies.isnull().sum()

"""- THere are **No** Missing values in this scrapped data from IMDB"""

#dropping the following unecessary and redudant variables in the analysis
data2_movies=data1_movies.drop(columns=['S.No','Language','Genre','Link','Country','Title','Release_Date'])

data2_movies.info()

data2_movies.First_Genre.describe()

#rearranging columns
data2_movies= data2_movies[['Rating', 'Budget', 'Opening_Week_Collection', 'Genre_no', 'Runtime','Director_Oscar', 'Director_Wins', 'Writer_Oscar', 'Writer_Wins','Actor_Oscar', 'Actor_Wins', 'perc_positive',     'perc_negative', 'perc_neutral', 'First_Genre']]
data2_movies.shape

#understanding the data distribution using Histogram plots
for a in range(0, 14):
    print(data2_movies.columns[a])
    sn.distplot(data2_movies.iloc[:,a])
    plt.show()

"""From the above plots we can observe that the following variables deviate from normal distribution heavily,
- perc_neutral
- Actor_Oscar
- Actor_Wins
- Director_Wins
- Director_Oscar
- Writer_Wins
- Writer_Oscar
"""

#boxplots of numeric variable to understand the distribution, for outlier observations
for a in range(0, 14):
    print(data2_movies.columns[a])
    sn.boxplot(data2_movies.iloc[:,a])
    plt.show()

"""From the above plots, we can observe that the following variables have outliers:


1.   Budget
2.   Opening week collection
3.   Director_Oscars
4.  Director_Wins
5. WriterOscar
6. Writer_Wins
7. Perc_positive
8. perc_negtive
9. perc_neutral

- Since, the previous achievements of the cast & crew in the team can indicate about thier technical capabilities, so we are not removing the values in the data.
"""

# creating a new derived variable:Percent_collected
data2_movies['percent_collected']=data2_movies['Opening_Week_Collection']/data2_movies['Budget']
sn.distplot(data2_movies.percent_collected)

data2_movies.columns

#rearrangin columns in the data fram
data2_movies =data2_movies[[ 'Budget', 'Opening_Week_Collection', 'Genre_no', 'Runtime', 'Director_Oscar', 'Director_Wins', 'Writer_Oscar', 'Writer_Wins','Actor_Oscar', 'Actor_Wins', 'perc_positive', 'perc_negative', 'perc_neutral', 'First_Genre', 'percent_collected','Rating']]

# Quick summary of the data with derived variable
data2_movies.describe().T

#Checking for colinearity
corr_matrix = data2_movies.corr()
corr_matrix

#heat map
corr_matrix.style.background_gradient(cmap='coolwarm')

"""- Since there is correlation between and budget and opening week collection, we are removing one variable and just keeping, 'budget' and 'percent_collected' (i.e. ratio of opening week collection to Budget)

- There is a correlation between these pairs of variables: {(Writer_Oscar,Writer_Wins);(Actor_Oscar,Actor_Wins);(Director_Wins,Director_Oscar)}. So we dropped one variable, from each pair in the modeling analysis to avoid rendundancies in the modeling
"""

#removing opening week collection from the data
data2_movies = data2_movies[[ 'Budget','percent_collected', 'Genre_no', 'Runtime', 'Director_Wins', 'Writer_Wins', 'Actor_Wins', 'perc_positive', 'perc_negative', 'perc_neutral', 'Rating']]

#performing PCA on the data
data_reduc_pca=data2_movies[['Budget','percent_collected', 'Genre_no', 'Runtime', 'Director_Wins', 'Writer_Wins', 'Actor_Wins', 'perc_positive', 'perc_negative', 'perc_neutral']]
column_names= data_reduc_pca.columns

data_reduc_pca_values = data_reduc_pca.values

data_reduc_pca.head()

data_reduc_pca.shape

pca_result = pca(n_components=10).fit(data_reduc_pca)

#Obtain eigenvalues
print(pca_result.explained_variance_)

#Components from the PCA
pca_result.components_.T * np.sqrt(pca_result.explained_variance_)

#screeplot
# Run this group of code together by highlighting it
# all and then running it

plt.figure(figsize=(7,5))
plt.plot([1,2,3,4,5,6,7,8,9,10], pca_result.explained_variance_ratio_, '-o')
plt.ylabel('Proportion of Variance Explained') 
plt.xlabel('Principal Component') 
plt.xlim(0.75,4.25) 
plt.ylim(0,1.05) 
plt.xticks([1,2,3,4,5,6,7,8,9,10])

factor_analysis = FactorAnalyzer(9,rotation='varimax')
factor_analysis.fit(data_reduc_pca)
factor_analysis.loadings_

factors_df = pd.DataFrame([[ 0.03726863, -0.11103787,  0.67636003, -0.00437127, -0.16380538,
         0.44408843, -0.18158685,  0.00585524,  0.        ],
       [ 0.03573954, -0.01735268, -0.24841462, -0.06536122,  0.60676961,
        -0.14738174,  0.00505092,  0.00440479,  0.        ],
       [ 0.05423231,  0.02947327,  0.06170408,  0.00104121, -0.07140883,
         0.58366693,  0.01083009, -0.00180704,  0.        ],
       [ 0.00164806,  0.00998904,  0.73390842,  0.18756439, -0.14476466,
        -0.03207198,  0.09140817, -0.00225299,  0.        ],
       [ 0.02316585,  0.11780202,  0.09670285,  0.6286117 , -0.01804783,
         0.01337571, -0.08288411, -0.07479069,  0.        ],
       [ 0.00972452,  0.07067651,  0.06671739,  0.50897734,  0.32724242,
         0.027691  ,  0.23699641,  0.00873821,  0.        ],
       [-0.0669422 , -0.07876635,  0.05629069,  0.54064543, -0.2960766 ,
        -0.03536999,  0.02390356,  0.11510088,  0.        ],
       [ 0.15114288,  0.98060357, -0.03996439,  0.09007717,  0.01588861,
         0.04373067,  0.01179664, -0.00763521,  0.        ],
       [-0.96605637, -0.23096824, -0.00444255, -0.01079629, -0.04511901,
        -0.08810645, -0.00225617,  0.00576225,  0.        ],
       [ 0.74492092, -0.65806326,  0.03942248, -0.06992726,  0.02697397,
         0.04142636, -0.00839165,  0.00151827,  0.        ]],columns = ["factor1", "factor2","factor3","factor4","factor5","factor6","factor7","factor8","factor9"],index=data_reduc_pca.columns)

factors_df

"""- Our target variable is "Rating" and the probable dependent variables for predicting the stabillised rating of the movie could be the following from the above data set.

"""
## Final Data used for modeling


data3_movies = data2_movies[[ 'Budget','percent_collected', 'Genre_no', 'Runtime', 'Director_Wins', 'Writer_Wins', 'Actor_Wins', 'perc_positive','perc_neutral', 'Rating']]

data3_movies.info()

"""dependent parameters considered in the model: 

1.   Budget
2.   Percent collected
3. perc_positive
4. perc_neutral
5. Director_Oscar
6. Director_Wins
7. Writer_Oscar
8. Writer_Wins
9. Actor_Oscar
10. Actor_Wins
11. First_Genre
12. Runtime

## Model1: Building Multiple Linear Regression
"""

#multiple regression model
regression1 = smf.ols('Rating ~ Budget+percent_collected+ perc_positive+perc_neutral+Director_Wins+Writer_Wins+ Actor_Wins+Runtime',data3_movies).fit()

"""### Summary of regression model"""

#regression model summary
regression1.summary()

"""Inference:
- Overall model is significant, based on the F-test result
- Above linear regression model explained the 24% of the variance in predicting the 'longterm rating' of a movie using the information collected after the first weekend when the movie is released

Validating assumption of Linear regression
1. Linearity Check:
"""

data1.plot.scatter(x='Budget',y='Rating')

"""- Visual Plot above seems very slight linear relation ship between rating and budget"""

data1.plot.scatter(x='perc_positive',y='Rating')
data1.plot.scatter(x='perc_neutral',y='Rating')
data1.plot.scatter(x='Runtime',y='Rating')

data1['percent_collected']

data1.plot.scatter(x='percent_collected',y='Rating')

"""- From the above plots, there seems a weak linear relation between %positve_tweets and rating variable. A similar, weak postive relation is identified between "% of neutral tweets" and "Rating"

- There seems a very good positve relation with Rating of the movie. Which is a new pattern observed in this data

- The movies which collected higher ratio of opening week collection to budget, has higher rating

### 2. Multicollinearity check

- Correlation matrix is developed among all the variables, to check the presence of multicillinearity in the data
"""

corr_matrix = data3_movies.corr()
corr_matrix.style.background_gradient(cmap='coolwarm')

"""- From the above table, based on the pearson correlation values among all possible pairs of variables it is observed that there isn't any strong observed among the variables
- There is a slight correlation between, "number of wins" by an actor and number of "oscars wons by actor"  which is about 0.499, we shall leave one out of these two variables in the modeling

### Assessing homoscedacity
"""

#Assess homoscedasticity
plt.scatter(linreg2.fittedvalues, linreg2.resid)
plt.xlabel('Predicted/Fitted Values')
plt.ylabel('Residual Values')
plt.title('Assessing Homoscedasticity')
plt.plot([0, 10],[0, 0], 'red', lw=2)   #Add horizontal line
plt.show()

"""- The above represent that the residuals are homoscedastic

### Normality of residuals check
"""

sts.probplot(linreg2.resid, dist="norm", plot=plt)

"""- From the the above plot, we can infer that the residuals are normally distributed

Since all the assumption as satisfied, we shall build the multiple regression model with sklean so that it is easier to compare the model performance with neural network models

### Building multiple Regression model with sklearn
"""

#splitting the data
x=data3_movies.iloc[:, :-1]
y=data3_movies.iloc[:,-1]

x.shape

from sklearn.utils import resample

#data partition (Train=100% with random state 1, test = 100% with random state 5)
tr=round(161*1)
te=round(161*1)
x_train=resample(x, n_samples=tr, replace=True,random_state=1)
y_train=resample(y, n_samples=tr, replace=True,random_state=1)
x_test=resample(x, n_samples=te, replace=True,random_state=5)
y_test=resample(y, n_samples=te, replace=True,random_state=5)
print("\n Total Difference among Dataset for Dependent variable \n",(x_train.mean()-x_test.mean()).sum())
print("\n % Difference among Dataset for Dependent variable \n",(x_train.mean()-x_test.mean())/x_test.mean())
print("\n Difference among Dataset for Target Variable \n",y_train.mean()-y_test.mean())

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

x_train.describe().T

x_test.describe().T

reg2 = LinearRegression(fit_intercept=True, normalize=True)
reg2.fit(x_train, y_train)

predict_reg2 = reg2.predict(x_test)

#model asssement1: Multiple Linear Regression
print("Multiple Linear Regression Results:")
print('Mean absolute error of test set is, ', round(metrics.mean_absolute_error(y_test, predict_reg2),4))

print('Mean squared error of test set is, ',round(metrics.mean_squared_error(y_test, predict_reg2),4))
print('Root Mean Squared Error:', round(np.sqrt(metrics.mean_squared_error(y_test, predict_reg2)),4))

print('R-Square, ',round(metrics.r2_score(y_test, predict_reg2),4))

print(x_train.columns)
print(reg2.coef_)
print(co_efficients)

co_efficients=x_train
co_efficients['Intercept']=pd.Series([1 for x in range(len(x_train.index))])
print(reg2.coef_.shape)
print(x_train.shape)

pd.DataFrame(reg2.coef_, columns=['coefficients'], index=x_train.columns)

coeff_df = pd.DataFrame(reg2.coef_, x_train.columns, columns=['Coefficient'])  
coeff_df

coeff_df = pd.DataFrame(reg2.coef_, co_efficients.columns, columns=['Coefficient'])  
coeff_df

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))



"""## Model2: Artifical Neural Network Model building"""

from sklearn.neural_network import MLPRegressor

#normalizing variables in the data
scaler = preprocessing.StandardScaler()
scaler.fit(x_train)

# Perform the standardization process
x_train_std = scaler.transform(x_train)
x_test_std = scaler.transform(x_test)

# Using activation function as logistic and optimization solver as stochastic gradient descent
nnreg1 = MLPRegressor(activation='logistic', solver='sgd', 
                      hidden_layer_sizes=(20,20), 
                      early_stopping=True)
nnreg1.fit(x_train_std, y_train)

nnpred1 = nnreg1.predict(x_test_std)

nnreg1.n_layers_

nnreg1.coefs_

#model asssement1: neural network (logistic function)
print("Artificial Neural Netowrk Model Results:")
print('Mean absolute error of test set is, ', round(metrics.mean_absolute_error(y_test, nnpred1),4))

print('Mean squared error of test set is, ',round(metrics.mean_squared_error(y_test, nnpred1),4))
print('Root Mean Squared Error:', round(np.sqrt(metrics.mean_squared_error(y_test, nnpred1)),4))
print('R-Square, ',round(metrics.r2_score(y_test, nnpred1),4))

# Artificial Neural Network model2 with: Activation function as 'relu' and solver as 'stochastics gradient descent
nnetreg2 = MLPRegressor(activation='relu', solver='sgd', hidden_layer_sizes=(20,20),early_stopping=True)
nnetreg2.fit(x_train_std, y_train)

nnetpred2 = nnetreg2.predict(x_test_std)

#model asssement: neural network2 (relu function)


print("Artificial Neural Netowrk Model Results:")
print('Mean absolute error of test set is, ', round(metrics.mean_absolute_error(y_test, nnetpred2),4))
print('Mean squared error of test set is, ',round(metrics.mean_squared_error(y_test, nnetpred2),4))
print('Root Mean Squared Error:', round(np.sqrt(metrics.mean_squared_error(y_test, nnetpred2)),4))
print('R-Square, ',round(metrics.r2_score(y_test, nnetpred2),4))




## Model3: Decision Tree Regression Model


from sklearn.tree import  DecisionTreeRegressor
from sklearn import  metrics
clf = DecisionTreeRegressor()
clf1=clf.fit(x_train,y_train)
predict_tree= clf1.predict(x_test)

#model asssement2: Decision Tree
print("Decision Tree Results:")
print('Mean absolute error of test set is, ', round(metrics.mean_absolute_error(y_test, predict_tree),4))

print('Mean squared error of test set is, ',round(metrics.mean_squared_error(y_test, predict_tree),4))
print('Root Mean Squared Error:', round(np.sqrt(metrics.mean_squared_error(y_test, predict_tree)),4))

print('R-Square, ',round(metrics.r2_score(y_test, predict_tree),4))

import plotly.graph_objs as go
from IPython.display import Image, display
import plotly 
from sklearn.externals.six import StringIO
import pydotplus
import plotly.io as pio
from sklearn import tree
from sklearn.tree import export_graphviz

dot_data = StringIO()
tree.export_graphviz(clf1, out_file=dot_data,
                     feature_names=x_train.columns,
                    max_depth = 3,)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
display(Image(graph.create_png()))

print(dict(zip(x_train.columns, clf1.feature_importances_)))

pd.DataFrame(clf1.feature_importances_, columns=['weight'], index=x_train.columns)

data3_movies.shape


"""### Inference:
- Since our objective is to predict the longterm stabilised rating of the movie, we will chose Decision Tree model as the champion model because of its higher robustness in explaining the variance of the target variable "Rating"
"""

