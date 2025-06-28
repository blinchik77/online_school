--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: delete_all(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.delete_all() RETURNS void
    LANGUAGE sql
    AS $$
TRUNCATE bookings,students,courses,teachers;
$$;


ALTER FUNCTION public.delete_all() OWNER TO postgres;

--
-- Name: delete_courses_by_subject(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.delete_courses_by_subject(c_subject text) RETURNS void
    LANGUAGE sql
    AS $$
delete from courses where position(c_subject in code) > 0;
$$;


ALTER FUNCTION public.delete_courses_by_subject(c_subject text) OWNER TO postgres;

--
-- Name: delete_courses_with_term(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.delete_courses_with_term(c_term integer) RETURNS void
    LANGUAGE sql
    AS $$
delete from courses where term = c_term;
$$;


ALTER FUNCTION public.delete_courses_with_term(c_term integer) OWNER TO postgres;

--
-- Name: insert_into_bookings(text, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insert_into_bookings(code text, email text) RETURNS void
    LANGUAGE sql
    AS $$
insert into bookings values (nextval('bookings_id'), code,email, current_timestamp);
$$;


ALTER FUNCTION public.insert_into_bookings(code text, email text) OWNER TO postgres;

--
-- Name: insert_into_students(text, text, text, numeric, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insert_into_students(s_email text, s_name text, s_city text, s_phone_number numeric(11,0), s_class integer) RETURNS void
    LANGUAGE sql
    AS $$
insert into students values(s_email, s_name, s_city, s_phone_number, s_class);
$$;


ALTER FUNCTION public.insert_into_students(s_email text, s_name text, s_city text, s_phone_number numeric, s_class integer) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookings (
    id integer NOT NULL,
    code text NOT NULL,
    email text NOT NULL,
    date_time timestamp without time zone
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- Name: print_bookings(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.print_bookings() RETURNS public.bookings
    LANGUAGE sql
    AS $$
select * from bookings;
$$;


ALTER FUNCTION public.print_bookings() OWNER TO postgres;

--
-- Name: courses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.courses (
    code text NOT NULL,
    subject text NOT NULL,
    term numeric(1,0),
    class integer NOT NULL,
    cost integer NOT NULL,
    inn numeric(12,0) NOT NULL,
    CONSTRAINT courses_class_check CHECK ((class <= 11)),
    CONSTRAINT courses_subject_check CHECK ((subject = ANY (ARRAY['Informatics'::text, 'Geography'::text, 'Physical Education'::text]))),
    CONSTRAINT courses_term_check CHECK ((term = ANY (ARRAY[(3)::numeric, (6)::numeric, (9)::numeric])))
);


ALTER TABLE public.courses OWNER TO postgres;

--
-- Name: print_courses(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.print_courses() RETURNS public.courses
    LANGUAGE sql
    AS $$
select * from courses;
$$;


ALTER FUNCTION public.print_courses() OWNER TO postgres;

--
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    email text NOT NULL,
    name text NOT NULL,
    city text NOT NULL,
    phone_number numeric(11,0),
    class integer,
    CONSTRAINT students_class_check CHECK ((class <= 11))
);


ALTER TABLE public.students OWNER TO postgres;

--
-- Name: print_students(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.print_students() RETURNS public.students
    LANGUAGE sql
    AS $$
select * from students;
$$;


ALTER FUNCTION public.print_students() OWNER TO postgres;

--
-- Name: print_students_from(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.print_students_from(t_city text) RETURNS public.students
    LANGUAGE sql
    AS $$
select * from students where city = t_city;
$$;


ALTER FUNCTION public.print_students_from(t_city text) OWNER TO postgres;

--
-- Name: teachers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teachers (
    inn numeric(12,0) NOT NULL,
    name text NOT NULL,
    experience integer,
    CONSTRAINT teachers_inn_check CHECK (((inn >= ('100000000000'::bigint)::numeric) AND (inn <= ('999999999999'::bigint)::numeric)))
);


ALTER TABLE public.teachers OWNER TO postgres;

--
-- Name: print_teachers(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.print_teachers() RETURNS public.teachers
    LANGUAGE sql
    AS $$
select * from teachers;
$$;


ALTER FUNCTION public.print_teachers() OWNER TO postgres;

--
-- Name: update_student(text, text, text, numeric, integer, text, text, numeric, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_student(old_email text, old_name text, old_city text, old_phone_number numeric, old_class integer, new_name text, new_city text, new_phone_number numeric, new_class integer) RETURNS void
    LANGUAGE sql
    AS $$
update students set name = new_name, city = new_city, phone_number = new_phone_number, class = new_class
where email = old_email AND name = old_name AND city = old_city AND phone_number = old_phone_number AND class = old_class;
$$;


ALTER FUNCTION public.update_student(old_email text, old_name text, old_city text, old_phone_number numeric, old_class integer, new_name text, new_city text, new_phone_number numeric, new_class integer) OWNER TO postgres;

--
-- Name: bookings_id; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bookings_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bookings_id OWNER TO postgres;

--
-- Name: bookings_id; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bookings_id OWNED BY public.bookings.id;


--
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookings (id, code, email, date_time) FROM stdin;
1	INF11LONG	dog@mail.ru	2024-12-18 14:31:16.180099
\.


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.courses (code, subject, term, class, cost, inn) FROM stdin;
INF9LONG	Informatics	9	9	20000	111111111111
GEO11LONG	Geography	9	11	25000	111111111111
GEO9LONG	Geography	9	9	17000	111111111111
PE11LONG	Physical Education	9	11	50000	111111111111
PE9LONG	Physical Education	9	9	40000	111111111111
INF11MED	Informatics	6	11	22000	222222222222
INF11SHORT	Informatics	3	11	15000	222222222222
INF9MED	Informatics	6	9	16000	333333333333
INF9SHORT	Informatics	3	9	10000	333333333333
GEO11MED	Geography	6	11	20000	101010101010
GEO11SHORT	Geography	3	11	15000	101010101010
GEO9SHORT	Geography	3	9	7000	101010101010
GEO9MED	Geography	6	9	14000	101010101010
PE11MED	Physical Education	6	11	35000	444444444444
PE9MED	Physical Education	6	9	30000	444444444444
PE9SHORT	Physical Education	3	9	20000	777777777777
PE11SHORT	Physical Education	3	11	25000	777777777777
INF11LONG	Informatics	9	11	30000	111111111111
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.students (email, name, city, phone_number, class) FROM stdin;
dog@mail.ru	Бульдог Гарик Юрьевич	Москва	88888888888	11
volya@mail.ru	Павел Воля	Пенза	89999999999	11
serg@mail.ru	Серж Горелый	Томск	87777777777	11
\.


--
-- Data for Name: teachers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teachers (inn, name, experience) FROM stdin;
111111111111	Сигма бой	100
222222222222	Блинов Никита Вадимович	5
333333333333	Преженцов Егор Андреевич	0
444444444444	Бакин Семён Николаевич	50
777777777777	Бирюков Алексей (он же OverDrive)	20
101010101010	Leo Messi	10
\.


--
-- Name: bookings_id; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookings_id', 1, true);


--
-- Name: bookings bookings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_pkey PRIMARY KEY (id);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (code);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (email);


--
-- Name: teachers teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (inn);


--
-- Name: experience_of_teachers; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX experience_of_teachers ON public.teachers USING btree (experience DESC);


--
-- Name: bookings bookings_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_code_fkey FOREIGN KEY (code) REFERENCES public.courses(code) ON DELETE CASCADE;


--
-- Name: bookings bookings_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_email_fkey FOREIGN KEY (email) REFERENCES public.students(email);


--
-- Name: courses courses_inn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_inn_fkey FOREIGN KEY (inn) REFERENCES public.teachers(inn);


--
-- Name: courses rabotayte_bratya; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT rabotayte_bratya FOREIGN KEY (inn) REFERENCES public.teachers(inn) ON DELETE RESTRICT;


--
-- Name: bookings vse_ravno_dengi_otdal; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT vse_ravno_dengi_otdal FOREIGN KEY (email) REFERENCES public.students(email) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

