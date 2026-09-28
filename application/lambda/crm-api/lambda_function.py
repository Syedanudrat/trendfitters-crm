import json
import os

import psycopg


def get_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
    )


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method")
        path = event.get("rawPath", "")

        connection = get_connection()

        with connection.cursor() as cursor:

            # PUT /customers/{id}
            if method == "PUT" and path.startswith("/customers/"):
                customer_id = event.get("pathParameters", {}).get("id")

                if not customer_id:
                    connection.close()

                    return response(400, {
                        "error": "Customer ID is required"
                    })

                body = json.loads(event.get("body") or "{}")

                first_name = body.get("first_name")
                last_name = body.get("last_name")
                email = body.get("email")
                phone = body.get("phone")
                company = body.get("company")

                if not first_name:
                    connection.close()

                    return response(400, {
                        "error": "first_name is required"
                    })

                cursor.execute(
                    """
                    UPDATE customers
                    SET
                        first_name = %s,
                        last_name = %s,
                        email = %s,
                        phone = %s,
                        company = %s
                    WHERE id = %s
                    RETURNING id;
                    """,
                    (
                        first_name,
                        last_name,
                        email,
                        phone,
                        company,
                        customer_id
                    )
                )

                updated_customer = cursor.fetchone()

                if not updated_customer:
                    connection.close()

                    return response(404, {
                        "error": "Customer not found"
                    })

                connection.commit()
                connection.close()

                return response(200, {
                    "message": "Customer updated successfully",
                    "customer_id": updated_customer[0]
                })
            
            # DELETE /customers/{id}
            if method == "DELETE" and path.startswith("/customers/"):
                customer_id = event.get("pathParameters", {}).get("id")

                if not customer_id:
                    connection.close()

                    return response(400, {
                        "error": "Customer ID is required"
                    })

                cursor.execute(
                    """
                    DELETE FROM customers
                    WHERE id = %s
                    RETURNING id;
                    """,
                    (customer_id,)
                )

                deleted_customer = cursor.fetchone()

                if not deleted_customer:
                    connection.close()

                    return response(404, {
                        "error": "Customer not found"
                    })

                connection.commit()
                connection.close()

                return response(200, {
                    "message": "Customer deleted successfully",
                    "customer_id": deleted_customer[0]
                })

            # GET /customers/{id}
            if method == "GET" and path.startswith("/customers/"):
                customer_id = event.get("pathParameters", {}).get("id")

                if not customer_id:
                    connection.close()

                    return response(400, {
                        "error": "Customer ID is required"
                    })

                cursor.execute(
                    """
                    SELECT id, first_name, last_name, email, phone, company, created_at
                    FROM customers
                    WHERE id = %s;
                    """,
                    (customer_id,)
                )

                row = cursor.fetchone()

                connection.close()

                if not row:
                    return response(404, {
                        "error": "Customer not found"
                    })

                return response(200, {
                    "id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "company": row[5],
                    "created_at": row[6].isoformat() if row[6] else None
                })
            
            # GET /customers
            if method == "GET" and path == "/customers":
                cursor.execute(
                    """
                    SELECT id, first_name, last_name, email, phone, company, created_at
                    FROM customers
                    ORDER BY id;
                    """
                )

                rows = cursor.fetchall()

                customers = [
                    {
                        "id": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "email": row[3],
                        "phone": row[4],
                        "company": row[5],
                        "created_at": row[6].isoformat() if row[6] else None
                    }
                    for row in rows
                ]

                connection.close()

                return response(200, {
                    "customers": customers
                })

            # POST /customers
            if method == "POST" and path == "/customers":
                body = json.loads(event.get("body") or "{}")

                first_name = body.get("first_name")
                last_name = body.get("last_name")
                email = body.get("email")
                phone = body.get("phone")
                company = body.get("company")

                if not first_name:
                    connection.close()

                    return response(400, {
                        "error": "first_name is required"
                    })

                cursor.execute(
                    """
                    INSERT INTO customers
                        (first_name, last_name, email, phone, company)
                    VALUES
                        (%s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (first_name, last_name, email, phone, company)
                )

                customer_id = cursor.fetchone()[0]

                connection.commit()
                connection.close()

                return response(201, {
                    "message": "Customer created successfully",
                    "customer_id": customer_id
                })

        connection.close()

        return response(404, {
            "error": "Route not found"
        })

    except Exception as error:
        return response(500, {
            "message": "Database operation failed",
            "error": str(error)
        })