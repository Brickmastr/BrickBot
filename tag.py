import os

HOME = os.path.expanduser('~') + '/splatoon_data/'


class TagHandler:
    def __init__(self):
        self.tags = {}
        with open(HOME + 'tags.txt', 'r') as f:
            for line in f:
                raw = line.rstrip().split(',')
                name = raw[0]
                contents = ''.join(raw[1:])
                self.tags[name] = contents

    def save(self):
        with open(HOME + 'tags.txt', 'w') as f:
            for tag in self.tags.keys():
                line = '{},{}\n'.format(tag, self.tags[tag])
                f.write(line)

    def read_tag(self, tag):
        try:
            return self.tags[tag.lower()]
        except KeyError:
            return 'Tag "{0}" not found. You can set a new tag using `!tag set {0}`'.format(tag)

    def create_tag(self, tag, contents):
        if tag.lower() in self.tags.keys():
            return 'Tag "{}" already exists. Please remove the tag before rewriting it.'.format(tag)
        self.tags[tag.lower()] = contents
        self.save()
        return 'Tag "{}" successfully saved.'.format(tag)

    def remove_tag(self, tag):
        if tag.lower() not in self.tags.keys():
            return 'Tag "{}" does not exist, not removing.'.format(tag)
        del self.tags[tag.lower()]
        self.save()
        return 'Tag "{}" successfully removed.'.format(tag)


if __name__ == '__main__':
    th = TagHandler()
    while True:
        feedback = input('!tag ')
        args = feedback.rstrip().split(' ')
        if args[0] == 'create':
            if len(args) >= 3:
                r = th.create_tag(args[1], ' '.join(args[2:]))
            else:
                r = 'No content provided! Please enter something to tag! Ex. `!tag create example cool link`'
        elif args[0] == 'remove':
            try:
                r = th.remove_tag(args[1])
            except IndexError:
                r = 'No tag provided! Please enter a tag to remove! Ex. `!tag remove example`'
        else:
            r = th.read_tag(args[0])
        print(r)
