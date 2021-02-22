-- Table: public.tbl_inventory

-- DROP TABLE public.tbl_inventory;

CREATE TABLE public.tbl_inventory
(
    id integer NOT NULL DEFAULT nextval('tbl_inventory_id_seq'::regclass),
    store_id numeric,
    product_id numeric,
    quantity numeric,
    location character varying COLLATE pg_catalog."default",
    CONSTRAINT tbl_inventory_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tbl_inventory
    OWNER to postgres;