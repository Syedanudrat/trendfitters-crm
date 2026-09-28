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

            # Create leads table if it does not exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100),
                    email VARCHAR(255),
                    phone VARCHAR(50),
                    company VARCHAR(255),
                    source VARCHAR(100),
                    status VARCHAR(50) DEFAULT 'new',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            connection.commit()

            # GET /leads
            if method == "GET" and path == "/leads":
                cursor.execute(
                    """
                    SELECT id, first_name, last_name, email, phone, company,
                        source, status, created_at
                    FROM leads
                    ORDER BY id;
                    """
                )

                rows = cursor.fetchall()

                leads = [
                    {
                        "id": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "email": row[3],
                        "phone": row[4],
                        "company": row[5],
                        "source": row[6],
                        "status": row[7],
                        "created_at": row[8].isoformat() if row[8] else None
                    }
                    for row in rows
                ]

                connection.close()

                return response(200, {
                    "leads": leads
                })

            # Create opportunities table if it does not exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS opportunities (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    customer_id INTEGER,
                    amount NUMERIC(12,2),
                    stage VARCHAR(100) DEFAULT 'prospecting',
                    probability INTEGER DEFAULT 0,
                    expected_close_date DATE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            connection.commit()

            # Create orders table if it does not exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER,
                    opportunity_id INTEGER,
                    order_number VARCHAR(100) UNIQUE NOT NULL,
                    total_amount NUMERIC(12,2),
                    status VARCHAR(50) DEFAULT 'pending',
                    order_date DATE DEFAULT CURRENT_DATE,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            connection.commit()

            # POST /opportunities
            if method == "POST" and path == "/opportunities":
                body = json.loads(event.get("body") or "{}")

                name = body.get("name")
                customer_id = body.get("customer_id")
                amount = body.get("amount")
                stage = body.get("stage", "prospecting")
                probability = body.get("probability", 0)
                expected_close_date = body.get("expected_close_date")
                description = body.get("description")

                if not name:
                    connection.close()

                    return response(400, {
                        "error": "name is required"
                    })

                cursor.execute(
                    """
                    INSERT INTO opportunities
                        (
                            name,
                            customer_id,
                            amount,
                            stage,
                            probability,
                            expected_close_date,
                            description
                        )
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        name,
                        customer_id,
                        amount,
                        stage,
                        probability,
                        expected_close_date,
                        description
                    )
                )

                opportunity_id = cursor.fetchone()[0]

                connection.commit()
                connection.close()

                return response(201, {
                    "message": "Opportunity created successfully",
                    "opportunity_id": opportunity_id
                })

                        # POST /orders
            if method == "POST" and path == "/orders":
                body = json.loads(event.get("body") or "{}")

                customer_id = body.get("customer_id")
                opportunity_id = body.get("opportunity_id")
                order_number = body.get("order_number")
                total_amount = body.get("total_amount")
                status = body.get("status", "pending")
                order_date = body.get("order_date")
                notes = body.get("notes")

                if not order_number:
                    connection.close()

                    return response(400, {
                        "error": "order_number is required"
                    })

                cursor.execute(
                    """
                    INSERT INTO orders
                        (
                            customer_id,
                            opportunity_id,
                            order_number,
                            total_amount,
                            status,
                            order_date,
                            notes
                        )
                    VALUES
                        (%s, %s, %s, %s, %s, COALESCE(%s, CURRENT_DATE), %s)
                    RETURNING id;
                    """,
                    (
                        customer_id,
                        opportunity_id,
                        order_number,
                        total_amount,
                        status,
                        order_date,
                        notes
                    )
                )

                order_id = cursor.fetchone()[0]

                connection.commit()
                connection.close()

                return response(201, {
                    "message": "Order created successfully",
                    "order_id": order_id
                })

                        # GET /orders
            if method == "GET" and path == "/orders":
                cursor.execute(
                    """
                    SELECT
                        id,
                        customer_id,
                        opportunity_id,
                        order_number,
                        total_amount,
                        status,
                        order_date,
                        notes,
                        created_at
                    FROM orders
                    ORDER BY id;
                    """
                )

                rows = cursor.fetchall()

                orders = [
                    {
                        "id": row[0],
                        "customer_id": row[1],
                        "opportunity_id": row[2],
                        "order_number": row[3],
                        "total_amount": float(row[4]) if row[4] is not None else None,
                        "status": row[5],
                        "order_date": row[6].isoformat() if row[6] else None,
                        "notes": row[7],
                        "created_at": row[8].isoformat() if row[8] else None
                    }
                    for row in rows
                ]

                connection.close()

                return response(200, {
                    "orders": orders
                })

                        # GET /opportunities
            if method == "GET" and path == "/opportunities":
                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        customer_id,
                        amount,
                        stage,
                        probability,
                        expected_close_date,
                        description,
                        created_at
                    FROM opportunities
                    ORDER BY id;
                    """
                )

                rows = cursor.fetchall()

                opportunities = [
                    {
                        "id": row[0],
                        "name": row[1],
                        "customer_id": row[2],
                        "amount": float(row[3]) if row[3] is not None else None,
                        "stage": row[4],
                        "probability": row[5],
                        "expected_close_date": row[6].isoformat() if row[6] else None,
                        "description": row[7],
                        "created_at": row[8].isoformat() if row[8] else None
                    }
                    for row in rows
                ]

                connection.close()

                return response(200, {
                    "opportunities": opportunities
                })

                        # Create contacts table if it does not exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100),
                    email VARCHAR(255),
                    phone VARCHAR(50),
                    job_title VARCHAR(150),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            connection.commit()

            # POST /contacts
            if method == "POST" and path == "/contacts":
                body = json.loads(event.get("body") or "{}")

                customer_id = body.get("customer_id")
                first_name = body.get("first_name")
                last_name = body.get("last_name")
                email = body.get("email")
                phone = body.get("phone")
                job_title = body.get("job_title")

                if not customer_id:
                    connection.close()
                    return response(400, {
                        "error": "customer_id is required"
                    })

                if not first_name:
                    connection.close()
                    return response(400, {
                        "error": "first_name is required"
                    })

                cursor.execute(
                    """
                    INSERT INTO contacts
                        (customer_id, first_name, last_name, email, phone, job_title)
                    VALUES
                        (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        customer_id,
                        first_name,
                        last_name,
                        email,
                        phone,
                        job_title
                    )
                )

                contact_id = cursor.fetchone()[0]

                connection.commit()
                connection.close()

                return response(201, {
                    "message": "Contact created successfully",
                    "contact_id": contact_id
                })

            # GET /contacts
            if method == "GET" and path == "/contacts":
                cursor.execute(
                    """
                    SELECT
                        id,
                        customer_id,
                        first_name,
                        last_name,
                        email,
                        phone,
                        job_title,
                        created_at
                    FROM contacts
                    ORDER BY id;
                    """
                )

                rows = cursor.fetchall()

                contacts = [
                    {
                        "id": row[0],
                        "customer_id": row[1],
                        "first_name": row[2],
                        "last_name": row[3],
                        "email": row[4],
                        "phone": row[5],
                        "job_title": row[6],
                        "created_at": row[7].isoformat() if row[7] else None
                    }
                    for row in rows
                ]

                connection.close()

                return response(200, {
                    "contacts": contacts
                })

                        # Create customer history table if it does not exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS customer_history (
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER NOT NULL,
                    activity_type VARCHAR(100) NOT NULL,
                    description TEXT,
                    activity_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

                        # Create tasks table if it does not exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    status VARCHAR(50) DEFAULT 'pending',
                    priority VARCHAR(50) DEFAULT 'medium',
                    due_date DATE,
                    assigned_to VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            connection.commit()

            connection.commit()

                        # POST /tasks
            if method == "POST" and path == "/tasks":
                body = json.loads(event.get("body") or "{}")

                customer_id = body.get("customer_id")
                title = body.get("title")
                description = body.get("description")
                status = body.get("status", "pending")
                priority = body.get("priority", "medium")
                due_date = body.get("due_date")
                assigned_to = body.get("assigned_to")

                if not title:
                    connection.close()

                    return response(400, {
                        "error": "title is required"
                    })

                cursor.execute(
                    """
                    INSERT INTO tasks
                        (customer_id, title, description, status, priority, due_date, assigned_to)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        customer_id,
                        title,
                        description,
                        status,
                        priority,
                        due_date,
                        assigned_to
                    )
                )

                task_id = cursor.fetchone()[0]

                connection.commit()
                connection.close()

                return response(201, {
                    "message": "Task created successfully",
                    "task_id": task_id
                })

            # GET /tasks
            if method == "GET" and path == "/tasks":
                cursor.execute(
                    """
                    SELECT
                        id,
                        customer_id,
                        title,
                        description,
                        status,
                        priority,
                        due_date,
                        assigned_to,
                        created_at
                    FROM tasks
                    ORDER BY id;
                    """
                )

                rows = cursor.fetchall()

                tasks = [
                    {
                        "id": row[0],
                        "customer_id": row[1],
                        "title": row[2],
                        "description": row[3],
                        "status": row[4],
                        "priority": row[5],
                        "due_date": row[6].isoformat() if row[6] else None,
                        "assigned_to": row[7],
                        "created_at": row[8].isoformat() if row[8] else None
                    }
                    for row in rows
                ]

                connection.close()

                return response(200, {
                    "tasks": tasks
                })

            # POST /customer-history
            if method == "POST" and path == "/customer-history":
                body = json.loads(event.get("body") or "{}")

                customer_id = body.get("customer_id")
                activity_type = body.get("activity_type")
                description = body.get("description")

                if not customer_id:
                    connection.close()

                    return response(400, {
                        "error": "customer_id is required"
                    })

                if not activity_type:
                    connection.close()

                    return response(400, {
                        "error": "activity_type is required"
                    })

                cursor.execute(
                    """
                    INSERT INTO customer_history
                        (customer_id, activity_type, description)
                    VALUES
                        (%s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        customer_id,
                        activity_type,
                        description
                    )
                )

                history_id = cursor.fetchone()[0]

                connection.commit()
                connection.close()

                return response(201, {
                    "message": "Customer history created successfully",
                    "history_id": history_id
                })

            # GET /customer-history
            if method == "GET" and path == "/customer-history":
                cursor.execute(
                    """
                    SELECT
                        id,
                        customer_id,
                        activity_type,
                        description,
                        activity_date,
                        created_at
                    FROM customer_history
                    ORDER BY id;
                    """
                )

                rows = cursor.fetchall()

                history = [
                    {
                        "id": row[0],
                        "customer_id": row[1],
                        "activity_type": row[2],
                        "description": row[3],
                        "activity_date": row[4].isoformat() if row[4] else None,
                        "created_at": row[5].isoformat() if row[5] else None
                    }
                    for row in rows
                ]

                connection.close()

                return response(200, {
                    "history": history
                })

            # POST /leads
            if method == "POST" and path == "/leads":
                body = json.loads(event.get("body") or "{}")

                first_name = body.get("first_name")
                last_name = body.get("last_name")
                email = body.get("email")
                phone = body.get("phone")
                company = body.get("company")
                source = body.get("source")
                status = body.get("status", "new")

                if not first_name:
                    connection.close()

                    return response(400, {
                        "error": "first_name is required"
                    })

                cursor.execute(
                    """
                    INSERT INTO leads
                        (first_name, last_name, email, phone, company, source, status)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        first_name,
                        last_name,
                        email,
                        phone,
                        company,
                        source,
                        status
                    )
                )

                lead_id = cursor.fetchone()[0]

                connection.commit()
                connection.close()

                return response(201, {
                    "message": "Lead created successfully",
                    "lead_id": lead_id
                })

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
                    (
                        first_name,
                        last_name,
                        email,
                        phone,
                        company
                    )
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