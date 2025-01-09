import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = '7bef2b7ad1bf4f5bff897df783e620fa'
BASE_URL = "https://api.themoviedb.org/3"

def get_user_movie_genre(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}?api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        genres = data['genres']
        genre_lists = [] 

        for genre in genres:
            genre_lists.append(genre['id'])       
        return genre_lists
    else:
        raise Exception(f"Error: {response.status_code}")

def get_movie_id(movie):
    url = f'{BASE_URL}/search/movie?api_key={API_KEY}&query={movie}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        if data['results']:
            return data['results'][0]['id']
        else:
            raise Exception("Movie not found.")
    else: 
        raise Exception(f"Error: {response.status_code}")

def get_movie_rating(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}?api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        rating = data.get('vote_average', 0)
        if rating:
            return rating
        else:
            raise Exception("Rating not available.")
    else:
        raise Exception(f"Error: {response.status_code}")

def build_movie_vector(rating, genre_list, all_genres):
    genre_vector = []
    for genre in all_genres:
        if genre in genre_list:
            genre_vector.append(1)
        else:
            genre_vector.append(0)
    # Combine rating and genre vector
    return np.array([rating] + genre_vector)

def get_possible_recommendations(user_genre_list):
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={user_genre_list[0]}&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        movies = response.json()['results']
        return movies
    else:
        raise Exception(f"Error: {response.status_code}")

def get_all_genre_ids():
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        genres = []
        for genre in genres:
            genres.append(genre['id'])
        return genres
    else:
        raise Exception(f"Error: {response.status_code}")
    
def get_similar_movies(user_movie):
    all_genres = get_all_genre_ids()

    #user movie information
    user_movie_id = get_movie_id(user_movie)
    user_genre_list = get_user_movie_genre(user_movie_id)
    user_rating = get_movie_rating(user_movie_id)
    user_movie_vector = build_movie_vector(user_rating, user_genre_list, all_genres)

    #all possible movies based on the user's movie
    possible_movies = get_possible_recommendations(user_genre_list)

    #checking for similarity rating
    similarity_list = []
    for movie in possible_movies:
        movie_rating = movie.get('vote_average', 0)
        movie_genres = movie.get('genre_ids', [])

        movie_vector = build_movie_vector(movie_rating, movie_genres, all_genres)

        #compute cosine similarity
        similarity = cosine_similarity([user_movie_vector], [movie_vector])[0][0]
        similarity_list.append((movie, similarity))

    similarity_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)

    recommended_movies = []
    for movie in similarity_list[:5]:
        recommended_movies.append(movie[0])

    return recommended_movies 

def display_movies(movies):
    count = 0
    if not movies:
        raise Exception("No movies found.")
    
    for movie in movies:
        title = movie['title']
        overview = movie['overview']
        rating = round(movie['vote_average'], 1)
        release_date = movie['release_date']
        print(f"Title: {title}\nRating: {rating}\nRelease Date: {release_date}\nOverview: {overview}\n")
        count += 1
        if count > 4:
            break

def recommend_movies_based_on_movie(movie_name):
    print(f"Fetching recommended movies based on '{movie_name}'...\n")
    
    try:
        similar_movies = get_similar_movies(movie_name)
        print("\nTop 5 Recommended Movies:\n")
        display_movies(similar_movies)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
user_input = input("What movie would you like to base your recommendations on? ")
recommend_movies_based_on_movie(user_input)