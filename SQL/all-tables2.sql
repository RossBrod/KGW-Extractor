--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.3

-- Started on 2025-05-15 20:02:37

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 540565)
-- Name: additional_plaintiffs; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.additional_plaintiffs (
    id integer NOT NULL,
    case_id character varying(300),
    name character varying(255) NOT NULL
);


ALTER TABLE public.additional_plaintiffs OWNER TO postgres1dev;

--
-- TOC entry 217 (class 1259 OID 540570)
-- Name: additional_plaintiffs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.additional_plaintiffs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.additional_plaintiffs_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4536 (class 0 OID 0)
-- Dependencies: 217
-- Name: additional_plaintiffs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.additional_plaintiffs_id_seq OWNED BY public.additional_plaintiffs.id;


--
-- TOC entry 218 (class 1259 OID 540571)
-- Name: case_causes; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.case_causes (
    case_id character varying(300) NOT NULL,
    cause_id integer NOT NULL
);


ALTER TABLE public.case_causes OWNER TO postgres1dev;

--
-- TOC entry 219 (class 1259 OID 540574)
-- Name: case_issues; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.case_issues (
    issue_id integer NOT NULL,
    case_id character varying(300) NOT NULL,
    issue_text text NOT NULL,
    issue_number integer NOT NULL,
    issues_embedding public.vector
);


ALTER TABLE public.case_issues OWNER TO postgres1dev;

--
-- TOC entry 220 (class 1259 OID 540579)
-- Name: case_issues_issue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.case_issues_issue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.case_issues_issue_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4537 (class 0 OID 0)
-- Dependencies: 220
-- Name: case_issues_issue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.case_issues_issue_id_seq OWNED BY public.case_issues.issue_id;


--
-- TOC entry 221 (class 1259 OID 540580)
-- Name: case_jurisdictions; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.case_jurisdictions (
    id integer NOT NULL,
    case_id character varying(300),
    jurisdiction_id integer
);


ALTER TABLE public.case_jurisdictions OWNER TO postgres1dev;

--
-- TOC entry 222 (class 1259 OID 540583)
-- Name: case_jurisdictions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.case_jurisdictions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.case_jurisdictions_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4538 (class 0 OID 0)
-- Dependencies: 222
-- Name: case_jurisdictions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.case_jurisdictions_id_seq OWNED BY public.case_jurisdictions.id;


--
-- TOC entry 223 (class 1259 OID 540584)
-- Name: case_law_domains; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.case_law_domains (
    case_id character varying(300) NOT NULL,
    domain_id integer NOT NULL
);


ALTER TABLE public.case_law_domains OWNER TO postgres1dev;

--
-- TOC entry 224 (class 1259 OID 540587)
-- Name: case_parties; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.case_parties (
    case_party_id integer NOT NULL,
    case_id character varying(300),
    party_id integer,
    role character varying(50) NOT NULL
);


ALTER TABLE public.case_parties OWNER TO postgres1dev;

--
-- TOC entry 225 (class 1259 OID 540590)
-- Name: case_parties_case_party_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.case_parties_case_party_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.case_parties_case_party_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4539 (class 0 OID 0)
-- Dependencies: 225
-- Name: case_parties_case_party_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.case_parties_case_party_id_seq OWNED BY public.case_parties.case_party_id;


--
-- TOC entry 226 (class 1259 OID 540591)
-- Name: case_rulings; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.case_rulings (
    ruling_id integer NOT NULL,
    case_id character varying(300) NOT NULL,
    legal_principle_text text NOT NULL,
    principle_number integer NOT NULL,
    ruling_embedding public.vector
);


ALTER TABLE public.case_rulings OWNER TO postgres1dev;

--
-- TOC entry 227 (class 1259 OID 540596)
-- Name: case_rulings_ruling_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.case_rulings_ruling_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.case_rulings_ruling_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4540 (class 0 OID 0)
-- Dependencies: 227
-- Name: case_rulings_ruling_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.case_rulings_ruling_id_seq OWNED BY public.case_rulings.ruling_id;


