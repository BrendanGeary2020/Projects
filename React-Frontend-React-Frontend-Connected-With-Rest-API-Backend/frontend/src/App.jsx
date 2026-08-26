import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";

import Navbar from "./components/Navbar";

import AdminDashboard from "./pages/AdminDashboard";
import CustomerDashboard from "./pages/CustomerDashboard";
import Customers from "./pages/Customers";
import Admins from "./pages/Admins";
import Accounts from "./pages/Accounts";
import MyAccounts from "./pages/MyAccounts";

function App() {

    return (
        <BrowserRouter>

            <Navbar />

            <Routes>

                <Route
                    path="/"
                    element={<AdminDashboard />}
                />

                <Route
                    path="/customer"
                    element={<CustomerDashboard />}
                />

                <Route
                    path="/customers"
                    element={<Customers />}
                />

                <Route
                    path="/admins"
                    element={<Admins />}
                />

                <Route
                    path="/accounts"
                    element={<Accounts />}
                />

                <Route
                    path="/my-accounts"
                    element={<MyAccounts />}
                />

            </Routes>

        </BrowserRouter>
    );
}


export default App;