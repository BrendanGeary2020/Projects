function CustomerDashboard() {

    return (
        <div>

            <h1>Customer Dashboard</h1>

            <p>
                Welcome to your Digital Bank account.
            </p>

            <h2>My Banking</h2>

            <ul style={{ listStyleType: "none", padding: 0 }}>

                <li>
                    <a href="/my-accounts">
                        My Accounts
                    </a>
                </li>

            </ul>

        </div>
    );
}


export default CustomerDashboard;