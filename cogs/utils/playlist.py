import config
import collections
import os
import csv
from random import shuffle


class PlayList:
    def __init__(self):
        self.songs = []
        self.current_track = None
        self.next_track = None
        self.playlist = collections.deque()

    def load_from_file(self):
        directory = config.HOME + 'music/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        pl_file = directory + 'playlist.csv'
        if not os.path.isfile(pl_file):
            return

        with open(pl_file, 'rb') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.songs.append(row)

    def save_file(self):
        directory = config.HOME + 'music/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        pl_file = directory + 'playlist.csv'
        if not os.path.isfile(pl_file):
            return

        field_names = ['title', 'url', 'adder']
        with open(pl_file, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for song in self.songs:
                writer.writerow(song)

    def shuffle(self):
        self.clear()
        self.playlist.extend(self.songs)
        shuffle(self.playlist)

    def clear(self):
        self.playlist.clear()

    def add_song(self, title, url, adder):
        index = self.search(url)
        if index != -1:
            return '"{}" already in the playlist, no need to add.'.format(title)

        new_song = {'title': title, 'url': url, 'adder': adder}
        self.songs.append(new_song)
        self.save_file()
        return '"{}" added to the playlist.'.format(title)

    def remove_song(self, url):
        index = self.search(url)
        if index == -1:
            return 'Song not found, no need to remove.'

        msg = '"{}" removed from the playlist.'.format(self.songs[index]['title'])
        self.songs.pop(index)
        self.save_file()
        return msg

    def search(self, url):
        for i, d in enumerate(self.playlist):
            if d['url'] == url:
                return i
        return -1
