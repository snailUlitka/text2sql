-- Table: public.trip

-- DROP TABLE IF EXISTS public.trip;

CREATE TABLE IF NOT EXISTS public.trip
(
    trip_id bigint NOT NULL DEFAULT nextval('trip_trip_id_seq'::regclass),
    company_id bigint,
    plane character varying(60) COLLATE pg_catalog."default",
    town_from character varying(60) COLLATE pg_catalog."default",
    town_to character varying(60) COLLATE pg_catalog."default",
    time_out timestamp without time zone,
    time_in timestamp without time zone,
    CONSTRAINT trip_pkey PRIMARY KEY (trip_id),
    CONSTRAINT fk_company FOREIGN KEY (company_id)
        REFERENCES public.company (company_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.trip
    OWNER to postgres;

REVOKE ALL ON TABLE public.trip FROM pg_read_all_data;

GRANT SELECT ON TABLE public.trip TO pg_read_all_data;

GRANT ALL ON TABLE public.trip TO postgres;