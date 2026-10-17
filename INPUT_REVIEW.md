# Input review

- **Synthetic microbiology ZIP:** original README read in full; all six CSV tables joined and preserved. 10,000 patients, 46,792 cultures, 24,571 isolates, 172,381 susceptibility rows, 9 locations, 13 antibiotic codes. Raw headers remain available beneath bilingual friendly names.
- **Tyks × Mylab challenge PDF:** read. The prototype addresses rolling four-week/annual reports, local filtering, usability, and exploratory deviation detection. It does not claim to be a validated clinical product or a live LIS connection.
- **Vestafy source ZIP:** reviewed its README, repository structure and application dependencies as a reference for the analytics → evidence → explanation workflow. It is a Next.js/Express/Supabase marketing app and uses Groq. Its business code, credentials and marketing data were not imported into this microbiology prototype.
- **Participant_guide.pdf:** the supplied copy has a missing/invalid PDF trailer and damaged cross-reference/font information. A recovery read produced only a partial, garbled page repeating the synthetic-data overview. It was not treated as a complete or reliable source of additional rules. The intact dataset README and challenge brief govern this implementation.

## Quantity audit

| Specimen | Raw category | Isolates |
|---|---|---:|
| urine | >=10^5 | 13,116 |
| urine | 10^4 | 3,759 |
| urine | 10^3 | 1,875 |
| wound | ++ | 1,989 |
| wound | + | 1,484 |
| wound | +++ | 1,446 |
| blood | blank | 902 |

These are raw source totals, not first-isolate reporting denominators. The dashboard's growth report uses the selected reporting cohort and independently deduplicates first isolates. Category percentages use that cohort denominator and are withheld below 30.
