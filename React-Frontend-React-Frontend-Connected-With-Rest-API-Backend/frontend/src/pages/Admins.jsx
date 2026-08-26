import { useEffect, useState } from "react";

import { getAdmins } from "../services/api";


function Admins() {

    const [admins, setAdmins] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    useEffect(() => {

        getAdmins()
            .then((data) => {
                setAdmins(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error(error);
                setError("Failed to load admins.");
                setLoading(false);
            });

    }, []);


    if (loading) {
        return <p>Loading admins...</p>;
    }


    if (error) {
        return <p>{error}</p>;
    }


    return (
        <div>

            <h1>Admins</h1>

            {admins.length === 0 ? (

                <p>No admins found.</p>

            ) : (

                <ul style={{ listStyleType: "none", padding: 0 }}>

                    {admins.map((admin) => (

                        <li
                            key={admin.id}
                            style={{ marginBottom: "15px" }}
                        >

                            <strong>User ID:</strong> {admin.id}
                            <br />

                            <strong>Name:</strong> {admin.name}
                            <br />

                            <strong>Email:</strong> {admin.email}
                            <br />

                            <strong>Username:</strong> {admin.username}

                        </li>

                    ))}

                </ul>

            )}

        </div>
    );
}


export default Admins;