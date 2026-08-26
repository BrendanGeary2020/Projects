const API_BASE_URL = "http://127.0.0.1:8000";

// This part above will likely need to be changed
// on the deployed version.
///////////////////////////////////////////////////////////////////////////////

export async function getCustomers() {

    const response = await fetch(
        `${API_BASE_URL}/customers/`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch customers");
    }

    return response.json();
}


export async function getAdmins() {

    const response = await fetch(
        `${API_BASE_URL}/admins/`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch admins");
    }

    return response.json();
}


export async function getAccounts() {

    const response = await fetch(
        `${API_BASE_URL}/accounts/`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch accounts");
    }

    return response.json();
}


export async function addAccount(
    customerId,
    accountType,
    startingBalance
) {
    const response = await fetch(
        `${API_BASE_URL}/accounts/`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                customer_id: Number(customerId),
                account_type: accountType,
                balance: Number(startingBalance)
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        // console.error(
        //     "ADD ACCOUNT ERROR:",
        //     data
        // );

        throw new Error(
            data.detail || "Failed to add account."
        );
    }

    return data;
}


export async function deleteAccount(accountId) {

    const response = await fetch(
        `${API_BASE_URL}/accounts/${accountId}`,
        {
            method: "DELETE"
        }
    );


    if (!response.ok) {
        throw new Error("Failed to delete account");
    }


    return response.json();
}


export async function makeDeposit(
    accountId,
    amount
) {

    const response = await fetch(
        `${API_BASE_URL}/accounts/${accountId}/deposit`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                amount: Number(amount)
            })
        }
    );


    if (!response.ok) {
        throw new Error("Failed to make deposit");
    }


    return response.json();
}


export async function makeWithdrawal(
    accountId,
    amount
) {

    const response = await fetch(
        `${API_BASE_URL}/accounts/${accountId}/withdraw`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                amount: Number(amount)
            })
        }
    );


    if (!response.ok) {
        throw new Error("Failed to make withdrawal");
    }


    return response.json();
}