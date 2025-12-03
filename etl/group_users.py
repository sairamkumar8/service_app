#!/usr/bin/env python3
"""
etl/group_users.py

Reads users, employment_info, and user_bank_info from the DB, groups users by:
 - bank_name
 - company_name
 - pincode

Outputs CSV files into --output-dir (default: etl/output/) with timestamped filenames.

Usage:
  python etl/group_users.py --db-uri "postgresql+psycopg2://user:pass@host:5432/db" --output-dir etl/output/
"""

import os
import argparse
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# -----------------------
# Config & Logging
# -----------------------
load_dotenv()  # optional: loads DATABASE_URL from a .env file if present

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)

# -----------------------
# Helper functions
# -----------------------
def get_engine(db_uri: str):
    """Create and return SQLAlchemy engine."""
    logging.debug("Creating engine for DB URI: %s", db_uri)
    return create_engine(db_uri, echo=False, future=True)


def read_tables(engine):
    """
    Read the three tables into pandas DataFrames.
    Returns: df_users, df_emp, df_bank
    """
    logging.info("Reading tables from database...")
    with engine.connect() as conn:
        # Use safe SELECTs (read whole tables - small sample DB expected)
        df_users = pd.read_sql(text("SELECT id AS user_id, first_name, last_name, email, phone, address_line1, city, state, pincode, created_at FROM users"), conn)
        df_emp = pd.read_sql(text("SELECT id AS employment_id, user_id, company_name, designation, start_date, end_date, is_current FROM employment_info"), conn)
        df_bank = pd.read_sql(text("SELECT id AS bank_id, user_id, bank_name, account_number, ifsc, account_type FROM user_bank_info"), conn)

    logging.info("Rows fetched: users=%d, employment=%d, bank=%d", len(df_users), len(df_emp), len(df_bank))
    return df_users, df_emp, df_bank


def group_and_write(mapping_df, group_col, output_dir: Path, prefix: str):
    """
    mapping_df: DataFrame that has at least columns [group_col, user_id]
    group_col: the column to group by (string)
    output_dir: pathlib.Path where file will be written
    prefix: filename prefix (e.g. 'group_by_bank')
    """
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{prefix}_{ts}.csv"
    out_path = output_dir / filename

    logging.info("Grouping by %s and writing to %s", group_col, out_path)

    # For each group, compute unique user_ids and count
    grouped = (
        mapping_df[[group_col, "user_id"]]
        .dropna(subset=[group_col])            # ignore null keys
        .drop_duplicates()                     # avoid duplicate (group,user) rows
        .groupby(group_col)["user_id"]
        .apply(lambda ids: sorted({int(i) for i in ids}))  # sorted unique ints
        .reset_index(name="user_ids")
    )

    # Create user_count column and convert user_ids to comma-separated string
    grouped["user_count"] = grouped["user_ids"].apply(len)
    grouped["user_ids"] = grouped["user_ids"].apply(lambda ids: ",".join(map(str, ids)))

    # Reorder columns: group_key, user_count, user_ids
    grouped = grouped[[group_col, "user_count", "user_ids"]]
    grouped.rename(columns={group_col: "group_key"}, inplace=True)

    # Write CSV
    grouped.to_csv(out_path, index=False)
    logging.info("Wrote %d rows to %s", len(grouped), out_path)
    return out_path


# -----------------------
# Main ETL flow
# -----------------------
def main(argv=None):
    parser = argparse.ArgumentParser(description="Group users and export CSVs by bank, company, and pincode.")
    parser.add_argument("--db-uri", dest="db_uri", default=os.getenv("DATABASE_URL"),
                        help="Full SQLAlchemy DB URI (example: postgresql+psycopg2://user:pass@host:5432/db). If not provided, DATABASE_URL env var is used.")
    parser.add_argument("--output-dir", dest="output_dir", default="etl/output", help="Directory to write CSV files.")
    parser.add_argument("--no-timestamp", dest="no_timestamp", action="store_true", help="If set, do not include timestamp in filenames.")
    parser.add_argument("--verbose", action="store_true", help="Enable DEBUG logging.")
    args = parser.parse_args(argv)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.db_uri:
        logging.error("Database URI is not provided. Use --db-uri or set DATABASE_URL in environment.")
        return 2

    engine = None
    try:
        engine = get_engine(args.db_uri)
    except Exception as exc:
        logging.exception("Failed to create DB engine: %s", exc)
        return 3

    # Ensure output dir exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        df_users, df_emp, df_bank = read_tables(engine)

        # --------------------------
        # Group by bank_name
        # --------------------------
        # Merge users with bank table to get (bank_name, user_id)
        logging.debug("Merging users and bank info for bank grouping...")
        if not df_bank.empty:
            bank_map = pd.merge(df_bank[["user_id", "bank_name"]].drop_duplicates(), df_users[["user_id"]], on="user_id", how="inner")
            bank_out = group_and_write(bank_map, "bank_name", output_dir, "group_by_bank")
        else:
            logging.info("No bank records found; skipping bank grouping.")
            bank_out = None

        # --------------------------
        # Group by company_name
        # --------------------------
        logging.debug("Merging users and employment info for company grouping...")
        if not df_emp.empty:
            comp_map = pd.merge(df_emp[["user_id", "company_name"]].drop_duplicates(), df_users[["user_id"]], on="user_id", how="inner")
            comp_out = group_and_write(comp_map, "company_name", output_dir, "group_by_company")
        else:
            logging.info("No employment records found; skipping company grouping.")
            comp_out = None

        # --------------------------
        # Group by pincode
        # --------------------------
        logging.debug("Preparing pincode grouping...")
        if not df_users.empty:
            pin_map = df_users[["user_id", "pincode"]].drop_duplicates()
            pin_out = group_and_write(pin_map, "pincode", output_dir, "group_by_pincode")
        else:
            logging.info("No user records found; skipping pincode grouping.")
            pin_out = None

        logging.info("ETL completed. Files: %s, %s, %s", bank_out, comp_out, pin_out)
        return 0

    except SQLAlchemyError as sqle:
        logging.exception("Database error: %s", sqle)
        return 4
    except Exception as exc:
        logging.exception("Unexpected error: %s", exc)
        return 5
    finally:
        if engine:
            engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
