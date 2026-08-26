import { Link, useLocation } from "react-router-dom";


function Navbar() {

    const location = useLocation();

    const isCustomerArea =
        location.pathname === "/customer" ||
        location.pathname.startsWith("/my-accounts");


    if (isCustomerArea) {

        return (
            <nav>

                <Link to="/customer">
                    Customer Dashboard
                </Link>

                {" | "}

                <Link to="/my-accounts">
                    My Accounts
                </Link>

            </nav>
        );
    }


    return (
        <nav>

            <Link to="/">
                Admin Dashboard
            </Link>

            {" | "}

            <Link to="/customers">
                Customers
            </Link>

            {" | "}

            <Link to="/admins">
                Admins
            </Link>

            {" | "}

            <Link to="/accounts">
                Accounts
            </Link>

        </nav>
    );
}


export default Navbar;