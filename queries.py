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
    FROM
            orders o
    JOIN
            orderdetails od ON od.OrderID = o.OrderID
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
    pass  # YOUR CODE HERE

def best_customers(db):
    # return the customers who have an average purchase greater than the general average purchase
    pass  # YOUR CODE HERE

def top_ordered_product_per_customer(db):
    # return the list of the top ordered product by each customer
    # based on the total ordered amount in USD
    pass  # YOUR CODE HERE

def average_number_of_days_between_orders(db):
    # return the average number of days between two consecutive orders of the same customer
    pass  # YOUR CODE HERE
