-- Table: public.pass_in_trip

-- DROP TABLE IF EXISTS public.pass_in_trip;

CREATE TABLE IF NOT EXISTS public.pass_in_trip
(
    pass_in_trip_id bigint NOT NULL DEFAULT nextval('pass_in_trip_pass_in_trip_id_seq'::regclass),
    trip_id bigint,
    passenger_id bigint,
    place character varying(60) COLLATE pg_catalog."default",
    CONSTRAINT pass_in_trip_pkey PRIMARY KEY (pass_in_trip_id),
    CONSTRAINT fk_passanger FOREIGN KEY (passenger_id)
        REFERENCES public.passenger (passenger_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_trip FOREIGN KEY (trip_id)
        REFERENCES public.trip (trip_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.pass_in_trip
    OWNER to postgres;

REVOKE ALL ON TABLE public.pass_in_trip FROM pg_read_all_data;

GRANT SELECT ON TABLE public.pass_in_trip TO pg_read_all_data;

GRANT ALL ON TABLE public.pass_in_trip TO postgres;