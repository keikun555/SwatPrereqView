#!/bin/bash
D=$1
python3 $D/scraper/scraper.py | python3 $D/converter/converter.py -o $D/static/data/graph.json
