import json
import sys

class League:
    
    def __init__(self,teamfile,playerfile,statfile):
        f = open(teamfile,'r')
        g = open(playerfile,'r')
        h = open(statfile,'r')
        team_data = json.load(f)
        player_data = json.load(g)
        stats = json.load(h)
        teams = []
        players = []
        team_data_teams = team_data['teams']
        for i in team_data_teams:
            name = i['name']
            shortName = i['abbreviation']
            conference = i['conference']
            conference_name = conference['name']
            division = i['division']
            division_name = division['name']
            team = Team(name,shortName,conference_name,division_name)
            teams.append(team)
            for a in player_data['data']:
                if i['id'] == a['currentTeamId']:
                    firstName = a['firstName']
                    lastName = a['lastName']
                    country = a['birthCountry']
                    birthDate = a['birthDate']
                    position = a['position']
                    player_id = a['id']
                    player = Player(firstName,lastName,country,birthDate,position,player_id)
                    players.append(player)
                    team.add_player(player)
                    for e in stats['data']:
                        goals = 0
                        points = 0
                        if a['id'] == e['playerId']:
                            goals = e['goals']
                            points = e['points']
                            team.add_goals(player,goals)
                            team.add_points(player,points)
                            break
                    else:
                        team.add_goals(player,goals)
                        team.add_points(player,points)
                        
        self.teamfile = teams
        self.playerfile = players
        self.statfile = stats

    def teams(self,conference = "", division = "" ):
        tiedot = self.teamfile
        teams = []
        name = ''
        limit = ''
        for i in tiedot:
            if len(conference) > 0:
                if i.conference == conference:
                    teams.append(i)
            elif len(division) > 0:
                if i.division == division:
                    teams.append(i)
            else:
                teams.append(i)
        teams = sorted(teams, key = lambda x:x.name)
        return teams


    def team(self,name):
        tiedot = self.teamfile
        for i in tiedot:
            if i.abbreviation == name:
                return i
        return None

    def players(self, country = ''):
        tiedot = self.playerfile
        players = []
        tiedot = sorted(tiedot, key = lambda x:x.id)
        tiedot = sorted(tiedot, key = lambda x: x.firstName)
        tiedot = sorted(tiedot, key = lambda x: x.lastName)
        if len(country) > 0:
            for i in tiedot:
                if i.country == country:
                    players.append(i)
            return players
        else:
            return tiedot

    def goals(self):
        tiedot = self.playerfile
        stats = self.statfile
        stats_data = stats['data']
        tupla = ()
        lista = []
        for i in tiedot:
            for a in stats_data:
                if a['playerId'] == i.id:
                    goals = a['goals']
                    tupla = (i,goals)
                    lista.append(tupla)
                    break
            else:
                tupla = (i,0)
                lista.append(tupla)
        lista.sort(key = lambda x:x[0])
        lista.sort(key = lambda x:x[1],reverse = True)
        return lista

    def points(self):
        tiedot = self.playerfile
        stats = self.statfile
        stats_data = stats['data']
        tupla = ()
        lista = []
        for i in tiedot:
            for a in stats_data:
                if a['playerId'] == i.id:
                    points = a['points']
                    tupla = (i,points)
                    lista.append(tupla)
                    break
            else:
                tupla = (i,0)
                lista.append(tupla)
        lista.sort(key = lambda x:x[0])
        lista.sort(key = lambda x:x[1],reverse = True)
        return lista
        

class Team:

    def __init__(self,name,abbreviation,conference,division):
        self.name = name
        self.abbreviation = abbreviation
        self.conference = conference
        self.division = division
        self.all_players = []
        self.all_goals = []
        self.all_points = []
    
    def __str__(self):
        return "".join(map(str,('{}'.format(self.name))))

    def add_player(self,player):
        self.all_players.append(player)


    def add_goals(self,player,goals):
        tupla = (player,goals)
        self.all_goals.append(tupla)

    def add_points(self,player,points):
        tupla = (player,points)
        self.all_points.append(tupla)

    def players(self):
        lista = self.all_players
        return lista

    def goals(self):
        lista = self.all_goals
        lista.sort(key=lambda tup: tup[0])
        lista.sort(key=lambda tup: tup[1],reverse = True)
        return lista

    def points(self):
        lista = self.all_points
        lista.sort(key=lambda tup: tup[0])
        lista.sort(key=lambda tup: tup[1],reverse = True)
        return lista
            
class Player:

    def __init__(self,firstName,lastName,country,birthDate,position,id):
        self.firstName = firstName
        self.lastName = lastName
        self.country = country
        real_birthdate = birthDate.split('-')
        real_birthdate = real_birthdate[2] + '.' + real_birthdate[1] + '.' + real_birthdate[0]
        self.birthDate = real_birthdate
        self.position = position
        self.id = id

    def __str__(self):

        return "".join(map(str,('{}, {} {} {} {}'.format(self.lastName,self.firstName,self.position,self.country,self.birthDate))))

    def __gt__(self,other):
        if self.lastName > other.lastName:
            return True
        elif self.lastName < other.lastName:
            return False
        else:
            if self.firstName > other.firstName:
                return True
            elif self.firstName < other.firstName:
                return False
            else:
                if self.id > other.id:
                    return True
                else:
                    return False

league = League("teams.json", "players_sample.json", "playerstats_sample.json")


## Testing

for t in league.teams(conference="Eastern"):
  print(t.name, t.abbreviation, t.conference, t.division, sep=", ")
print("\n")

for t in league.teams(division="Atlantic"):
  print(t.name, t.abbreviation, t.conference, t.division, sep=", ")
print("\n")

print(league.team("WSH").name)
print("\n")

for p in league.players():
  print(p)
print("\n")

for p in league.players("USA"):
  print(p)
print("\n")

for p,v in league.goals():
  print(v, p)
print("\n")

for p,v in league.points():
  print(v, p)
print("\n")

for t in league.teams():
  print(t.name, t.abbreviation, t.conference, t.division, sep=", ")

  for p in sorted(t.players(), reverse=True):
    print(p.firstName + " " + p.lastName, p.country, p.birthDate, p.position, sep=", ")
  print()

  for p,v in t.points():
    print(v, p)
  print()

  for p,v in t.goals():
    print(v, p)
  print("\n")