class SqlQueries:
    create_tables = """
        CREATE TABLE IF NOT EXISTS public.stg_REMS_ENV (
                sol INT NOT NULL,
                timestamp BIGINT NOT NULL,
                lmst VARCHAR NOT NULL,
                ltst VARCHAR NOT NULL,
                ambient_temp FLOAT,
                pressure FLOAT,
                horizontal_wind_speed FLOAT,
                vertical_wind_speed FLOAT,
                volume_mixing_ratio FLOAT,
                local_relative_humidity FLOAT
        );

        CREATE TABLE IF NOT EXISTS public.stg_REMS_ADR (
                sol INT NOT NULL,
                timestamp BIGINT NOT NULL,
                lmst VARCHAR NOT NULL,
                ltst VARCHAR NOT NULL,
                solar_longitude_angle FLOAT,
                solar_zenithal_angle FLOAT,
                rover_position_x FLOAT,
                rover_position_y FLOAT,
                rover_position_z FLOAT,
                rover_velocity FLOAT,
                rover_pitch FLOAT,
                rover_yaw FLOAT,
                rover_roll FLOAT
        );

        CREATE TABLE IF NOT EXISTS public.measures (
                measure_id VARCHAR NOT NULL,
                sol INT,
                location_id VARCHAR,
                time_id VARCHAR,
                ambient_temp FLOAT,
                pressure INT,
                horizontal_wind_speed FLOAT,
                vertical_wind_speed FLOAT,
                local_relative_humidity FLOAT
        );

        CREATE TABLE IF NOT EXISTS public.time (
                time_id VARCHAR NOT NULL,
                sol INT NOT NULL,
                timestamp BIGINT NOT NULL,
                lmst VARCHAR NOT NULL,
                ltst VARCHAR NOT NULL,
                solar_longitude_angle FLOAT,
                solar_zenithal_angle FLOAT
        );

        CREATE TABLE IF NOT EXISTS public.location (
                location_id VARCHAR NOT NULL,
                rover_position_x FLOAT,
                rover_position_y FLOAT,
                rover_position_z FLOAT,
                rover_velocity FLOAT,
                rover_pitch FLOAT,
                rover_yaw FLOAT,
                rover_roll FLOAT
        );
    """

    measures_table_insert = """
        SELECT  (e.sol::VARCHAR || '_' ||
                 row_number() OVER
                 (PARTITION BY e.sol ORDER BY e.timestamp)::VARCHAR
                 ) AS measure_id,
                 e.sol,
                (a.rover_position_x::VARCHAR || '_'
                        || a.rover_position_y::VARCHAR || '_'
                        || a.rover_position_z::VARCHAR) AS location_id,
                (e.sol::VARCHAR || '_' || e.timestamp::VARCHAR) AS time_id,
                e.ambient_temp,
                e.pressure,
                e.horizontal_wind_speed,
                e.vertical_wind_speed,
                e.local_relative_humidity
        FROM stg_rems_env e
        LEFT JOIN stg_rems_adr a
        ON (e.sol = a.sol)
        AND (e.timestamp = a.timestamp)
    """

    location_table_insert = """
        SELECT distinct
                (rover_position_x::VARCHAR || '_'
                        || rover_position_y::VARCHAR || '_'
                        || rover_position_z::VARCHAR) AS location_id,
                rover_position_x,
                rover_position_y,
                rover_position_z,
                rover_velocity,
                rover_pitch,
                rover_yaw,
                rover_roll
        FROM stg_rems_adr
    """

    time_table_insert = """
        SELECT (s.sol::VARCHAR || '_' || s.timestamp::VARCHAR) AS time_id,
                s.sol,
                s.timestamp,
                s.lmst,
                s.ltst,
                s.solar_longitude_angle,
                s.solar_zenithal_angle
        FROM
                (SELECT distinct
                        CASE WHEN e.sol IS NULL
                                THEN a.sol ELSE e.sol END AS sol,
                        CASE WHEN e.timestamp IS NULL
                                THEN a.timestamp ELSE e.timestamp
                                END AS timestamp,
                        CASE WHEN e.lmst IS NULL
                                THEN a.lmst ELSE e.lmst END AS lmst,
                        CASE WHEN e.ltst IS NULL
                                THEN a.ltst ELSE a.ltst END AS ltst,
                        a.solar_longitude_angle,
                        a.solar_zenithal_angle

                FROM stg_rems_env e
                LEFT OUTER JOIN stg_rems_adr a
                ON (e.sol = a.sol)
                AND (e.timestamp = a.timestamp)) s
    """
