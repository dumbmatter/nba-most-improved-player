# Take 2-parsed.csv and transform it to 3-processed.csv by merging dupe player-seasons and adding columns containing diffs from last season

from collections import defaultdict
import csv

players = defaultdict(dict)

with open('csv/2-parsed.csv') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        row['season'] = int(row['season'])
        row['mp'] = int(row['mp'])
        row['ws'] = float(row['ws'])
        row['ws48'] = float(row['ws48'])
        if (row['season'] in players[row['id']]):
            # Merge with existing row, must have been traded (weighted sum for ws48 might not be valid)
            players[row['id']][row['season']]['ws48'] = (row['mp'] * row['ws48'] + players[row['id']][row['season']]['mp'] * players[row['id']][row['season']]['ws48']) / (row['mp'] + players[row['id']][row['season']]['mp']);
            players[row['id']][row['season']]['ws'] += row['ws'];
            players[row['id']][row['season']]['mp'] += row['mp'];
        else:
            players[row['id']][row['season']] = row;

def ws_max(rows, current_season):
    ws_max = -float('inf')
    for row in rows:
        if (row['ws'] > ws_max and row['season'] < current_season):
            ws_max = row['ws']
    return ws_max

# Fill in new values: num_seasons, mp_old, ws_old, ws48_old
rows = []
for i in players:
    seasons = players[i].keys()

    for s in seasons:
        row = players[i][s]
        row['ws_max'] = ws_max(players[i].values(), s)
        if (s - 1) in seasons:
            old = players[i][s - 1]
            row['mp_old'] = old['mp']
            row['ws_old'] = old['ws']
            row['ws48_old'] = old['ws48']
            rows.append(row)

with open('csv/3-processed.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, ['id', 'name', 'season', 'team', 'mp_old', 'mp', 'ws_old', 'ws', 'ws_max', 'ws48_old', 'ws48'])
    dict_writer.writeheader()
    dict_writer.writerows(rows)
