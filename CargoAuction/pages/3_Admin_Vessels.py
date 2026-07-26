from datetime import datetime, time

import pandas as pd
import streamlit as st
from sqlalchemy import select

from db import get_session_factory
from models import Port, Vessel, VesselSchedule

st.title("Manage Vessels")

session_factory = get_session_factory()

port_tab, vessel_tab, schedule_tab = st.tabs(["Ports", "Vessels", "Vessel Schedule"])

with port_tab:
    st.subheader("Add a port")
    with st.form("add_port_form", clear_on_submit=True):
        name = st.text_input("Port name")
        country = st.text_input("Country")
        if st.form_submit_button("Add port"):
            if not name:
                st.warning("Port name is required.")
            else:
                with session_factory() as session:
                    session.add(Port(name=name, country=country))
                    session.commit()
                st.success(f"Port '{name}' added.")
                st.rerun()

    with session_factory() as session:
        ports = session.execute(select(Port).order_by(Port.name)).scalars().all()
    st.dataframe(
        pd.DataFrame([{"ID": p.id, "Name": p.name, "Country": p.country} for p in ports]),
        use_container_width=True,
        hide_index=True,
    )

with vessel_tab:
    st.subheader("Add a vessel")
    with st.form("add_vessel_form", clear_on_submit=True):
        vessel_name = st.text_input("Vessel name")
        if st.form_submit_button("Add vessel"):
            if not vessel_name:
                st.warning("Vessel name is required.")
            else:
                with session_factory() as session:
                    session.add(Vessel(name=vessel_name))
                    session.commit()
                st.success(f"Vessel '{vessel_name}' added.")
                st.rerun()

    with session_factory() as session:
        vessels = session.execute(select(Vessel).order_by(Vessel.name)).scalars().all()
    st.dataframe(
        pd.DataFrame([{"ID": v.id, "Name": v.name, "Status": v.status} for v in vessels]),
        use_container_width=True,
        hide_index=True,
    )

with schedule_tab:
    st.subheader("Add a port call to a vessel's route")
    with session_factory() as session:
        vessels = session.execute(select(Vessel).order_by(Vessel.name)).scalars().all()
        ports = session.execute(select(Port).order_by(Port.name)).scalars().all()

    if not vessels or not ports:
        st.info("Add at least one vessel and one port first.")
    else:
        vessel_choice = st.selectbox("Vessel", vessels, format_func=lambda v: v.name, key="schedule_vessel")

        with st.form("add_schedule_form", clear_on_submit=True):
            port_choice = st.selectbox("Port", ports, format_func=lambda p: p.name)
            sequence = st.number_input("Call sequence (1 = first port of call)", min_value=1, step=1)
            eta_date = st.date_input("ETA date")
            eta_time = st.time_input("ETA time", value=time(0, 0))
            if st.form_submit_button("Add port call"):
                with session_factory() as session:
                    session.add(
                        VesselSchedule(
                            vessel_id=vessel_choice.id,
                            port_id=port_choice.id,
                            sequence=int(sequence),
                            eta=datetime.combine(eta_date, eta_time),
                        )
                    )
                    session.commit()
                st.success("Port call added.")
                st.rerun()

        with session_factory() as session:
            schedule_rows = session.execute(
                select(VesselSchedule, Port)
                .join(Port, VesselSchedule.port_id == Port.id)
                .where(VesselSchedule.vessel_id == vessel_choice.id)
                .order_by(VesselSchedule.sequence)
            ).all()
        st.dataframe(
            pd.DataFrame(
                [{"Sequence": s.sequence, "Port": p.name, "ETA": s.eta} for s, p in schedule_rows]
            ),
            use_container_width=True,
            hide_index=True,
        )
