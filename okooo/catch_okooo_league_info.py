__author__ = 'mahy'
# -*- coding: utf8 -*-
import requests
import bs4

import collections

def getScores(season,url,lg,outputfile):
    # season = '18/19'
    # url = 'http://www.okooo.com/soccer/league/35/schedule/13829/1-42-1/'
    response = requests.get(url)
    content = bs4.BeautifulSoup(response.content.decode("gb18030"), "lxml")
    scorctable = content.find_all("table",attrs={"class": "ddtable"})
    scorelist = scorctable[1].find_all("tr",attrs={"class": "BlackWords"})

    for tr in scorelist:
        tds = tr.find_all("td")
        ranking = tds[0].string
        tname = tds[1].string
        total_game_num = tds[2].string
        total_win =  tds[3].string
        total_draw = tds[4].string
        total_lost = tds[5].string
        total_goals = tds[6].string
        total_goals_lost = tds[7].string
        total_net_goals = tds[8].string

        home_game_num = tds[9].string
        home_win = tds[10].string
        home_draw = tds[11].string
        home_lost = tds[12].string
        home_goals = tds[13].string
        home_goals_lost = tds[14].string


        away_game_num = tds[15].string
        away_win = tds[16].string
        away_draw = tds[17].string
        away_lost = tds[18].string
        away_goals = tds[19].string
        away_goals_lost = tds[20].string
        score = tds[21].string.strip()
        print(ranking,tname,total_game_num,total_win,total_draw,total_lost,total_goals,total_goals_lost,total_net_goals,home_game_num,home_win,home_draw,home_lost,home_goals,home_goals_lost,away_game_num,away_win,away_draw,away_lost,away_goals,away_goals_lost,score,season,lg,sep=',',file=outputfile)

def getOdds(season,url,lg,outputfile):
    print(url)
    response = requests.get(url)
    content = bs4.BeautifulSoup(response.content.decode("gb18030"), "lxml")
    scorctable = content.find_all("table", attrs={"class": "ddtable"})
    oddslist = scorctable[0].find_all("tr", attrs={"class": "BlackWords"})
    #print(oddslist)
    for tr in oddslist:
        tds = tr.find_all("td")
        round = tds[0].string
        gametime = tds[1].string
        hname = tds[2].string.strip()
        score = ''
        gurl = ''
        if tds[3].find_all("strong"):
            score = tds[3].find_all("strong")[0].string
            gurl = tds[3].find_all("a")[0]['href']
        aname = tds[4].string.strip()
        win = tds[5].string.strip()
        draw = tds[6].string.strip()
        lost = tds[7].string.strip()
        score_arr = score.split('-')
        hg = ''
        ag = ''
        if len(score_arr) > 1:
            hg = score_arr[0]
            ag = score_arr[1]
        print(round,gametime,hname,hg,ag,aname,win,draw,lost,gurl,season,lg,sep=',',file=outputfile)


if __name__ == '__main__':
    seasons = collections.OrderedDict()
    # seasons['18/19'] = 'http://www.okooo.com/soccer/league/35/schedule/13829/1-42'
    # seasons['17/18'] = 'http://www.okooo.com/soccer/league/35/schedule/13262/1-42'
    # seasons['16/17'] = 'http://www.okooo.com/soccer/league/35/schedule/12694/1-42'
    # seasons['15/16'] = 'http://www.okooo.com/soccer/league/35/schedule/12137/1-42'
    # seasons['14/15'] = 'http://www.okooo.com/soccer/league/35/schedule/8238/1-42'
    # lg = '德甲'

    # seasons['18/19'] = 'http://www.okooo.com/soccer/league/17/schedule/13782/1-1'
    # seasons['17/18'] = 'http://www.okooo.com/soccer/league/17/schedule/13222/1-1'
    # seasons['16/17'] = 'http://www.okooo.com/soccer/league/17/schedule/12651/1-1'
    # seasons['15/16'] = 'http://www.okooo.com/soccer/league/17/schedule/12084/1-1'
    # seasons['14/15'] = 'http://www.okooo.com/soccer/league/17/schedule/8186/1-1'
    # lg = '英超'

    # seasons['18/19'] = 'http://www.okooo.com/soccer/league/182/schedule/13779/1-19'
    # seasons['17/18'] = 'http://www.okooo.com/soccer/league/182/schedule/13223/1-19'
    # seasons['16/17'] = 'http://www.okooo.com/soccer/league/182/schedule/12641/1-19'
    # seasons['15/16'] = 'http://www.okooo.com/soccer/league/182/schedule/12096/1-19'
    # seasons['14/15'] = 'http://www.okooo.com/soccer/league/182/schedule/8124/1-19'
    # lg = '法乙'

    # seasons['18/19'] = 'http://www.okooo.com/soccer/league/8/schedule/13846/1-36'
    # seasons['17/18'] = 'http://www.okooo.com/soccer/league/8/schedule/13342/1-36'
    # seasons['16/17'] = 'http://www.okooo.com/soccer/league/8/schedule/12749/1-36'
    # seasons['15/16'] = 'http://www.okooo.com/soccer/league/8/schedule/12176/1-36'
    # seasons['14/15'] = 'http://www.okooo.com/soccer/league/8/schedule/8578/1-36'
    # lg = '西甲'

    # seasons['18/19'] = 'http://www.okooo.com/soccer/league/23/schedule/13844/1-33'
    # seasons['17/18'] = 'http://www.okooo.com/soccer/league/23/schedule/13347/1-33'
    # seasons['16/17'] = 'http://www.okooo.com/soccer/league/23/schedule/12786/1-33'
    # seasons['15/16'] = 'http://www.okooo.com/soccer/league/23/schedule/12257/1-33'
    # seasons['14/15'] = 'http://www.okooo.com/soccer/league/23/schedule/8618/1-33'
    # lg = '意甲'

    seasons['18/19'] = 'http://www.okooo.com/soccer/league/34/schedule/13766/1-4'
    seasons['17/18'] = 'http://www.okooo.com/soccer/league/34/schedule/13224/1-4'
    seasons['16/17'] = 'http://www.okooo.com/soccer/league/34/schedule/12639/1-4'
    seasons['15/16'] = 'http://www.okooo.com/soccer/league/34/schedule/12095/1-4'
    seasons['14/15'] = 'http://www.okooo.com/soccer/league/34/schedule/8122/1-4'
    lg = '法甲'



    # seasons['19/20'] = 'http://www.okooo.com/soccer/league/44/schedule/14003/1-41'
    # lg = '德乙'

    # with open('/Users/hongyanma/okooo/odds.txt', 'w') as outputfile:
    #     getOdds('19/20', 'http://www.okooo.com/soccer/league/35/schedule/13951/1-42-1/', lg, outputfile)

    # with open('/Users/hongyanma/okooo/scores.txt','w') as outputfile:
    #     for sn in seasons:
    #         getScores(sn,seasons[sn]+'-1/',lg,outputfile)
    with open('/Users/hongyanma/okooo/odds.txt', 'w') as outputfile:
        for sn in seasons:
            for i in range(38):
                getOdds(sn,seasons[sn]+'-'+str(i+1)+'/',lg,outputfile)
    print('done !!!')
    # load data local infile '/Users/hongyanma/okooo/odds.txt' into table jc.tb_okooo_league_odds character set utf8 fields TERMINATED BY ','  (round,gametime,hname,hg,ag,aname,win,draw,lost,gurl,season,lg);
