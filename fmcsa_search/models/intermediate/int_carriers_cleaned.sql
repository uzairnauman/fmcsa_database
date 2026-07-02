with staged_data as (
    select * from {{ ref('stg_carriers') }}
)

select
    *,
    
    -- Mapping string codes to readable UI Dropdown entries
    case status_code                                                               -- Field 3
        when 'A' then 'Active'
        when 'I' then 'Inactive'
        when 'P' then 'Pending'
        else 'Unknown'
    end as status_label,

    case carrier_operation_code                                                    -- Field 8
        when 'A' then 'Interstate'
        when 'B' then 'Intrastate Hazmat'
        when 'C' then 'Intrastate Non-Hazmat'
        else 'Unclassified'
    end as operational_scope_label,

    case business_org_id                                                           -- Field 9
        when 1 then 'Individual'
        when 2 then 'Partnership'
        when 3 then 'Corporation'
        else 'Not Declared'
    end as business_structure_label,

    -- Dynamic grouping parameter calculated from Field 24
    case 
        when total_power_units = 1 then '1 Unit (Owner-Operator)'
        when total_power_units between 2 and 10 then '2-10 Units (Small Fleet)'
        when total_power_units between 11 and 100 then '11-100 Units (Medium Fleet)'
        when total_power_units > 100 then '100+ Units (Enterprise)'
        else '0 Units / Pending Equipment'
    end as fleet_size_bracket,

    -- Translating Entity Operations Codes (Field 33)
    -- Handles single codes or multi-letter combinations gracefully
    case 
        when carship_code = 'C' then 'Carrier'
        when carship_code = 'S' then 'Shipper'
        when carship_code = 'B' then 'Broker'
        when carship_code = 'R' then 'Registrant'
        when carship_code = 'F' then 'Freight Forwarder'
        when carship_code = 'I' then 'Intermodal Equipment Provider'
        when carship_code = 'T' then 'Cargo Tank Facility'
        when contains(carship_code, 'C') and contains(carship_code, 'B') then 'Carrier & Broker'
        when carship_code is null or carship_code = '' then 'Not Specified'
        else 'Multiple/Other Operations (' || carship_code || ')'
    end as entity_operations_label

from staged_data