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

- HTML, CSS — no framework, no build step
- [Formspree](https://formspree.io) — email-capture form (free tier)
- GitHub Pages — static hosting on the custom domain
- Inline SVG — illustrated AirPods scattered as an animated background

## Run locally

No build step. Just open the file:

```bash
git clone https://github.com/ax-eclair/podsreunion.com.git
cd podsreunion.com
open index.html
```

Or serve it on a local port if you want a more realistic environment:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Project structure

```
.
├── index.html          # Landing page with email signup
├── style.css           # All page styles + background animation
├── logo.png            # Brand illustration
├── impressum.html      # Legal notice (TMG §5)
├── datenschutz.html    # Privacy policy (GDPR)
├── CNAME               # Custom domain for GitHub Pages
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
