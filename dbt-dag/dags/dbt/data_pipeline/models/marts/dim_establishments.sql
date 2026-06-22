select
    establishment_id,
    establishment_name,
    establishment_address,
    establishment_phone,
    latitude,
    longitude
from
    {{ ref('stg_dinesafe') }}
where
    establishment_id is not null

qualify row_number() over (
    partition by establishment_id 
    order by inspection_date desc, row_id desc
) = 1