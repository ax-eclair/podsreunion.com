# PodsReunion — v1 Scope

> The locked plan for the first version of the marketplace. When in doubt, read this. When tempted to add a feature, read the "What's NOT in v1" section first.

## One-line description

A trust-first marketplace in Germany for individual AirPod parts (left earbud, right earbud, case) — verified, unlocked, with held-payment buyer protection.

## Locked decisions

| Decision | Value | Why |
|----------|-------|-----|
| Business model | Pure marketplace (commission only) | Capital-light, no inventory risk, faster MVP |
| Country | Germany only | 3× lower complexity than multi-country |
| Products | AirPods 1, 2, 3, 4, Pro 1, Pro 2 (Lightning + USB-C) | Tight catalog, easier verification |
| Pricing | Seller sets freely + UI shows "average price" hint | Vinted-style, natural seller autonomy |
| Listing expiry | 30 days, one-click renew | Standard, prevents stale catalog |
| Communication | Real-time chat (Django Channels + Redis), text only, 1-on-1 | Genuine learning project, smooth UX |
| Buyer protection | Vinted-style escrow via Stripe Connect | Defuses "is this locked/stolen?" fear |
| Buyer protection fee | 7% (Vinted-aligned) | Best revenue-per-transaction for zero added complexity |
| Confirmation window | 3 days post-delivery, auto-release on timeout | Standard escrow pattern |
| Dispute resolution | Manual (email-based) for v1 | No automation needed at low volume |
| Multi-seller cart | Not in v1 | Significant complexity; sequential purchases work fine |
| Wishlist UI | None — auto-derived from user's listing | Less data entry for users |
| Anonymous browsing | Yes; account required only at checkout | Lower friction for pure buyers |

## What's IN v1

### Listings
- Users list 1–3 items they have: model + generation + side (or case) + condition (A/B/C) + price + photos
- Auto-expire after 30 days, one-click renew
- Seller sets price; UI shows "Listings like yours sell for around €X" based on platform data
- Optional checkbox: "Notify me when I could complete this set" — system auto-derives missing parts

### Verification (manual review by admin before listing goes public)
- **Stage 1** — photo of the model number on the stem (or inside the case lid)
- **Stage 2** — condition photos (A/B/C grade)
- **Stage 3** — Find My screenshot showing the part removed from the seller's Apple ID

### Search & matching
- Browse and filter by model + generation + side
- **Direct match** notification: a new listing pings every user whose missing parts include this listing
- **Triangle completion** notification: when you have one part listed and the other parts become available, you get an email

### Real-time chat
- Django Channels + Redis, text only, 1-on-1 between buyer ↔ seller of a specific listing
- Email notification when offline ("You have a new message")
- Report button → admin inbox

### Buyer protection (Stripe Connect)
- Buyer pays listing price + 7% protection fee at checkout
- Funds held in platform Stripe account
- Seller ships, manual tracking entry (no DHL/Hermes API in v1)
- Buyer has 3 days post-delivery to confirm OK or report a problem
- Auto-release on timeout
- Disputes handled manually by admin

## What's NOT in v1

Read this list whenever you're tempted to add something. Refusing these saves months.

- AirPods Max, Beats, generic earbuds
- Multi-seller cart / single-checkout assembly (buyers complete sets via sequential individual purchases, guided by the matching email)
- Image attachments or voice notes in chat
- Typing indicators, read receipts, online status
- Push notifications (web or mobile) — email only
- Mobile app
- Star ratings or seller reviews
- Automated dispute resolution
- Carrier API integration
- "Make an offer" / negotiation flow
- Refurbished bundled-pair offering (potential phase 2)
- Seller ID verification beyond email
- International shipping
- Multi-language UI

## Tech stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Backend | Django + PostgreSQL | Beginner-friendly, hireable, mature |
| ASGI server | Daphne | Required for WebSockets |
| Real-time | Django Channels + Redis | WebSocket consumers, pub/sub broker |
| Frontend | Django templates + HTMX + Tailwind | No build step, fast to ship |
| Chat client | Vanilla JS WebSocket | Minimum learning curve |
| Auth | django-allauth | Email confirmation, password reset out of the box |
| Payments | Stripe Checkout + Stripe Connect Express | Industry standard; delayed transfers fit escrow |
| Email | Postmark or Mailgun | Reliable transactional delivery |
| Photos | Cloudinary (free tier) | No self-hosted image pipeline |
| Hosting | Render or Railway | Push-to-deploy, supports ASGI + Redis |

Realistic running cost at zero traffic: **~€10–15/month** (Redis + email).

## Data model (preview)

Six core tables:

```
User           email, name, shipping_address
Listing        user, model, gen, side, condition, price, photos,
               notify_when_completable, status, created_at, expires_at
Verification   listing, stage_1_photo, stage_2_photos, stage_3_screenshot,
               status, reviewed_by, reviewed_at, notes
Conversation   listing, buyer, seller, created_at
Message        conversation, sender, body, read, created_at
Order          listing, buyer, amount, protection_fee,
               stripe_payment_intent, status, tracking_number,
               paid_at, delivered_at, completed_at
Dispute        order, opened_by, reason, photos, resolution,
               opened_at, resolved_at
```

## Roadmap to soft launch

Targeting ~10 hours/week of work, 3.5 months from skeleton to launch.

| Weeks | Focus |
|-------|-------|
| 1–2  | Django project skeleton, models, admin, deploy empty app |
| 3–4  | Auth (django-allauth), listing creation, photo upload (Cloudinary) |
| 5–6  | Verification workflow, manual admin review tool |
| 7–8  | Browse, search, matching engine, notification emails |
| 9–10 | Real-time chat (Django Channels + Redis + ASGI deployment) |
| 11–12 | Stripe Connect, buyer protection, escrow flow |
| 13   | Legal pages (German), German UI strings, polish |
| 14   | Soft launch to Kleinanzeigen contacts + waitlist signups |

## Validation phase (parallel, ongoing)

- Landing page live at podsreunion.com
- Email waitlist via Formspree
- Outreach via Kleinanzeigen DMs
- Goal: 5 user interviews (10-min calls) by end of week 2 to inform listing-page design

## Reference

- Direct competitor (reseller, not marketplace): [mypods24.de](https://mypods24.de)
- Spiritual reference for trust UX: Vinted (buyer protection, escrow flow)
- Spiritual reference for vertical marketplace: StockX (verification, condition grading)