--
-- TOC entry 228 (class 1259 OID 540597)
-- Name: case_summaries; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.case_summaries (
    summary_id integer NOT NULL,
    case_id character varying(300),
    case_name character varying(255),
    overview text,
    legal_domain text,
    plaintiff_arguments text,
    plaintiff_arguments_type character varying(255),
    defendant_arguments text,
    defendant_arguments_type character varying(255),
    applicability text,
    winning_party character varying(50)
);


ALTER TABLE public.case_summaries OWNER TO postgres1dev;

--
-- TOC entry 229 (class 1259 OID 540602)
-- Name: case_summaries_summary_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.case_summaries_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.case_summaries_summary_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4541 (class 0 OID 0)
-- Dependencies: 229
-- Name: case_summaries_summary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.case_summaries_summary_id_seq OWNED BY public.case_summaries.summary_id;


--
-- TOC entry 230 (class 1259 OID 540603)
-- Name: cases; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.cases (
    case_id character varying(300) NOT NULL,
    name character varying(255),
    filing_date date,
    filing_court character varying(255),
    court character varying(300),
    date_published character varying(300),
    citation character varying(300),
    id integer NOT NULL
);


ALTER TABLE public.cases OWNER TO postgres1dev;

--
-- TOC entry 231 (class 1259 OID 540608)
-- Name: cases_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.cases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cases_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4542 (class 0 OID 0)
-- Dependencies: 231
-- Name: cases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.cases_id_seq OWNED BY public.cases.id;


--
-- TOC entry 232 (class 1259 OID 540609)
-- Name: cause_legal_bases; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.cause_legal_bases (
    cause_id integer NOT NULL,
    basis_id integer NOT NULL
);


ALTER TABLE public.cause_legal_bases OWNER TO postgres1dev;

--
-- TOC entry 233 (class 1259 OID 540612)
-- Name: causes_of_action; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.causes_of_action (
    cause_id integer NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(100),
    description text,
    name_embedding public.vector(1024)
);


ALTER TABLE public.causes_of_action OWNER TO postgres1dev;

--
-- TOC entry 234 (class 1259 OID 540617)
-- Name: causes_of_action_cause_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.causes_of_action_cause_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.causes_of_action_cause_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4543 (class 0 OID 0)
-- Dependencies: 234
-- Name: causes_of_action_cause_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.causes_of_action_cause_id_seq OWNED BY public.causes_of_action.cause_id;


--
-- TOC entry 235 (class 1259 OID 540618)
-- Name: employmentcases; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.employmentcases (
    case_id character varying(300)
);


ALTER TABLE public.employmentcases OWNER TO postgres1dev;

--
-- TOC entry 236 (class 1259 OID 540621)
-- Name: facts; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.facts (
    fact_id integer NOT NULL,
    case_id character varying(300),
    type character varying(255),
    name text,
    concept text,
    symbol text,
    description text,
    relationship_type character varying(100)
);


ALTER TABLE public.facts OWNER TO postgres1dev;

--
-- TOC entry 237 (class 1259 OID 540626)
-- Name: facts_fact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.facts_fact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.facts_fact_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4544 (class 0 OID 0)
-- Dependencies: 237
-- Name: facts_fact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.facts_fact_id_seq OWNED BY public.facts.fact_id;


--
-- TOC entry 238 (class 1259 OID 540627)
-- Name: jurisdictions; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.jurisdictions (
    jurisdiction_id integer NOT NULL,
    name character varying(255) NOT NULL,
    level character varying(50),
    location character varying(100)
);


ALTER TABLE public.jurisdictions OWNER TO postgres1dev;

--
-- TOC entry 239 (class 1259 OID 540630)
-- Name: jurisdictions_jurisdiction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.jurisdictions_jurisdiction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jurisdictions_jurisdiction_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4545 (class 0 OID 0)
-- Dependencies: 239
-- Name: jurisdictions_jurisdiction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.jurisdictions_jurisdiction_id_seq OWNED BY public.jurisdictions.jurisdiction_id;


