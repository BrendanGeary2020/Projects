import { useEffect, useState } from "react";

import {
    getAccounts,
    makeDeposit,
    makeWithdrawal
} from "../services/api";


function MyAccounts() {

    // Temporary customer ID.
    // Later this will come from login.
    const customerId = 2;

    const [accounts, setAccounts] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    const [selectedAccount, setSelectedAccount] = useState(null);

    const [transactionType, setTransactionType] = useState(null);

    const [amount, setAmount] = useState("");

    const [processing, setProcessing] = useState(false);

    const [message, setMessage] = useState(null);


    async function loadAccounts() {

        try {

            const data = await getAccounts();

            const filteredAccounts = data.filter(
                (account) =>
                    Number(account.customer_id) ===
                    Number(customerId)
            );

            setAccounts(filteredAccounts);

        } catch (error) {

            console.error(error);

            setError("Failed to load accounts.");

        } finally {

            setLoading(false);

        }
    }


    useEffect(() => {

        loadAccounts();

    }, []);


    function openTransaction(account, type) {

        setSelectedAccount(account);

        setTransactionType(type);

        setAmount("");

        setMessage(null);

    }


    function closeTransaction() {

        setSelectedAccount(null);

        setTransactionType(null);

        setAmount("");

        setMessage(null);

    }


    async function handleTransactionSubmit(event) {

        event.preventDefault();

        const transactionAmount = Number(amount);


        // Frontend validation
        if (!transactionAmount || transactionAmount <= 0) {

            setMessage({
                type: "error",
                text: "Amount must be greater than $0."
            });

            return;
        }


        // Additional withdrawal check
        if (
            transactionType === "Withdraw" &&
            transactionAmount >
            Number(selectedAccount.balance)
        ) {

            setMessage({
                type: "error",
                text: "Insufficient funds."
            });

            return;
        }


        setProcessing(true);

        setMessage(null);


        try {

            if (transactionType === "Deposit") {

                await makeDeposit(
                    selectedAccount.id,
                    transactionAmount
                );

            } else if (transactionType === "Withdraw") {

                await makeWithdrawal(
                    selectedAccount.id,
                    transactionAmount
                );

            }


            setMessage({
                type: "success",
                text:
                    `${transactionType} of $${transactionAmount.toFixed(2)} successful.`
            });


            setAmount("");


            // Reload account balances.
            await loadAccounts();


            setSelectedAccount(null);

            setTransactionType(null);

        } catch (error) {

            console.error(error);

            setMessage({
                type: "error",
                text:
                    `Failed to ${transactionType.toLowerCase()}.`
            });

        } finally {

            setProcessing(false);

        }
    }


    if (loading) {

        return (
            <p>
                Loading accounts...
            </p>
        );

    }


    if (error) {

        return (
            <p>
                {error}
            </p>
        );

    }


    return (

        <div>

            <h1>
                My Accounts
            </h1>


            {message && (

                <div
                    style={{
                        marginBottom: "20px",
                        padding: "10px",
                        border: "1px solid #ccc",
                        borderRadius: "5px"
                    }}
                >

                    {message.text}

                </div>

            )}


            {accounts.length === 0 ? (

                <p>
                    No accounts found.
                </p>

            ) : (

                accounts.map((account) => (

                    <div
                        key={account.id}
                        style={{
                            border: "1px solid #ccc",
                            padding: "20px",
                            marginBottom: "20px",
                            borderRadius: "8px"
                        }}
                    >

                        <h2>
                            Account {account.id}
                        </h2>


                        <p>

                            <strong>
                                Account Type:
                            </strong>{" "}

                            {account.account_type}

                        </p>


                        <p>

                            <strong>
                                Current Balance:
                            </strong>{" "}

                            ${Number(account.balance).toFixed(2)}

                        </p>


                        <div
                            style={{
                                marginTop: "15px"
                            }}
                        >

                            <button
                                onClick={() =>
                                    openTransaction(
                                        account,
                                        "Deposit"
                                    )
                                }
                            >
                                Deposit
                            </button>


                            {" "}


                            <button
                                onClick={() =>
                                    openTransaction(
                                        account,
                                        "Withdraw"
                                    )
                                }
                            >
                                Withdraw
                            </button>

                        </div>


                        {selectedAccount?.id === account.id && (

                            <form
                                onSubmit={
                                    handleTransactionSubmit
                                }
                                style={{
                                    marginTop: "20px"
                                }}
                            >
                                <h3>
                                    {transactionType}
                                </h3>
                                
                                <label>

                                    Amount:{" "}

                                    <input
                                        type="number"
                                        min="0.01"
                                        step="0.01"
                                        value={amount}
                                        onChange={(event) =>
                                            setAmount(
                                                event.target.value
                                            )
                                        }
                                        required
                                        disabled={processing}
                                    />

                                </label>


                                <div
                                    style={{
                                        marginTop: "15px"
                                    }}
                                >

                                    <button
                                        type="submit"
                                        disabled={processing}
                                    >

                                        {processing
                                            ? "Processing..."
                                            : transactionType}

                                    </button>


                                    {" "}


                                    <button
                                        type="button"
                                        onClick={
                                            closeTransaction
                                        }
                                        disabled={processing}
                                    >
                                        Cancel
                                    </button>

                                </div>

                            </form>

                        )}

                    </div>

                ))

            )}

        </div>

    );

}


export default MyAccounts;