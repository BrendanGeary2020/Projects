

using System;
using System.Collections.Generic;

class BankApp
{
    static int customerID = 1;

    static List<Customer> customers = new List<Customer>();
    static List<Admin> admins = new List<Admin>();
    static List<User> users = new List<User>();

    static void Main(string[] args)
    {
        // Initialize users
        User u1 = new User("BillyBankAccount", "digitalSnail12345");
        User u2 = new User("SaraBanking", "MewAndMewTwo2000");
        User u3 = new User("DanMoney", "ProGamerAtCandyCrush247");

        User u4 = new User("admin", "AdminAtDigitalBank2026Secure");

        users.Add(u1);
        users.Add(u2);
        users.Add(u3);

        // Initialize customers
        Customer c1 = new Customer(
            customerID++,
            "Billy",
            new List<Account>(),
            u1.Username,
            u1.Password
        );

        Customer c2 = new Customer(
            customerID++,
            "Sara",
            new List<Account>(),
            u2.Username,
            u2.Password
        );

        Customer c3 = new Customer(
            customerID++,
            "Dan",
            new List<Account>(),
            u3.Username,
            u3.Password
        );

        customers.Add(c1);
        customers.Add(c2);
        customers.Add(c3);

        // Initialize example accounts
        CheckingAccount billyChecking = new CheckingAccount();
        billyChecking.Id = 1;
        billyChecking.Balance = 15;

        CheckingAccount saraChecking = new CheckingAccount();
        saraChecking.Id = 2;
        saraChecking.Balance = 1000;

        SavingsAccount saraSavings = new SavingsAccount();
        saraSavings.Id = 3;
        saraSavings.Balance = 15000;

        SavingsAccount danSavings = new SavingsAccount();
        danSavings.Id = 4;
        danSavings.Balance = 250;

        // Add accounts to customers

        c1.Accounts.Add(billyChecking);
        c2.Accounts.Add(saraChecking);
        c2.Accounts.Add(saraSavings);
        c3.Accounts.Add(danSavings);

        // Initialize admins
        Admin a1 = new Admin(
            u4.Username,
            u4.Password
        );

        admins.Add(a1);

        // Main flow
        Welcome();

        string loginResult = Login();

        if (loginResult == "validation_failed")
        {
            Console.WriteLine("Validation Failed");
        }
        else if (loginResult == "admin")
        {
            AdminDashboard();
        }
        else
        {
            CustomerDashboard(loginResult);
        }
    }

    static void Welcome()
    {
        Console.WriteLine();
        Console.WriteLine("Welcome to Digital Bank!");
    }

