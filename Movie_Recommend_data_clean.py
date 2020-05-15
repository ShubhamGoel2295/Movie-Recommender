import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',None)

df= pd.read_csv(r'C:\Users\egoeshu\Desktop\testingdoc\Movie Recomender\movie_metadata.csv')
# print(df.head())
# print(df.columns)
# print(df.info())
# print(df.describe())

# 1. find missing values
# 2. all the numerical variable
# 3. distribution of numerical variable
# 4. categorical variable
# 5. cardinality of categorical varibale
# 6. outliers

null_col= df.isnull().sum() #giving counts of all nan values in each column
# print(null_col)
numerical_feature= [feature for feature in df.columns if df[feature].dtype != 'O'] #dtype is not object type i.e string generally
# print(numerical_feature)
numerical_null_col= df[numerical_feature].isnull().sum() #fetching total null values
# print(numerical_null_col)
for column in numerical_feature: # finding unique count in each numerical feature
    numerical_unique_count= len(df[column].unique())
    # print(f'total unique count of {column} is {numerical_unique_count}')
#--discrete numerical EDA
discrete_num_feature= [feature for feature in numerical_feature if len(df[feature].unique())<=100] #as per analysis considering discrete variable if unique count less than 100
# print(discrete_num_feature)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# print(df.columns)

column_to_combine= ['director_name', 'actor_1_name', 'actor_2_name', 'actor_3_name', 'genres','movie_title'] #columns to consider in making recommendation by countvectorizer
# print(df[column_to_combine].head())
for column in column_to_combine:
    # print(f'Null values in {column} are {df[column].isnull().sum()}') #last two does not have null value i.e genre adn movie title
    pass
# Filling missing values
# print(df['director_name'].describe())
directorname_null_row= df.loc[df['director_name'].isnull(), column_to_combine].head() #checking rows having director nan
# print(directorname_null_row)
for column in column_to_combine:
    df[column]= df[column].replace(np.nan, 'unknown') #filling null value with unknown
for column in column_to_combine:
    # print(f'Null values in {column} are {df[column].isnull().sum()}') # now all values are filled
    pass
#--- Genre column cleaning
# print(df['genres'].head())
df['genres']= df['genres'].apply(lambda x: x.replace('|', ', ')) # removing | with , to separate
# print(df['genres'].head())
#-- movie title cleaning
# print(df.loc[:, 'movie_title']) #printing all movies names
# print(df['movie_title'].str[:-1]) # same as above
df['movie_title']= df['movie_title'].str[:-1]
# print(df['movie_title'].describe()) #tells count, unique count etc
df['movie_title']= df['movie_title'].str.lower() #coverting to lower
# print(df['movie_title'])

cleaned_data= df[column_to_combine]
cleaned_data.to_csv(r'C:\Users\egoeshu\Desktop\testingdoc\Movie Recomender\cleaned_data.csv', index=False)