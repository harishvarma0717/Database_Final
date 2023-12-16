#!/usr/bin/env python
# coding: utf-8

import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="Database@123",
        database="project",
        auth_plugin='mysql_native_password'  # Specify the authentication plugin
    )

def execute_query(query, params=None):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def participant_workflow(participant_id):
    # Query 1: Fetch Events Attended by the Participant
    query1 = "SELECT EventsAttended FROM Participants WHERE ParticipantID = %s;"
    events_attended = execute_query(query1, (participant_id,))

    # Assuming events_attended is a list of event IDs
    if events_attended:
        event_ids = events_attended[0][0]  # Adjust based on your data format
        # Query 2: Fetch Organizers of These Events and Suggest Similar Events
        query2 = """
        SELECT e.EventID, e.Name, e.Venue, eo.Name AS OrganizerName, eo.ContactInfo
        FROM Events e
        JOIN EventOrganizers eo ON e.OrganizerID = eo.OrganizerID
        WHERE e.EventID IN (%s);
        """
        similar_events = execute_query(query2, (event_ids,))
        for event in similar_events:
            print(event)
    else:
        print("No events attended by participant.")

def vendor_workflow(vendor_id):
    # Query 3: Fetch Events Where Vendor Participated
    query3 = "SELECT EventID FROM EventVendors WHERE VendorID = %s;"
    events_with_vendor = execute_query(query3, (vendor_id,))

    # Assuming events_with_vendor is a list of event IDs
    if events_with_vendor:
        event_ids = [event[0] for event in events_with_vendor]
        # Query 4: Fetch Events Organized by the Organizers of These Events
        query4 = """
        SELECT e.EventID, e.Name, e.Venue
        FROM Events e
        WHERE e.OrganizerID IN (
            SELECT OrganizerID 
            FROM Events 
            WHERE EventID IN (%s)
        );
        """
        # This query will need to be adjusted to handle multiple event_ids
        # ...

        # Printing or processing the results
        for event in events_with_vendor:
            print(event)
    else:
        print("No events found for this vendor.")

def event_organizer_workflow(organizer_id):
    # Query 5: Fetch List of Events Organized
    query5 = "SELECT ListOfEvents FROM EventOrganizers WHERE OrganizerID = %s;"
    list_of_events = execute_query(query5, (organizer_id,))

    # Assuming list_of_events is a list of event IDs
    if list_of_events:
        event_ids = list_of_events[0][0]  # Adjust based on your data format
        # Query 6: Fetch Events Attended by Participants of These Events
        query6 = """
        SELECT EventID, Name, CarbonFootprint
        FROM Events
        WHERE EventID IN (
            SELECT EventID 
            FROM EventParticipants 
            WHERE ParticipantID IN (
                SELECT ParticipantID 
                FROM EventParticipants 
                WHERE EventID IN (%s)
            )
        )
        ORDER BY CarbonFootprint ASC
        LIMIT 5;
        """
        # This query will need to be adjusted to handle multiple event_ids
        # ...

        # Printing or processing the results
        for event in list_of_events:
            print(event)
    else:
        print("No events found for this event organizer.")

def main():
    print("Select an option:\n1. Participant\n2. Vendor\n3. Event Organizer")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        participant_id = input("Enter Participant ID: ")
        participant_workflow(participant_id)

    elif choice == '2':
        vendor_id = input("Enter Vendor ID: ")
        vendor_workflow(vendor_id)

    elif choice == '3':
        organizer_id = input("Enter Event Organizer ID: ")
        event_organizer_workflow(organizer_id)

    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
