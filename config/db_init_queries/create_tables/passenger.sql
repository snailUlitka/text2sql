-- SEQUENCE: public.passenger_passenger_id_seq

-- DROP SEQUENCE IF EXISTS public.passenger_passenger_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.passenger_passenger_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

-- Table: public.passenger

-- DROP TABLE IF EXISTS public.passenger;

CREATE TABLE IF NOT EXISTS public.passenger
(
    passenger_id bigint NOT NULL DEFAULT nextval('passenger_passenger_id_seq'::regclass),
    passenger_name character varying(60) COLLATE pg_catalog."default",
    CONSTRAINT passenger_pkey PRIMARY KEY (passenger_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.passenger
    OWNER to postgres;

REVOKE ALL ON TABLE public.passenger FROM pg_read_all_data;

GRANT SELECT ON TABLE public.passenger TO pg_read_all_data;

GRANT ALL ON TABLE public.passenger TO postgres;

ALTER SEQUENCE public.passenger_passenger_id_seq
    OWNED BY public.passenger.passenger_id;

ALTER SEQUENCE public.passenger_passenger_id_seq
    OWNER TO postgres;

GRANT SELECT, USAGE ON SEQUENCE public.passenger_passenger_id_seq TO pg_read_all_data;

GRANT ALL ON SEQUENCE public.passenger_passenger_id_seq TO postgres;