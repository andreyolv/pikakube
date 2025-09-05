--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-1.pgdg120+1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: myschema; Type: SCHEMA; Schema: -; Owner: andreyolv
--

CREATE SCHEMA myschema;


ALTER SCHEMA myschema OWNER TO andreyolv;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: employees; Type: TABLE; Schema: myschema; Owner: andreyolv
--

CREATE TABLE myschema.employees (
    id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    email character varying(100),
    hire_date date
);


ALTER TABLE myschema.employees OWNER TO andreyolv;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: myschema; Owner: andreyolv
--

CREATE SEQUENCE myschema.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE myschema.employees_id_seq OWNER TO andreyolv;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: myschema; Owner: andreyolv
--

ALTER SEQUENCE myschema.employees_id_seq OWNED BY myschema.employees.id;


--
-- Name: employees id; Type: DEFAULT; Schema: myschema; Owner: andreyolv
--

ALTER TABLE ONLY myschema.employees ALTER COLUMN id SET DEFAULT nextval('myschema.employees_id_seq'::regclass);


--
-- Data for Name: employees; Type: TABLE DATA; Schema: myschema; Owner: andreyolv
--

COPY myschema.employees (id, first_name, last_name, email, hire_date) FROM stdin;
1	John	Doe	john@example.com	2023-01-01
2	Jane	Smith	jane@example.com	2023-02-15
3	Michael	Johnson	michael@example.com	2023-03-10
4	Emily	Brown	emily@example.com	2023-04-05
5	William	Miller	william@example.com	2023-05-20
6	Sophia	Jones	sophia@example.com	2023-06-18
7	James	Davis	james@example.com	2023-07-12
8	Olivia	Wilson	olivia@example.com	2023-08-08
9	Liam	Moore	liam@example.com	2023-09-25
10	Andrey	Oliveira	andreyolv@example.com	2023-10-30
\.


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: myschema; Owner: andreyolv
--

SELECT pg_catalog.setval('myschema.employees_id_seq', 10, true);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: myschema; Owner: andreyolv
--

ALTER TABLE ONLY myschema.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

