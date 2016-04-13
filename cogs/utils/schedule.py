import datetime
import pyrfc3339
import pytz
import requests
import config


class Schedule:
    def __init__(self):
        self.uri_link = 'https://id.nintendo.net/oauth/authorize'
        self.json_link = 'https://splatoon.nintendo.net/schedule/index.json?utf8=✓'
        self.client_id = '12af3d0a3a1f441eb900411bb50a835a'
        self.response_type = 'code'
        self.redirect_uri = 'https://splatoon.nintendo.net/users/auth/nintendo/callback'
        self.username = config.NN_USER
        self.password = config.NN_PWD
        self.cookie = {'_wag_session': self.get_new_splatnet_cookie()}

    def get_data(self):
        data = requests.get(self.json_link, cookies=self.cookie, data={'locale': 'na'})
        # print(data.url)
        # print("data.headers:")
        # for item in data.headers.items():
        #     print('\t', item)
        if data.status_code == 503:
            return data.status_code
        else:
            return data.json()

    def get_new_splatnet_cookie(self):
        parameters = {'client_id': self.client_id,
                      'response_type': 'code',
                      'redirect_uri': self.redirect_uri,
                      'username': self.username,
                      'password': self.password}

        response = requests.post(self.uri_link, data=parameters)

        cookie = response.history[-1].cookies.get('_wag_session')
        if cookie is None:
            raise Exception("Couldn't retrieve cookie")
        return cookie

    def schedule_message(self, data, time_slot):
        now_obj = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        min_time_to_start = datetime.timedelta(hours=time_slot*4-4)
        max_time_to_start = datetime.timedelta(hours=time_slot*4)

        if time_slot == 0:
            intro = '**Current Rotation (Ends in {} hours and {} minutes):**\n'
        else:
            intro = '**In {} hours and {} minutes:**\n'

        for data_set in data['schedule']:
            start = pyrfc3339.parse(data_set['datetime_begin'])
            end = pyrfc3339.parse(data_set['datetime_end'])
            time_to_start = start - now_obj
            time_to_end = end - now_obj
            # print(min_time_to_start.total_seconds(), time_to_start.total_seconds(), max_time_to_start.total_seconds())
            if min_time_to_start <= time_to_start <= max_time_to_start:
                reg_1 = data_set['stages']['regular'][0]['name']
                reg_2 = data_set['stages']['regular'][1]['name']
                rank_1 = data_set['stages']['gachi'][0]['name']
                rank_2 = data_set['stages']['gachi'][1]['name']
                mode = data_set['gachi_rule']
                if time_slot == 0:
                    time_left = time_to_end
                else:
                    time_left = time_to_start
                hours = int(time_left.total_seconds() / 3600)
                minutes = int(time_left.total_seconds()/60) % 60
                msg = intro + "Turf War is {} and {}\n{} is {} and {}"
                return msg.format(hours, minutes, reg_1, reg_2, mode, rank_1, rank_2)

        return "There is no data currently for this time slot."

    def splatfest_message(self, data):
        now_obj = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        msg = '**Splatfest Time! (Ends in {} hours and {} minutes)**\n' \
              'Teams are **{}** and **{}**\n' \
              'Maps are {}, {}, and {}'
        end = pyrfc3339.parse(data['schedule'][0]['datetime_end'])
        time_to_end = end - now_obj
        hours = int(time_to_end.total_seconds() / 3600)
        minutes = int(time_to_end.total_seconds()/60) % 60
        team_a = data['schedule'][0]['team_alpha_name']
        team_b = data['schedule'][0]['team_bravo_name']
        stage_1 = data['schedule'][0]['stages'][0]['name']
        stage_2 = data['schedule'][0]['stages'][1]['name']
        stage_3 = data['schedule'][0]['stages'][2]['name']
        return msg.format(hours, minutes, team_a, team_b, stage_1, stage_2, stage_3)

    def maps(self,  time_slot=None):
        data = self.get_data()
        if data['festival']:
            frm_msg = self.splatfest_message(data)
        elif time_slot is not None:
            frm_msg = self.schedule_message(data, time_slot)
        else:
            frm_msg = self.schedule_message(data, 0) + '\n\n' + \
                      self.schedule_message(data, 1) + '\n\n' + \
                      self.schedule_message(data, 2)
        return frm_msg


if __name__ == '__main__':
    s = Schedule()
    print(s.get_data())
