import matplotlib.pyplot as plt
import requests
from hockey_rink import NHLRink
from matplotlib import cm
import numpy as np



player_to_chart = "Kirill Kaprizov"
team_of_player = "MIN"
#https://statsapi.web.nhl.com/api/v1/teams
team_id = "30"

#All MIN games
fig=plt.figure(figsize=(10,10))
plt.xlim([0,100])
plt.ylim([-42.5, 42.5])
xc=[]
yc=[]
seasons = ["20212022"]
shot_attempts = 0
sog = 0
goals = 0
for season in seasons:
    min_schedule = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?season="+season+"&teamId="+team_id+"&gameType=R")
    schedule = min_schedule.json()
    schedule = schedule["dates"]

    game_ids=[]
    for game in schedule:
        game_data=game["games"]
        game_data=(game_data[0])
        status = game_data["status"]
        status = status["abstractGameState"]
        if status == "Preview":
            continue
        else:
            id = game_data["gamePk"]
            game_ids.append(id)

    for ids in game_ids:
        url = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + str(ids) + "/feed/live")
        content = url.json()

        event = content["liveData"]
        game_data = content["gameData"]
        date = game_data["datetime"]
        datetime = date["dateTime"]
        datetime = datetime[0:10]
        teams = game_data["teams"]
        away = teams["away"]
        home = teams["home"]
        away_team = away["abbreviation"]
        home_team = home["abbreviation"]
        plays = event["plays"]
        all_plays = plays["allPlays"]
        if home_team == team_of_player:
            team_to_chart = home_team
        else:
            team_to_chart = away_team
        for i in all_plays:
            result = i["result"]
            event = result["event"]
            if event=="Goal" or event == "Shot":
                team_info = i["team"]
                team = team_info["triCode"]
                if team == team_to_chart:
                    players = (i["players"])
                    player = (players[0])
                    player = (player["player"])
                    player = (player["fullName"])
                    if player == player_to_chart:
                        shot_attempts += 1
                        print(player)
                        print(team)
                        print(event)
                        coords = (i["coordinates"])
                        print(coords)
                        print()
                        x = int(coords["x"])
                        y = int(coords["y"])

                        if x < 0:
                            x = abs(x)
                            xc.append(x)
                            y = y*-1
                            yc.append(y)

                        else:
                            x=x
                            xc.append(x)
                            y=y
                            yc.append(y)

                   
                         #if event=="Goal":
#                             goals+=1
#                             plt.plot(x, y, 'h', color="#4bad53",markersize=10)
                    
#                         elif event=="Shot":
#                             sog+=1
#                             #plt.plot(x, y, '.', color="#f0a911",markersize=15)
                        
            else:
                continue


rink = NHLRink()
ax = rink.draw(display_range="ozone")
hb = rink.hexbin(xc, yc, gridsize=30, alpha=0.95, cmap='Reds', reduce_C_function=np.sum)
cb = fig.colorbar(hb, ax=ax, label='counts')
# plt.title("Marcus Foligno All Shot Attempts: 2021-2022")
# plt.show()

# rink = NHLRink()
# ax = rink.draw(display_range="ozone")

plt.title( player_to_chart + ": All Shots on Goal: 2021-2022\n" + str(shot_attempts) + " Shots on Goal")
plt.show()
