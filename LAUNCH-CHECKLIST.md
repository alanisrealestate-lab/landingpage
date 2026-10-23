# Sell for 2% launch checklist

Live site: https://sellfor2.theorangerealestategroup.com

## Send to Claude (to finish the code)

- [ ] **GHL webhook URL.** In GHL, create a workflow with an "Inbound Webhook" trigger and copy its URL. Until it's connected, form submissions aren't saved anywhere; only calendar bookings reach you.
- [ ] **Contact email.** It still says `hello@example.com` in the footer and in the Privacy Policy ("To exercise these rights…").
- [ ] **Brokerage license number** for the footer. BK3297706 is your personal broker license. Send the brokerage's own number, or say to use yours.
- [ ] **Meta Pixel ID** (and a GTM or GA4 ID if you use them), to add ad tracking to all five pages.
- [ ] **Social links:** your Facebook, Instagram and Google Business Profile URLs. The footer icons don't go anywhere yet.
- [ ] **"What if I find a buyer on my own?"** Your exact terms for this FAQ answer and the matching row in the comparison table. Both are still placeholders.
- [ ] **Service areas:** confirm the FAQ list (Bradenton, Sarasota, Lakewood Ranch, Parrish, Palmetto, Ellenton, plus the surrounding Manatee and Sarasota County area).
- [ ] **SMS consent wording** under the form. It's placeholder text; have it reviewed, then send any changes.

## Set up in GHL

- [ ] Set the main Sell for 2% step as the domain's **default page**, so the plain domain opens it.
- [ ] Set the step paths to exactly `thank-you`, `visit-booked`, `privacy-policy` and `terms-of-use`, and paste the matching `ghl/` file into each one.
- [ ] Set the default 404 page to the main Sell for 2% page.
- [ ] Calendar: set the redirect after booking to `https://sellfor2.theorangerealestategroup.com/visit-booked`.
- [ ] Calendar: 15-minute slots, a 30–45 minute buffer, 2–3 hours minimum notice, only the hours you'll go out, and text confirmations plus 24-hour and 2-hour reminders.
- [ ] Workflows: an instant text after the form, a booking confirmation, the reminders, and a "didn't book" follow-up. The message text is in the chat.
- [ ] Main step SEO settings: title, description and social image (`images/og-image.jpg`).
- [ ] Funnel favicon: your logo icon.
- [ ] Reviews widget styling: white background, text #1A1A1A, accent #FAA32A, Plus Jakarta Sans or Inter, carousel layout.

## Outside GHL

- [ ] Meta Business Settings > Brand Safety > Domains: verify theorangerealestategroup.com.
- [ ] **End-to-end test on your phone:** fill out the form, check the thank-you page (calendar loads and is pre-filled), book a time, land on the "You're booked" page, get the text, and confirm the lead shows up in GHL.

## Optional

- [ ] Switch the remaining #FF9800 accents (section labels, 2% badge, calculator slider) to the logo orange #FAA32A.
- [ ] Make the final orange banner the darker orange (#B35C00) so the white text is easier to read.
- [ ] Rename the main step's path from `landing-page-page` to something cleaner, like `sell-for-2`.
- [ ] Make `www.sellfor2.theorangerealestategroup.com` work too: add a CNAME record for `www.sellfor2` with the same value as `sellfor2`, add it as a domain in GHL, and redirect it to the version without www.
- [ ] Make the "Call Adrian" buttons on the thank-you and "You're booked" pages orange (logo orange #FAA32A, like the other main buttons) instead of the black outline.
