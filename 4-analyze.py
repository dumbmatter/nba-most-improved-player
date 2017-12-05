from collections import defaultdict
import csv

results = defaultdict(list)

with open('csv/3-processed.csv') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        row['season'] = int(row['season'])
        row['mp'] = int(row['mp'])
        row['mp_old'] = int(row['mp_old'])
        row['ws_old'] = float(row['ws_old'])
        row['ws'] = float(row['ws'])
        row['ws_max'] = float(row['ws_max'])
        row['ws48'] = float(row['ws48'])
        row['ws48_old'] = float(row['ws48_old'])

        # Increasing WS by 5 is equal weight to increasing WS/48 by 0.1
        row['score'] = 0.02 * (row['ws'] - row['ws_old']) + (row['ws48'] - row['ws48_old'])

        # Penalty - lose 0.05 for every mpg last season under 15 (assuming 82 games)
        if row['mp_old'] < 82 * 15:
            row['score'] -= 0.05 * (15 - row['mp_old'] / 82)

        # Penalty - lose additional 0.05 for every mpg last season under 10 (assuming 82 games)
        if row['mp_old'] < 82 * 15:
            row['score'] -= 0.05 * (15 - row['mp_old'] / 82)

        # Penalty - lose 0.01 for every mpg this season under 30 (assuming 82 games)
        if row['mp'] < 82 * 30:
            row['score'] -= 0.01 * (30 - row['mp'] / 82)

        # Penalty - baseline required is 125% of previous best season. Lose 0.01 for every 1% below that.
        if row['ws'] < 1.25 * row['ws_max']:
            ratio = 1
            if row['ws_max'] != 0.0:
                ratio = row['ws'] / row['ws_max']

            # Sanity check... don't want two negative numbers blowing up the ratio
            if ratio < 0 or (row['ws'] < 0 and row['ws_max'] < 0):
                ratio = 0.0

            row['score'] -= 1.25 - ratio

        results[row['season']].append(row)

for s in sorted(results.keys()):
    sorted_results = sorted(results[s], key=lambda row: row['score'], reverse=True)
    print()
    print("%d season" % (s,))
    for i in range(len(sorted_results)):
        row = sorted_results[i]
        print("%2d. %s\n    Score: %.3f\n    WS %.1f -> %.1f, WS48 %.3f -> %.3f, MP: %d -> %d" % (i + 1, row['name'], row['score'], row['ws_old'], row['ws'], row['ws48_old'], row['ws48'], row['mp_old'], row['mp']))
        if (i >= 9):
            break
