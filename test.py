import streetview_explorer

# Test coords
good_coords = [-33.85693857571269, 151.2144895142714]
klamath_coords = [42.225811, -121.784302]
empty_coords = [76.88924, -142.12060]
bad_coords = [76.88924, -192.12060]

data = streetview3.get_region_metadata(klamath_coords[0], klamath_coords[1])
print(data)

# pano_tile_response = streetview3.fetch_pano_tile(data["pano_id"], 90, 0)
# img = open("temp2.jpeg", "wb")
# img.write(pano_tile_response.content)