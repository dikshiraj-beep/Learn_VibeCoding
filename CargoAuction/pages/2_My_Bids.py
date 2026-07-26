import pandas as pd
import streamlit as st
from sqlalchemy import select

from auth import current_profile
from db import get_session_factory
from models import Bid, CargoAuction, Port, Vessel

st.title("My Bids")

profile = current_profile()
session_factory = get_session_factory()

if st.button("Refresh"):
    st.rerun()

with session_factory() as session:
    rows = session.execute(
        select(Bid, CargoAuction, Vessel, Port)
        .join(CargoAuction, Bid.auction_id == CargoAuction.id)
        .join(Vessel, CargoAuction.vessel_id == Vessel.id)
        .join(Port, CargoAuction.discharge_port_id == Port.id)
        .where(Bid.customer_id == profile.id)
        .order_by(Bid.bid_time.desc())
    ).all()

if not rows:
    st.info("You haven't placed any bids yet. Visit Browse Auctions to get started.")
    st.stop()

status_labels = {"pending": "⏳ Pending", "won": "✅ Won", "lost": "❌ Lost"}

table = pd.DataFrame(
    [
        {
            "Vessel": vessel.name,
            "Discharge port": port.name,
            "Cargo": bid.cargo_description,
            "Quantity": float(bid.cargo_weight),
            "Bid rate": float(bid.bid_rate),
            "Auction status": auction.status,
            "Bid status": status_labels.get(bid.status, bid.status),
            "Submitted": bid.bid_time,
        }
        for bid, auction, vessel, port in rows
    ]
)
STATUS_COLORS = {
    "⏳ Pending": "background-color: #FFF3CD; color: #7A5B00;",
    "✅ Won": "background-color: #D4EDDA; color: #155724;",
    "❌ Lost": "background-color: #F8D7DA; color: #721C24;",
}
styled_table = table.style.map(lambda v: STATUS_COLORS.get(v, ""), subset=["Bid status"])
st.dataframe(styled_table, use_container_width=True, hide_index=True)
