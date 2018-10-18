import json
import os
from stac import __version__, utils


class STACError(Exception):
    pass


class Thing(object):

    def __init__(self, data, filename=None):
        """ Initialize a new class with a dictionary """
        self.filename = filename
        self.data = data
        if 'links' not in self.data.keys():
            self.data['links'] = []

    def __repr__(self):
        return self.id

    @classmethod
    def open(cls, filename):
        """ Open an existing JSON data file """
        # TODO - open remote URLs
        with open(filename) as f:
            dat = json.loads(f.read())
        return cls(dat, filename=filename)

    @property
    def id(self):
        return self.data['id']

    @property
    def path(self):
        return os.path.dirname(self.filename) if self.filename else None

    def keys(self):
        """ Get keys from catalog """
        return self.data.keys()

    def links(self, rel=None):
        """ Get links for specific rel type """
        links = self.data.get('links', [])
        if rel is not None:
            links = [l for l in links if l.get('rel') == rel]
        links = [l['href'] for l in links]
        if self.filename is not None:
            _links = []
            for l in links:
                if not os.path.isabs(l):
                    fname = os.path.join(os.path.dirname(self.filename), l)
                    _links.append(os.path.abspath(fname))
            links = _links
        return links

    def __getitem__(self, key):
        """ Get key from properties """
        props = self.data.get('properties', {})
        return props.get(key, None)

    def save(self):
        """ Write a catalog file """
        if self.filename is None:
            raise STACError('No filename, use save_as()')
        utils.mkdirp(os.path.dirname(self.filename))
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.data))

    def save_as(self, filename):
        """ Write a catalog file to a new file """
        self.filename = filename
        self.save()