--
-- TOC entry 240 (class 1259 OID 540631)
-- Name: law_domains; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.law_domains (
    domain_id integer NOT NULL,
    broad character varying(255),
    subdomain character varying(255),
    specific character varying(255),
    domain_embedding public.vector,
    broad_subdomain_embedding public.vector
);


ALTER TABLE public.law_domains OWNER TO postgres1dev;

--
-- TOC entry 241 (class 1259 OID 540636)
-- Name: law_domains_domain_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.law_domains_domain_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.law_domains_domain_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4546 (class 0 OID 0)
-- Dependencies: 241
-- Name: law_domains_domain_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.law_domains_domain_id_seq OWNED BY public.law_domains.domain_id;


--
-- TOC entry 242 (class 1259 OID 540637)
-- Name: legal_bases; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.legal_bases (
    basis_id integer NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(100),
    description text
);


ALTER TABLE public.legal_bases OWNER TO postgres1dev;

--
-- TOC entry 243 (class 1259 OID 540642)
-- Name: legal_bases_basis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.legal_bases_basis_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.legal_bases_basis_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4547 (class 0 OID 0)
-- Dependencies: 243
-- Name: legal_bases_basis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.legal_bases_basis_id_seq OWNED BY public.legal_bases.basis_id;


--
-- TOC entry 244 (class 1259 OID 540643)
-- Name: legal_principles; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.legal_principles (
    principle_id integer NOT NULL,
    case_id character varying(300),
    type character varying(255),
    name text,
    doctrine_principle text,
    description text,
    relationship_type character varying(100),
    doctrine_principle_embedding public.vector
);


ALTER TABLE public.legal_principles OWNER TO postgres1dev;

--
-- TOC entry 245 (class 1259 OID 540648)
-- Name: legal_principles_principle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.legal_principles_principle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.legal_principles_principle_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4548 (class 0 OID 0)
-- Dependencies: 245
-- Name: legal_principles_principle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.legal_principles_principle_id_seq OWNED BY public.legal_principles.principle_id;


--
-- TOC entry 246 (class 1259 OID 540649)
-- Name: parties; Type: TABLE; Schema: public; Owner: postgres1dev
--

