"""..."""
# TODO: Copy your first assignment to this file, then update it to use Movie class
# Optionally, you may also use MovieCollection class

from movie import Movie
from operator import itemgetter

def menu():
    print("Menu: ")
    print("L - List movies ")
    print("A - Add new movies ")
    print("W - Watch a movie ")
    print("Q - Quit ")
    userInput = input().upper()
    return userInput

def list_movies(movies):
    i = 0
    Movieswatched = 0
    while i < len(movies):
        if movies[i][3] == "n":
            print("{:2}. * {:35} - {:4} ({})".format(i, movies[i][0], movies[i][1], movies[i][2]))
            Movieswatched = Movieswatched + 1
        else:
            print("{:2}.   {:35} - {:4} ({})".format(i, movies[i][0], movies[i][1], movies[i][2]))
        i = i + 1
    movies_watched = len(movies) - Movieswatched
    print("{} movies watched, {} movies still to watch".format(movies_watched, Movieswatched))

def add_movies():
    new_movie = []
    movie_name = str(input("Title: "))
    while True:
        try:
            movie_year = int(input("Year: "))
            if movie_year < 0:
                print("Number must be >= 0")
                continue
            break
        except ValueError:
            print("Invalid input; enter a valid number")
    while True:
        try:
            movie_category = str(input("Category: "))
            if movie_category == '' or movie_category == ' ':
                print("Input can not be blank")
                continue
            if '  ' in movie_category:
                print("Input contains too many spaces")
            break
        except ValueError:
            print("Input can not be a number")
    new_movie.append(movie_name)
    new_movie.append(movie_year)
    new_movie.append(movie_category)
    new_movie.append('n')
    print("{} ({} from {}) added to movie list".format(movie_name, movie_category, movie_year))
    return new_movie

def watch_movies(movies):
    while True:
        try:
            movie_watched = int(input("Enter the number of a movie to mark as watched: "))
            if 'y' in movies[movie_watched]:
                print("You have already watched {} ".format(movies[movie_watched][0]))
                continue
            if movie_watched < 0 or movie_watched > len(movies) - 1:
                print("Please enter a valid number")
                continue
            break
        except ValueError:
            print("please enter a number")
    movies[movie_watched][3] = 'y'
    print("{} from {} watched".format(movies[movie_watched][0], movies[movie_watched][1]))
    return movies

def main():
    root_file = open("movies.csv", "r")
    data = root_file.readlines()
    movie_list = []

    for n in data:
        values = n.strip().split(',')
        movie_list.append(values)
    for i in range(len(movie_list)):
        movie_list[i][1] = int(movie_list[i][1])
    movie_list.sort(key=itemgetter(1, 0))
    root_file.close()
    initial_movies = len(movie_list)

    print("Movies To Watch 1.0 - by <Jiale Tang>")
    print("{} movies loaded".format(initial_movies))
    print("Menu: ")
    print("L - List movies ")
    print("A - Add new movies ")
    print("W - Watch a movie ")
    print("Q - Quit ")

    user_input = input().upper()
    while user_input != "Q":
        if user_input == "L":
            list_movies(movie_list)
            user_input = menu()
        elif user_input == "A":
            movie_list.append(add_movies())
            movie_list.sort(key=itemgetter(1, 0))
            user_input = menu()
        elif user_input == "W":
            movie_list = watch_movies(movie_list)
            user_input = menu()
        else:
            print("I did not understand that response. Please choose either L, A, W or Q. ")
            user_input = menu()

    movies_added = len(movie_list) - initial_movies
    final_movies = movies_added + initial_movies
    print("{} movies saved to movies.csv Have a nice day :D".format(final_movies))

    for i in range(len(movie_list)):
        movie_list[i][1] = str(movie_list[i][1])
    out_file = open("movies.csv", 'w')
    for n in movie_list:
        print("{},{}".format(n[0], ','.join(n[1:])), file=out_file)
    out_file.close()


if __name__ == '__main__':
    main()