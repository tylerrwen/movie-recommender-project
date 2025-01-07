import requests
import random

API_KEY = '7bef2b7ad1bf4f5bff897df783e620fa'
BASE_URL = "https://api.themoviedb.org/3"

# Function to get the genre ID
def get_genre_id(genre_name):
    # Get the list of genres available on TMDb
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            genres = response.json()['genres']
            # Find the genre by name and return the genre ID
            for genre in genres:
                if genre['name'].lower() == genre_name.lower():
                    return genre['id']
        except Exception:
            print("Genre not found")
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

def get_user_movie_genre(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}?api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        genres = data['genres']
        genre_names = [] 

        for genre in genres:
            genre_names.append(genre['name'])       
        return genre_names
    else:
        raise Exception(f"Error: {response.status_code}")

# Function to get recommended movies by genre ID
def get_movies_by_genre(genre_name):
    genre_id = get_genre_id(genre_name)
    page = random.randint(0,500)
    
    if genre_id is None:
        raise Exception(f"Genre '{genre_name}' not found.")
    
    # Fetch movies of the specified genre
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}&page={page}"
    response = requests.get(url)
    
    if response.status_code == 200:
        movies = response.json()['results']
        return movies
    else:
        raise Exception(f"Error: {response.status_code}")


# Function to display movie details
def display_movies(movies):
    count = 0
    if not movies:
        raise Exception("No movies found.")
    
    for movie in movies:
        title = movie['title']
        overview = movie['overview']
        release_date = movie['release_date']
        print(f"Title: {title}\nRelease Date: {release_date}\nOverview: {overview}\n")
        count += 1
        if count > 4:
            break

def recommend_movies_based_on_movie(movie_name):
    print(f"Fetching recommended movies based on {movie_name}...\n")
    
    movie_id = get_movie_id(movie_name)
    genre_name = get_user_movie_genre(movie_id)
    print(genre_name)
    if len(genre_name) > 1:
        movies = get_movies_by_genre(genre_name[random.randint(0,len(genre_name))])
    else:
        movies = get_movies_by_genre(genre_name[0])
    display_movies(movies)

# Example usage
user_input = input("What movie would you like to base your recommendations on? ")

recommend_movies_based_on_movie(user_input)