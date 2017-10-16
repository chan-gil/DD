# import folium

lat_long = [49.2856399, -123.1201878]
# map2 = folium.Map(location = lat_long, zoom_start=13)
# map2.Marker(location = lat_long, radius=500, popup='downtown', line_color='#3186cc', fill_color='#3186cc')
# # map2.create_map(path='downtown.html')




import folium

map_osm=folium.Map(lat_long, zoom_start=6, tiles='Stamen Terrain')
folium.Marker(lat_long, popup='test_section').add_to(map_osm)

map_osm.save('spst.html')