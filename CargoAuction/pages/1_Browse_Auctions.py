from datetime import datetime, timezone

import pandas as pd
import streamlit as st
from sqlalchemy import select

from auth import current_profile
from db import get_session_factory
from models import Bid, CargoAuction, Port, Vessel, VesselSchedule

st.title("Browse Auctions")
st.write(
    "Available vessel space open for bidding. This is a sealed-bid auction — "
    "you won't see other bidders' offers. Submit your cargo details and your best rate."
)

profile = current_profile()
session_factory = get_session_factory()

with session_factory() as session:
    open_auctions = session.execute(
        select(CargoAuction, Vessel)
        .join(Vessel, CargoAuction.vessel_id == Vessel.id)
        .where(CargoAuction.status == "open")
        .order_by(CargoAuction.auction_close_at)
    ).all()

if not open_auctions:
    st.info("No open auctions right now. Check back later.")
    st.stop()

vessel_options = {f"{vessel.name} — auction #{auction.id}": auction.id for auction, vessel in open_auctions}
selected_label = st.selectbox("Select a vessel / auction", list(vessel_options.keys()))
auction_id = vessel_options[selected_label]

with session_factory() as session:
    auction = session.get(CargoAuction, auction_id)
    vessel = session.get(Vessel, auction.vessel_id)
    load_port = session.get(Port, auction.load_port_id)
    discharge_port = session.get(Port, auction.discharge_port_id)

    schedule_rows = session.execute(
        select(VesselSchedule, Port)
        .join(Port, VesselSchedule.port_id == Port.id)
        .where(VesselSchedule.vessel_id == vessel.id)
        .order_by(VesselSchedule.sequence)
    ).all()

col1, col2 = st.columns(2)
with col1:
    st.subheader(vessel.name)
    st.write(f"Load port: **{load_port.name}**")
    st.write(f"Discharge port: **{discharge_port.name}**")
    st.write(f"Space available: **{auction.capacity_available} {auction.capacity_unit}**")
    st.write(f"Base rate: **{auction.base_rate} {auction.currency}** per {auction.capacity_unit}")
    st.write(f"Auction closes: **{auction.auction_close_at}**")

with col2:
    st.subheader("Vessel route")
    route_df = pd.DataFrame(
        [{"Port": port.name, "ETA": stop.eta} for stop, port in schedule_rows]
    )
    st.dataframe(route_df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Place your bid")

auction_closed = auction.auction_close_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc)
if auction_closed:
    st.warning("This auction has passed its closing time and can no longer accept bids.")
else:
    with st.form("bid_form", clear_on_submit=True):
        cargo_description = st.text_input("Cargo description")
        cargo_weight = st.number_input(
            f"Cargo quantity ({auction.capacity_unit})",
            min_value=0.0,
            max_value=float(auction.capacity_available),
            step=1.0,
        )
        bid_rate = st.number_input(
            f"Your bid rate ({auction.currency} per {auction.capacity_unit})",
            min_value=float(auction.base_rate),
            step=1.0,
        )
        submitted = st.form_submit_button("Submit bid")
        if submitted:
            if not cargo_description or cargo_weight <= 0:
                st.warning("Cargo description and a positive quantity are required.")
            else:
                with session_factory() as session:
                    bid = Bid(
                        auction_id=auction_id,
                        customer_id=profile.id,
                        cargo_description=cargo_description,
                        cargo_weight=cargo_weight,
                        bid_rate=bid_rate,
                    )
                    session.add(bid)
                    session.commit()
                st.success("Bid submitted. Track its status on the My Bids page.")
                st.rerun()
