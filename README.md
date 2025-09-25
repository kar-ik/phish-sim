# phish-sim
Phish-Sim Tool: Consent-First Phishing Simulation &amp; Awareness CLI
# Phish-Sim Tool: Consent-First Phishing Simulation & Awareness CLI

## Purpose
A consent-first, configurable phishing simulation and awareness automation tool for authorized campaigns. Helps admins measure outcomes and deliver training while enforcing safety controls. **NOT for malicious use.** Requires explicit authorization.

## Hard Constraints
- Explicit consent (PDF upload) required before launch.
- No real credential capture: Only boolean events logged.
- Default: Sandbox mode (no real emails).
- Audit logs, RBAC, rate limits, kill switch enforced.
- Privacy: 30-day data retention.

## Quickstart (Sandbox Mode)
1. Clone repo: `git clone <repo>`
2. Install: `pip install -e .`
3. Run: `phish-sim --help`
4. Create campaign: `phish-sim create-campaign --title "Test" --consent-path consent.pdf --passphrase "secret"`
5. Simulate: `phish-sim simulate --campaign-id 1`
6. View metrics: `phish-sim dashboard --campaign-id 1`
7. Kill switch: `phish-sim kill --campaign-id 1 --confirm`

For real sending (DANGER: Admin-only): Set `SENDGRID_API_KEY` env, use `--enable-sendgrid`, provide domain proof, two-person approval.

## Security & Governance
- Read `docs/PrivacyPolicy.md`.
- Consent template: `docs/ConsentTemplate.md`.
- Audit logs: `./logs/audit.json`.
- Enable connectors: Manual only; see `config.py`.

## Usage Policy
Use only with volunteers and documented consent. Authors not liable for misuse. 

License: Apache-2.0
