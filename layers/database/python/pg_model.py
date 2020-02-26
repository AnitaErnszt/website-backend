import psycopg2.extras
from pgutils import pg_in_brackets, create_pg_conn


def get_cashback_transactions(user_id):
    conn = create_pg_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute(
            """
            SELECT
                *
            FROM
                cashback_transactions
            WHERE
                user_id = %s
            ORDER BY timestamp DESC
        """,
            (user_id,),
        )

        transactions = []
        for row in cur:
            transactions.append(
                {
                    "id": row["id"],
                    "timestamp": row["timestamp"],
                    "type": row["type"],
                    "reason": row["reason"],
                    "amount": row["amount"],
                    "currency": row["currency"],
                }
            )
    except Exception as e:
        cur.close()
        conn.close()
        raise
    else:
        cur.close()
        conn.close()
        return transactions


def get_savings_history(user_id):
    conn = create_pg_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute(
            """
            SELECT
                *
            FROM
                savings_history
            WHERE
                user_id = %s
            ORDER BY month DESC
        """,
            (user_id,),
        )

        history = []
        for row in cur:
            history.append(
                {
                    "month": row["month"],
                    "amount": row["amount"],
                    "currency": row["currency"],
                }
            )
    except Exception as e:
        cur.close()
        conn.close()
        raise
    else:
        cur.close()
        conn.close()
        return history


def get_savings_transactions(user_id):
    conn = create_pg_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute(
            """
            SELECT
                *
            FROM
                account_transactions
            WHERE
                user_id = %s
            ORDER BY timestamp DESC
        """,
            (user_id,),
        )

        transactions = []
        for row in cur:
            transactions.append(
                {
                    "id": row["id"],
                    "timestamp": row["timestamp"],
                    "type": row["type"],
                    "amount": row["amount"],
                    "currency": row["currency"],
                }
            )
    except Exception as e:
        cur.close()
        conn.close()
    else:
        cur.close()
        conn.close()
        return transactions
