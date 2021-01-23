"""..."""


# TODO: Create your Movie class in this file


class Movie:
    """creat a Movie class"""
    def __init__(self, title='', year=0, category='', is_watched=False):
        self.title = title
        self.category = category
        self.year = year
        self.is_watched = is_watched

    def __str__(self):
        """Return movie info"""
        watch_check = 'watched' \
            if self.is_watched \
            else 'unwatched'

        return '{} - {} ({}) ({})'.format(self.title, self.year, self.category, watch_check)

    #def list_movies(movies):
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

    def mark_watched(self):
        """Changing movie to watched"""
        self.is_watched = True

    def mark_unwatched(self):
        """Changing movie to unwatched"""
        self.is_watched = False