   static string Login()
    {
        Console.WriteLine();
        Console.WriteLine(
            "Please enter your username, then enter a space, then enter your password:"
        );
        while (true)
        {
            string input = Console.ReadLine();

            // Allow user to quit
            if (input.Equals("quit", StringComparison.OrdinalIgnoreCase) ||
                input.Equals("exit", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("Have a good day, and thank you for choosing Digital Bank!\n");
                Environment.Exit(0);
            }

            // Split the input by spaces
            string[] usernamePassword = input.Split(
                ' ',
                StringSplitOptions.RemoveEmptyEntries
            );

            // Must have exactly 2 entries:
            // username + password
            if (usernamePassword.Length != 2)
            {
                Console.WriteLine(
                    "\nValidation failed! Please try again or Type 'quit' or 'exit' to close the application."
                );
                Console.WriteLine(
                    "Please enter your username, then enter a space, then enter your password:"
                );

                continue;
            }

            string username = usernamePassword[0];
            string password = usernamePassword[1];

            // Admin login
            foreach (Admin admin in admins)
            {
                if (admin.Username == username &&
                    admin.Password == password)
                {
                    return "admin";
                }
            }

            // Customer login
            foreach (User user in users)
            {
                if (user.Username == username &&
                    user.Password == password)
                {
                    return user.Username;
                }
            }

            // Username/password did not match
            Console.WriteLine(
                "Validation failed. Please try again."
            );
        }
    }

    static void CustomerDashboard(string loginResult)
    {
        Console.WriteLine();
        Console.WriteLine("Welcome customer, " + loginResult);

        // Find the logged-in customer
        Customer loggedInCustomer = null;

        foreach (Customer customer in customers)
        {
            if (customer.Username == loginResult)
            {
                loggedInCustomer = customer;
                break;
            }
        }

        if (loggedInCustomer == null)
        {
            Console.WriteLine("Customer not found.");
            return;
        }

        bool running = true;

        while (running)
        {
            Console.WriteLine();
            Console.WriteLine("Customer Menu");
            Console.WriteLine("1. See account(s)");
            Console.WriteLine("2. Deposit");
            Console.WriteLine("3. Withdraw");
            Console.WriteLine("4. Logout");
            Console.Write("Please select an option: ");

            string choice = Console.ReadLine();

            switch (choice)
            {
                case "1":
                    // See all accounts belonging to this customer
                    if (loggedInCustomer.Accounts.Count == 0)
                    {
                        Console.WriteLine("You do not have any accounts.");
                    }
                    else
                    {
                        Console.WriteLine("Your Accounts:");

                        foreach (Account account in loggedInCustomer.Accounts)
                        {
                            if (account is CheckingAccount)
                            {
                                Console.WriteLine(
                                    "Account ID: " + account.Id +
                                    " | Type: Checking Account" +
                                    " | Balance: $" + account.Balance
                                );
                            }
                            else if (account is SavingsAccount)
                            {
                                Console.WriteLine(
                                    "Account ID: " + account.Id +
                                    " | Type: Savings Account" +
                                    " | Balance: $" + account.Balance
                                );
                            }
                        }
                    }
                    break;
                case "2":
                // Deposit
                if (loggedInCustomer.Accounts.Count == 0)
                {
                    Console.WriteLine("You do not have any accounts.");
                    break;
                }

                Console.WriteLine("\nDeposit");

                Console.Write("Enter Account ID: ");

                int depositAccountId;

                if (!int.TryParse(Console.ReadLine(), out depositAccountId))
                {
                    Console.WriteLine("Invalid Account ID.");
                    break;
                }

                Account depositAccount = null;

                foreach (Account account in loggedInCustomer.Accounts)
                {
                    if (account.Id == depositAccountId)
                    {
                        depositAccount = account;
                        break;
                    }
                }

                if (depositAccount == null)
                {
                    Console.WriteLine("Account not found.");
                    break;
                }

                Console.Write("Enter deposit amount: ");

                double depositAmount;

                if (!double.TryParse(Console.ReadLine(), out depositAmount))
                {
                    Console.WriteLine("Invalid deposit amount.");
                    break;
                }

                if (depositAmount <= 0)
                {
                    Console.WriteLine("Deposit amount must be greater than zero.");
                    break;
                }

                double depositBeforeBalance = depositAccount.Balance;

                depositAccount.Balance += depositAmount;

                double depositAfterBalance = depositAccount.Balance;

                Console.WriteLine();
                Console.WriteLine("Deposit successful.");
                Console.WriteLine("Before Balance: $" + depositBeforeBalance);
                Console.WriteLine("Deposit Amount: $" + depositAmount);
                Console.WriteLine("After Balance: $" + depositAfterBalance);

                break;


            case "3":
                // Withdraw
                if (loggedInCustomer.Accounts.Count == 0)
                {
                    Console.WriteLine("You do not have any accounts.");
                    break;
                }

                Console.WriteLine("\nWithdraw");

                Console.Write("Enter Account ID: ");

                int withdrawAccountId;

                if (!int.TryParse(Console.ReadLine(), out withdrawAccountId))
                {
                    Console.WriteLine("Invalid Account ID.");
                    break;
                }

                Account withdrawAccount = null;

                foreach (Account account in loggedInCustomer.Accounts)
                {
                    if (account.Id == withdrawAccountId)
                    {
                        withdrawAccount = account;
                        break;
                    }
                }

                if (withdrawAccount == null)
                {
                    Console.WriteLine("Account not found.");
                    break;
                }

                Console.Write("Enter withdrawal amount: ");

                double withdrawalAmount;

                if (!double.TryParse(Console.ReadLine(), out withdrawalAmount))
                {
                    Console.WriteLine("Invalid withdrawal amount.");
                    break;
                }

                if (withdrawalAmount <= 0)
                {
                    Console.WriteLine("Withdrawal amount must be greater than zero.");
                    break;
                }

                if (withdrawalAmount > withdrawAccount.Balance)
                {
                    Console.WriteLine("Insufficient funds.");
                    Console.WriteLine("Current Balance: $" + withdrawAccount.Balance);
                    break;
                }

                double withdrawBeforeBalance = withdrawAccount.Balance;

                withdrawAccount.Balance -= withdrawalAmount;

                double withdrawAfterBalance = withdrawAccount.Balance;

                Console.WriteLine();
                Console.WriteLine("Withdrawal successful.");
                Console.WriteLine("Before Balance: $" + withdrawBeforeBalance);
                Console.WriteLine("Withdrawal Amount: $" + withdrawalAmount);
                Console.WriteLine("After Balance: $" + withdrawAfterBalance);

                break;

                
                case "4":
                    Console.WriteLine("Logging out...");
                    Console.WriteLine("Have a good day, and thank you for choosing Digital Bank!\n");
                    running = false;
                    break;

                default:
                    Console.WriteLine("Invalid option. Please try again.");
                    break;
            }
        }
    }


    static void AdminDashboard()
    {
        Console.WriteLine("Welcome Admin");

        bool running = true;

        // Account ID counter
        int accountID = 1;

        while (running)
        {
            Console.WriteLine();
            Console.WriteLine("Admin Menu");
            Console.WriteLine("1. See all customers");
            Console.WriteLine("2. See all accounts");
            Console.WriteLine("3. Add account");
            //Console.WriteLine("4. Add interest to savings account"); // comment out if interest should show for all accounts types
            Console.WriteLine("4. Add interest to account"); // comment out if interest should only show for savings accounts
            Console.WriteLine("5. Delete any account");
            Console.WriteLine("6. Logout");
            Console.Write("Please select an option: ");

            string choice = Console.ReadLine();

            switch (choice)
            {
                case "1":
                    // See all customers
                    Console.WriteLine();
                    Console.WriteLine("All Customers:");

                    foreach (Customer customer in customers)
                    {
                        Console.WriteLine(customer);
                    }
                    break;

                case "2":
                    // See all accounts
                    Console.WriteLine();
                    Console.WriteLine("All Accounts:");

                    bool accountsExist = false;

                    foreach (Customer customer in customers)
                    {
                        foreach (Account account in customer.Accounts)
                        {
                            accountsExist = true;

                            string accountType = "";

                            if (account is CheckingAccount)
                            {
                                accountType = "Checking Account";
                            }
                            else if (account is SavingsAccount)
                            {
                                accountType = "Savings Account";
                            }

                            Console.WriteLine(
                                "Account ID: " + account.Id +
                                " | Customer: " + customer.Name +
                                " | Username: " + customer.Username +
                                " | Type: " + accountType +
                                " | Balance: $" + account.Balance
                            );
                        }
                    }

                    if (!accountsExist)
                    {
                        Console.WriteLine("There are no accounts.");
                    }
                    break;

                case "3":
                    // Add account
                    Console.WriteLine();
                    Console.WriteLine("Add Account");

                    Console.Write("Enter Customer ID: ");

                    int customerId;

                    if (!int.TryParse(Console.ReadLine(), out customerId))
                    {
                        Console.WriteLine("Invalid Customer ID.");
                        break;
                    }

                    Customer selectedCustomer = null;

                    foreach (Customer customer in customers)
                    {
                        if (customer.Id == customerId)
                        {
                            selectedCustomer = customer;
                            break;
                        }
                    }

                    if (selectedCustomer == null)
                    {
                        Console.WriteLine("Customer not found.");
                        break;
                    }

                    Console.WriteLine("1. Checking Account");
                    Console.WriteLine("2. Savings Account");
                    Console.Write("Select account type: ");

                    string accountChoice = Console.ReadLine();

                    bool accountAlreadyExists = false;

                    foreach (Account account in selectedCustomer.Accounts)
                    {
                        if (accountChoice == "1" && account is CheckingAccount)
                        {
                            accountAlreadyExists = true;
                            break;
                        }

                        if (accountChoice == "2" && account is SavingsAccount)
                        {
                            accountAlreadyExists = true;
                            break;
                        }
                    }

                    if (accountAlreadyExists)
                    {
                        Console.WriteLine(
                            "This customer already has this type of account."
                        );

                        break;
                    }

                    Console.Write("Enter starting balance: ");

                    double startingBalance;

                    if (!double.TryParse(Console.ReadLine(), out startingBalance))
                    {
                        Console.WriteLine("Invalid balance.");
                        break;
                    }

                    Account newAccount = null;

                    if (accountChoice == "1")
                    {
                        newAccount = new CheckingAccount();
                    }
                    else if (accountChoice == "2")
                    {
                        newAccount = new SavingsAccount();
                    }
                    else
                    {
                        Console.WriteLine("Invalid account type.");
                        break;
                    }

                    newAccount.Id = accountID++;
                    newAccount.Balance = startingBalance;

                    selectedCustomer.Accounts.Add(newAccount);

                    Console.WriteLine("Account successfully added.");
                    Console.WriteLine("Account ID: " + newAccount.Id);
                    break;
                case "4":
                    // only have start message be for for all account types or just savings accounts, Commentout one of the two

                    // Add interest to a Savings Account
                    //Console.WriteLine("\nAdd Interest to Savings Account");

                    //Message incase both account types are preferred to recieve interest
                    Console.WriteLine("\nAdd Interest to Account");

                    Console.Write("Enter Account ID: ");

                    int interestAccountId;

                    if (!int.TryParse(Console.ReadLine(), out interestAccountId))
                    {
                        Console.WriteLine("Invalid Account ID.");
                        break;
                    }

                    Account interestAccount = null;
                    Customer accountOwner = null;

                    // Find the account
                    foreach (Customer customer in customers)
                    {
                        foreach (Account account in customer.Accounts)
                        {
                            if (account.Id == interestAccountId)
                            {
                                interestAccount = account;
                                accountOwner = customer;
                                break;
                            }
                        }

                        if (interestAccount != null)
                        {
                            break;
                        }
                    }

                    if (interestAccount == null)
                    {
                        Console.WriteLine("Account not found.");
                    }
                    // comment out or portion of if both account types is preferred to receive interest
                    // for example,
                    // else if (interestAccount is SavingsAccount) // || interestAccount is CheckingAccount)
                    else if (interestAccount is SavingsAccount || interestAccount is CheckingAccount)
                    {
                        double oldBalance = interestAccount.Balance;

                        double newBalance = interestAccount.AddInterest();

                        Console.WriteLine(
                            "Interest added successfully to " +
                            accountOwner.Name + "'s Savings Account."
                        );

                        Console.WriteLine("Old Balance: $" + oldBalance);
                        Console.WriteLine("New Balance: $" + newBalance);
                    }
                    else
                    {
                        Console.WriteLine(
                            "Interest can only be added to Checking Accounts!"
                        );
                    }
                    

                    break;
                case "5":
                    // Delete any account
                    Console.WriteLine();
                    Console.WriteLine("Delete Account");

                    Console.Write("Enter Account ID to delete: ");

                    int deleteAccountId;

                    if (!int.TryParse(Console.ReadLine(), out deleteAccountId))
                    {
                        Console.WriteLine("Invalid Account ID.");
                        break;
                    }

                    bool accountDeleted = false;

                    foreach (Customer customer in customers)
                    {
                        Account accountToDelete = null;

                        foreach (Account account in customer.Accounts)
                        {
                            if (account.Id == deleteAccountId)
                            {
                                accountToDelete = account;
                                break;
                            }
                        }

                        if (accountToDelete != null)
                        {
                            customer.Accounts.Remove(accountToDelete);

                            Console.WriteLine(
                                "Account " + deleteAccountId +
                                " deleted successfully."
                            );

                            accountDeleted = true;
                            break;
                        }
                    }

                    if (!accountDeleted)
                    {
                        Console.WriteLine("Account not found.");
                    }

                    break;

                case "6":
                    Console.WriteLine("Logging out...");
                    Console.WriteLine("Have a good day, and thank you for choosing Digital Bank!\n");
                    running = false;
                    break;

                default:
                    Console.WriteLine("Invalid option. Please try again.");
                    break;
            }
        }
    }
}


// User - Abstract Parent class for Customer and Admin
class User
{
    public string Username { get; set; }
    public string Password { get; set; }

