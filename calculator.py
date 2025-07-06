import os
import sys
import readchar  # Make sure to install this: pip install readchar


def calculate_mortgage_payment(principal, annual_interest_rate, loan_term_years):
    """
    Calculates the monthly mortgage payment.

    Args:
        principal (float): The total amount of money borrowed.
        annual_interest_rate (float): The annual interest rate (e.g., 0.045 for 4.5%).
        loan_term_years (int): The loan term in years (e.g., 25 for 25 years).

    Returns:
        float: The calculated monthly mortgage payment.
        str: An error message if the inputs are invalid.
    """
    if principal <= 0:
        return "Error: Principal must be a positive number."
    if annual_interest_rate < 0:
        return "Error: Annual interest rate cannot be negative."
    if loan_term_years <= 0:
        return "Error: Loan term in years must be a positive integer."

    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = annual_interest_rate / 12

    # Calculate total number of payments
    total_payments = loan_term_years * 12

    # Handle the special case where interest rate is 0
    if monthly_interest_rate == 0:
        return principal / total_payments

    # Apply the mortgage payment formula
    # M = P [ i(1 + i)^n ] / [ (1 + i)^n – 1]

    # Calculate (1 + i)^n
    power_of_i = (1 + monthly_interest_rate) ** total_payments

    # Calculate the numerator and denominator
    numerator = monthly_interest_rate * power_of_i
    denominator = power_of_i - 1

    # Calculate the monthly payment
    monthly_payment = principal * (numerator / denominator)

    return monthly_payment


def calculate_loan_amount(monthly_payment, annual_interest_rate, loan_term_years):
    """
    Calculates the maximum loan amount based on desired monthly payment,
    interest rate, and loan term.

    Args:
        monthly_payment (float): The desired monthly payment.
        annual_interest_rate (float): The annual interest rate (e.g., 0.045 for 4.5%).
        loan_term_years (int): The loan term in years (e.g., 25 for 25 years).

    Returns:
        float: The calculated maximum loan amount.
        str: An error message if the inputs are invalid.
    """
    if monthly_payment <= 0:
        return "Error: Monthly payment must be a positive number."
    if annual_interest_rate < 0:
        return "Error: Annual interest rate cannot be negative."
    if loan_term_years <= 0:
        return "Error: Loan term in years must be a positive integer."

    monthly_interest_rate = annual_interest_rate / 12
    total_payments = loan_term_years * 12

    if monthly_interest_rate == 0:
        return monthly_payment * total_payments

    # Rearrange the mortgage payment formula to solve for Principal (P)
    # P = M * [ (1 + i)^n – 1 ] / [ i(1 + i)^n ]

    power_of_i = (1 + monthly_interest_rate) ** total_payments

    numerator = power_of_i - 1
    denominator = monthly_interest_rate * power_of_i

    principal_amount = monthly_payment * (numerator / denominator)

    return principal_amount


def clear_screen():
    """Clears the console screen."""
    # 'cls' for Windows, 'clear' for Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu_and_get_selection(options, prompt_text="What would you like to do?"):
    """
    Displays a selectable menu and returns the index of the selected option.
    Allows navigation with arrow keys and selection with Enter/Space.
    Returns -1 if the user presses ESC or Ctrl+C.
    """

    selected_index = 0
    num_options = len(options)

    while True:
        clear_screen()
        print("-----------------------------------------")
        print("   Mortgage Monthly Repayment Calculator ")
        print("-----------------------------------------")
        print(prompt_text)
        print("\nUse ↑↓ arrow keys to navigate, Space/Enter to select. (Press ESC or Ctrl+C to quit)\n")

        for i, option in enumerate(options):
            if i == selected_index:
                print(f"> [{i + 1}] {option} <")  # Highlight selected option
            else:
                print(f"  [{i + 1}] {option}")

        # Read a single key press without waiting for Enter
        key = readchar.readkey()

        # Using match/case for key press handling (Python 3.10+)
        match key:
            case readchar.key.UP:
                selected_index = (selected_index - 1) % num_options
            case readchar.key.DOWN:
                selected_index = (selected_index + 1) % num_options
            case readchar.key.ENTER | ' ':  # Enter or Space to select
                return selected_index
            case readchar.key.ESC | readchar.key.CTRL_C:  # Allow exiting with Esc or Ctrl+C
                return -1  # Indicate exit
            case _:  # Default case for any other key press (do nothing)
                pass


