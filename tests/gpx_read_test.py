import gpxpy

with open('2020-06-22T12_07_46+00_00_5328568219.gpx') as file:
    gpx = gpxpy.parse(file)

print(len(gpx.tracks[0].segments))
segment = gpx.tracks[0].segments[0]

print(segment.length_2d())
print(segment.length_3d())
