-- Table: public.tbl_store

-- DROP TABLE public.tbl_store;

CREATE TABLE public.tbl_store
(
    id integer NOT NULL DEFAULT nextval('tbl_store_id_seq'::regclass),
    store_name character varying COLLATE pg_catalog."default",
    address character varying COLLATE pg_catalog."default",
    phone character varying COLLATE pg_catalog."default",
    country character varying COLLATE pg_catalog."default",
    CONSTRAINT tbl_store_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tbl_store
    OWNER to postgres;