# pylint:disable=C0111,C0103

def get_average_purchase(db):
    # return the average amount spent per order for each customer ordered by customer ID
    query = """
    SELECT
        CustomerID,
        AVG(OrderAmount) AS AverageOrderedAmount
    FROM (
        SELECT
            o.CustomerID,
            o.OrderID,
            SUM(ROUND(od.UnitPrice * od.Quantity, 2)) AS OrderAmount
        FROM orders o
        JOIN orderdetails od ON od.OrderID = o.OrderID
        GROUP BY o.CustomerID, o.OrderID
    ) AS Subquery
    GROUP BY CustomerID
    ORDER BY CustomerID;
    """

    results = db.execute(query)
    results = results.fetchall()

    return results

def get_general_avg_order(db):
    # return the average amount spent per order
    query = """
    WITH TemporaryTableName AS (
        SELECT
            OrderID,
            SUM(UnitPrice * Quantity) AS ProductAmount
        FROM OrderDetails
        GROUP BY OrderID
    )
    SELECT AVG(ProductAmount) AS GeneralAvgOrder
    FROM TemporaryTableName;
    """

    result = db.execute(query)
    general_avg_order = result.fetchone()[0]

    return general_avg_order

def best_customers(db):
    # return the customers who have an average purchase greater than the general average purchase
    query = """
        WITH CustomerAvgOrders AS (
            SELECT
                c.customerid,
                ROUND(SUM(od.UnitPrice * od.Quantity) / COUNT(DISTINCT o.OrderID), 2) AS AverageOrderedAmount
            FROM
                customers c
            JOIN
                orders o ON o.customerid = c.customerid
            JOIN
                orderdetails od ON od.orderid = o.orderid
            GROUP BY
                o.customerid
        ),
        GeneralAverage AS (
            SELECT ROUND(SUM(od.UnitPrice * od.Quantity) / COUNT(DISTINCT o.OrderID), 2) AS GeneralAverageOrderedAmount
            FROM
                orders o
            JOIN
                orderdetails od ON od.orderid = o.orderid
        )
        SELECT
            cao.customerid,
            cao.AverageOrderedAmount
        FROM CustomerAvgOrders cao, GeneralAverage gao
        WHERE cao.AverageOrderedAmount > gao.GeneralAverageOrderedAmount
        ORDER BY cao.AverageOrderedAmount DESC
    """
    results = db.execute(query)
    results = results.fetchall()

    return results


def top_ordered_product_per_customer(db):
    # return the list of the top ordered product by each customer
    # based on the total ordered amount in USD
    query = """
        WITH OrderedProducts AS (
            SELECT
                CustomerID,
                ProductID, SUM(OrderDetails.Quantity * OrderDetails.UnitPrice) AS ProductValue
            FROM OrderDetails
            JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
            GROUP BY Orders.CustomerID, OrderDetails.ProductID
            ORDER BY ProductValue DESC
        ),
        ranks AS (
        SELECT
            OrderedProducts.CustomerID,
            OrderedProducts.ProductID,
            OrderedProducts.ProductValue,
            RANK() OVER(PARTITION BY OrderedProducts.CustomerID ORDER BY OrderedProducts.ProductValue DESC) as order_rank
            FROM OrderedProducts
            )
        SELECT ranks.CustomerID,ranks.ProductID, ranks.ProductValue
        from ranks
        WHERE order_rank = 1
        ORDER BY ranks.ProductValue DESC
    """
    results = db.execute(query)
    results = results.fetchall()

    return results


def average_number_of_days_between_orders(db):
    # return the average number of days between two consecutive orders of the same customer
    query = """
        WITH DatedOrders AS (
            SELECT
                CustomerID,
                OrderID,
                OrderDate,
                LAG(OrderDate, 1, 0) OVER (
                    PARTITION BY CustomerID
                    ORDER By OrderDate
                ) PreviousOrderDate
            FROM Orders
        )
        SELECT ROUND(AVG(JULIANDAY(OrderDate) - JULIANDAY(PreviousOrderDate))) AS delta
        FROM DatedOrders
        WHERE PreviousOrderDate != 0
    """
    return int(db.execute(query).fetchone()[0])
