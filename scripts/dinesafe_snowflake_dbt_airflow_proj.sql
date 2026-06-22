use role accountadmin;

-- 1. Create a warehouse
create warehouse if not exists dinesafe_wh with warehouse_size='x-small';

-- 2. Create isolated database layers
create database if not exists raw_zone_db;
create database if not exists analytics_zone_db;


-- 3. Create a role
create role if not exists dinesafe_dev_role;

-- 4. Delegate full control to your developer role
grant usage on warehouse dinesafe_wh to role dinesafe_dev_role;
grant role dinesafe_dev_role to user karsonfu;
grant all on database raw_zone_db to role dinesafe_dev_role;
grant all on database analytics_zone_db to role dinesafe_dev_role;

-- 5. Create Schemas
use role dinesafe_dev_role;
use warehouse dinesafe_wh;
create schema if not exists raw_zone_db.toronto_open_data;
create schema if not exists analytics_zone_db.dinesafe_marts;


