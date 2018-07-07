import json

with open('places.json', 'r') as file_reader:
    all_places = json.load(file_reader)

bars = []

for place in all_places:
    place_type = place['Cells']['TypeObject']
    if place_type == 'бар':
        bars.append(place)

with open('bars.json', 'w') as file_writer_bars:
    json.dump(bars, file_writer_bars)