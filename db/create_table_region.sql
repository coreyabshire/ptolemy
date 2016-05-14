CREATE TABLE regions (
  id         SERIAL PRIMARY KEY,
  name       TEXT NOT NULL,
  project_id INTEGER REFERENCES projects (id)
);
