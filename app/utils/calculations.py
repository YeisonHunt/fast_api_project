from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import calendar
from typing import Tuple, Dict, List
from app.models.models import Service, Consumption, Injection, Record, Tariff, XmDataHourlyPerAgent


def get_month_date_range(year: int, month: int) -> Tuple[datetime, datetime]:
    """Get the start and end dates for a specific month"""
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
    return first_day, last_day


def calculate_EA(db: Session, client_id: int, year: int, month: int) -> Tuple[float, float, float]:
    """Calculate EA (Active Energy)"""
    first_day, last_day = get_month_date_range(year, month)

    # Get service for the client
    service = db.query(Service).filter(Service.id_service == client_id).first()
    if not service:
        raise ValueError(f"Client with ID {client_id} not found")

    # Get sum of consumption
    total_consumption = db.query(func.sum(Consumption.value)).join(
        Record
    ).filter(
        Record.id_service == client_id,
        Record.record_timestamp >= first_day,
        Record.record_timestamp <= last_day
    ).scalar() or 0

    # Get tariff
    voltage_level = service.voltage_level
    cdi = service.cir if voltage_level not in [2, 3] else 0  # cdi doesn't matter if voltage_level is 2 or 3

    tariff = db.query(Tariff).filter(
        Tariff.id_market == service.id_market,
        Tariff.voltage_level == voltage_level
    )

    if voltage_level not in [2, 3]:
        tariff = tariff.filter(Tariff.cdi == cdi)

    tariff = tariff.first()

    if not tariff:
        raise ValueError("Tariff not found for the given service parameters")

    cu_rate = tariff.CU
    total_ea = total_consumption * cu_rate

    return total_consumption, cu_rate, total_ea


def calculate_EC(db: Session, client_id: int, year: int, month: int) -> Tuple[float, float, float]:
    """Calculate EC (Energy Excess Commercialization)"""
    first_day, last_day = get_month_date_range(year, month)

    # Get service for the client
    service = db.query(Service).filter(Service.id_service == client_id).first()
    if not service:
        raise ValueError(f"Client with ID {client_id} not found")

    # Get sum of injection
    total_injection = db.query(func.sum(Injection.value)).join(
        Record
    ).filter(
        Record.id_service == client_id,
        Record.record_timestamp >= first_day,
        Record.record_timestamp <= last_day
    ).scalar() or 0

    # Get tariff
    voltage_level = service.voltage_level
    cdi = service.cir if voltage_level not in [2, 3] else 0  # cdi doesn't matter if voltage_level is 2 or 3

    tariff = db.query(Tariff).filter(
        Tariff.id_market == service.id_market,
        Tariff.voltage_level == voltage_level
    )

    if voltage_level not in [2, 3]:
        tariff = tariff.filter(Tariff.cdi == cdi)

    tariff = tariff.first()

    if not tariff:
        raise ValueError("Tariff not found for the given service parameters")

    c_rate = tariff.C
    total_ec = total_injection * c_rate

    return total_injection, c_rate, total_ec


def calculate_EE1(db: Session, client_id: int, year: int, month: int) -> Tuple[float, float, float]:
    """Calculate EE1 (Energy Excess type 1)"""
    first_day, last_day = get_month_date_range(year, month)

    # Get service for the client
    service = db.query(Service).filter(Service.id_service == client_id).first()
    if not service:
        raise ValueError(f"Client with ID {client_id} not found")

    # Get sum of consumption and injection
    total_consumption = db.query(func.sum(Consumption.value)).join(
        Record
    ).filter(
        Record.id_service == client_id,
        Record.record_timestamp >= first_day,
        Record.record_timestamp <= last_day
    ).scalar() or 0

    total_injection = db.query(func.sum(Injection.value)).join(
        Record
    ).filter(
        Record.id_service == client_id,
        Record.record_timestamp >= first_day,
        Record.record_timestamp <= last_day
    ).scalar() or 0

    # Calculate EE1 quantity: min(total_injection, total_consumption)
    ee1_quantity = min(total_injection, total_consumption)

    # Get tariff
    voltage_level = service.voltage_level
    cdi = service.cir if voltage_level not in [2, 3] else 0  # cdi doesn't matter if voltage_level is 2 or 3

    tariff = db.query(Tariff).filter(
        Tariff.id_market == service.id_market,
        Tariff.voltage_level == voltage_level
    )

    if voltage_level not in [2, 3]:
        tariff = tariff.filter(Tariff.cdi == cdi)

    tariff = tariff.first()

    if not tariff:
        raise ValueError("Tariff not found for the given service parameters")

    # Tariff for EE1 is negative CU
    ee1_rate = -tariff.CU
    total_ee1 = ee1_quantity * ee1_rate

    return ee1_quantity, ee1_rate, total_ee1


