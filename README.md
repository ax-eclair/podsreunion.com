# PodsReunion

A planned marketplace where people who lost a single AirPod can match with someone who has the complementary orphan part — verified, unlocked, and sustainable.

Live site: [podsreunion.com](https://podsreunion.com)

## The problem

When you lose one AirPod, your only realistic option today is to pay Apple ~€95 for an official single replacement. Meanwhile, millions of orphaned left/right earbuds and cases sit in drawers, useless on their own. Refurbishers can't help: an estimated 80% of returned AirPods are still locked to a previous owner's Apple ID via Find My, and only the original owner can unlock them.

## The idea

A two-sided marketplace that fixes this by keeping the original owner in the loop:

1. Someone with an orphan part (e.g. a left AirPod Pro 2) lists it.
2. Someone who lost the matching part (a right AirPod Pro 2) finds the listing.
3. The seller removes the part from their Apple ID via Find My.
4. PodsReunion verifies the unlock and brokers the transaction.
5. Each piece is shipped to the buyer or to a collection point where matched left + right + case can be combined into a working set.

Every part is sold by its rightful, willing owner, properly unlocked. No grey-area sourcing.

## Status

**Phase 1 — Validation (current).** This repository contains a static landing page used to gauge demand before any product is built. Visitors can read the pitch and join an email waitlist. The goal is to learn whether real users in Germany want this before investing months in building the marketplace.

**Phase 2 — MVP.** Once demand is validated, build a small Django + PostgreSQL marketplace covering listings, matching, messaging, Find My unlock verification, and Stripe payments.

## Tech stack (Phase 1)

- Django — serves the current public pages locally
- Django templates and static files — no frontend build step
- `uv` — Python dependency management
- SQLite — default local database
- Heroku-ready settings — foundation only, not deployed yet

## Run locally

Install dependencies:

```bash
uv sync
```

Run migrations:

```bash
make migrate
```

Start Django:

```bash
make run
```

Then visit [http://localhost:8100](http://localhost:8100).
Use `make run PORT=8102` to run on a different local port.

Run tests:

```bash
make test
```

See [Getting Started](docs/guides/getting-started.md) for more details.

## Project structure

```
.
├── manage.py
├── podsreunion/        # Django project and settings
├── pages/              # Public page views
├── templates/pages/    # Landing and legal templates
├── static/             # CSS, favicons, logo, AirPods assets
├── docs/               # Local setup, deployment notes, architecture docs
├── tests/              # Small 200-response test suite
├── CNAME               # Custom domain record from the static-site era
└── README.md
```

## Roadmap

- [x] Validation landing page live
- [ ] First 30 waitlist signups
- [ ] User interviews (5 calls with people who lost an AirPod)
- [ ] Django marketplace MVP
- [ ] Find My unlock verification flow
- [ ] Stripe payments + escrow
- [ ] First 10 real transactions

## Contact

Built by Axel Giret — [giretaxel@gmail.com](mailto:giretaxel@gmail.com)

If you've ever lost a single AirPod, I'd love to hear what you did about it.
