-- Table: public.tbl_products

-- DROP TABLE public.tbl_products;

CREATE TABLE public.tbl_products
(
    id integer NOT NULL DEFAULT nextval('tbl_products_id_seq'::regclass),
    name_product character varying COLLATE pg_catalog."default",
    brand character varying COLLATE pg_catalog."default",
    model character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    sku character varying COLLATE pg_catalog."default",
    price numeric,
    CONSTRAINT tbl_products_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tbl_products
    OWNER to postgres;