select
    row_id as fact_inspection_key,
    unique_id as inspection_record_key,
    establishment_id,
    inspection_date,
    court_outcome_date,
    inspection_status,
    infraction_type,
    inspection_observation,
    infraction_details,
    infraction_severity,
    court_outcome_description,
    coalesce(amount_fined, 0.00) as amount_fined
from
    {{ ref('stg_dinesafe') }}
where
    establishment_id is not null