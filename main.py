import folium
import time

def input_from_file(year):
    '''
    str -> list
    Generate list of films and their location of the such year
    '''

    file_name = "d:/UCU/2semestr/lab2/film_map_creator/locations.list"
    f = open(file_name, encoding='utf-8', errors='ignore')
    data = f.readline()

    while not data.startswith("=============="):
        data = f.readline().strip()
    info = []

    while not data.startswith("-----------------------------------------------------------------------------"):
        data = f.readline()
        year1 = '(' + year + ')'
        if year1 in data:
            data1 = data.split("\t")
            data4 = []
            for j in data1:
                if j:
                    data3 = []
                    data3.append(j)
                    data4.append(data3)
            info.append(data4)

    return info

def loc_fun(list1, lat, lon):
    '''
    list -> list
    Return list of coordinates and film names
    '''
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent = "myGeocoder")
    list_film = []
    for i in list1:
        loc = i[1]
        location1 = geolocator.geocode(loc)
        lat1 = location1.latitude
        lon1 = location1.longitude
        list_film.append([[lat1, lon1], i[0]])
        time.sleep(1)

    n = 100
    while len(list_film) > 10:
        for i in list_film:
            loc = i[0]
            lat2 = loc[0]
            lon2 = loc[1]

            if ((lat - n) > lat2) and ((lat + n) < lat2):
                list_film.pop([i])

            if ((lon - n) > lon2) and ((lon + n) < lon2):
                list_film.pop([i])

            n = n * 0.1
        
        return list_film

def map_creator(lat, lon, list_film):
    '''
    int, int, list -> NoneType
    Create a html map
    '''
    map = folium.Map(location=[lat, lon],
                    zoom_start=10)

    fg_fl = folium.FeatureGroup(name="Films")

    for k in list_film:
        lt = k[0][0]
        ln = k[0][1]
        film = k[1]
        fg_fl.add_child(folium.CircleMarker(location = [lt, ln],
                                            radius = 10,
                                            popup = film,
                                            color = 'red',
                                            fill_opacity = 0.5))

    fg_pp = folium.FeatureGroup(name="Population")

    fg_pp.add_child(folium.GeoJson(data = open('d:/UCU/2semestr/lab2/film_map_creator/world.json', 'r',
                                encoding = 'utf-8-sig').read(),
                                style_function = lambda x: {'fillColor':'green'
        if x['properties']['POP2005'] < 10000000
        else 'blue' if 10000000 <= x['properties']['POP2005'] < 20000000
        else 'yellow' if 20000000 <= x['properties']['POP2005'] < 30000000
        else 'orange' if 30000000 <= x['properties']['POP2005'] < 40000000
        else 'pink' if 40000000 <= x['properties']['POP2005'] < 50000000
        else 'purple' if 50000000 <= x['properties']['POP2005'] < 60000000
        else 'red'}))

    map.add_child(fg_fl)
    map.add_child(fg_pp)
    map.add_child(folium.LayerControl())
    map.save('d:/UCU/2semestr/lab2/film_map_creator/movies_map.html')

def start():
    '''
    NoneType -> NoneType
    Launch the module
    '''

    year = input('Please enter a year you would like to have a map for: ')

    if int(year) > 1500 and int(year) < 2021:
        list1 = input_from_file(year)
        location = input('Please enter your location (format: lat, long): ')
        location = location.split(', ')

        try:
            lat = float(location[0])
            lon = float(location[1])
            print("Map is generating...")

            list_films = loc_fun(list1, lat, lon)
            print("Please wait...")

            map_creator(lat, lon, list_films)
            print("Finished. Please have look on the map movies_map.html")

        except ValueError:
            print("Error")

    else:
        print("Error")

start()
