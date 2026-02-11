# This file handles reading the data from the file.

def iterate_rows(file):
    file.stream.seek(0)
    for line in file.stream:
        yield line.decode("utf-8").replace("\r", "").split("\t")
        
def scan_file_layout(file):
    layout = {
        "Boat_Info_Line": None,
        "Column_Name_Line": None,
        "Data_Start_Line": None,
        "Data_End_Line": None,
        "Big_Data_Start_Line": None,
        "Big_Data_Column_Line": None,
        "GPS_Start_Line": None,
        "GPS_End_Line": None,
        "Side_Start_Line": None,
        "Crew_Info_Line": None,
        "Date_Line": None,
        "Serial_Line": None,
        "Seats": None,
        "RowingType": None,
        "GPS_Origin": None,
        "Lat": None,
        "Lon": None,
        "Big_Data_Headers": None,
        "Regular_Data_Headers": None,
        "Date": None,
        "OarLength": None,
        "Inboard": None,
    }

    for i, row in enumerate(iterate_rows(file)):
        if len(row) > 0:
            if (row[0] == 'Side\n') or (row[0] == 'Side'):
                layout['Side_Start_Line'] = i + 1

        if len(row) > 1:
            if (row[1] == 'SwivelPower'):
                layout['Data_Start_Line'] = i + 2
                layout['Column_Name_Line'] = i
                layout['Regular_Data_Headers'] = row

            if (i == layout['GPS_Origin']):
                layout['Lat'] = float(row[0])
                layout['Lon'] = float(row[1])

            if (row[1] == 'Seats'):
                layout['Boat_Info_Line'] = i + 1

            if (i == layout['Boat_Info_Line']) and (i != 0):
                layout['Seats'] = int(row[1])
                layout['RowingType'] = row[3]

        if len(row) > 2:
            if (row[2] == 'Chanb007'):
                if layout['Data_End_Line'] == None:
                    layout['Data_End_Line'] = i - 2

            if (row[0] == 'Sweep Oar Inboard'):
                layout['Inboard'] = row[1]

            if (row[0] == 'Sweep Oar Length'):
                layout['OarLength'] = row[1]

            if (row[2] == '0x800A\n') or (row[2] == '0x800A'):
                layout['GPS_End_Line'] = i
                
        if len(row) > 4:
            if (row[3] == 'Start Time'):
                layout['Date_Line'] = i + 1

        if i == layout['Date_Line']:
            layout['Date'] = str(row[3]).strip('"')
        
        if len(row) > 3:
            if (row[0]) == 'Lat':
                layout['GPS_Origin'] = i + 1

        if len(row) > 7:
            if row[0] == 'Serial #':
                layout['Serial_Line'] = i + 1

        if len(row) > 10:
            if row[1] == 'GateAngle':
                layout['Big_Data_Start_Line'] = i + 2
                layout['Big_Data_Column_Line'] = i
                layout['Big_Data_Headers'] = row

        if len(row) > 10:
            if row[1] == 'Name':
                layout['Crew_Info_Line'] = i + 1

        if len(row) > 12:
            if row[1] == 'GPS X Lo':
                layout['GPS_Start_Line'] = i + 2


    return layout
