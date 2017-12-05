# NBA Most Improved Player Finder

This is a formula I made to determine the most improved player in an NBA season, for use in my video game [Basketball GM](https://basketball-gm.com/).

## Method

A score is computed for every player representing how much they improved this season relative to last season. It takes these variables as inputs:

* mp: Total minutes played this season
* mp_old: Total minutes played last season
* ws: [Win shares](https://www.basketball-reference.com/about/ws.html) this season
* ws_old: Win shares last season
* ws_max: Max win shares from any prior season (for the earlier seasons in this dataset, this might not be computed accurately, but it doesn't seem to cause huge problems)
* ws48: Win shares per 48 minutes this season
* ws48_old: Win shares per 48 minutes last season

This method is designed to roughly equally value improvements in both total production (win shares) and per-minute productivity (win shares per 48 minutes) while penalizing players whose playing time is too low or who are already establisihed stars coming off a bad season.

For details, see 4-analyze.py.

## Data

The data came from screen scraping basketball-reference.com, which is not something I want to put in a public repo because I don't want to encourage tons of people hammering their servers (as if tons of people will ever read this...). For that reason, the first two steps in the analysis (1-get-data.sh and 2-parse.py) are blank. But I did include the parsed data in a CSV file, 2-parsed.csv.

Then, 3-process.py takes that data and computes the derived variables mentioned above, saving it to 3-processed.csv.

Finally, 4-analyze.py computes the score described above and displays the top 10 most improved players for every season from 2005-2017.

## More

[There are more details in this blog post I wrote.](https://basketball-gm.com/blog/2017/12/most-improved-player-award/) Also, go play [Basketball GM](https://basketball-gm.com/) and then send me some improvements [on GitHub](https://github.com/dumbmatter/basketball-gm).
