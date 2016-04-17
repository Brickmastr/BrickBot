import config
import collections
import os
from random import shuffle


class PlayList:
    def __init__(self, auto=True):
        self.songs = []
        self.current_track = None
        self.next_track = None
        self.playlist = collections.deque()
        self.auto = auto
        if auto:
            self.load_from_file()

    def load_from_file(self):

        pl_file = config.HOME + 'playlist.txt'
        if not os.path.isfile(pl_file):
            return

        with open(pl_file, 'r') as f:
            for row in f:
                try:
                    title, url, adder = row.split(',')
                except ValueError:
                    pass
                else:
                    self.songs.append({'title': title, 'url': url, 'adder': adder.rstrip()})

    def save_file(self):
        pl_file = config.HOME + 'playlist.txt'

        with open(pl_file, 'w') as f:
            for song in self.songs:
                row = '{0[title]},{0[url]},{0[adder]}\n'.format(song)
                f.write(row)

    def shuffle(self):
        self.playlist = collections.deque(self.songs)
        shuffle(self.playlist)

    def clear(self):
        self.playlist.clear()

    def add_song(self, title, url, adder):
        index = self.search(url)
        if index != -1:
            return '"{}" already in the playlist, no need to add.'.format(title)

        new_song = {'title': title, 'url': url, 'adder': adder}
        self.songs.append(new_song)
        if self.auto:
            self.save_file()
        else:
            self.playlist.append(new_song)
        return '"{}" added to the playlist.'.format(title)

    def remove_song(self, url):
        index = self.search(url)
        if index == -1:
            return 'Song not found, no need to remove.'

        msg = '"{}" removed from the playlist.'.format(self.songs[index]['title'])
        self.songs.pop(index)
        if self.auto:
            self.save_file()
        return msg

    def search(self, url):
        for i, d in enumerate(self.songs):
            if d['url'] == url:
                return i
        return -1
