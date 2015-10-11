curl -s -O http://s3.amazonaws.com/alexa-static/top-1m.csv.zip
unzip -q -o top-1m.csv.zip top-1m.csv
head -1000 top-1m.csv | cut -d, -f2 | cut -d'/' -f1 > topsites.txt
rm top-1m.csv top-1m.csv.zip
