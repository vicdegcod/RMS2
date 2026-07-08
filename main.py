# ==========================================
# REHABILITATION MANAGEMENT SYSTEM
# main.py (Part 1)
# ==========================================

# -------- IMPORT MODULES --------

from auth import login, logout, change_password

from client import (
    add_client,
    view_clients,
    update_client,
    delete_client,
    view_progress
)

from therapist import (
    add_therapist,
    view_therapists,
    update_therapist,
    delete_therapist
)

from appointment import (
    book_appointment,
    view_appointments,
    cancel_appointment,
    complete_appointment,
    delete_appointment
)

from notes import (
    add_note,
    view_notes,
    search_notes,
    update_note,
    delete_note,
    export_notes_csv,
    count_notes
)

from database import close_database


# ==========================================
# MENU FUNCTIONS
# (Implemented in Part 2 and Part 3)
# ==========================================

# ==========================================
# THERAPIST MENU
# ==========================================

def therapist_menu(user):

    while True:

        print("\n")
        print("=" * 50)
        print("             THERAPIST MENU")
        print("=" * 50)
        print("1. View Clients")
        print("2. View Therapists")
        print("3. Book Appointment")
        print("4. View Appointments")
        print("5. Cancel Appointment")
        print("6. Complete Appointment")
        print("7. Add Therapy Note")
        print("8. View Therapy Notes")
        print("9. Search Therapy Notes")
        print("10. Export Therapy Notes to CSV")
        print("11. Count Therapy Notes")
        print("12. View Client Progress")
        print("13. Change Password")
        print("14. Logout")
        print("=" * 50)

        choice = input("Enter your choice: ")

        # ---------- CLIENTS ----------

        if choice == "1":
            view_clients()

        # ---------- THERAPISTS ----------

        elif choice == "2":
            view_therapists()

        # ---------- APPOINTMENTS ----------

        elif choice == "3":
            book_appointment()

        elif choice == "4":
            view_appointments()

        elif choice == "5":
            cancel_appointment()

        elif choice == "6":
            complete_appointment()

        # ---------- THERAPY NOTES ----------

        elif choice == "7":
            add_note()

        elif choice == "8":
            view_notes()

        elif choice == "9":
            search_notes()

        elif choice == "10":
            export_notes_csv()

        elif choice == "11":
            count_notes()

        # ---------- CLIENT PROGRESS ----------

        elif choice == "12":
            view_progress()

        # ---------- PASSWORD ----------

        elif choice == "13":
            change_password(user)

        # ---------- LOGOUT ----------

        elif choice == "14":

            logout()

            break

        else:
            print("Invalid choice. Please try again.")


def therapist_menu(user):
    pass


# ==========================================
# MAIN PROGRAM
# ==========================================

# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    while True:

        try:

            print("\n")
            print("=" * 55)
            print("     REHABILITATION MANAGEMENT SYSTEM")
            print("=" * 55)
            print("1. Login")
            print("2. Exit")
            print("=" * 55)

            choice = input("Enter your choice: ").strip()

            if choice == "1":

                user = login()

                if user is None:
                    continue

                if user["role"] == "Admin":
                    admin_menu(user)

                elif user["role"] == "Therapist":
                    therapist_menu(user)

                else:
                    print("Unknown user role.")

            elif choice == "2":

                print("\nSaving database...")

                close_database()

                print("Thank you for using the Rehabilitation Management System.")
                print("Goodbye!")

                break

            else:

                print("Invalid choice. Please enter 1 or 2.")

        except KeyboardInterrupt:

            print("\n\nProgram interrupted by user.")
            close_database()
            break

        except Exception as error:

            print("\nAn unexpected error occurred.")
            print("Error:", error)


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":
    main()

# ==========================================
# ADMIN MENU
# ==========================================

def admin_menu(user):

    while True:

        print("\n")
        print("=" * 50)
        print("               ADMIN MENU")
        print("=" * 50)
        print("1.  Add Client")
        print("2.  View Clients")
        print("3.  Update Client")
        print("4.  Delete Client")
        print("------------------------------------------")
        print("5.  Add Therapist")
        print("6.  View Therapists")
        print("7.  Update Therapist")
        print("8.  Delete Therapist")
        print("------------------------------------------")
        print("9.  Book Appointment")
        print("10. View Appointments")
        print("11. Cancel Appointment")
        print("12. Complete Appointment")
        print("13. Delete Appointment")
        print("------------------------------------------")
        print("14. Add Therapy Note")
        print("15. View Therapy Notes")
        print("16. Search Therapy Notes")
        print("17. Update Therapy Note")
        print("18. Delete Therapy Note")
        print("19. Export Therapy Notes to CSV")
        print("20. Count Therapy Notes")
        print("------------------------------------------")
        print("21. View Client Progress")
        print("22. Change Password")
        print("23. Logout")
        print("=" * 50)

        choice = input("Enter your choice: ")

        # ---------- CLIENTS ----------

        if choice == "1":
            add_client()

        elif choice == "2":
            view_clients()

        elif choice == "3":
            update_client()

        elif choice == "4":
            delete_client()

        # ---------- THERAPISTS ----------

        elif choice == "5":
            add_therapist()

        elif choice == "6":
            view_therapists()

        elif choice == "7":
            update_therapist()

        elif choice == "8":
            delete_therapist()

        # ---------- APPOINTMENTS ----------

        elif choice == "9":
            book_appointment()

        elif choice == "10":
            view_appointments()

        elif choice == "11":
            cancel_appointment()

        elif choice == "12":
            complete_appointment()

        elif choice == "13":
            delete_appointment()

        # ---------- THERAPY NOTES ----------

        elif choice == "14":
            add_note()

        elif choice == "15":
            view_notes()

        elif choice == "16":
            search_notes()

        elif choice == "17":
            update_note()

        elif choice == "18":
            delete_note()

        elif choice == "19":
            export_notes_csv()

        elif choice == "20":
            count_notes()

        # ---------- PROGRESS ----------

        elif choice == "21":
            view_progress()

        # ---------- PASSWORD ----------

        elif choice == "22":
            change_password(user)

        # ---------- LOGOUT ----------

        elif choice == "23":

            logout()

            break

        else:
            print("Invalid choice. Please try again.")