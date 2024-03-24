import openpyxl as op
wb = op.load_workbook("Cordonnees_GPS.xlsx", read_only=True)
ws = wb.active

for row in ws.iter_rows():
    print(row[0].value," Cordonne: ",row[1].value,"  ",row[2].value)
    

import geopy.distance
coords_nktt = (18.0783994226296, -15.885155269477)
coords_ndb = (21.0200766331283, -15.9151199295992)
distance=geopy.distance.geodesic(coords_nktt, coords_ndb).km 
print(distance)

