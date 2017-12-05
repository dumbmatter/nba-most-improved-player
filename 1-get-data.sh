# This required some manual effort after, to deal with renamed teams

teams=( "ATL" "BOS" "BRK" "NJN" "CHA" "CHO" "CHI" "CLE" "DAL" "DEN" "DET" "GSW" "HOU" "IND" "LAC" "LAL" "MEM" "MIA" "MIL" "MIN" "NOH" "NOK" "NOP" "NYK" "OKC" "ORL" "PHI" "PHO" "POR" "SAC" "SAS" "TOR" "UTA" "WAS" )
seasons=( 2017 2016 2015 2014 2013 2012 2011 2010 2009 2008 2007 2006 2005 2004 )

mkdir -p html
mkdir -p csv

for team in "${teams[@]}"
do
    for season in "${seasons[@]}"
    do
        wget -O html/${team}_${season}.html https://www.basketball-reference.com/teams/${team}/${season}.html
        sleep $[ ( $RANDOM % 10 )  + 1 ]s
    done
done