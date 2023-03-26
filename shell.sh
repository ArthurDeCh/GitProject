#!/bin/bash
#get HTML code from the site
curl -s https://www.tradingsat.com/airbus-group-NL0000235190/ >Projet/output.html
#Get date
date=$(date +"%Y-%m-%d %H:%M:%S")
#get the price from the HTML code
price=$(grep -oP '<span class="price">\K[\d\.]+(?=\s+€</span>)' Projet/output.html)

price=$(echo "$price" | sed 's/\s//g')

echo "$date,$price" >> Projet/prix_airbus.csv
echo "The price is: €$price"
