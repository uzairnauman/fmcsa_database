with prepped_dimensions as (
    select * from {{ ref('int_carriers_cleaned') }}
)

select
    -- Identification, Dates & Status
    mcs150_date as "MCS-150 Entry Date",                                          -- Field 1 
    added_date as "System Entry Date",                                              -- Field 2 
    status_label as "Status",                                                       -- Field 3 (Derived) 
    dot_number as "USDOT Number",                                                   -- Field 4 
    operational_scope_label as "Operating Scope",                                   -- Field 8 (Derived) 
    business_structure_label as "Business Structure",                               -- Field 9 (Derived) 
    total_cars as "Light Commercial Vehicles",                                      -- Field 13 

    -- Contacts & Fleet Telemetry
    phone as "Office Phone",                                                        -- Field 17 
    cell_phone as "Mobile Phone",                                                   -- Field 19 
    total_trucks as "Straight Trucks Count",                                        -- Field 23 
    total_power_units as "Power Units Count",                                       -- Field 24 
    fleetsize_code as "Fleetsize Code Designation",                                 -- Field 26 
    entity_operations_label as "Entity Operations",                                 -- Field 33 (Derived) 

    -- Operational Context Arrays
    hazmat_indicator as "Hazmat Flag",                                              -- Field 44 
    total_cdl_drivers as "CDL License Count",                                       -- Field 49 
    total_drivers as "Total Workforce Drivers",                                     -- Field 50 
    classification_definition as "Classification Definition Text",                  -- Field 52 [cite: 11]

    -- Identification Strings
    legal_name as "Company Name",                                                   -- Field 53 [cite: 11]
    dba_name as "DBA Name",                                                         -- Field 54 [cite: 11]

    -- Physical Locations
    physical_city as "State Location City",                                         -- Field 56 [cite: 11]
    physical_state as "Physical State",                                             -- Field 58 [cite: 11]
    physical_zip as "Physical ZIP Code",                                            -- Field 59 [cite: 11]

    -- Mailing Coordinates & Comms Dropdowns
    mailing_state as "Mailing State",                                               -- Field 62 [cite: 11]
    mailing_city as "Mailing City",                                                 -- Field 63 [cite: 11]
    mailing_zip as "Mailing ZIP Code",                                              -- Field 65 [cite: 11]
    email_address as "Corporate Email",                                             -- Field 69 [cite: 11]

    -- Cargo Classifications Matrix Flags
    carries_general_freight as "Flag: General Freight",                             -- Field 75 [cite: 11]
    carries_household_goods as "Flag: Household Goods",                             -- Field 76 [cite: 11]
    carries_metal_sheets as "Flag: Metal Sheets",                                   -- Field 77 [cite: 11]
    carries_motor_vehicles as "Flag: Motor Vehicles",                               -- Field 78 [cite: 11]
    carries_driveaway_towaway as "Flag: Driveaway Towaway",                         -- Field 79 [cite: 11]
    carries_logs_poles as "Flag: Logs and Poles",                                   -- Field 80 [cite: 11]
    carries_building_materials as "Flag: Building Materials",                       -- Field 81 [cite: 11]
    carries_mobile_homes as "Flag: Mobile Homes",                                   -- Field 82 [cite: 11]
    carries_machinery_large_objects as "Flag: Large Machinery",                     -- Field 83 [cite: 11]
    carries_fresh_produce as "Flag: Fresh Produce",                                 -- Field 84 [cite: 11]
    carries_liquids_gases as "Flag: Liquids and Gases",                             -- Field 85 [cite: 11]
    carries_intermodal_containers as "Flag: Intermodal Containers",                 -- Field 86 [cite: 11]
    carries_passengers as "Flag: Passenger Transport",                              -- Field 87 [cite: 11]
    carries_oilfield_equipment as "Flag: Oilfield Equipment",                       -- Field 88 [cite: 11]
    carries_livestock as "Flag: Livestock",                                         -- Field 89 [cite: 11]
    carries_grain_feed_hay as "Flag: Grain and Feed",                               -- Field 90 [cite: 16]
    carries_coal_coke as "Flag: Coal and Coke",                                     -- Field 91 [cite: 16]
    carries_meat as "Flag: Meat Products",                                          -- Field 92 [cite: 16]
    carries_garbage_refuse as "Flag: Waste Management",                             -- Field 93 [cite: 16]
    carries_us_mail as "Flag: US Mail Contracting",                                 -- Field 94 [cite: 16]
    carries_chemicals as "Flag: Chemicals",                                         -- Field 95 [cite: 16]
    carries_dry_bulk as "Flag: Dry Bulk Commodities",                               -- Field 96 [cite: 16]
    carries_refrigerated_food as "Flag: Cold Chain Food",                           -- Field 97 [cite: 16]
    carries_beverages as "Flag: Beverage Distribution",                             -- Field 98 [cite: 16]
    carries_paper_products as "Flag: Paper Products",                               -- Field 99 [cite: 16]
    carries_utility as "Flag: Utility Fleet Support",                               -- Field 100 [cite: 16]
    
    -- Fleet Sizing Meta-Dimension
    fleet_size_bracket as "Fleet Size Bracket"                                      -- Derived Attribute

from prepped_dimensions
where dot_number is not null
order by added_date desc