def calculate_EE2(db: Session, client_id: int, year: int, month: int) -> Tuple[float, float, float]:
    """Calculate EE2 (Energy Excess type 2)"""
    first_day, last_day = get_month_date_range(year, month)

    # Get service for the client
    service = db.query(Service).filter(Service.id_service == client_id).first()
    if not service:
        raise ValueError(f"Client with ID {client_id} not found")

    # Get sum of consumption and injection
    total_consumption = db.query(func.sum(Consumption.value)).join(
        Record
    ).filter(
        Record.id_service == client_id,
        Record.record_timestamp >= first_day,
        Record.record_timestamp <= last_day
    ).scalar() or 0

    total_injection = db.query(func.sum(Injection.value)).join(
        Record
    ).filter(
        Record.id_service == client_id,
        Record.record_timestamp >= first_day,
        Record.record_timestamp <= last_day
    ).scalar() or 0

    # Calculate EE2 quantity
    ee2_quantity = 0
    ee2_rate = 0
    total_ee2 = 0

    # Only calculate EE2 if injection exceeds consumption
    if total_injection > total_consumption:
        ee2_quantity = total_injection - total_consumption

        # Get hourly injection and hourly consumption
        hourly_injections = {}
        hourly_consumptions = {}

        # Get all records with injection for the client in the given month
        injection_records = db.query(
            Record.record_timestamp,
            Injection.value
        ).join(
            Injection
        ).filter(
            Record.id_service == client_id,
            Record.record_timestamp >= first_day,
            Record.record_timestamp <= last_day
        ).all()

        # Get all records with consumption for the client in the given month
        consumption_records = db.query(
            Record.record_timestamp,
            Consumption.value
        ).join(
            Consumption
        ).filter(
            Record.id_service == client_id,
            Record.record_timestamp >= first_day,
            Record.record_timestamp <= last_day
        ).all()

        # Organize by hour
        for timestamp, value in injection_records:
            hour = timestamp.hour
            if hour not in hourly_injections:
                hourly_injections[hour] = 0
            hourly_injections[hour] += value

        for timestamp, value in consumption_records:
            hour = timestamp.hour
            if hour not in hourly_consumptions:
                hourly_consumptions[hour] = 0
            hourly_consumptions[hour] += value

        # Calculate excess by hour
        excess_by_hour = {}
        accumulated_injection = 0
        consumption_threshold = total_consumption

        # Sort hours for consistent processing
        sorted_hours = sorted(hourly_injections.keys())

        for hour in sorted_hours:
            injection_value = hourly_injections.get(hour, 0)
            accumulated_injection += injection_value

            # If we've exceeded the consumption threshold, record the excess
            if accumulated_injection > consumption_threshold:
                excess = min(injection_value, accumulated_injection - consumption_threshold)
                if excess > 0:
                    excess_by_hour[hour] = excess
                    consumption_threshold += excess  # Update threshold for next hour

        # Get hourly rates from xm_data_hourly_per_agent
        hourly_rates = {}
        for hour in excess_by_hour.keys():
            # Find the rate for this hour
            hour_start = datetime(year, month, 1, hour, 0, 0)
            hour_end = hour_start + timedelta(hours=1)

            rate = db.query(XmDataHourlyPerAgent.value).filter(
                XmDataHourlyPerAgent.record_timestamp >= hour_start,
                XmDataHourlyPerAgent.record_timestamp < hour_end
            ).first()

            hourly_rates[hour] = rate[0] if rate else 0

        # Calculate EE2 total
        hourly_totals = {}
        for hour, excess in excess_by_hour.items():
            hourly_totals[hour] = excess * hourly_rates[hour]

        total_ee2 = sum(hourly_totals.values())

        # Calculate average rate
        ee2_rate = total_ee2 / ee2_quantity if ee2_quantity > 0 else 0

    return ee2_quantity, ee2_rate, total_ee2


