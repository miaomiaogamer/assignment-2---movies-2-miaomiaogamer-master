from movie import Movie
from operator import attrgetter
import csv


# TODO: Create your MovieCollection class in this file


class MovieCollection:
    """Movie collection class"""
    def __init__(self):
        """Constructor of movie class"""
        movies = []
        self.movies = movies
        # Initiate in file for opening and saving file
        self.in_file = None

        self.search_list = []

    def load_movies(self, filename):
        """Load movie and save into movies list"""
        # Open file for reading and writing
        self.in_file = open(filename, 'r')
        # Get data from file
        data = self.in_file.readlines()
        for movie in data:
            # Split data by ',', original format: Persian-Roman War,557,Action,u\n
            split_data = movie.split(',')
            title = split_data[0]
            year = split_data[1]
            category = split_data[2]
            is_watched = 'w' in split_data[3]
            # Append to movie list
            self.movies.append(Movie(title, year, category, is_watched))

        self.in_file.close()

    def add_movie(self, movie):
        """Add movie to movie list"""
        self.movies.append(movie)

    def count_unwatch(self):
        """Check for unwatched movies"""
        return len([movie for movie in self.movies if not movie.is_watched])

    def count_watch(self):
        """Check for watched movie"""
        return len([movie for movie in self.movies if movie.is_watched])

    def save_movies(self, filename):
        """Save movie to file"""
        self.in_file = open(filename, 'w')
        data_to_save = ''
        # Reformat the data to save: e.g: Persian-Roman War,557,Action,u\n
        for movie in self.movies:
            watch_sign = 'w' if movie.is_watched else 'u'
            data_to_save += '{},{},{},{}\n'.format(movie.title, movie.year, movie.category, watch_sign)

        # Remove the last \n of the data to make data cleaner
        data_to_save = data_to_save[:-1]
        # Write and close file
        self.in_file.write(data_to_save)
        self.in_file.close()

    def sort_movies(self, key=None, desc=False):
        """Sorting data by key, desc or asc order. use sorted to not touch the original list."""
        # If there is any search, soft for the search movies only
        movies = self.search_list if self.search_list else self.movies
        sort_data = []
        # Sort by year
        if key.lower() == 'year':
            # Lambda function is anonymous, take x as argument and return int(x.year)
            sort_data = sorted(movies, key=lambda movie: int(movie.year), reverse=desc)
        # Sort by title
        if key.lower() == 'title':
            sort_data = sorted(movies, key=lambda movie: movie.title, reverse=desc)
        # Sort by category
        if key.lower() == 'category':
            sort_data = sorted(movies, key=lambda movie: movie.category, reverse=desc)
        # Sort by watched, unwatched
        if key.lower() == 'unwatch':
            sort_data = sorted(movies, key=lambda movie: movie.is_watched, reverse=desc)

        return sort_data

    def search_movies(self, key, year='', category='', watch=None):
        """Filter data by title, year, category and unwatched or watched"""
        # Filter function
        def filter_movies(movie):
            # Return true if key search in title if movie
            filter_title = key.lower() in movie.title.lower()
            # Return true if year input == year of movie, else True to return true for all
            filter_year = int(movie.year) == int(year) if year else True
            # Return true if category input == category of movie, else return true for all
            filter_category = movie.category.lower() == category.lower() if category else True
            # Return true if watch is not provided, else filter by watched or unwatched
            filter_watch = True
            # Only filter watch if watch = True or False is provided
            if type(watch) is bool:
                # If watch == true, return true for all watched movies, else return true for all unwatched movies
                filter_watch = movie.is_watched if watch else not movie.is_watched

            # If all condition is true, return movie to the filter list
            return filter_title and filter_year and filter_category and filter_watch

        # Search list is object so first return it to list type
        self.search_list = list(filter(filter_movies, self.movies))

    @staticmethod
    def format_data(raw_data):
        """Format the data to print out"""
        output_data = ''
        if raw_data:
            # Find longest title for formatting
            longest_title_len = max([len(movie.title) for movie in raw_data])
            # Append output data for each movie to print out
            for index, movie in enumerate(raw_data, start=1):
                mark = '' if movie.is_watched else '*'
                output_data += '{0}. {1:<2} {2:<{3}} - {4:<4} ({5})\n' \
                    .format(index, mark, movie.title, longest_title_len, movie.year, movie.category)

        return output_data

    def __str__(self):
        """Print out list of movies"""
        return self.format_data(self.movies)
