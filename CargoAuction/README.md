# Cargo Auction

Auctions off available vessel space to customers. Vessels, routes, and port
ETAs are managed by admins; customers browse open auctions and bid their own
cargo details and rate against a base rate. Highest bid wins when an admin
closes the auction.

## Stack

- Streamlit (UI + navigation)
- Supabase Auth (login/signup, via `supabase-py`)
- Supabase Postgres (app data, via SQLAlchemy)

## Setup

1. Create a Supabase project at [supabase.com](https://supabase.com).
2. In the Supabase dashboard:
   - **Project Settings > API** — copy the Project URL, `anon` public key,
     and `service_role` key.
   - **Project Settings > Database** — copy the host/port/database/user/password
     (use the "Connection pooling" host if deploying somewhere serverless).
   - **Authentication > Providers** — for local testing, consider disabling
     "Confirm email" so accounts created through the app can log in immediately.
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill
   in the values from step 2. This file is gitignored — never commit it or
   paste its contents anywhere outside your own machine.
4. Install dependencies (from the `CargoAuction/` directory):
   ```
   pip install -r requirements.txt
   ```
5. Create the first admin account:
   ```
   python scripts/create_admin.py --email admin@example.com --password "..." --username admin
   ```
6. Run the app:
   ```
   streamlit run cargoauction.py
   ```

Tables are created automatically on first run (`init_db()` in `models.py`).

## Roles

- **Customer** — self-registers through the app's Register tab. Can browse
  open auctions, view a vessel's route/ETA, and submit bids.
- **Admin** — created only via `scripts/create_admin.py` (uses the Supabase
  service role key). Manages vessels, ports, schedules, and auctions, and
  closes auctions to select a winner.

## Deploying for a public URL

The simplest option is [Streamlit Community Cloud](https://streamlit.io/cloud):
push this folder to a GitHub repo, deploy `cargoauction.py`, and paste the
contents of your local `secrets.toml` into the app's Secrets settings in the
Streamlit Cloud dashboard (never into source control).

Alternatively, build and run the included `Dockerfile` on any host that can
reach your Supabase project, passing the same values as environment variables
(the app falls back to env vars when a key isn't in `st.secrets`).

## Known limitations (v1)

- Login session lives in `st.session_state`, so a hard browser refresh logs
  the user out. Adding persistent sessions (cookies/query params) is a
  reasonable follow-up.
- App data tables connect via the Postgres `postgres` role and rely on
  application-level checks (not Row-Level Security) for authorization, since
  Streamlit itself is the trusted server-side boundary. Enabling RLS on the
  `cargo_auction` schema tables is a good defense-in-depth follow-up before
  handling real customer data in production.
- No email notifications — winners currently find out via the "My Bids" page
  after logging in.
