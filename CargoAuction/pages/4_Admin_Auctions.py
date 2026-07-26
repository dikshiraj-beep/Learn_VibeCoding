from datetime import datetime, time

import pandas as pd
import streamlit as st
from sqlalchemy import func, select

from auth import current_profile
from db import get_session_factory
from models import Bid, CargoAuction, Port, Profile, Vessel, VesselSchedule

st.title("Manage Auctions")

profile = current_profile()
session_factory = get_session_factory()

create_tab, manage_tab = st.tabs(["Create Auction", "Bids & Closing"])

with create_tab:
    with session_factory() as session:
        vessels = session.execute(select(Vessel).order_by(Vessel.name)).scalars().all()

    if not vessels:
        st.info("Add a vessel with a schedule first, on the Manage Vessels page.")
    else:
        vessel_choice = st.selectbox("Vessel", vessels, format_func=lambda v: v.name, key="auction_vessel")

        with session_factory() as session:
            schedule_rows = session.execute(
                select(VesselSchedule, Port)
                .join(Port, VesselSchedule.port_id == Port.id)
                .where(VesselSchedule.vessel_id == vessel_choice.id)
                .order_by(VesselSchedule.sequence)
            ).all()

        if len(schedule_rows) < 2:
            st.info("This vessel needs at least two port calls (load + discharge) in its schedule first.")
        else:
            port_options = {f"{p.name} (call #{s.sequence})": p.id for s, p in schedule_rows}
            with st.form("create_auction_form", clear_on_submit=True):
                load_label = st.selectbox("Load port", list(port_options.keys()), key="load_port")
                discharge_label = st.selectbox(
                    "Discharge port", list(port_options.keys()), index=len(port_options) - 1, key="discharge_port"
                )
                capacity_available = st.number_input("Space available", min_value=0.0, step=1.0)
                capacity_unit = st.selectbox("Unit", ["MT", "TEU", "CBM"])
                base_rate = st.number_input("Base rate (per unit)", min_value=0.0, step=1.0)
                currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR"])
                close_date = st.date_input("Auction closes on")
                close_time = st.time_input("Auction closes at", value=time(17, 0))
                submitted = st.form_submit_button("Create auction")
                if submitted:
                    if port_options[load_label] == port_options[discharge_label]:
                        st.warning("Load port and discharge port must be different.")
                    elif capacity_available <= 0 or base_rate <= 0:
                        st.warning("Space available and base rate must be greater than zero.")
                    else:
                        with session_factory() as session:
                            session.add(
                                CargoAuction(
                                    vessel_id=vessel_choice.id,
                                    load_port_id=port_options[load_label],
                                    discharge_port_id=port_options[discharge_label],
                                    capacity_available=capacity_available,
                                    capacity_unit=capacity_unit,
                                    base_rate=base_rate,
                                    currency=currency,
                                    auction_close_at=datetime.combine(close_date, close_time),
                                    created_by=profile.id,
                                )
                            )
                            session.commit()
                        st.success("Auction created.")
                        st.rerun()

with manage_tab:
    with session_factory() as session:
        auctions = session.execute(
            select(CargoAuction, Vessel)
            .join(Vessel, CargoAuction.vessel_id == Vessel.id)
            .order_by(CargoAuction.created_at.desc())
        ).all()

    if not auctions:
        st.info("No auctions created yet.")
        st.stop()

    auction_options = {f"#{a.id} — {v.name} ({a.status})": a.id for a, v in auctions}
    selected_label = st.selectbox("Select an auction", list(auction_options.keys()))
    auction_id = auction_options[selected_label]

    with session_factory() as session:
        auction = session.get(CargoAuction, auction_id)
        bids = session.execute(
            select(Bid, Profile)
            .join(Profile, Bid.customer_id == Profile.id)
            .where(Bid.auction_id == auction_id)
            .order_by(Bid.bid_rate.desc())
        ).all()

    st.write(f"Status: **{auction.status}** · Closes: **{auction.auction_close_at}**")

    if bids:
        bids_df = pd.DataFrame(
            [
                {
                    "Bidder": bidder.username,
                    "Company": bidder.company_name,
                    "Cargo": bid.cargo_description,
                    "Quantity": float(bid.cargo_weight),
                    "Bid rate": float(bid.bid_rate),
                    "Status": bid.status,
                    "Submitted": bid.bid_time,
                }
                for bid, bidder in bids
            ]
        )
        status_colors = {
            "pending": "background-color: #FFF3CD; color: #7A5B00;",
            "won": "background-color: #D4EDDA; color: #155724;",
            "lost": "background-color: #F8D7DA; color: #721C24;",
        }
        styled_bids = bids_df.style.map(lambda v: status_colors.get(v, ""), subset=["Status"])
        st.dataframe(styled_bids, use_container_width=True, hide_index=True)
    else:
        st.info("No bids submitted yet.")

    if auction.status == "open":
        if st.button("Close auction and select winner", type="primary", disabled=not bids):
            with session_factory() as session:
                winning_bid = session.execute(
                    select(Bid)
                    .where(Bid.auction_id == auction_id)
                    .order_by(Bid.bid_rate.desc())
                    .limit(1)
                ).scalar_one()
                session.execute(
                    Bid.__table__.update()
                    .where(Bid.auction_id == auction_id, Bid.id != winning_bid.id)
                    .values(status="lost")
                )
                winning_bid.status = "won"
                auction_obj = session.get(CargoAuction, auction_id)
                auction_obj.status = "closed"
                auction_obj.winning_bid_id = winning_bid.id
                session.commit()
            st.success("Auction closed. Winning bidder has been marked as won.")
            st.rerun()
    else:
        st.info("This auction is closed.")
