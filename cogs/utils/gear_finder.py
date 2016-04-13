import os

HOME = os.path.expanduser('~') + '/splatoon_data/'


class GearFinder:
    def __init__(self):
        self.abilities = []
        self.brands = []
        self.weapons = []
        self.gear_dict = {'headgear': [], 'clothing': [], 'shoes': []}
        self.order = ['headgear', 'clothing', 'shoes']

        with open(HOME + 'abilities.txt', 'r') as f:
            for line in f:
                self.abilities.append(line.rstrip())

        with open(HOME + 'brands.txt', 'r') as f:
            for line in f:
                self.brands.append(line.rstrip().split(','))

        with open(HOME + 'weapons.txt', 'r') as f:
            for line in f:
                self.weapons.append(line.rstrip().split(','))

        for gear_type in self.order:
            with open(HOME + '{}.txt'.format(gear_type), 'r') as f:
                for line in f:
                    self.gear_dict[gear_type].append(line.rstrip().split(','))

    def extract_brand_info(self, brand_info):
        brand_name = brand_info[0]

        try:
            brand_buff_num = int(brand_info[1]) - 1
            brand_buff = self.abilities[brand_buff_num]
        except ValueError:
            brand_buff = 'None'

        try:
            brand_nerf_num = int(brand_info[2]) - 1
            brand_nerf = self.abilities[brand_nerf_num]
        except ValueError:
            brand_nerf = 'None'

        return brand_name, brand_buff, brand_nerf

    def extract_gear_info(self, gear_info):
        gear_txt = gear_info[0]
        main_num = int(gear_info[1]) - 1
        main_txt = self.abilities[main_num]
        brand_num = int(gear_info[2]) - 1
        brand_info = self.brands[brand_num]
        brand_txt_list = self.extract_brand_info(brand_info)
        return gear_txt, main_txt, brand_txt_list

    def find_abilities(self, desired_abilities):
        if len(desired_abilities) == 0:
            msg = 'No abilities found. Please check your command and try again. (Did you miss your "quotes"?)'

        elif len(desired_abilities) > 6:
            msg = "Too many abilities entered! Max 6 at a time please!"

        elif len(desired_abilities) == 1:
            msg_list = []
            desired_ability = desired_abilities[0]

            if desired_ability.lower() in (brand[0].lower() for brand in self.brands):
                brand_name = ''
                for brand in self.brands:
                    if brand[0].lower() == desired_ability.lower():
                        brand_name = brand[0]
                        break

                msg_list.append('__**{}** Gear:__'.format(brand_name))

                for gt in self.order:
                    temp_msg = '__**{}**__:'.format(gt.capitalize())
                    for gear_info in self.gear_dict[gt]:
                        gear_txt, main_txt, brand_info = self.extract_gear_info(gear_info)
                        bn = brand_info[0]
                        if bn == brand_name:
                            temp_msg += '\n\t**{}** ({})'.format(gear_txt, main_txt)
                    msg_list.append(temp_msg)

            elif desired_ability.lower() in (a.lower() for a in self.abilities):
                ability_name = ''
                for a in self.abilities:
                    if desired_ability.lower() == a.lower():
                        ability_name = a
                        break

                msg_list.append('__**{}** Gear:__'.format(ability_name))

                for gt in self.order:
                    temp_msg = '__**{}**__:'.format(gt.capitalize())
                    for gear_info in self.gear_dict[gt]:
                        gear_txt, main_txt, brand_info = self.extract_gear_info(gear_info)
                        brand_buff = brand_info[1]
                        if brand_buff == ability_name:
                            temp_msg += '\n\t**{}** (Main: {})'.format(gear_txt, main_txt)
                        elif main_txt == ability_name:
                            temp_msg += '\n\t**{}** (Brand Buff: {})'.format(gear_txt, brand_buff)
                    msg_list.append(temp_msg)

            else:
                msg_list.append('Ability or brand not found! Please try again.')

            msg = '\n\n'.join(msg_list)

        else:
            msg_list = []
            matching = {'headgear': {'Good': [], 'Brandless': []},
                        'clothing': {'Good': [], 'Brandless': []},
                        'shoes': {'Good': [], 'Brandless': []}}

            for gt in self.order:
                temp_msg = ''
                for gear_info in self.gear_dict[gt]:
                    gear_txt, main_txt, brand_info = self.extract_gear_info(gear_info)
                    brand_buff = brand_info[1]
                    if main_txt.lower() in desired_abilities and brand_buff == 'None':
                        matching[gt]['Brandless'].append([gear_txt, main_txt])
                    elif main_txt.lower() in desired_abilities and brand_buff.lower() in desired_abilities:
                        matching[gt]['Good'].append([gear_txt, main_txt, brand_buff])
                    elif len(desired_abilities) == 1 and (main_txt.lower() in desired_abilities or
                                                          brand_buff.lower() in desired_abilities):
                        matching[gt]['Good'].append([gear_txt, main_txt, brand_buff])

                if len(matching[gt]['Good']) > 0:
                    temp_msg += 'Matching {} Found:\n'.format(gt.capitalize())
                    for gear in matching[gt]['Good']:
                        temp_msg += '\t**{0[0]}**\n\t\tMain: {0[1]}\n\t\tBrand Buff: {0[2]}\n'.format(gear)

                elif len(matching[gt]['Brandless']) > 0:
                    temp_msg += 'Brandless {} Found:\n'.format(gt.capitalize())
                    for gear in matching[gt]['Brandless']:
                        temp_msg += '\t**{0[0]}**\n\t\tMain: {0[1]}\n'.format(gear)

                else:
                    temp_msg += 'No Matching {} Found.'.format(gt.capitalize())
                msg_list.append(temp_msg)

            msg = '\n\n'.join(msg_list)

        return msg

    def define_gear(self, desired_gear_txt):
        for gt in self.order:
            pn = 'are' if gt == 'shoes' else 'is'
            pn2 = 'have' if gt == 'shoes' else 'has'
            for gear_info in self.gear_dict[gt]:
                gear_txt, main_txt, brand_info = self.extract_gear_info(gear_info)
                if desired_gear_txt.lower() == gear_txt.lower():
                    return ('**{0}** {4} {3}, {5} the main ability **{1}** and {4} **{2[0]}** brand (buffs **{2[1]}** '
                            'and nerfs **{2[2]}**)'.format(gear_txt, main_txt, brand_info, gt, pn, pn2))

        for brand_info in self.brands:
            name, buff, nerf = self.extract_brand_info(brand_info)
            if desired_gear_txt.lower() == name.lower():
                if buff == nerf == 'None':
                    return '**{}** is a neutral brand with no favored ability.'.format(name)
                else:
                    return ('**{0}** is a brand that has a high chance to roll **{1}** and a low chance to roll '
                            '**{2}**.'.format(name, buff, nerf))

        for weapon_info in self.weapons:
            name, sub, special = weapon_info
            if desired_gear_txt.lower() == name.lower():
                return '**{}** has the **{}** sub weapon and the **{}** special.'.format(name, sub, special)

        return ('No weapon kit, gear or brand by the name **{}** was found. Please check your spelling and try '
                'again.'.format(desired_gear_txt))


if __name__ == "__main__":
    gf = GearFinder()
    while True:
        feedback = input('\n!gear ').lower().rstrip()
        command = feedback.split(' ')[0]
        desired_raw = feedback.split('"')
        desired = desired_raw[1::2]

        if command == 'find':
            print(gf.find_abilities(desired))
        elif command == 'define':
            print(gf.define_gear(desired[0]))
        else:
            print('Command not found. Please try again.')