def calculate_all_concepts(db: Session, client_id: int, year: int, month: int) -> Dict:
    """Calculate all energy concepts for a client in a specific month"""
    ea_quantity, ea_rate, ea_total = calculate_EA(db, client_id, year, month)
    ec_quantity, ec_rate, ec_total = calculate_EC(db, client_id, year, month)
    ee1_quantity, ee1_rate, ee1_total = calculate_EE1(db, client_id, year, month)
    ee2_quantity, ee2_rate, ee2_total = calculate_EE2(db, client_id, year, month)

    total_invoice = ea_total + ec_total + ee1_total + ee2_total

    return {
        "client_id": client_id,
        "month": month,
        "year": year,
        "EA": {
            "quantity": ea_quantity,
            "tariff": ea_rate,
            "total": ea_total
        },
        "EC": {
            "quantity": ec_quantity,
            "tariff": ec_rate,
            "total": ec_total
        },
        "EE1": {
            "quantity": ee1_quantity,
            "tariff": ee1_rate,
            "total": ee1_total
        },
        "EE2": {
            "quantity": ee2_quantity,
            "tariff": ee2_rate,
            "total": ee2_total
        },
        "total": total_invoice
    }


def get_client_statistics(db: Session, client_id: int) -> Dict:
    """Get consumption and injection statistics for a client"""
    # Get all records for the client
    records = db.query(
        func.extract('year', Record.record_timestamp).label('year'),
        func.extract('month', Record.record_timestamp).label('month'),
        func.sum(Consumption.value).label('consumption'),
        func.sum(Injection.value).label('injection')
    ).outerjoin(
        Consumption, Record.id_record == Consumption.id_record
    ).outerjoin(
        Injection, Record.id_record == Injection.id_record
    ).filter(
        Record.id_service == client_id
    ).group_by(
        func.extract('year', Record.record_timestamp),
        func.extract('month', Record.record_timestamp)
    ).all()

    monthly_stats = []
    total_consumption = 0
    total_injection = 0
    months_count = 0

    for year, month, consumption, injection in records:
        consumption = consumption or 0
        injection = injection or 0
        net = consumption - injection

        monthly_stats.append({
            "month": int(month),
            "year": int(year),
            "consumption": consumption,
            "injection": injection,
            "net": net
        })

        total_consumption += consumption
        total_injection += injection
        months_count += 1

    avg_consumption = total_consumption / months_count if months_count > 0 else 0
    avg_injection = total_injection / months_count if months_count > 0 else 0
    avg_net = (total_consumption - total_injection) / months_count if months_count > 0 else 0

    return {
        "client_id": client_id,
        "monthly_statistics": monthly_stats,
        "average_consumption": avg_consumption,
        "average_injection": avg_injection,
        "average_net": avg_net
    }


def get_system_load(db: Session, date: datetime) -> Dict:
    """Get system load by hour for a specific date"""
    start_date = datetime(date.year, date.month, date.day, 0, 0, 0)
    end_date = datetime(date.year, date.month, date.day, 23, 59, 59)

    # Get hourly consumption for the system
    hourly_loads = db.query(
        func.extract('hour', Record.record_timestamp).label('hour'),
        func.sum(Consumption.value).label('load')
    ).join(
        Consumption
    ).filter(
        Record.record_timestamp >= start_date,
        Record.record_timestamp <= end_date
    ).group_by(
        func.extract('hour', Record.record_timestamp)
    ).all()

    return {
        "date": date,
        "hourly_loads": [
            {"hour": int(hour), "load": load} for hour, load in hourly_loads
        ]
    }