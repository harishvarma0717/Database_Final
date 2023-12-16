#!/usr/bin/env python
# coding: utf-8

# ### Data Preprocessing

# #### Handeling Missing values and Duplicates

# In[10]:


import pandas as pd

# Function to preprocess Event Organizers dataset
def preprocess_organizers(df):
    # Handling Missing Values
    df.fillna({'Name': 'Unknown', 'Contact Information': 'No Contact'}, inplace=True)
    df['List of Events'] = df['List of Events'].fillna("[]")
    
    # Remove rows with 'Unknown' or empty entries
    df = df[~df.isin(['Unknown', '']).any(axis=1)]
    return df

    # Remove Duplicates
    df.drop_duplicates(inplace=True)

    return df

# Function to preprocess Vendors dataset
def preprocess_vendors(df):
    # Handling Missing Values
    df['Name'].fillna('Unknown', inplace=True)
    df['Service/Product Description'].fillna('Not Specified', inplace=True)
    df['Sustainability Rating'].fillna(df['Sustainability Rating'].mean(), inplace=True)
    df['Contact Information'].fillna('No Contact', inplace=True)
    
    # Remove rows with 'Unknown' or empty entries
    df = df[~df.isin(['Unknown', '']).any(axis=1)]
    return df

    # Remove Duplicates
    df.drop_duplicates(inplace=True)

    return df

# Function to preprocess Participants dataset
def preprocess_participants(df):
    # Handling Missing Values
    df['Name'].fillna('Unknown', inplace=True)
    df['Contact Information'].fillna('No Contact', inplace=True)
    df['Events Attended'] = df['Events Attended'].fillna("[]")
    
    # Remove rows with 'Unknown' or empty entries
    df = df[~df.isin(['Unknown', '']).any(axis=1)]
    return df

    # Remove Duplicates
    df.drop_duplicates(inplace=True)

    return df

# Function to preprocess Events dataset
def preprocess_events(df):
    # Handling Missing Values
    df['Name'].fillna('Unnamed Event', inplace=True)
    df['Date & Time'].fillna('2023-01-01 00:00', inplace=True)
    df['Venue'].fillna('Unknown', inplace=True)
    df['Organizer ID'].fillna('No Organizer', inplace=True)
    df['List of Vendors'].fillna("[]", inplace=True)
    df['List of Participants'].fillna("[]", inplace=True)
    df['Sustainability Checklist'].fillna("[]", inplace=True)
    df['Carbon Footprint'].fillna(df['Carbon Footprint'].mean(), inplace=True)
    
    # Remove rows with 'Unknown' or empty entries
    df = df[~df.isin(['Unknown', '']).any(axis=1)]
    return df

    # Remove Duplicates
    df.drop_duplicates(inplace=True)

    return df

# Paths to the enriched datasets
organizers_path = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\enriched_event_organizers.csv"
vendors_path = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\enriched_vendors.csv"
participants_path = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\enriched_participants.csv"
events_path = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\enriched_events.csv"

# Loading the datasets
df_organizers = pd.read_csv(organizers_path)
df_vendors = pd.read_csv(vendors_path)
df_participants = pd.read_csv(participants_path)
df_events = pd.read_csv(events_path)

# Preprocessing each dataset
preprocessed_organizers = preprocess_organizers(df_organizers)
preprocessed_vendors = preprocess_vendors(df_vendors)
preprocessed_participants = preprocess_participants(df_participants)
preprocessed_events = preprocess_events(df_events)

# Saving the preprocessed datasets to new CSV files
output_path_organizers = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\event_organizers.csv"
output_path_vendors = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\vendors.csv"
output_path_participants = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\participants.csv"
output_path_events = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\events.csv"

# Corrected paths in the to_csv function
preprocessed_organizers.to_csv(output_path_organizers, index=False)
preprocessed_vendors.to_csv(output_path_vendors, index=False)
preprocessed_participants.to_csv(output_path_participants, index=False)
preprocessed_events.to_csv(output_path_events, index=False)



# #### Data Transformation

# In[11]:


import pandas as pd
from datetime import datetime

# Load the preprocessed datasets
df_organizers = pd.read_csv(r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\event_organizers.csv")
df_vendors = pd.read_csv(r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\vendors.csv")
df_participants = pd.read_csv(r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\participants.csv")
df_events = pd.read_csv(r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\events.csv")

# Transform Event Organizers dataset
df_organizers['ID'] = df_organizers['ID'].astype(str)
df_organizers['Name'] = df_organizers['Name'].astype(str)
df_organizers['Contact Information'] = df_organizers['Contact Information'].astype(str)
# Assuming 'List of Events' is a string representation of a list
df_organizers['List of Events'] = df_organizers['List of Events'].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Transform Vendors dataset
df_vendors['ID'] = df_vendors['ID'].astype(str)
df_vendors['Name'] = df_vendors['Name'].astype(str)
df_vendors['Service/Product Description'] = df_vendors['Service/Product Description'].astype(str)
df_vendors['Sustainability Rating'] = pd.to_numeric(df_vendors['Sustainability Rating'], errors='coerce')
df_vendors['Contact Information'] = df_vendors['Contact Information'].astype(str)

# Transform Participants dataset
df_participants['ID'] = df_participants['ID'].astype(str)
df_participants['Name'] = df_participants['Name'].astype(str)
df_participants['Contact Information'] = df_participants['Contact Information'].astype(str)
# Assuming 'Events Attended' is a string representation of a list
df_participants['Events Attended'] = df_participants['Events Attended'].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Transform Events dataset
df_events['ID'] = df_events['ID'].astype(str)
df_events['Name'] = df_events['Name'].astype(str)
df_events['Date & Time'] = pd.to_datetime(df_events['Date & Time'], errors='coerce')
df_events['Venue'] = df_events['Venue'].astype(str)
df_events['Organizer ID'] = df_events['Organizer ID'].astype(str)
# Assuming 'List of Vendors' and 'List of Participants' are string representations of lists
df_events['List of Vendors'] = df_events['List of Vendors'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df_events['List of Participants'] = df_events['List of Participants'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df_events['Sustainability Checklist'] = df_events['Sustainability Checklist'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df_events['Carbon Footprint'] = pd.to_numeric(df_events['Carbon Footprint'], errors='coerce')

# Specified file paths for saving the transformed datasets
output_path_organizers = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\event_organizers.csv"
output_path_vendors = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\vendors.csv"
output_path_participants = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\participants.csv"
output_path_events = r"E:\UMassD\Fall23\CIS552 - DBD\Course Project\Cleaned datasets\events.csv"

# Saving the transformed datasets to the specified paths
df_organizers.to_csv(output_path_organizers, index=False)
df_vendors.to_csv(output_path_vendors, index=False)
df_participants.to_csv(output_path_participants, index=False)
df_events.to_csv(output_path_events, index=False)


# In[ ]:





# In[ ]:




