"""
Name:Jiale Tang
Date:18/1/2021
Brief Project Description:Movies to watch 2.0 with GUI
GitHub URL:https://github.com/JCUS-CP1404/assignment-2---movies-2-miaomiaogamer
"""
# TODO: Create your main program in this file, using the MoviesToWatchApp class

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.button import Button
from movie import Movie
from moviecollection import MovieCollection
from string import capwords


class MoviesToWatchApp(App):
    """Watchmovies app GUI version"""
    sort_by = StringProperty()
    category = ListProperty()
    order = ListProperty()
    current_order = StringProperty()

    def __init__(self, **kwargs):
        """Creat the core of Watchmovies app"""
        Window.size = (900, 700)
        super(MoviesToWatchApp, self).__init__(**kwargs)
        self.my_collection = MovieCollection()
        self.movie_to_show = []

    def build(self):
        """Build kivy GUI file"""
        self.title = "Movie To Watch 2.0 by JialeTang "
        self.root = Builder.load_file('app.kv')
        # Setting category lists
        self.category = ['Title', 'Year', 'Category']
        self.sort_by = self.category[0]
        return self.root

    def on_start(self):
        self.my_collection.load_movies('movies.csv')
        self.movie_to_show = self.my_collection.movies
        self.root.ids.movie_list.bind(minimum_height=self.root.ids.movie_list.setter('height'))
        # Show the message
        self.root.ids.message.text = 'Let\'s watch some movies :)'
        # Load movies
        self.load_movies()
        # Showing watched or unwatch
        self.count_watch()

    def on_stop(self):
        """Saving the data to csv when close the app"""
        self.my_collection.save_movies('movies.csv')

    def count_watch(self):
        self.root.ids.watch_count.text = 'To watch: {}. Watched: {}'.format(self.my_collection.count_unwatch(),
                                                                            self.my_collection.count_watch())

    def sort_movies(self, key):
        """Sort movie based on key"""
        self.sort_by = key
        self.load_movies()

    def handle_order(self, element):
        """Sort movie based on order"""
        self.current_order = element
        self.load_movies()

    def handle_add_movie(self, title, year, category):
        """Add movies to the movies list"""
        # Only add movie when title, year, category are provided
        if title and year and category:
            title_check = self.handle_input(title, is_title=True)
            category_check = self.handle_input(category, is_category=True)
            year_check = self.handle_input(year, is_year=True)
            if year_check and category_check and title_check:
                clean_title = ' '.join(title.split())
                pretty_title = capwords(clean_title)
                if self.check_exist(title_check, year_check, category_check):
                    self.show_popup_message('The movie is already exist')
                else:
                    self.my_collection.add_movie(Movie(title_check, year_check, category_check))
                    self.load_movies()
                    self.show_popup_message('{} have been add to movie list'.format(pretty_title))
                    self.handle_clear_button(is_add=True)

        else:
            # Showing error message if any field is blank
            self.show_popup_message('All fields are required')

    def load_movies(self):
        self.root.ids.movie_list.clear_widgets()
        desc = self.current_order == 'Descending Order'
        self.movie_to_show = self.my_collection.sort_movies(self.sort_by, desc)
        for index, movie in enumerate(self.movie_to_show):
            watch_mark = 'watched' if movie.is_watched else ''
            btn = Button(text='{} ({} from {}) {}'.format(movie.title, movie.category, movie.year, watch_mark),
                         size_hint_y=None, height=200)
            btn.movie = movie
            btn.bind(on_press=self.handle_watch_movie)
            # background color
            if watch_mark:
                btn.background_color = (0.5, 0.25, 1.0, 1.0)
            else:
                btn.background_color = (1, 0, 0, 5)
            self.root.ids.movie_list.add_widget(btn)

    def handle_watch_movie(self, instance):
        """Handle watch movie if user click on movie"""
        current_movie = instance.movie
        current_movie.is_watched = not current_movie.is_watched
        self.load_movies()
        watch_mark = 'watched' if current_movie.is_watched else 'unwatched'

        self.root.ids.message.text = 'You have {} {}'.format(watch_mark, current_movie.title)
        self.count_watch()

    def show_popup_message(self, text):
        """show popup message"""
        self.root.ids.popup_message.text = text
        self.root.ids.popup.open()

    def handle_close_popup(self):
        """Close the popup"""
        self.root.ids.popup_message.text = ''
        self.root.ids.popup.dismiss()

    def handle_clear_button(self, is_add=False, is_search=False):
        """Clear input when pressed"""
        if is_add:
            self.root.ids.title.text = ''
            self.root.ids.year.text = ''
            self.root.ids.category.text = ''
        elif is_search:
            self.root.ids.title_search.text = ''
            self.root.ids.year_search.text = ''
            self.root.ids.category_search.text = ''
            self.root.ids.watch_search.text = ''
        # Else clear all
        else:
            self.root.ids.title.text = ''
            self.root.ids.year.text = ''
            self.root.ids.category.text = ''
            self.root.ids.title_search.text = ''
            self.root.ids.year_search.text = ''
            self.root.ids.category_search.text = ''
            self.root.ids.watch_search.text = ''


    def check_exist(self, title, year, category):
        """Check if movie is existed"""
        def find_duplicate(movie):
            filter_title = title.lower() == movie.title.lower()
            filter_year = int(movie.year) == int(year)
            filter_category = movie.category.lower() == category.lower()
            return filter_title and filter_year and filter_category

        return list(filter(find_duplicate, self.my_collection.movies))

    def handle_input(self, input_data, is_title=False, is_year=False, is_category=False, is_watch=False, blank=False):
        """Handle input data"""
        if blank and not input_data:
            return True
        else:
            if is_year:
                try:
                    year = int(input_data)
                    if year < 0:
                        raise ValueError()
                    return input_data.strip()
                except ValueError:
                    self.show_popup_message('Your year must be a number and greater than 0')

            elif is_category:
                if input_data.lower().strip() not in ['action', 'comedy', 'documentary', 'drama', 'fantasy',
                                                      'thriller']:
                    self.show_popup_message('Please enter a correct category '
                                            '(Action, Comedy, Documentary, Drama, Fantasy, Thriller)')
                else:
                    return input_data.strip()
            elif is_watch:
                if input_data.lower() not in ['y', 'n']:
                    self.show_popup_message('Your watch field must be Y or N')
                else:
                    return True
            elif not input_data.strip() and is_title:
                self.show_popup_message('Your title must not be blank')
            else:
                return input_data.strip()


if __name__ == '__main__':
    MoviesToWatchApp().run()