def run_mortgage_calculator_app():
    """
    Runs the mortgage calculator as a console application with selectable options.
    """
    while True:
        menu_options = [
            "Calculate Monthly Mortgage Payment (M)",
            "Calculate Affordable House Price (P)",
            "Exit"
        ]

        selected_choice_index = display_menu_and_get_selection(menu_options)

        if selected_choice_index == -1 or menu_options[selected_choice_index].lower() == "exit":
            clear_screen()
            print("\nThank you for using the Mortgage Calculator!")
            break

        elif selected_choice_index == 0:
            clear_screen()
            print("-----------------------------------------")
            print("   Calculate Monthly Mortgage Payment    ")
            print("-----------------------------------------")
            try:
                principal_str = input(
                    "\nEnter the principal loan amount (e.g., 200000): £")
                principal = float(principal_str)

                annual_rate_str = input(
                    "Enter the annual interest rate (e.g., 4.5 for 4.5%): ")
                # Convert percentage to decimal
                annual_rate = float(annual_rate_str) / 100

                term_years_str = input(
                    "Enter the loan term in years (e.g., 25): ")
                term_years = int(term_years_str)

                monthly_payment = calculate_mortgage_payment(
                    principal, annual_rate, term_years)

                if isinstance(monthly_payment, float):
                    print(f"\n--- Calculation Result ---")
                    print(f"Loan Amount:             £{principal:,.2f}")
                    print(f"Annual Interest Rate:    {annual_rate * 100:.2f}%")
                    print(f"Loan Term:               {term_years} years")
                    print(f"-----------------------------------")
                    print(
                        f"Estimated Monthly Payment: £{monthly_payment:,.2f}")
                    print(f"-----------------------------------\n")
                else:
                    # Display error message from the calculation function
                    print(f"\nError: {monthly_payment}\n")

            except ValueError:
                print(
                    "\nInvalid input. Please enter valid numbers for the amounts, rates, and years.\n")
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}\n")

            # Pause before returning to menu
            input("Press Enter to return to the main menu...")

        # "Calculate Mortgage Loan Amount (P)"
        elif selected_choice_index == 1:
            clear_screen()
            print("-----------------------------------------")
            print("   Calculate Affordable House Price (P)    ")
            print("-----------------------------------------")
            try:
                monthly_payment_str = input(
                    "\nEnter your desired monthly payment (e.g., 1110.00): £")
                monthly_payment = float(monthly_payment_str)

                deposit_str = input("How much deposit do you have?")
                deposit_amount = float(deposit_str) if deposit_str else 0.0

                annual_rate_str = input(
                    "Enter the annual interest rate (e.g., 4.5 for 4.5%): ")
                # Convert percentage to decimal
                annual_rate = float(annual_rate_str) / 100

                term_years_str = input(
                    "Enter the loan term in years (e.g., 25): ")
                term_years = int(term_years_str)

                principal_amount = calculate_loan_amount(
                    monthly_payment, annual_rate, term_years)

                if (isinstance(principal_amount, float)):
                    deposit_percentage = (
                        deposit_amount / (principal_amount +
                                          deposit_amount) * 100)
                else:
                    deposit_percentage = -1

                if isinstance(principal_amount, float):
                    print(f"\n--- Calculation Result ---")
                    print(f"Desired Monthly Payment: £{monthly_payment:,.2f}")
                    print(f"Annual Interest Rate:    {annual_rate * 100:.2f}%")
                    print(f"Loan Term:               {term_years} years")
                    print(f"Deposit Amount:          £{deposit_amount:,.2f}")
                    print(
                        f"Deposit Percentage:      {deposit_percentage:,.2f}%")
                    print(f"-----------------------------------")

                    if (deposit_percentage < float(10)):
                        print(
                            "You may not be granted a mortgage as your LTV ratio is more than 90%")
                        print(f"-----------------------------------")
                    print(
                        f"Estimated House Price Could Afford (inc deposit): £{principal_amount + deposit_amount:,.2f}")
                    print(f"Consisting of Deposit: £{deposit_amount:,.2f}")
                    print(
                        f"Total House Price (affordable): £{principal_amount:,.2f}")
                    print(f"-----------------------------------\n")
                else:
                    print(f"\nError: {principal_amount}\n")

            except ValueError:
                print(
                    "\nInvalid input. Please enter valid numbers for the amounts, rates, and years.\n")
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}\n")

            # Pause before returning to menu
            input("Press Enter to return to the main menu...")

        else:
            # This case should ideally not be reached if display_menu_and_get_selection works correctly
            # and handles all valid selections. Included for robustness.
            clear_screen()
            print("\nInvalid selection. Please try again.\n")
            input("Press Enter to return to the main menu...")


# --- Run the console application ---
if __name__ == "__main__":
    # Check if readchar is installed before running the app
    try:
        import readchar
    except ImportError:
        print("The 'readchar' library is required for interactive menu selection.")
        print("Please install it using: pip install readchar")
        sys.exit(1)  # Exit the script if the library is not found

    run_mortgage_calculator_app()