CREATE TABLE public.parties (
    party_id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.parties OWNER TO postgres1dev;

--
-- TOC entry 247 (class 1259 OID 540652)
-- Name: parties_party_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres1dev
--

CREATE SEQUENCE public.parties_party_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parties_party_id_seq OWNER TO postgres1dev;

--
-- TOC entry 4549 (class 0 OID 0)
-- Dependencies: 247
-- Name: parties_party_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres1dev
--

ALTER SEQUENCE public.parties_party_id_seq OWNED BY public.parties.party_id;


--
-- TOC entry 248 (class 1259 OID 540653)
-- Name: vw_case_summaries_law_domains; Type: VIEW; Schema: public; Owner: postgres1dev
--

CREATE VIEW public.vw_case_summaries_law_domains AS
 SELECT cs.case_id,
    TRIM(BOTH FROM split.parts[1]) AS broad,
    TRIM(BOTH FROM split.parts[2]) AS subdomain,
    TRIM(BOTH FROM split.parts[3]) AS specific
   FROM (((public.case_summaries cs
     CROSS JOIN LATERAL regexp_split_to_table(cs.legal_domain, '
?
'::text) raw_line(raw_line))
     CROSS JOIN LATERAL ( SELECT regexp_replace(raw_line.raw_line, '^\s*[-•]\s*'::text, ''::text) AS line_clean) cleaned)
     CROSS JOIN LATERAL ( SELECT regexp_split_to_array(cleaned.line_clean, '\s*->\s*'::text) AS parts) split)
  WHERE (array_length(split.parts, 1) = 3)
  ORDER BY cs.case_id, split.parts[1];


ALTER VIEW public.vw_case_summaries_law_domains OWNER TO postgres1dev;

--
-- TOC entry 249 (class 1259 OID 540658)
-- Name: vw_usefullcases; Type: VIEW; Schema: public; Owner: postgres1dev
--

CREATE VIEW public.vw_usefullcases AS
 SELECT DISTINCT d.broad,
    count(DISTINCT c.case_id) AS count
   FROM (((public.law_domains d
     JOIN public.case_law_domains cld ON ((cld.domain_id = d.domain_id)))
     JOIN public.cases c ON (((c.case_id)::text = (cld.case_id)::text)))
     JOIN public.case_summaries cs ON (((c.case_id)::text = (cs.case_id)::text)))
  WHERE ((c.name IS NULL) AND ((lower((d.broad)::text) ~~ lower('%Employment%'::text)) OR (lower((d.broad)::text) ~~ lower('%Labor%'::text)) OR (lower((d.broad)::text) ~~ lower('%Administrative%'::text)) OR (lower((d.broad)::text) ~~ lower('%Civil%'::text)) OR (lower((d.broad)::text) ~~ lower('%Proced%'::text)) OR (lower((d.broad)::text) ~~ lower('%Remedies%'::text)) OR (lower((d.broad)::text) ~~ lower('%Retaliation%'::text)) OR (lower((d.broad)::text) ~~ lower('%Workers%'::text))))
  GROUP BY d.broad;


ALTER VIEW public.vw_usefullcases OWNER TO postgres1dev;

--
-- TOC entry 4272 (class 2604 OID 540663)
-- Name: additional_plaintiffs id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.additional_plaintiffs ALTER COLUMN id SET DEFAULT nextval('public.additional_plaintiffs_id_seq'::regclass);


--
-- TOC entry 4273 (class 2604 OID 540664)
-- Name: case_issues issue_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_issues ALTER COLUMN issue_id SET DEFAULT nextval('public.case_issues_issue_id_seq'::regclass);


--
-- TOC entry 4274 (class 2604 OID 540665)
-- Name: case_jurisdictions id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_jurisdictions ALTER COLUMN id SET DEFAULT nextval('public.case_jurisdictions_id_seq'::regclass);


--
-- TOC entry 4275 (class 2604 OID 540666)
-- Name: case_parties case_party_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_parties ALTER COLUMN case_party_id SET DEFAULT nextval('public.case_parties_case_party_id_seq'::regclass);


--
-- TOC entry 4276 (class 2604 OID 540667)
-- Name: case_rulings ruling_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_rulings ALTER COLUMN ruling_id SET DEFAULT nextval('public.case_rulings_ruling_id_seq'::regclass);


--
-- TOC entry 4277 (class 2604 OID 540668)
-- Name: case_summaries summary_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_summaries ALTER COLUMN summary_id SET DEFAULT nextval('public.case_summaries_summary_id_seq'::regclass);


--
-- TOC entry 4278 (class 2604 OID 540669)
-- Name: cases id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.cases ALTER COLUMN id SET DEFAULT nextval('public.cases_id_seq'::regclass);


--
-- TOC entry 4279 (class 2604 OID 540670)
-- Name: causes_of_action cause_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.causes_of_action ALTER COLUMN cause_id SET DEFAULT nextval('public.causes_of_action_cause_id_seq'::regclass);


--
-- TOC entry 4280 (class 2604 OID 540671)
-- Name: facts fact_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.facts ALTER COLUMN fact_id SET DEFAULT nextval('public.facts_fact_id_seq'::regclass);


--
-- TOC entry 4281 (class 2604 OID 540672)
-- Name: jurisdictions jurisdiction_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.jurisdictions ALTER COLUMN jurisdiction_id SET DEFAULT nextval('public.jurisdictions_jurisdiction_id_seq'::regclass);


--
-- TOC entry 4282 (class 2604 OID 540673)
-- Name: law_domains domain_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.law_domains ALTER COLUMN domain_id SET DEFAULT nextval('public.law_domains_domain_id_seq'::regclass);


--
-- TOC entry 4283 (class 2604 OID 540674)
-- Name: legal_bases basis_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.legal_bases ALTER COLUMN basis_id SET DEFAULT nextval('public.legal_bases_basis_id_seq'::regclass);


--
-- TOC entry 4284 (class 2604 OID 540675)
-- Name: legal_principles principle_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.legal_principles ALTER COLUMN principle_id SET DEFAULT nextval('public.legal_principles_principle_id_seq'::regclass);


--
-- TOC entry 4285 (class 2604 OID 540676)
-- Name: parties party_id; Type: DEFAULT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.parties ALTER COLUMN party_id SET DEFAULT nextval('public.parties_party_id_seq'::regclass);


--
-- TOC entry 4287 (class 2606 OID 540678)
-- Name: additional_plaintiffs additional_plaintiffs_case_id_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.additional_plaintiffs
    ADD CONSTRAINT additional_plaintiffs_case_id_name_key UNIQUE (case_id, name);


--
-- TOC entry 4289 (class 2606 OID 540680)
-- Name: additional_plaintiffs additional_plaintiffs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.additional_plaintiffs
    ADD CONSTRAINT additional_plaintiffs_pkey PRIMARY KEY (id);


--
-- TOC entry 4292 (class 2606 OID 540682)
-- Name: case_causes case_causes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_causes
    ADD CONSTRAINT case_causes_pkey PRIMARY KEY (case_id, cause_id);


--
-- TOC entry 4295 (class 2606 OID 540684)
-- Name: case_issues case_issues_case_id_issue_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_issues
    ADD CONSTRAINT case_issues_case_id_issue_number_key UNIQUE (case_id, issue_number);


--
-- TOC entry 4297 (class 2606 OID 540686)
-- Name: case_issues case_issues_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_issues
    ADD CONSTRAINT case_issues_pkey PRIMARY KEY (issue_id);


--
-- TOC entry 4300 (class 2606 OID 540688)
-- Name: case_jurisdictions case_jurisdictions_case_id_jurisdiction_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_jurisdictions
    ADD CONSTRAINT case_jurisdictions_case_id_jurisdiction_id_key UNIQUE (case_id, jurisdiction_id);


--
-- TOC entry 4302 (class 2606 OID 540690)
-- Name: case_jurisdictions case_jurisdictions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_jurisdictions
    ADD CONSTRAINT case_jurisdictions_pkey PRIMARY KEY (id);


--
-- TOC entry 4306 (class 2606 OID 540692)
-- Name: case_law_domains case_law_domains_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_law_domains
    ADD CONSTRAINT case_law_domains_pkey PRIMARY KEY (case_id, domain_id);


--
-- TOC entry 4309 (class 2606 OID 540694)
-- Name: case_parties case_parties_case_id_party_id_role_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_parties
    ADD CONSTRAINT case_parties_case_id_party_id_role_key UNIQUE (case_id, party_id, role);


--
-- TOC entry 4311 (class 2606 OID 540696)
-- Name: case_parties case_parties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_parties
    ADD CONSTRAINT case_parties_pkey PRIMARY KEY (case_party_id);


--
-- TOC entry 4315 (class 2606 OID 540698)
-- Name: case_rulings case_rulings_case_id_principle_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_rulings
    ADD CONSTRAINT case_rulings_case_id_principle_number_key UNIQUE (case_id, principle_number);


--
-- TOC entry 4317 (class 2606 OID 540700)
-- Name: case_rulings case_rulings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_rulings
    ADD CONSTRAINT case_rulings_pkey PRIMARY KEY (ruling_id);


--
-- TOC entry 4320 (class 2606 OID 540702)
-- Name: case_summaries case_summaries_case_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_summaries
    ADD CONSTRAINT case_summaries_case_id_key UNIQUE (case_id);


--
-- TOC entry 4322 (class 2606 OID 540704)
-- Name: case_summaries case_summaries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_summaries
    ADD CONSTRAINT case_summaries_pkey PRIMARY KEY (summary_id);


--
-- TOC entry 4326 (class 2606 OID 540706)
-- Name: cases cases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.cases
    ADD CONSTRAINT cases_pkey PRIMARY KEY (case_id);


--
-- TOC entry 4331 (class 2606 OID 540708)
-- Name: cause_legal_bases cause_legal_bases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.cause_legal_bases
    ADD CONSTRAINT cause_legal_bases_pkey PRIMARY KEY (cause_id, basis_id);


--
-- TOC entry 4334 (class 2606 OID 540710)
-- Name: causes_of_action causes_of_action_name_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.causes_of_action
    ADD CONSTRAINT causes_of_action_name_type_key UNIQUE (name, type);


--
-- TOC entry 4336 (class 2606 OID 540712)
-- Name: causes_of_action causes_of_action_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.causes_of_action
    ADD CONSTRAINT causes_of_action_pkey PRIMARY KEY (cause_id);


--
-- TOC entry 4339 (class 2606 OID 540714)
-- Name: facts facts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.facts
    ADD CONSTRAINT facts_pkey PRIMARY KEY (fact_id);


--
-- TOC entry 4341 (class 2606 OID 540716)
-- Name: facts facts_unique_entry; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.facts
    ADD CONSTRAINT facts_unique_entry UNIQUE (case_id, type, name);


--
-- TOC entry 4344 (class 2606 OID 540718)
-- Name: jurisdictions jurisdictions_name_level_location_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.jurisdictions
    ADD CONSTRAINT jurisdictions_name_level_location_key UNIQUE (name, level, location);


--
-- TOC entry 4346 (class 2606 OID 540720)
-- Name: jurisdictions jurisdictions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.jurisdictions
    ADD CONSTRAINT jurisdictions_pkey PRIMARY KEY (jurisdiction_id);


--
-- TOC entry 4352 (class 2606 OID 540722)
-- Name: law_domains law_domains_broad_subdomain_specific_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.law_domains
    ADD CONSTRAINT law_domains_broad_subdomain_specific_key UNIQUE (broad, subdomain, specific);


--
-- TOC entry 4354 (class 2606 OID 540724)
-- Name: law_domains law_domains_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.law_domains
    ADD CONSTRAINT law_domains_pkey PRIMARY KEY (domain_id);


--
-- TOC entry 4357 (class 2606 OID 540726)
-- Name: legal_bases legal_bases_name_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.legal_bases
    ADD CONSTRAINT legal_bases_name_type_key UNIQUE (name, type);


--
-- TOC entry 4359 (class 2606 OID 540728)
-- Name: legal_bases legal_bases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.legal_bases
    ADD CONSTRAINT legal_bases_pkey PRIMARY KEY (basis_id);


--
-- TOC entry 4363 (class 2606 OID 540730)
-- Name: legal_principles legal_principles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.legal_principles
    ADD CONSTRAINT legal_principles_pkey PRIMARY KEY (principle_id);


--
-- TOC entry 4367 (class 2606 OID 540732)
-- Name: parties parties_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.parties
    ADD CONSTRAINT parties_name_key UNIQUE (name);


--
-- TOC entry 4369 (class 2606 OID 540734)
-- Name: parties parties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.parties
    ADD CONSTRAINT parties_pkey PRIMARY KEY (party_id);


--
-- TOC entry 4329 (class 2606 OID 540736)
-- Name: cases unique_case_id; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.cases
    ADD CONSTRAINT unique_case_id UNIQUE (case_id);


--
-- TOC entry 4365 (class 2606 OID 540738)
-- Name: legal_principles unique_case_principle; Type: CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.legal_principles
    ADD CONSTRAINT unique_case_principle UNIQUE (case_id, name);


--
-- TOC entry 4290 (class 1259 OID 540739)
-- Name: idx_additional_plaintiffs_case_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_additional_plaintiffs_case_id ON public.additional_plaintiffs USING btree (case_id);


--
-- TOC entry 4293 (class 1259 OID 540740)
-- Name: idx_case_causes_case_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_causes_case_id ON public.case_causes USING btree (case_id);


--
-- TOC entry 4298 (class 1259 OID 540741)
-- Name: idx_case_issues_case_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_issues_case_id ON public.case_issues USING btree (case_id);


--
-- TOC entry 4303 (class 1259 OID 540742)
-- Name: idx_case_jurisdictions_case_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_jurisdictions_case_id ON public.case_jurisdictions USING btree (case_id);


--
-- TOC entry 4304 (class 1259 OID 540743)
-- Name: idx_case_jurisdictions_jurisdiction_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_jurisdictions_jurisdiction_id ON public.case_jurisdictions USING btree (jurisdiction_id);


--
-- TOC entry 4307 (class 1259 OID 540744)
-- Name: idx_case_law_domains_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_law_domains_id ON public.case_law_domains USING btree (case_id);


--
-- TOC entry 4312 (class 1259 OID 540745)
-- Name: idx_case_parties_case_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_parties_case_id ON public.case_parties USING btree (case_id);


--
-- TOC entry 4313 (class 1259 OID 540746)
-- Name: idx_case_parties_party_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_parties_party_id ON public.case_parties USING btree (party_id);


--
-- TOC entry 4318 (class 1259 OID 540747)
-- Name: idx_case_rulings_case_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_rulings_case_id ON public.case_rulings USING btree (case_id);


--
-- TOC entry 4323 (class 1259 OID 540748)
-- Name: idx_case_summaries_case_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_summaries_case_id ON public.case_summaries USING btree (case_id);


--
-- TOC entry 4324 (class 1259 OID 540749)
-- Name: idx_case_summaries_legal_domain; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_case_summaries_legal_domain ON public.case_summaries USING btree (legal_domain);


--
-- TOC entry 4327 (class 1259 OID 540750)
-- Name: idx_cases_name; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_cases_name ON public.cases USING btree (name);


--
-- TOC entry 4332 (class 1259 OID 540751)
-- Name: idx_cause_legal_bases_cause_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_cause_legal_bases_cause_id ON public.cause_legal_bases USING btree (cause_id);


--
-- TOC entry 4337 (class 1259 OID 540752)
-- Name: idx_causes_of_action_name; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_causes_of_action_name ON public.causes_of_action USING btree (name);


--
-- TOC entry 4342 (class 1259 OID 540753)
-- Name: idx_facts_case_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_facts_case_id ON public.facts USING btree (case_id);


--
-- TOC entry 4347 (class 1259 OID 540754)
-- Name: idx_law_domains_broad; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_law_domains_broad ON public.law_domains USING btree (broad);


--
-- TOC entry 4348 (class 1259 OID 540755)
-- Name: idx_law_domains_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_law_domains_id ON public.law_domains USING btree (domain_id);


--
-- TOC entry 4349 (class 1259 OID 540756)
-- Name: idx_law_domains_specific; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_law_domains_specific ON public.law_domains USING btree (specific);


--
-- TOC entry 4350 (class 1259 OID 540757)
-- Name: idx_law_domains_subdomain; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_law_domains_subdomain ON public.law_domains USING btree (subdomain);


--
-- TOC entry 4355 (class 1259 OID 540758)
-- Name: idx_legal_bases_name; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_legal_bases_name ON public.legal_bases USING btree (name);


--
-- TOC entry 4360 (class 1259 OID 540759)
-- Name: idx_legal_principles_case_id; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_legal_principles_case_id ON public.legal_principles USING btree (case_id);


--
-- TOC entry 4361 (class 1259 OID 540760)
-- Name: idx_legal_principles_name; Type: INDEX; Schema: public; Owner: postgres1dev
--

CREATE INDEX idx_legal_principles_name ON public.legal_principles USING btree (name);


--
-- TOC entry 4370 (class 2606 OID 540761)
-- Name: additional_plaintiffs additional_plaintiffs_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.additional_plaintiffs
    ADD CONSTRAINT additional_plaintiffs_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


--
-- TOC entry 4371 (class 2606 OID 540766)
-- Name: case_causes case_causes_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_causes
    ADD CONSTRAINT case_causes_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


--
-- TOC entry 4372 (class 2606 OID 540771)
-- Name: case_causes case_causes_cause_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_causes
    ADD CONSTRAINT case_causes_cause_id_fkey FOREIGN KEY (cause_id) REFERENCES public.causes_of_action(cause_id);


--
-- TOC entry 4373 (class 2606 OID 540776)
-- Name: case_issues case_issues_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_issues
    ADD CONSTRAINT case_issues_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


--
-- TOC entry 4374 (class 2606 OID 540781)
-- Name: case_jurisdictions case_jurisdictions_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_jurisdictions
    ADD CONSTRAINT case_jurisdictions_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


--
-- TOC entry 4375 (class 2606 OID 540786)
-- Name: case_jurisdictions case_jurisdictions_jurisdiction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_jurisdictions
    ADD CONSTRAINT case_jurisdictions_jurisdiction_id_fkey FOREIGN KEY (jurisdiction_id) REFERENCES public.jurisdictions(jurisdiction_id);


--
-- TOC entry 4376 (class 2606 OID 540791)
-- Name: case_law_domains case_law_domains_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_law_domains
    ADD CONSTRAINT case_law_domains_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


--
-- TOC entry 4377 (class 2606 OID 540796)
-- Name: case_law_domains case_law_domains_domain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_law_domains
    ADD CONSTRAINT case_law_domains_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES public.law_domains(domain_id) ON DELETE CASCADE;


--
-- TOC entry 4378 (class 2606 OID 540801)
-- Name: case_parties case_parties_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_parties
    ADD CONSTRAINT case_parties_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


--
-- TOC entry 4379 (class 2606 OID 540806)
-- Name: case_parties case_parties_party_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_parties
    ADD CONSTRAINT case_parties_party_id_fkey FOREIGN KEY (party_id) REFERENCES public.parties(party_id) ON DELETE CASCADE;


--
-- TOC entry 4380 (class 2606 OID 540811)
-- Name: case_rulings case_rulings_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_rulings
    ADD CONSTRAINT case_rulings_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


--
-- TOC entry 4381 (class 2606 OID 540816)
-- Name: case_summaries case_summaries_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.case_summaries
    ADD CONSTRAINT case_summaries_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


--
-- TOC entry 4382 (class 2606 OID 540821)
-- Name: cause_legal_bases cause_legal_bases_basis_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.cause_legal_bases
    ADD CONSTRAINT cause_legal_bases_basis_id_fkey FOREIGN KEY (basis_id) REFERENCES public.legal_bases(basis_id);


--
-- TOC entry 4383 (class 2606 OID 540826)
-- Name: cause_legal_bases cause_legal_bases_cause_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.cause_legal_bases
    ADD CONSTRAINT cause_legal_bases_cause_id_fkey FOREIGN KEY (cause_id) REFERENCES public.causes_of_action(cause_id);


--
-- TOC entry 4384 (class 2606 OID 540831)
-- Name: facts facts_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.facts
    ADD CONSTRAINT facts_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


--
-- TOC entry 4385 (class 2606 OID 540836)
-- Name: legal_principles legal_principles_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres1dev
--

ALTER TABLE ONLY public.legal_principles
    ADD CONSTRAINT legal_principles_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(case_id) ON DELETE CASCADE;


-- Completed on 2025-05-15 20:02:41

--
-- PostgreSQL database dump complete
--

