# Create a CSV file (2-parse.csv) containing data extracted from the HTML files

import csv
from lxml import html

teams = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
seasons = [2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004]

def get_adv_stats_table(filename):
    output = ''
    with open(filename, 'r') as f:
        started = False
        for line in f:
            if '<table class="sortable stats_table" id="advanced"' in line:
                started = True
            if started:
                if '</table>' in line:
                    return output
                output += line

    raise Exception('Could not find start and/or end of advanced stats table in %s' % (filename))

# https://stackoverflow.com/a/1034633/786644
def xstr(s):
    if s is None:
        return '0'
    return str(s)

rows = []

for team in teams:
    for season in seasons:
        if (team == 'CHO' and season == 2004):
            # Team didn't exist this season!
            continue

        filename = 'html/%s_%d.html' % (team, season)
        print(filename)
        adv_stats_table = get_adv_stats_table(filename)

        tree = html.fromstring(adv_stats_table)

        player_id = tree.xpath('//td/@data-append-csv')
        name = tree.xpath('//td[@data-stat="player"]/a')
        mp = tree.xpath('//td[@data-stat="mp"]')
        ws = tree.xpath('//td[@data-stat="ws"]')
        ws48 = tree.xpath('//td[@data-stat="ws_per_48"]')

        if (len(mp) != len(player_id) or len(mp) != len(ws) or len(mp) != len(ws48) or len(mp) != len(name)):
            print('player_id len', len(player_id))
            print('name len', len(name))
            print('mp len', len(mp))
            print('ws len', len(ws))
            print('ws48 len', len(ws48))
            raise Exception('Not all lengths equal')

        for i in range(len(mp)):
            #id, team, season, num_seasons, min_old, min, ws_old, ws, ws48_old, ws48
            row = {
                'id': player_id[i],
                'name': name[i].text,
                'team': team,
                'season': season,
                'mp': xstr(mp[i].text),
                'ws': xstr(ws[i].text),
                'ws48': xstr(ws48[i].text),
            }

            rows.append(row)

with open('csv/2-parsed.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, ['id', 'name', 'season', 'team', 'mp', 'ws', 'ws48'])
    dict_writer.writeheader()
    dict_writer.writerows(rows)
