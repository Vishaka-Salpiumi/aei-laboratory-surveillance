# Lovable project comparison and integration

Reviewed upload: MicrobeLog-main.zip, including routes, patient joins, surveillance calculations, clinical heuristics, microscopy, bilingual labels and AI endpoint. Existing MicrobeLog remains the deployed application; the React/TanStack project was not substituted for it.

## Added
- Calendar-year antibiotic comparisons; organism–antibiotic resistance heatmap with year selector and multi-antibiotic female/male urinary E. coli comparison.
- Bulk annual species × sample type × antibiotic CSV, retaining other selected cohort filters. Calendar years are deduplicated separately. Missing/under-30 rates remain blank.
- Quarterly observed resistance and four-quarter experimental extrapolation. At least four complete quarters with 30 tested isolates are required. Weighted linear fit on smoothed log odds, inverse-logit output bounded 0–100%. Partial quarters are shown but not fitted. No clinical validation or prediction intervals claimed.
- Patient directory with demographics, age/date bounds, location/care setting, culture results, ISO year/week, organism count, organism, growth, phenotype, antibiotic result and guideline filters. Linked conditions apply to the same culture and isolate/test; result-only searches work. Paged matching patient summaries export as CSV.
- Patient review counts: positive blood cultures, samples at least two days after admission, and recorded ESBL/MRSA/VRE/CPE flags. No arbitrary numerical patient risk score.
- Growth distribution comparison across specimen types, with separate denominators and CSV.
- Microscopy Gaussian blur, sharpening, Sobel edges, histogram equalization, Otsu thresholding and intensity histogram. Filters operate on displayed pixels. Two-point distances use actual canvas coordinates. Optional user-supplied µm/pixel calibration supplies physical length and exported region areas; no invented default scale. Region coverage and mean area are shown.
- New chat conversation control. New screens have English and Finnish text and responsive layouts.

## Already present and retained
Rolling 28-day/365-day surveillance, first-isolate deduplication, minimum 30 tested isolates, statistical alerts, complete source-table explorer, patient record export, bilingual local data assistant, optional server-side Groq/xAI interpretation, real CDC reference microscopy, embedded ImageJ, optional webR, R scripts, installable mobile web app and downloadable source.

## Deliberate differences / remaining integrations
- Lovable's rule-based disease labels and arbitrary 0–100 risk score cannot be validated against this dataset, which has no diagnoses, symptoms, medications or outcomes. They were replaced with observed findings and experimental population resistance projections.
- Lovable's generated microscopy illustrations were not transferred as scientific samples. Existing real public-domain CDC images remain; user image upload supports other organisms. No patient image linkage is invented.
- LOVABLE_API_KEY and Lovable's hosted AI gateway are not portable runtime configuration. Deployed static app retains its explicit local-assistant label. External AI requires a configured backend; see AI_SETUP.md. No credentials are included in source.
- This remains an installable responsive web application, not App Store/Play Store native binaries or a clinical production system.

## Verification
`node check_engine.cjs` and `node check_workspace.cjs` cover the calculation engine, 24 bilingual screen renders in a lightweight DOM harness, linked-patient result matching, minimum sample counts and bounded/insufficient-data forecasts. JavaScript syntax checks pass. The managed browser preview is unavailable in this environment (browser sandbox mount failure), so visual browser QA and external ImageJ/webR runtime loading are not verified here.
