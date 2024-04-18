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