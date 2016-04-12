import random


class Squad:
    def __init__(self):
        self.active = []
        self.current = []

    def new_squad(self, squad_list):
        self.active = list(squad_list)
        return self.refresh_team()

    def add_member(self, member):
        if member not in self.active:
            self.active.append(member)
            return '{} Added'.format(member)
        else:
            return '{} Already in the member pool!'.format(member)

    def remove_member(self, member):
        if member in self.active:
            self.active.remove(member)
            if member in self.current:
                self.current.remove(member)
            return '{} Removed'.format(member)
        else:
            return '{} not in member pool!'.format(member)

    def refresh_team(self):
        addable = [mem for mem in self.active if mem not in self.current]
        adding = random.sample(set(addable), min(4, len(addable)))
        removing = []
        for i, member in enumerate(self.current):
            if len(removing) >= min(len(adding), len(self.current)):
                break
            elif len(removing) <= min(len(adding), len(self.current)) - (len(self.current) - i):
                # print(len(removing), i, min(len(adding), len(self.current)))
                removing.append(member)
            else:
                coin = random.randint(0, len(adding))
                # print('{}: {}'.format(member, coin))
                if coin >= 1:
                    removing.append(member)

        for mem in removing:
            self.current.remove(mem)
        self.current.extend(adding)

        addable = [mem for mem in self.active if mem not in self.current]
        while len(self.current) < 4 and len(addable) > 0:
            mem = addable.pop()
            if mem not in self.current:
                self.current.append(mem)

        m = '\n\t'.join(self.current)
        return 'Next Squad:\n\t{}'.format(m)


if __name__ == '__main__':
    s = Squad()
    while True:
        message = input('message: ')
        args = message.split(' ')
        err_msg = ''
        good_msg = ''

        if args[1] == 'new':
            try:
                status = s.new_squad(args[2:])
            except IndexError:
                status = 'not enough args'
        elif args[1] == 'next':
            status = s.refresh_team()
        elif args[1] == 'add':
            err_msg = 'already exists'
            good_msg = 'added to'
            try:
                status = s.add_member(args[2])
            except IndexError:
                status = 'not enough args'
        elif args[1] == 'remove':
            err_msg = 'does not exist'
            good_msg = 'removed from'
            try:
                status = s.remove_member(args[2])
            except IndexError:
                status = 'not enough args'
        else:
            status = 'not implemented'

        if status == 'not enough args':
            msg = 'You have not entered a name. Please add a name to your command for it to work. ' \
                  'Please see `!help squad`.'
        elif status == 'not implemented':
            msg = 'That is not a usable command for !squad. Please see `!help squad`.'
        elif status is False:
            msg = 'That squad member currently {}. Cannot perform action.'.format(err_msg)
        elif status is True:
            msg = '{} {} the squad'.format(args[2], good_msg)
        else:
            members = '\n\t'.join(status)
            msg = 'Next Squad:\n\t{}'.format(members)

        print(msg)
