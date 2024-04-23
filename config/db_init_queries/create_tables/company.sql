-- SEQUENCE: public.company_company_id_seq

-- DROP SEQUENCE IF EXISTS public.company_company_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.company_company_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

-- Table: public.company

-- DROP TABLE IF EXISTS public.company;

CREATE TABLE IF NOT EXISTS public.company
(
    company_id bigint NOT NULL DEFAULT nextval('company_company_id_seq'::regclass),
    company_name character varying(60) COLLATE pg_catalog."default",
    CONSTRAINT company_pkey PRIMARY KEY (company_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.company
    OWNER to postgres;

REVOKE ALL ON TABLE public.company FROM pg_read_all_data;

GRANT SELECT ON TABLE public.company TO pg_read_all_data;

GRANT ALL ON TABLE public.company TO postgres;

ALTER SEQUENCE public.company_company_id_seq
    OWNED BY public.company.company_id;

ALTER SEQUENCE public.company_company_id_seq
    OWNER TO postgres;

GRANT SELECT, USAGE ON SEQUENCE public.company_company_id_seq TO pg_read_all_data;

GRANT ALL ON SEQUENCE public.company_company_id_seq TO postgres;