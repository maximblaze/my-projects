import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
import random
import csv


#source bin/activate - старт работы с виртуальной средой

class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        self.operators = ["/", "*", "+", "-"]
        self.fifa_db = "fifa_db_full.csv"
        self.current_teams_box = 'fifa_actual.csv'
        self.groups = {'A': [], 'B': [], 'C': [], 'D': [],
                       'E': [], 'F': [], 'G': [], 'H': []}#,
                     #  'I': [], 'J': []}
        self.hosts = ['Colombia']

        self.instant = TextInput(
            multiline=False, readonly=False, halign="right", font_size=55
        )

        self.drawed_group_show = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )

        self.teams = self.teams_list()

        self.boxe = self.generate_boxes(self.teams)

        self.boxes = self.boxe[0]

        self.teams = self.boxe[1]

        self.semened_teams = []

        self.team_to_draw = None

        layout_boxes_outer = BoxLayout()
        for i in self.boxes.keys():
            layout_boxes = GridLayout(cols=1, rows=11, row_force_default=True, row_default_height=32.3)

            layout_boxes.add_widget(Button(text='Box '+i, size_hint_x=None, width=700, background_color= [1,2,0,3]))
            for j in range(8):
                layout_boxes.add_widget(Button(text=self.boxes[i][j]['Team'], size_hint_x=None, width=700))
            layout_boxes_outer.add_widget(layout_boxes)


        main_layout.add_widget(layout_boxes_outer)

        layout_groups_outer = BoxLayout()
        self.groups_layouts = []
        for i in self.groups.keys():
            layout_group = GridLayout(cols=1, rows=5, row_force_default=True,  row_default_height=70.3)
            layout_group.add_widget(Button(text='Group '+i, size_hint_x=None, width=400))
            group_teams = []
            for position in range(4):
                pos_team = TextInput(
                    multiline=False, readonly=True, halign="left", font_size=35
                )
                layout_group.add_widget(pos_team)
                group_teams.append(pos_team)
            self.groups_layouts.append({i: group_teams})
            layout_groups_outer.add_widget(layout_group)


        main_layout.add_widget(layout_groups_outer)
        main_layout.add_widget(self.instant)
        main_layout.add_widget(self.drawed_group_show)

        choose_team_button = Button(
            text="Find the team for draw!", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        choose_team_button.bind(on_press=self.on_button_press_to_choose_team)

        choose_group_button = Button(
            text="Find the group for the team!", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        choose_group_button.bind(on_press=self.on_button_press_to_draw_team)


        layout_buttons = BoxLayout()
        layout_buttons.add_widget(choose_team_button)
        layout_buttons.add_widget(choose_group_button)

        main_layout.add_widget(layout_buttons)



        return main_layout


    def teams_list(self):
        current_teams_box = []
        with open(self.current_teams_box, mode='r') as current_teams:
            reader = csv.reader(current_teams)
            for row in reader:
                current_teams_box.append(row[2])
        with open(self.fifa_db, mode='r') as infile:
            reader = csv.reader(infile)
            teams = []
            for row in reader:
                print(row)
                if row[1] in current_teams_box:
                    team = {'Team': row[1], 'Confederation': row[2], 'Rec_box': row[3], 'Rank_place': row[0]}
                    teams.append(team)
                else:
                    pass
            teams_ranked = sorted(teams, key=lambda k: k['Rec_box'])
        return teams_ranked



    def choose_group(self, team, max_teams_in_group = 4): #team - dict with 4 keys: Name, Confederation, Box, Rank_place
        if type(team) == None:
            return 'Enter real team'
        available_groups = []
        for number, group in self.groups.items():
            if len(group) == 0:
                available_groups.append(number)
            elif len(group) == max_teams_in_group:
                pass
            else:
                checker = 1
                num_uefa = 0
                for semen_team in group:
                    if semen_team['Confederation'] == 'UEFA':
                        num_uefa += 1
                for semen_team in group:
                    if semen_team['Confederation'] != team['Confederation']:
                        pass
                    else:
                        if team['Confederation'] == 'UEFA' and num_uefa < 2:
                            pass
                        else:
                            checker = 0
                if checker == 1:
                    available_groups.append(number)
                else:
                    pass
        random.shuffle(available_groups)
        if team['Team'] in self.hosts:
            available_groups = ['A', 'B']
            available_groups.sort(key=lambda elem: len(self.groups[elem]))
            target_group = available_groups[0]
            self.groups[target_group].append(team)
            self.semened_teams.append(team)
            return target_group
        if len(available_groups) == 0:
            return 'Error with forming groups'
        available_groups.sort(key=lambda elem: len(self.groups[elem]))
        target_group = available_groups[0]
        self.groups[target_group].append(team)
        self.semened_teams.append(team)
        return target_group


    def generate_boxes(self, teams):
        ranked_teams = []
        host_teams = self.hosts
        for team in teams:
            if team['Team'] in host_teams:
                ranked_teams.append(team)
                teams.remove(team)
        ranked_teams.extend(teams)
        boxes = {'1': ranked_teams[0:8], '2': ranked_teams[8:16], '3': ranked_teams[16:24], '4': ranked_teams[24:32]}
        return boxes, ranked_teams


    def on_button_press_to_choose_team(self, instance):
        self.drawed_group_show.text = ''
        button_text = instance.text
        if button_text:
            self.team_to_draw = None
            for team in self.teams:
                if team not in self.semened_teams:
                    self.instant.text = team['Team']
                    self.team_to_draw = team
                    break


    def on_button_press_to_draw_team(self, instance):
            if self.team_to_draw in self.semened_teams:
                self.drawed_group_show.text = 'This team is already in the group'
            else:
                if self.team_to_draw == None:
                    self.drawed_group_show.text = 'All teams are in their groups'
                else:
                    group = self.choose_group(self.team_to_draw)
                    if group == 'Error with forming groups':
                        self.drawed_group_show.text = group
                    else:
                        for dict in self.groups_layouts:
                            if group in dict.keys():
                                for i in range(4):
                                    if dict[group][i].text == '':
                                        dict[group][i].text = self.team_to_draw['Team']
                                        break
                        self.drawed_group_show.text = group


if __name__ == "__main__":
    app = MainApp()
    app.run()
