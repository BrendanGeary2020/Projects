function AdminDashboard() {

    return (
        <div>

            <h1>Admin Dashboard</h1>

            <p>
                Welcome to the Digital Bank administration system.
            </p>

            <h2>Management</h2>

            <ul style={{ listStyleType: "none", padding: 0 }}>

                <li>
                    <a href="/customers">
                        Manage Customers
                    </a>
                </li>

                <li>
                    <a href="/admins">
                        Manage Admins
                    </a>
                </li>

                <li>
                    <a href="/accounts">
                        Manage Accounts
                    </a>
                </li>

            </ul>

        </div>
    );
}

export default AdminDashboard;