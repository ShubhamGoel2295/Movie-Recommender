import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, render_template, jsonify
pd.set_option('display.max_columns',None)

# cleaned_data= pd.read_csv(r'C:\Users\egoeshu\Desktop\testingdoc\Movie Recomender\cleaned_data.csv')
# # print(cleaned_data.head())
# cleaned_data['Combined']= cleaned_data['director_name']+ ' ' +cleaned_data['actor_1_name']+ ' '+cleaned_data['actor_2_name']+ ' ' +cleaned_data['actor_3_name']+ ' ' +cleaned_data['genres']+ ' '+cleaned_data['movie_title'] # joining all the datato apply countvectorizer
# # print(cleaned_data['Combined'])
#
# cv= CountVectorizer()
# count_matrix= cv.fit_transform(cleaned_data['Combined']) #converting each word into vector
# # print(count_matrix) # sparse matrix
#
# similarity= cosine_similarity(count_matrix) # applying cosine similarity
# # print(similarity) # in array, showing the similarity
#
# np.save(r'C:\Users\egoeshu\Desktop\testingdoc\Movie Recomender\similarity_matrix', similarity) # saving similarity matrix locally
# cleaned_data.to_csv(r'C:\Users\egoeshu\Desktop\testingdoc\Movie Recomender\updated_cleaned_data.csv', index=False) #saving cleaned data

# # print(cleaned_data['movie_title'].index[2]) # wll show index i.e 2
# # print(cleaned_data.loc[cleaned_data['movie_title']== 'avatar'].index[0]) # it will tell index of movie which is given


trained_data= pd.read_csv('updated_cleaned_data.csv')
similarity_value= np.load('similarity_matrix.npy')

#--- Simple way to understand below coding in deployment part
a= np.array([9,8,7,6,5])
# print(a)
a= list(enumerate(a)) # will print with its index
sort_a= sorted(a, key=lambda x: x[1], reverse=True) # high value appear first means descending order
# print(sort_a)
#---

#--- Deploying Model---

def recommend_func(movie):
    movie= movie.lower()
    if movie not in trained_data['movie_title'].unique():
        return ('This movie is not in our database.\nPlease check if you spelled it correct.')
    else:
        i= trained_data.loc[trained_data['movie_title']== movie].index[0] # taking index of movie row
        lst= list(enumerate(similarity_value[i])) # fetching cosine value of that index row and converting into list
        sorted_value= sorted(lst, key= lambda x: x[1], reverse=True) # sorting in descending order of cosine value
        sorted_value= sorted_value[1:11] # taking top 10 movies's value excluding 1st one as it is itself
        movie_list= []
        for i in range(len(sorted_value)):
            a= sorted_value[i][0] # taking index
            movie_list.append(trained_data['movie_title'][a]) # giving index no. to fetch movie title
        return movie_list


app= Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend')
def recommend(): # name has to be same as above given otherwise will give build error
    # if request.method== 'POST':
        entered_movie= request.args.get('movie')
        suggested_movies= recommend_func(entered_movie)
        entered_movie= entered_movie.upper()
        if type(suggested_movies) == type('string'): # if error shows about no movie found
            return render_template('recommend.html', movie=entered_movie, r= suggested_movies, t='s')
        else:
            return render_template('recommend.html', movie=entered_movie, r= suggested_movies, t='l') # for list of movies


if __name__ == '__main__':
    app.run(debug=True)
