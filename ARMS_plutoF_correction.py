#do imports 
import sys
import os
import time
import json
import csv

# variables here
#import json file names ./ARMS_data.json
#get parent dir of current file 
parent_dit = os.path.dirname(os.path.abspath(__file__))
json_data = open(os.path.join(parent_dit, 'ARMS_data.json'))

#try and create the working output dir
try:
    os.mkdir(os.path.join(parent_dit, 'ARMS_output'))
except FileExistsError:
    print('ARMS_output dir already exists')

output_dir = os.path.join(parent_dit, 'ARMS_output')

#load json file
json_data_loaded = json.load(json_data)

#get the following variables from the json file
#sampling areas ids
sampling_areas_ids = []
#child_areas_ids
child_areas_ids = []
#get all sampling_event_ids
sampling_event_ids = []
for sampling_area in json_data_loaded['sampling_areas']:
    sampling_areas_ids.append(sampling_area['id'])
    for child_area in sampling_area['child_areas']:
        child_areas_ids.append(child_area['id'])
        for sampling_event in child_area['sampling_events']:
            sampling_event_ids.append(sampling_event['id'])
        
#make the following csv files
# Main.csv => Station, Country, ARMS_unit, Date_start, Date_end, Event_description, Material Samples, Observations, Sequences, Associated Date, Created, Updated
main_csv_data = []
for sampling_area in json_data_loaded['sampling_areas']:
    material_samples_csv = []
    observations_csv = []
    sequences_csv = []
    associated_data_csv = []
    main_data_csv = []
    try:
        os.mkdir(os.path.join(output_dir, sampling_area['name']))
    except Exception as e:
        print(e)
    
    #coun
    #country
    country = sampling_area['country']
    station = sampling_area['name']
    for child_area in sampling_area['child_areas']:
        pre_ARMS_unit = child_area['name']
        pre_ARMS_unit = pre_ARMS_unit.replace(station, '')
        pre_ARMS_unit = pre_ARMS_unit.replace('_', '')
        pre_ARMS_unit = pre_ARMS_unit.replace('ARMS', '')
        ARMS_unit = pre_ARMS_unit
        for sampling_event in child_area['sampling_events']:
            #date_start
            date_start = sampling_event['timespan_begin']
            #date_end
            date_end = sampling_event['timespan_end']
            #event_id
            event_id = sampling_event['id']
            #event_description
            try:
                date_end_desc = date_end.replace('-', '')
                date_start_desc = date_start.replace('-', '')
                if len(date_end.replace('-','')) != 8:
                    date_end_desc = "00000000"
                if len(date_start.replace('-','')) != 8:
                    date_start_desc = "00000000"
                event_description = "ARMS_" + station + '_' + ARMS_unit + '_' + date_start_desc + "_" + date_end_desc
            except:
                event_description = "ARMS_" + station + '_' + ARMS_unit + '_' + "00000000" + "_" + "00000000"
            #material_samples
            material_samples = len(sampling_event['material_samples'])
            #observations
            observations = len(sampling_event['observations'])
            #sequences
            sequences = len(sampling_event['sequences'])
            #associated_date
            associated_date = len(sampling_event['files'])
            #created
            created = sampling_event['created_at']
            #updated
            updated = sampling_event['updated_at']
            
            #material_sample table here
            for material_sample in sampling_event['material_samples']:
                sample_id = material_sample['id']
                sample_description = material_sample['description']
                material_sample_id = material_sample['name']
                sample_id_created_at = material_sample['created_at']
                sample_id_updated_at = material_sample['updated_at']
                sequences_in_sample = 0
                for sequence in sampling_event['sequences']:
                    if sequence["object_id"] == sample_id:
                        sequences_in_sample += 1
                material_samples_csv.append({'Material_Sample_ID': material_sample_id,"Parent_Event_ID": event_description,"Description": sample_description, "Created_At": sample_id_created_at, "Updated_At": sample_id_updated_at, "Sequences": sequences_in_sample, "Associated data": associated_date})
                
            #observation table here
            for observation in sampling_event['observations']:
                observation_id = observation['id']
                observation_remarks = observation['remarks']
                observation_is_varified = observation['moderation_status']
                for determination in observation['determinations']:
                    observation_updated_at = determination['updated_at']
                    observation_created_at = determination['created_at']
                    taxon_name = determination['taxon_node']
                    observations_csv.append({
                        "Station": station,
                        "Country": country,
                        "ARMS_unit": ARMS_unit,
                        "date_start": date_start,
                        "date_end": date_end,
                        "Event_id": event_description,
                        "Remarks": observation_remarks,
                        "Is_Varified": observation_is_varified,
                        "Taxon_Name": taxon_name,
                        "created_at": observation_created_at,
                        "updated_at": observation_updated_at
                    })
            
            #sequences table here
            for sequence in sampling_event['sequences']:
                sequence_id = sequence['id']
                sequence_updated_at = sequence['updated_at']
                sequence_created_at = sequence['created_at']
                sequence_sequence = sequence['sequence']
                sequence_chimeric = sequence['chimeric_status']
                sequence_unite_status = sequence['unite_status']
                sequence_low_quality = sequence['quality_status']
                sequence_forward_primer = sequence['forw_primer_sequence']
                sequence_reverse_primer = sequence['rev_primer_sequence']
                sequence_remarks = sequence['remarks']
                sequence_regions = ";".join(sequence['regions'])
                sequences_csv.append({
                    "Station": station,
                    "Country": country,
                    "ARMS_unit": ARMS_unit,
                    "date_start": date_start,
                    "date_end": date_end,
                    "Event_id": event_description,
                    "Sequence_ID": sequence_id,
                    "Sequence": sequence_sequence,
                    "Chimeric": sequence_chimeric,
                    "Unite_Status": sequence_unite_status,
                    "Low_Quality": sequence_low_quality,
                    "Forward_Primer": sequence_forward_primer,
                    "Reverse_Primer": sequence_reverse_primer,
                    "Remarks": sequence_remarks,
                    "Regions": sequence_regions,
                    "created_at": sequence_created_at,
                    "updated_at": sequence_updated_at
                })
                
            #associated_data table here
            for file in sampling_event['files']:   
                file_name = file['identifier'] 
                file_type = file['type']
                file_download_url = file['download_link']
                associated_data_csv.append({
                    "Station": station,
                    "Country": country,
                    "ARMS_unit": ARMS_unit,
                    "date_start": date_start,
                    "date_end": date_end,
                    "Event_id": event_description,
                    "File_Name": file_name,
                    "File_Type": file_type,
                    "File_Download_URL": file_download_url,
                    "created_at": created,
                    "updated_at": updated
                })
            
            main_data_csv.append({'Station': station, 'Country': country, 'ARMS_unit': ARMS_unit, 'Date_start': date_start, 'Date_end': date_end, 'Event_ID': event_description, 'Material Samples': material_samples, 'Observations': observations, 'Sequences': sequences, 'Associated Date': associated_date, 'Created': created, 'Updated': updated})
            #append dictionary of data to main_csv_data
            main_csv_data.append({'Station': station, 'Country': country, 'ARMS_unit': ARMS_unit, 'Date_start': date_start, 'Date_end': date_end, 'Event_ID': event_description, 'Material Samples': material_samples, 'Observations': observations, 'Sequences': sequences, 'Associated Date': associated_date, 'Created': created, 'Updated': updated})
    with open(os.path.join(output_dir, sampling_area['name'],"material_samples_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Material_Sample_ID', 'Parent_Event_ID', 'Description', 'Created_At', 'Updated_At', 'Sequences', 'Associated data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in material_samples_csv:
            writer.writerow(data)
    
    with open(os.path.join(output_dir, sampling_area['name'],"observations_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Station', 'Country', 'ARMS_unit', 'date_start', 'date_end', 'Event_id', 'Remarks', 'Is_Varified', 'Taxon_Name', 'created_at', 'updated_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in observations_csv:
            writer.writerow(data)
    
    with open(os.path.join(output_dir, sampling_area['name'],"sequences_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Station', 'Country', 'ARMS_unit', 'date_start', 'date_end', 'Event_id', 'Sequence_ID', 'Sequence', 'Chimeric', 'Unite_Status', 'Low_Quality', 'Forward_Primer', 'Reverse_Primer', 'Remarks', 'Regions', 'created_at', 'updated_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in sequences_csv:
            writer.writerow(data)
            
    with open(os.path.join(output_dir, sampling_area['name'],"associated_data_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Station', 'Country', 'ARMS_unit', 'date_start', 'date_end', 'Event_id', 'File_Name', 'File_Type', 'File_Download_URL', 'created_at', 'updated_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in associated_data_csv:
            #decode all the binary values in the data dict by utf-8 and encode them to cp850 and then decode again by cp580
            #
            data = {k: v.encode('cp850','replace').decode('cp850') for k, v in data.items()}
            writer.writerow(data)
    
    with open(os.path.join(output_dir, sampling_area['name'],"overview_data_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Station', 'Country', 'ARMS_unit', 'Date_start', 'Date_end', 'Event_ID', 'Material Samples', 'Observations', 'Sequences', 'Associated Date', 'Created', 'Updated']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in main_data_csv:
            writer.writerow(data)

#write the main.csv
with open(os.path.join(output_dir, 'overview.csv'), 'w', newline='') as csvfile:
    fieldnames = ['Station', 'Country', 'ARMS_unit', 'Date_start', 'Date_end', 'Event_ID', 'Material Samples', 'Observations', 'Sequences', 'Associated Date', 'Created', 'Updated']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in main_csv_data:
        writer.writerow(data)
