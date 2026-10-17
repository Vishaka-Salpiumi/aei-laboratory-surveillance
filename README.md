# MicrobeLog

Bilingual English/Finnish laboratory surveillance and synthetic patient record prototype for the Tyks Laboratories × Mylab JunctionX Turku challenge.

Input analysis and the damaged participant-guide limitation are documented in INPUT_REVIEW.md.

## Run

Python 3, no dependencies or API keys required:

```bash
python serve.py
```

Open http://localhost:8000. The supplied synthetic data is included. `dist/` is a buildless web application; `.openai/hosting.json` configures the existing private Site. Do not upload secrets or personal health records.

## Workspaces

- **Ward overview / Osaston yleiskuva:** rolling 28-day and 365-day R/S rates; resistance trend; women/men urinary E. coli comparison; antibiotic evidence and Wilson 95% intervals.
- **Resistance changes / Resistenssin muutokset:** previous-year baseline excluding the current 28 days; exploratory ≥10 percentage-point watch rule; one-sided Fisher test with Benjamini–Hochberg adjustment for review signals. Not validated outbreak detection.
- **Patient records / Potilastiedot:** all demographics, all cultures (including negative), all isolates and recorded S/R results, quantities and ESBL/MRSA/VRE/CPE. Complete linked JSON download. Patient presentation is a view, not separate patient authentication.
- **Bacterial growth / Bakteerikasvu:** category shares and specimen-specific interpretation, coloured lower/intermediate/higher growth bands, explicit denominator. Colours are not clinical risk or safety thresholds.
- **Laboratory data / Laboratoriotiedot:** all six original tables, all original columns with friendly bilingual headings and technical names; field search, pagination, original/filtered CSV downloads.
- **Microscopy lab / Mikroskopialaboratorio:** local reference images, PNG/JPEG/WebP opening, brightness/contrast, grayscale/inversion, binary threshold, 4-connected white-region measurements, CSV object export and PNG image export. These are uncalibrated pixel-region measurements, not validated bacterial counts. Actual ImageJ.JS embeds on demand with full menus and the public CDC image. Third-party runtime/browser restrictions may prevent embedding; a separate-window link is included. Desktop ImageJ review macro also provided.
- **Statistics & R / Tilastot ja R:** complete CSVs, tidy current statistics, independent raw-record `analysis.R`, and an actual webR notebook on demand. The notebook receives aggregate statistics named `stats`; its runtime is downloaded from the official webR host. No patient rows are sent to webR. Third-party runtime execution was not browser-verified in this environment.
- **Ask MicrobeLog / Kysy MicrobeLogilta:** working local English/Finnish query parser for patient IDs, antibiotics, organisms, wards, specimen and sex comparisons. Parsed scope is shown. No external LLM is configured on the static hosted demo. See AI_SETUP.md for optional server-side Groq/Grok interpretation.
- **Methods & help / Menetelmät ja ohjeet:** calculation definitions, limitations, installation and dataset README.

## Reporting rule

Join patients → cultures → isolates → susceptibility on their IDs. Apply cohort/date filters, sort by date, culture ID and isolate ID, then retain the first isolate per patient, species and specimen type **within the selected cohort and reporting period**. Do this independently for recent, annual and historical periods. Do not select a later isolate just because it has more tests.

For each antibiotic, count only recorded S/R results on selected first isolates. R% = R/(R+S) × 100; S% = S/(R+S) × 100. Percentages are suppressed for n < 30 tested isolates; counts remain visible. Missing tests are never susceptible. Annual means a rolling 365-day period, not a calendar year. Admission day 3 means at least two calendar days after admission (admission day = day 1); timing does not establish hospital acquisition.

Filters: care location, species (Latin names), specimen, sex, age group, organisation type, inpatient/outpatient, home area, admission timing, phenotype and reporting date. The full-table explorer and patient record are independent of report filters.

## Quantity and clinical interpretation

