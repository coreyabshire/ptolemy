-- Table: public.places

-- DROP TABLE public.places;

CREATE TYPE place_disposition AS ENUM ('known', 'tentative', 'unknown');

CREATE TABLE public.places
(
  ptolemy_id character(10) NOT NULL, -- The ptolemy id, using the notation we've adopted based on Stückelberger and Grasshoff's labeling method.
  ptolemy_name character varying(80), -- The name we've taken into the spreadsheet as some translation from some source of the Ptolemy name for the place. In most cases this is the German from S&G, but in others it may be the English we've found from some other source.
  modern_name character varying(80), -- The modern name as given in our spreadsheet, which denotes our best guess for the place that corresponds to the Ptolemy location.
  ptolemy_point geography(POINT), -- The ptolemy coordinates for this location.
  modern_point geography(POINT), -- The modern coordinates for this location.
  disposition place_disposition, -- Indicator of whether our modern point is known, tentative, or unknown (predicted).
  CONSTRAINT places_pkey PRIMARY KEY (ptolemy_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.places
  OWNER TO ptolemy;
COMMENT ON TABLE public.places
  IS 'Initial storage location for the information we''ve collected in our spreadsheets for the Ptolemy project.';
COMMENT ON COLUMN public.places.ptolemy_id IS 'The ptolemy id, using the notation we''ve adopted based on Stückelberger and Grasshoff''s labeling method.';
COMMENT ON COLUMN public.places.ptolemy_name IS 'The name we''ve taken into the spreadsheet as some translation from some source of the Ptolemy name for the place. In most cases this is the German from S&G, but in others it may be the English we''ve found from some other source.';
COMMENT ON COLUMN public.places.modern_name IS 'The modern name as given in our spreadsheet, which denotes our best guess for the place that corresponds to the Ptolemy location.';
COMMENT ON COLUMN public.places.ptolemy_point IS 'The ptolemy coordinates for this location.';
COMMENT ON COLUMN public.places.modern_point IS 'The ptolemy coordinates for this location.';
COMMENT ON COLUMN public.places.disposition IS 'Indicator of whether our modern point is known, tentative, or unknown (predicted).';

