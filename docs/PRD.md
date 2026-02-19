# PRD: Reservation Drop Tracker + Assisted Booker (Option B)

## Goals
- Help a single user discover hard-to-book restaurants in NYC and Philadelphia by mining Reddit discussions.
- Infer reservation drop rules (lead time + opening time + provider) and allow manual override.
- Let the user browse restaurants and quickly plan a booking request.
- Execute booking in an assisted and policy-safe way:
  - Open deep links at the right time by default.
  - Optionally run headed Playwright to pre-fill and assist.
  - Always pause for login/CAPTCHA/2FA.
  - Always require final confirmation before submission.

## Non-goals
- Multi-user accounts, hosted service, team workflows.
- Any anti-bot evasion or CAPTCHA bypass.
- Reverse engineering private APIs for Resy/OpenTable.
- Guaranteed booking success.

## Guardrails
- No stealth, no ToS evasion, no credential capture.
- Playwright is assisted-only and may be interrupted for manual user action.
- Minimal PII storage; logs must redact emails/phones.
- Automation defaults to `dry_run` for safer testing.

## Target users
- One technically-inclined person trying to secure reservations in NYC/PHL.

## Geography and providers
- Cities: NYC, PHL only.
- Providers: Resy and OpenTable only (unknown allowed until inferred).

## UX/workflows
1. **Discovery refresh** (`resy_sniper refresh`)
   - Fetch Reddit posts/comments from configured subreddits.
   - Extract candidate restaurant entities + hard-to-book signals.
   - Save mention counts and evidence snippets.

2. **Drop rule inference** (`resy_sniper infer`)
   - Parse evidence for lead time/time/provider phrases.
   - Build confidence score and source links.
   - Persist inferred DropRule per restaurant.

3. **Browse** (`resy_sniper browse`)
   - Select city and inspect provider/rule/confidence.
   - Review evidence count and next drop time estimate.

4. **Plan** (`resy_sniper plan ...`)
   - Create booking request for party/date/window.
   - Compute next run time and create queued job.

5. **Book** (`resy_sniper book ...`)
   - If drop open, run now; else schedule.
   - Default mode opens deep link.
   - `--assist` uses headed Playwright and pauses when blocked/challenged.

## Success metrics
- >80% of manually verified restaurants have at least one evidence-backed inferred rule.
- User can generate a job from browse/plan in <2 minutes.
- Logs show zero raw credentials and redacted PII patterns.

## Risks
- Reddit quality/noise may cause false positives.
- Selector fragility in UI automation.
- Inference ambiguity in natural-language drop discussions.

## MVP scope in this repo
- Local CLI app with SQLite storage.
- Basic Reddit fetch with mock fallback.
- Heuristic inference + manual edit command.
- Browse list in terminal.
- Scheduler and deep-link booking execution.
- Playwright-assisted stubs with explicit TODO selectors.
