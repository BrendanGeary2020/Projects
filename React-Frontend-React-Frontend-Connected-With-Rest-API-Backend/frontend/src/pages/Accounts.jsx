import { useEffect, useState } from "react";

import {
    getAccounts,
    addAccount,
    deleteAccount
} from "../services/api";


function Accounts() {

    const [accounts, setAccounts] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);


    // Balance filter

    const [balanceFilter, setBalanceFilter] =
        useState("");

    const [filterActive, setFilterActive] =
        useState(false);


    // Add account

    const [showAddAccount, setShowAddAccount] =
        useState(false);

    const [customerId, setCustomerId] =
        useState("");

    const [accountType, setAccountType] =
        useState("checking");

    const [startingBalance, setStartingBalance] =
        useState("");

    const [addingAccount, setAddingAccount] =
        useState(false);

    const [addAccountMessage, setAddAccountMessage] =
        useState(null);


    // Delete account

    const [deletingAccountId, setDeletingAccountId] =
        useState(null);

    const [deleteMessage, setDeleteMessage] =
        useState(null);


    // Load accounts

    async function loadAccounts() {

        try {

            const data = await getAccounts();

            console.log(
                "ACCOUNTS DATA:",
                data
            );

            setAccounts(data);

        } catch (error) {

            console.error(error);

            setError(
                "Failed to load accounts."
            );

        } finally {

            setLoading(false);

        }
    }


    useEffect(() => {

        loadAccounts();

    }, []);


    // Add account

    async function handleAddAccount(event) {

        event.preventDefault();


        console.log(
            "ADD ACCOUNT FORM:"
        );

        console.log(
            "Customer ID:",
            customerId
        );

        console.log(
            "Account Type:",
            accountType
        );

        console.log(
            "Starting Balance:",
            startingBalance
        );


        setAddingAccount(true);

        setAddAccountMessage(null);


        try {
            const newAccount = await addAccount(
                customerId,
                accountType,
                startingBalance
            );

            console.log("ADD ACCOUNT RESPONSE:", newAccount);

            // Backend handled the request normally,
            // but the customer already has this account type.
            if (newAccount.success === false) {
                setAddAccountMessage({
                    type: "error",
                    text: newAccount.message
                });

                return;
            }

            // Account was actually created.
            setAddAccountMessage({
                type: "success",
                text: `Account ${newAccount.id} successfully added.`
            });

            // Clear form
            setCustomerId("");
            setAccountType("checking");
            setStartingBalance("");

            // Reload accounts
            await loadAccounts();

        } catch (error) {
            console.error("ADD ACCOUNT FAILED:", error);

            setAddAccountMessage({
                type: "error",
                text: error.message || "Failed to add account."
            });
        }finally {

            setAddingAccount(false);

        }
    }


    // Delete account

    async function handleDeleteAccount(
        accountId
    ) {

        const confirmed =
            window.confirm(
                `Are you sure you want to delete Account ${accountId}?`
            );


        if (!confirmed) {

            return;

        }


        setDeletingAccountId(
            accountId
        );

        setDeleteMessage(null);


        try {

            await deleteAccount(
                accountId
            );


            setDeleteMessage({
                type: "success",
                text:
                    `Account ${accountId} deleted successfully.`
            });


            await loadAccounts();


        } catch (error) {

            console.error(
                "DELETE ACCOUNT FAILED:",
                error
            );


            setDeleteMessage({
                type: "error",
                text:
                    error.message ||
                    `Failed to delete Account ${accountId}.`
            });


        } finally {

            setDeletingAccountId(
                null
            );

        }
    }


    // Balance filter

    function applyFilter() {

        if (
            balanceFilter === ""
        ) {

            setFilterActive(
                false
            );

            return;

        }


        setFilterActive(
            true
        );

    }


    function clearFilter() {

        setBalanceFilter("");

        setFilterActive(
            false
        );

    }


    // Loading

    if (loading) {

        return (
            <p>
                Loading accounts...
            </p>
        );

    }


    // Error

    if (error) {

        return (
            <p>
                {error}
            </p>
        );

    }


    // Filter accounts

    const filterAmount =
        Number(balanceFilter);


    const displayedAccounts =
        filterActive &&
        balanceFilter !== ""
            ? accounts.filter(
                (account) =>
                    Number(
                        account.balance
                    ) > filterAmount
            )
            : accounts;


    return (

        <div>

            <h1>
                Accounts
            </h1>


            {/* ========================= */}
            {/* ADD ACCOUNT BUTTON */}
            {/* ========================= */}

            <button
                onClick={() => {

                    setShowAddAccount(
                        !showAddAccount
                    );

                    setAddAccountMessage(
                        null
                    );

                }}
            >

                {showAddAccount
                    ? "Cancel Add Account"
                    : "Add Account"}

            </button>


            {/* ========================= */}
            {/* ADD ACCOUNT FORM */}
            {/* ========================= */}

            {showAddAccount && (

                <form
                    onSubmit={
                        handleAddAccount
                    }
                    style={{
                        marginTop:
                            "20px",

                        marginBottom:
                            "30px",

                        padding:
                            "20px",

                        border:
                            "1px solid #ccc",

                        borderRadius:
                            "8px"
                    }}
                >

                    <h2>
                        Add Account
                    </h2>


                    {/* Customer ID */}

                    <div
                        style={{
                            marginBottom:
                                "10px"
                        }}
                    >

                        <label>

                            Customer ID:{" "}

                            <input
                                type="number"
                                min="1"
                                value={
                                    customerId
                                }
                                onChange={
                                    (event) =>
                                        setCustomerId(
                                            event.target.value
                                        )
                                }
                                required
                            />

                        </label>

                    </div>


                    {/* Account Type */}

                    <div
                        style={{
                            marginBottom:
                                "10px"
                        }}
                    >

                        <label>

                            Account Type:{" "}

                            <select
                                value={
                                    accountType
                                }
                                onChange={
                                    (event) =>
                                        setAccountType(
                                            event.target.value
                                        )
                                }
                            >

                                <option value="checking">
                                    Checking Account
                                </option>

                                <option value="savings">
                                    Savings Account
                                </option>

                            </select>

                        </label>

                    </div>


                    {/* Starting Balance */}

                    <div
                        style={{
                            marginBottom:
                                "15px"
                        }}
                    >

                        <label>

                            Starting Balance:{" "}

                            <input
                                type="number"
                                min="0"
                                step="0.01"
                                value={
                                    startingBalance
                                }
                                onChange={
                                    (event) =>
                                        setStartingBalance(
                                            event.target.value
                                        )
                                }
                                required
                            />

                        </label>

                    </div>


                    {/* Submit */}

                    <button
                        type="submit"
                        disabled={
                            addingAccount
                        }
                    >

                        {addingAccount
                            ? "Adding..."
                            : "Add Account"}

                    </button>


                    {/* Add message */}

                    {addAccountMessage && (

                        <p>

                            {
                                addAccountMessage.text
                            }

                        </p>

                    )}

                </form>

            )}


            {/* ========================= */}
            {/* BALANCE FILTER */}
            {/* ========================= */}

            <div
                style={{
                    marginTop:
                        "20px",

                    marginBottom:
                        "20px"
                }}
            >

                <label>

                    Show accounts with balance over:{" "}

                    <input
                        type="number"
                        min="0"
                        step="0.01"
                        value={
                            balanceFilter
                        }
                        onChange={
                            (event) =>
                                setBalanceFilter(
                                    event.target.value
                                )
                        }
                    />

                </label>


                {" "}


                <button
                    onClick={
                        applyFilter
                    }
                >
                    Check
                </button>


                {" "}


                <button
                    onClick={
                        clearFilter
                    }
                >
                    Show All
                </button>

            </div>


            {/* ========================= */}
            {/* DELETE MESSAGE */}
            {/* ========================= */}

            {deleteMessage && (

                <p>

                    {
                        deleteMessage.text
                    }

                </p>

            )}


            {/* ========================= */}
            {/* ACCOUNTS */}
            {/* ========================= */}

            {displayedAccounts.length === 0 ? (

                <p>
                    No accounts found.
                </p>

            ) : (

                displayedAccounts.map(
                    (account) => (

                        <div
                            key={
                                account.id
                            }
                            style={{
                                border:
                                    "1px solid #ccc",

                                padding:
                                    "15px",

                                marginBottom:
                                    "15px",

                                borderRadius:
                                    "8px"
                            }}
                        >

                            <strong>
                                Account ID:
                            </strong>{" "}

                            {
                                account.id
                            }

                            <br />


                            <strong>
                                Customer ID:
                            </strong>{" "}

                            {
                                account.customer_id
                            }

                            <br />


                            <strong>
                                Account Type:
                            </strong>{" "}

                            {
                                account.account_type
                            }

                            <br />


                            <strong>
                                Balance:
                            </strong>{" "}

                            $
                            {
                                Number(
                                    account.balance
                                ).toFixed(2)
                            }

                            <br />


                            {/* Delete */}

                            <button
                                onClick={() =>
                                    handleDeleteAccount(
                                        account.id
                                    )
                                }
                                disabled={
                                    deletingAccountId ===
                                    account.id
                                }
                                style={{
                                    marginTop:
                                        "10px"
                                }}
                            >

                                {
                                    deletingAccountId ===
                                    account.id
                                        ? "Deleting..."
                                        : "Delete Account"
                                }

                            </button>

                        </div>

                    )
                )

            )}

        </div>

    );

}


export default Accounts;
