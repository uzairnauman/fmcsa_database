with source as (
    select * from {{ source('raw', 'raw_census') }}
)

select
    -- Core Identification, Dates & Status
    strptime(nullif(left(MCS150_DATE::VARCHAR, 8), ''), '%Y%m%d')::DATE as mcs150_date,    -- Field 1 Modified
    strptime(nullif(left(ADD_DATE::VARCHAR, 8), ''), '%Y%m%d')::DATE as added_date,        -- Field 2 Modified    
    STATUS_CODE as status_code,                                                    -- Field 3
    cast(DOT_NUMBER as INT) as dot_number,                                         -- Field 4
    CARRIER_OPERATION as carrier_operation_code,                                   -- Field 8
    cast(BUSINESS_ORG_ID as INT) as business_org_id,                               -- Field 9
    cast(TOTAL_CARS as INT) as total_cars,                                         -- Field 13

    -- Contacts & Sizing Codes
    PHONE as phone,                                                                -- Field 17
    CELL_PHONE as cell_phone,                                                      -- Field 19
    (coalesce(cast(OWNTRUCK as INT), 0) + 
     coalesce(cast(TRMTRUCK as INT), 0) + 
     coalesce(cast(TRPTRUCK as INT), 0)) as total_trucks,                          -- Field 23
    (coalesce(cast(OWNTRUCK as INT), 0) + 
     coalesce(cast(OWNTRACT as INT), 0) + 
     coalesce(cast(OWNCOACH as INT), 0) + 
     coalesce(cast(OWNSCHOOL_1_8 as INT), 0) + 
     coalesce(cast(OWNSCHOOL_9_15 as INT), 0) + 
     coalesce(cast(OWNSCHOOL_16 as INT), 0) + 
     coalesce(cast(OWNBUS_16 as INT), 0) + 
     coalesce(cast(OWNVAN_1_8 as INT), 0) + 
     coalesce(cast(OWNVAN_9_15 as INT), 0) + 
     coalesce(cast(OWNLIMO_1_8 as INT), 0) + 
     coalesce(cast(OWNLIMO_9_15 as INT), 0) + 
     coalesce(cast(OWNLIMO_16 as INT), 0)) as total_power_units,                   -- Field 24
    FLEETSIZE as fleetsize_code,                                                   -- Field 26
    CARSHIP as carship_code,                                                       -- Field 33

    -- Identifiers & Workforces
    HM_Ind as hazmat_indicator,                                                    -- Field 44
    cast(TOTAL_CDL as INT) as total_cdl_drivers,                                   -- Field 49
    cast(TOTAL_DRIVERS as INT) as total_drivers,                                   -- Field 50
    CLASSDEF as classification_definition,                                         -- Field 52

    -- Physical & Mailing Geography Vectors
    PHY_CITY as physical_city,                                                     -- Field 56
    PHY_STATE as physical_state,                                                   -- Field 58
    PHY_ZIP as physical_zip,                                                       -- Field 59
    CARRIER_MAILING_STATE as mailing_state,                                        -- Field 62
    CARRIER_MAILING_CITY as mailing_city,                                          -- Field 63
    CARRIER_MAILING_ZIP as mailing_zip,                                            -- Field 65
    EMAIL_ADDRESS as email_address,                                                -- Field 69

    -- Basic String Identifiers
    LEGAL_NAME as legal_name,                                                      -- Field 53
    DBA_NAME as dba_name,                                                          -- Field 54

    -- Commodity Matrix Conversions ('X' or Null -> True/False)
    case when CRGO_GENFREIGHT = 'X' then true else false end as carries_general_freight,          -- Field 75
    case when CRGO_HOUSEHOLD = 'X' then true else false end as carries_household_goods,            -- Field 76
    case when CRGO_METALSHEET = 'X' then true else false end as carries_metal_sheets,              -- Field 77
    case when CRGO_MOTOVEH = 'X' then true else false end as carries_motor_vehicles,               -- Field 78
    case when CRGO_DRIVETOW = 'X' then true else false end as carries_driveaway_towaway,           -- Field 79
    case when CRGO_LOGPOLE = 'X' then true else false end as carries_logs_poles,                   -- Field 80
    case when CRGO_BLDGMAT = 'X' then true else false end as carries_building_materials,           -- Field 81
    case when CRGO_MOBILEHOME = 'X' then true else false end as carries_mobile_homes,             -- Field 82
    case when CRGO_MACHLRG = 'X' then true else false end as carries_machinery_large_objects,      -- Field 83
    case when CRGO_PRODUCE = 'X' then true else false end as carries_fresh_produce,                -- Field 84
    case when CRGO_LIQGAS = 'X' then true else false end as carries_liquids_gases,                 -- Field 85
    case when CRGO_INTERMODAL = 'X' then true else false end as carries_intermodal_containers,     -- Field 86
    case when CRGO_PASSENGERS = 'X' then true else false end as carries_passengers,               -- Field 87
    case when CRGO_OILFIELD = 'X' then true else false end as carries_oilfield_equipment,          -- Field 88
    case when CRGO_LIVESTOCK = 'X' then true else false end as carries_livestock,                  -- Field 89
    case when CRGO_GRAINFEED = 'X' then true else false end as carries_grain_feed_hay,             -- Field 90
    case when CRGO_COALCOKE = 'X' then true else false end as carries_coal_coke,                   -- Field 91
    case when CRGO_MEAT = 'X' then true else false end as carries_meat,                            -- Field 92
    case when CRGO_GARBAGE = 'X' then true else false end as carries_garbage_refuse,               -- Field 93
    case when CRGO_USMAIL = 'X' then true else false end as carries_us_mail,                       -- Field 94
    case when CRGO_CHEM = 'X' then true else false end as carries_chemicals,                       -- Field 95
    case when CRGO_DRYBULK = 'X' then true else false end as carries_dry_bulk,                     -- Field 96
    case when CRGO_COLDFOOD = 'X' then true else false end as carries_refrigerated_food,           -- Field 97
    case when CRGO_BEVERAGES = 'X' then true else false end as carries_beverages,                 -- Field 98
    case when CRGO_PAPERPROD = 'X' then true else false end as carries_paper_products,             -- Field 99
    case when CRGO_UTILITY = 'X' then true else false end as carries_utility                      -- Field 100

from source