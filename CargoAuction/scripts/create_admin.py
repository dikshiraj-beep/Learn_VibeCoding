"""Bootstrap an admin account. Run from the CargoAuction/ directory:

    python scripts/create_admin.py --email admin@example.com --password "..." --username admin

Requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .streamlit/secrets.toml.
The service role key is never used by the main app — only by this script.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from supabase import create_client  # noqa: E402

from db import _secret_or_env, get_session_factory  # noqa: E402
from models import Profile, init_db  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Cargo Auction admin account")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--username", required=True)
    parser.add_argument("--company-name", default="")
    args = parser.parse_args()

    url = _secret_or_env("SUPABASE_URL")
    service_role_key = _secret_or_env("SUPABASE_SERVICE_ROLE_KEY")
    admin_client = create_client(url, service_role_key)

    init_db()

    response = admin_client.auth.admin.create_user(
        {
            "email": args.email,
            "password": args.password,
            "email_confirm": True,
        }
    )
    if response.user is None:
        print("Failed to create auth user.", file=sys.stderr)
        sys.exit(1)

    session_factory = get_session_factory()
    with session_factory() as session:
        session.add(
            Profile(
                id=response.user.id,
                username=args.username,
                email=args.email,
                company_name=args.company_name,
                role="admin",
            )
        )
        session.commit()

    print(f"Admin account created for {args.email}.")


if __name__ == "__main__":
    main()
