CREATE DATABASE PROJECT;

USE PROJECT;

CREATE TABLE EventOrganizers (
    OrganizerID VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255),
    ContactInfo VARCHAR(255),
    ListOfEvents TEXT
);

CREATE TABLE Vendors (
    VendorID VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255),
    ServiceProductDescription TEXT,
    SustainabilityRating DECIMAL(5,2),
    ContactInfo VARCHAR(255)
);

CREATE TABLE Participants (
    ParticipantID VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255),
    ContactInfo VARCHAR(255),
    EventsAttended TEXT
);

CREATE TABLE Events (
    EventID VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255),
    Venue VARCHAR(255),
    OrganizerID VARCHAR(255),
    ListOfVendors TEXT,
    ListOfParticipants TEXT,
    CarbonFootprint DECIMAL(10,2),
    FOREIGN KEY (OrganizerID) REFERENCES EventOrganizers(OrganizerID)
);
CREATE TABLE EventVendors (
    EventID VARCHAR(255),
    VendorID VARCHAR(255),
    PRIMARY KEY (EventID, VendorID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (VendorID) REFERENCES Vendors(VendorID)
);

CREATE TABLE EventParticipants (
    EventID VARCHAR(255),
    ParticipantID VARCHAR(255),
    PRIMARY KEY (EventID, ParticipantID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (ParticipantID) REFERENCES Participants(ParticipantID)
);

-- Participant Workflow Queries

-- Query 1: Fetch Events Attended by the Participant
-- Replace `%s` with the Participant ID in the application
SELECT EventsAttended
FROM Participants
WHERE ParticipantID = '%s';

-- Query 2: Fetch Organizers of These Events and Suggest Similar Events
-- Replace `%s` with the list of Event IDs obtained from Query 1
SELECT e.EventID, e.Name, e.Venue, eo.Name AS OrganizerName, eo.ContactInfo
FROM Events e
JOIN EventOrganizers eo ON e.OrganizerID = eo.OrganizerID
WHERE e.EventID IN (
    SELECT EventID 
    FROM Events 
    WHERE OrganizerID IN (
        SELECT OrganizerID 
        FROM Events 
        WHERE EventID IN ('%s')
    )
);

-- Vendor Workflow Queries

-- Query 3: Fetch Events Where Vendor Participated
-- Replace `%s` with the Vendor ID
SELECT EventID
FROM EventVendors
WHERE VendorID = '%s';

-- Query 4: Fetch Events Organized by the Organizers of These Events
-- Replace `%s` with the list of Event IDs obtained from Query 3
SELECT e.EventID, e.Name, e.Venue
FROM Events e
WHERE e.OrganizerID IN (
    SELECT OrganizerID 
    FROM Events 
    WHERE EventID IN ('%s')
);

-- Event Organizer Workflow Queries

-- Query 5: Fetch List of Events Organized
-- Replace `%s` with the Event Organizer ID
SELECT ListOfEvents
FROM EventOrganizers
WHERE OrganizerID = '%s';

-- Query 6: Fetch Events Attended by Participants of These Events
-- Replace `%s` with the list of Event IDs obtained from Query 5
SELECT EventID, Name, CarbonFootprint
FROM Events
WHERE EventID IN (
    SELECT EventID 
    FROM EventParticipants 
    WHERE ParticipantID IN (
        SELECT ParticipantID 
        FROM EventParticipants 
        WHERE EventID IN ('%s')
    )
)
ORDER BY CarbonFootprint ASC
LIMIT 5;



-- Indexing for optimization
CREATE INDEX idx_participant_id ON Participants(ParticipantID);
CREATE INDEX idx_vendor_id ON Vendors(VendorID);
CREATE INDEX idx_event_id ON Events(EventID);
CREATE INDEX idx_organizer_id ON EventOrganizers(OrganizerID);
CREATE INDEX idx_eventvendors_event_id ON EventVendors(EventID);
CREATE INDEX idx_eventvendors_vendor_id ON EventVendors(VendorID);
CREATE INDEX idx_eventparticipants_event_id ON EventParticipants(EventID);
CREATE INDEX idx_eventparticipants_participant_id ON EventParticipants(ParticipantID);

-- Optimized Query 1: Fetch Events Attended by the Participant
-- This query remains the same, but ensure the Participants table has an index on ParticipantID
SELECT EventsAttended
FROM Participants
WHERE ParticipantID = '%s';

-- Optimized Query 2: Fetch Organizers of These Events and Suggest Similar Events
-- Rewritten to use joins instead of IN subquery for better performance
SELECT e.EventID, e.Name, e.Venue, eo.Name AS OrganizerName, eo.ContactInfo
FROM Participants p
JOIN Events e2 ON FIND_IN_SET(e2.EventID, p.EventsAttended) > 0
JOIN EventOrganizers eo ON e2.OrganizerID = eo.OrganizerID
JOIN Events e ON eo.OrganizerID = e.OrganizerID
WHERE p.ParticipantID = '%s';

-- Optimized Query 3: Fetch Events Where Vendor Participated
-- This query is efficient if EventVendors has an index on VendorID
SELECT EventID
FROM EventVendors
WHERE VendorID = '%s';

-- Optimized Query 4: Fetch Events Organized by the Organizers of These Events
-- Use join and derived tables for efficient querying
SELECT e.EventID, e.Name, e.Venue
FROM Events e
JOIN (
    SELECT DISTINCT OrganizerID
    FROM Events
    WHERE EventID IN (
        SELECT EventID
        FROM EventVendors
        WHERE VendorID = '%s'
    )
) AS org ON e.OrganizerID = org.OrganizerID;

-- Optimized Query 5: Fetch List of Events Organized
-- This query is efficient if EventOrganizers has an index on OrganizerID
SELECT ListOfEvents
FROM EventOrganizers
WHERE OrganizerID = '%s';

-- Optimized Query 6: Fetch Events Attended by Participants of These Events
-- This query assumes EventParticipants and Participants have indices on their IDs
SELECT e.EventID, e.Name, e.CarbonFootprint
FROM Events e
JOIN EventParticipants ep ON e.EventID = ep.EventID
JOIN (
    SELECT ParticipantID
    FROM EventParticipants
    WHERE EventID IN (
        SELECT EventID
        FROM EventOrganizers
        WHERE OrganizerID = '%s'
    )
) AS p ON ep.ParticipantID = p.ParticipantID
ORDER BY e.CarbonFootprint ASC
LIMIT 5;

