CREATE TABLE public.image_color
(
    id character varying(224) COLLATE pg_catalog."default" NOT NULL,
    colors json NOT NULL,
    CONSTRAINT image_color_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.image_color
    OWNER to pixelhunter;