Urine categories are 10^3, 10^4 and >=10^5 CFU/mL. Wound grades +, ++ and +++ are ordinal; blood quantity is blank. Display colours indicate lower/intermediate/higher **recorded growth only**. The top urine category is a lower bound, not an exact count. Quantity is not a percentage; a displayed percentage is the share of eligible first isolates in that category. The README provides no wound-grade CFU conversion.

Lower counts may be significant in symptomatic patients; high counts can occur without symptomatic infection. There are no universally safe colour zones. No disease probabilities or treatment recommendations are produced: diagnoses, symptoms, medication and clinical outcomes are absent. The UI explains these limits instead of inventing predictions.

Sources: UKHSA urinary tract infection diagnostic guidance https://www.gov.uk/government/publications/urinary-tract-infection-diagnosis/diagnosis-of-urinary-tract-infections-quick-reference-tools-for-primary-care ; IDSA 2019 asymptomatic bacteriuria guideline https://www.idsociety.org/practice-guideline/asymptomatic-bacteriuria/ . The original DATA_README.md documents Finres 2023 calibration, illustrative rates and EUCAST Expected Resistant Phenotypes v1.2. This is S/R only: no I, MIC or inhibition-zone data. Do not infer clinical efficacy from surveillance rates.

## Images and external tools

Included images are public domain, not synthetic patient specimens:

- CDC PHIL 12166, E. coli fecal smear, CDC/Charles Farmer, 1965. https://wwwn.cdc.gov/phil/Details.aspx?pid=12166
- CDC PHIL 2296, S. aureus photomicrograph, CDC/Dr. Richard Facklam, 1980. https://wwwn.cdc.gov/phil/Details.aspx?pid=2296

They are linked by species for teaching; they do not validate a patient's quantity, disease or resistance. No pixel calibration is supplied. Attribution and original source links are displayed. ImageJ.JS https://imagej.net/software/imagej-js ; webR https://docs.r-wasm.org/webr/latest/ . Their respective software licenses apply; third-party runtimes are loaded externally, not bundled.

## Mobile app

Installable progressive web app with responsive mobile navigation, manifest, home-screen icons, safe-area support and network-only service worker. Android: Chrome menu → Add to Home screen → Install. iOS/iPadOS: Safari Share → Add to Home Screen. It is **not** a native APK/IPA or an App Store/Google Play release. Internet access and access to the private demo are required. Laboratory records are not service-worker cached. Only language preference is saved locally.

## Data updates

While open, the app polls data.json every 60 seconds, invalidates raw-table caches and recomputes changed reports. It also offers manual refresh. Current source files are static and historical replay simulates arriving results, not a hospital LIS feed. Update the hosted dataset by rebuilding and redeploying the complete set atomically:

```bash
python prepare_data.py /path/to/synthetic_microbiology_dataset.zip
node check_engine.cjs
node check_workspace.cjs
python package_source.py
```

Production requires a validated ingestion service, authenticated patient/staff permissions and clinical validation. This prototype implements none of those production controls.

## Validation and source

`check_engine.cjs` checks real-data counts, first-isolate deduplication, missing-test handling, dates and statistics. `check_workspace.cjs` checks all 18 view/language combinations in a lightweight DOM harness, real-data chat lookup, patient lookup, connected-region analysis and advanced filters. The harness is not visual browser QA. The managed preview environment failed before launch, so browser rendering, ImageJ runtime, webR runtime and phone installation remain unverified.

`dist/source/` contains a source browser and `microbelog-source.zip`. It inherits site access: the existing Site remains owner-private. Upload the source ZIP to a judge-accessible GitHub repository for submission. No public GitHub repository has been created by this prototype.

AI-assisted implementation. No licence was asserted over the supplied challenge dataset; verify redistribution terms before public sharing.


## Lovable feature integration
See [FEATURE_COMPARISON.md](FEATURE_COMPARISON.md) for added views, methods, deliberate differences and validation limits. New UI features are in `dist/extensions.js`.

## GitHub data packaging
The generated susceptibility JSON is split into two parts to fit the upload transport limit. The application combines both parts before querying. All 172,381 susceptibility records and the original susceptibility CSV are included. This packaging does not change any surveillance calculations.