    public User(string username, string password)
    {
        Username = username;
        Password = password;
    }
}


// Customer
class Customer : User
{
    public int Id { get; set; }
    public string Name { get; set; }

    public List<Account> Accounts { get; set; }

    public Customer(
        int id,
        string name,
        List<Account> accounts,
        string username,
        string password)
        : base(username, password)
    {
        Id = id;
        Name = name;
        Accounts = accounts;
    }

    public override string ToString()
    {
        return $"Customer {{ Id = {Id}, Name = {Name}, Username = {Username}, Accounts = {Accounts.Count} }}";
    }
}


// Admin

class Admin : User
{
    public int Id { get; set; }

    public Admin(string username, string password)
        : base(username, password)
    {
    }
}


// Account - abstract clasee for CheckingAccount and Savings Account
abstract class Account
{
    public int Id { get; set; }
    public double Balance { get; set; }

    public abstract double AddInterest();
}


// Checking Account
class CheckingAccount : Account
{
    public string AccountType { get; set; } = "CheckingAccount";

    // interest for checking accounts, but if not needed/desired can uncomment bellow code and readd the admin call that blocks adding
    // interest to checking accounts
    public override double AddInterest()
    {
        // Add 2% to current balance

        Balance = Balance + (Balance * 0.02);

        return Balance;
    }
}


// Savings Account
class SavingsAccount : Account
{
    public string AccountType { get; set; } = "SavingsAccount";

    public override double AddInterest()
    {
        // Add 3% to current balance

        Balance = Balance + (Balance * 0.03);

        return Balance;
    }
}