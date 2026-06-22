select
    -- Identifiers
    _id as row_id,
    unique_id,
    estId as establishment_id,
    oldEstId as old_establishment_id,
    
    -- Establishment Descriptive Attributes
    trim(estName) as establishment_name,
    trim(address) as establishment_address,
    phone as establishment_phone,
    cast(latitude as decimal(9,6)) as latitude,
    cast(longitude as decimal(9,6)) as longitude,
    
    -- Operational Inspection Attributes
    inspectionStatus as inspection_status,
    cast(inspectionDate as date) as inspection_date,
    trim(observation) as inspection_observation,
    
    -- Infraction / Deficiency Specifics
    trim(typeDesc) as infraction_type,
    trim(deficiencyDesc) as infraction_details,
    severity as infraction_severity,
    
    -- Court & Financial Outcomes
    cast(OutcomeDate as date) as court_outcome_date,
    trim(OutcomeDesc) as court_outcome_description,
    cast(amountFined as decimal(10,2)) as amount_fined

from 
    {{ source('toronto_open_data', 'raw_dinesafe') }}

