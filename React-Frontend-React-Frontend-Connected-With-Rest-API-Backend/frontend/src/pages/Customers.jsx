import { useEffect, useState } from "react";

import { getCustomers } from "../services/api";


function Customers() {

    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    useEffect(() => {

        getCustomers()
            .then((data) => {
                setCustomers(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error(error);
                setError("Failed to load customers.");
                setLoading(false);
            });

    }, []);


    if (loading) {
        return <p>Loading customers...</p>;
    }


    if (error) {
        return <p>{error}</p>;
    }


    return (
        <div>

            <h1>Customers</h1>

            {customers.length === 0 ? (

                <p>No customers found.</p>

            ) : (

                <ul style={{ listStyleType: "none", padding: 0 }}>

                    {customers.map((customer) => (

                        <li key={customer.id} style={{ marginBottom: "15px" }}>
                            <strong>User ID:</strong> {customer.id}
                            <br />
                            <strong>Name:</strong> {customer.name}
                            <br />
                            <strong>Email:</strong> {customer.email}
                            <br />
                            <strong>Username:</strong> {customer.username}
                        </li>

                    ))}

                </ul>

            )}

        </div>
    );
}


export default Customers;