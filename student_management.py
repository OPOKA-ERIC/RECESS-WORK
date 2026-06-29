"""
Student Record Management System
A menu-driven application demonstrating OOP, file I/O, exception handling, and logging
Author: Opoka Eric
Registration: U/24/10784/EVE
Student Number: 2400710784
"""

import csv
import json
import os
import logging
from datetime import datetime

# Configure logging to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("student_system.log"),
        logging.StreamHandler()
    ]
)

# Constants
CSV_FILE = "students.csv"
JSON_FILE = "students.json"
CSV_HEADERS = ["reg_number", "name", "student_number", "program", "address", "contact"]
LOG_FILE = "student_system.log"


# --- Custom Exception ---
class StudentNotFoundError(Exception):
    """Raised when a student is not found in the system."""
    pass


class DuplicateStudentError(Exception):
    """Raised when a student with the same registration number already exists."""
    pass


class InvalidDataError(Exception):
    """Raised when input data is invalid."""
    pass


# --- Core Functions ---

def init_files():
    """Initialise CSV and JSON files if they don't exist."""
    try:
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS)
            logging.info(f"Created {CSV_FILE}")

        if not os.path.exists(JSON_FILE):
            with open(JSON_FILE, "w") as f:
                json.dump([], f)
            logging.info(f"Created {JSON_FILE}")

    except Exception as e:
        logging.error(f"Failed to initialise files: {e}")
        raise


def read_csv():
    """Read all students from CSV file and return as list of dicts."""
    students = []
    try:
        with open(CSV_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        logging.warning(f"{CSV_FILE} not found. Returning empty list.")
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
    return students


def write_csv(students):
    """Write list of student dicts to CSV file."""
    try:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(students)
        logging.info(f"Written {len(students)} records to {CSV_FILE}")
    except Exception as e:
        logging.error(f"Error writing CSV: {e}")
        raise


def read_json():
    """Read additional student details from JSON file."""
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"{JSON_FILE} not found. Returning empty list.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format: {e}")
        return []
    except Exception as e:
        logging.error(f"Error reading JSON: {e}")
        return []


def write_json(data):
    """Write additional student details to JSON file."""
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Written {len(data)} records to {JSON_FILE}")
    except Exception as e:
        logging.error(f"Error writing JSON: {e}")
        raise


# --- Validation ---

def validate_reg_number(reg_number):
    """Validate registration number format."""
    if not reg_number or not reg_number.strip():
        raise InvalidDataError("Registration number cannot be empty")


def validate_name(name):
    """Validate student name."""
    if not name or not name.strip():
        raise InvalidDataError("Name cannot be empty")


def validate_student_number(student_number):
    """Validate student number."""
    if not student_number or not student_number.strip():
        raise InvalidDataError("Student number cannot be empty")


def validate_program(program):
    """Validate program name."""
    if not program or not program.strip():
        raise InvalidDataError("Program cannot be empty")


# --- Student Operations ---

def add_student():
    """Add a new student record to both CSV and JSON files."""
    print("\n--- Add New Student ---")
    try:
        reg_number = input("Enter Registration Number: ").strip()
        validate_reg_number(reg_number)

        # Check for duplicates
        students = read_csv()
        if any(s["reg_number"] == reg_number for s in students):
            raise DuplicateStudentError(f"Student with registration number {reg_number} already exists")

        name = input("Enter Full Name: ").strip()
        validate_name(name)

        student_number = input("Enter Student Number: ").strip()
        validate_student_number(student_number)

        program = input("Enter Program: ").strip()
        validate_program(program)

        address = input("Enter Address: ").strip()
        contact = input("Enter Contact: ").strip()

        # Save to CSV
        students.append({
            "reg_number": reg_number,
            "name": name,
            "student_number": student_number,
            "program": program,
            "address": address,
            "contact": contact
        })
        write_csv(students)

        # Save additional details to JSON
        json_data = read_json()
        json_data.append({
            "reg_number": reg_number,
            "name": name,
            "student_number": student_number,
            "program": program,
            "address": address,
            "contact": contact,
            "created_at": datetime.now().isoformat()
        })
        write_json(json_data)

        logging.info(f"Student added successfully: {reg_number} - {name}")
        print("Student added successfully!")

    except DuplicateStudentError as e:
        print(f"Error: {e}")
        logging.warning(f"Duplicate student attempt: {e}")
    except InvalidDataError as e:
        print(f"Validation Error: {e}")
        logging.warning(f"Invalid data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Unexpected error adding student: {e}")


def view_all_students():
    """Display all student records."""
    print("\n--- View All Students ---")
    try:
        students = read_csv()
        if not students:
            print("No students found in the system.")
            logging.info("Viewed all students: empty list")
            return

        print(f"\n{'Reg Number':<20} {'Name':<25} {'Student No':<15} {'Program':<20} {'Address':<20} {'Contact':<15}")
        print("-" * 115)
        for s in students:
            print(f"{s['reg_number']:<20} {s['name']:<25} {s['student_number']:<15} {s['program']:<20} {s['address']:<20} {s['contact']:<15}")
        print(f"\nTotal students: {len(students)}")
        logging.info(f"Viewed all students: {len(students)} records")

    except Exception as e:
        print(f"Error reading student records: {e}")
        logging.error(f"Error viewing students: {e}")


def search_student():
    """Search for a student by registration number."""
    print("\n--- Search Student ---")
    try:
        reg_number = input("Enter Registration Number to search: ").strip()
        validate_reg_number(reg_number)

        students = read_csv()
        found = [s for s in students if s["reg_number"] == reg_number]

        if not found:
            raise StudentNotFoundError(f"No student found with registration number: {reg_number}")

        s = found[0]
        print(f"\nStudent Found:")
        print(f"  Registration Number: {s['reg_number']}")
        print(f"  Name: {s['name']}")
        print(f"  Student Number: {s['student_number']}")
        print(f"  Program: {s['program']}")
        print(f"  Address: {s['address']}")
        print(f"  Contact: {s['contact']}")

        # Also show from JSON if available
        json_data = read_json()
        json_match = [j for j in json_data if j["reg_number"] == reg_number]
        if json_match:
            print(f"  Created At: {json_match[0].get('created_at', 'N/A')}")

        logging.info(f"Searched and found student: {reg_number}")

    except StudentNotFoundError as e:
        print(f"Error: {e}")
        logging.warning(f"Search failed: {e}")
    except InvalidDataError as e:
        print(f"Validation Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Error searching student: {e}")


def update_student():
    """Update details of an existing student."""
    print("\n--- Update Student ---")
    try:
        reg_number = input("Enter Registration Number of student to update: ").strip()
        validate_reg_number(reg_number)

        students = read_csv()
        index = None
        for i, s in enumerate(students):
            if s["reg_number"] == reg_number:
                index = i
                break

        if index is None:
            raise StudentNotFoundError(f"No student found with registration number: {reg_number}")

        student = students[index]
        print(f"\nCurrent details for {student['name']}:")
        print(f"  1. Name: {student['name']}")
        print(f"  2. Student Number: {student['student_number']}")
        print(f"  3. Program: {student['program']}")
        print(f"  4. Address: {student['address']}")
        print(f"  5. Contact: {student['contact']}")

        print("\nEnter new values (leave blank to keep current):")
        name = input(f"  Name [{student['name']}]: ").strip()
        if name:
            validate_name(name)
            student["name"] = name

        student_number = input(f"  Student Number [{student['student_number']}]: ").strip()
        if student_number:
            validate_student_number(student_number)
            student["student_number"] = student_number

        program = input(f"  Program [{student['program']}]: ").strip()
        if program:
            student["program"] = program

        address = input(f"  Address [{student['address']}]: ").strip()
        if address:
            student["address"] = address

        contact = input(f"  Contact [{student['contact']}]: ").strip()
        if contact:
            student["contact"] = contact

        # Update CSV
        students[index] = student
        write_csv(students)

        # Update JSON
        json_data = read_json()
        for j in json_data:
            if j["reg_number"] == reg_number:
                j.update({
                    "name": student["name"],
                    "student_number": student["student_number"],
                    "program": student["program"],
                    "address": student["address"],
                    "contact": student["contact"],
                    "updated_at": datetime.now().isoformat()
                })
                break
        write_json(json_data)

        logging.info(f"Student updated: {reg_number}")
        print("Student details updated successfully!")

    except StudentNotFoundError as e:
        print(f"Error: {e}")
        logging.warning(f"Update failed: {e}")
    except InvalidDataError as e:
        print(f"Validation Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Error updating student: {e}")


def delete_student():
    """Delete a student record from both CSV and JSON files."""
    print("\n--- Delete Student ---")
    try:
        reg_number = input("Enter Registration Number of student to delete: ").strip()
        validate_reg_number(reg_number)

        students = read_csv()
        before_count = len(students)
        students = [s for s in students if s["reg_number"] != reg_number]

        if len(students) == before_count:
            raise StudentNotFoundError(f"No student found with registration number: {reg_number}")

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete student {reg_number}? (y/n): ").strip().lower()
        if confirm != "y":
            print("Deletion cancelled.")
            return

        # Update CSV
        write_csv(students)

        # Update JSON
        json_data = read_json()
        json_data = [j for j in json_data if j["reg_number"] != reg_number]
        write_json(json_data)

        logging.info(f"Student deleted: {reg_number}")
        print("Student record deleted successfully!")

    except StudentNotFoundError as e:
        print(f"Error: {e}")
        logging.warning(f"Delete failed: {e}")
    except InvalidDataError as e:
        print(f"Validation Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Error deleting student: {e}")


# --- Menu ---

def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("STUDENT RECORD MANAGEMENT SYSTEM")
    print("Author: Opoka Eric | U/24/10784/EVE | 2400710784")
    print("=" * 60)
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student by Registration Number")
    print("4. Update Student Details")
    print("5. Delete Student Record")
    print("6. Exit")
    print("-" * 60)


def main():
    """Main program loop."""
    try:
        init_files()
        logging.info("Student Record Management System started")
    except Exception as e:
        print(f"Fatal error initialising system: {e}")
        logging.critical(f"System initialisation failed: {e}")
        return

    while True:
        try:
            display_menu()
            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                add_student()
            elif choice == "2":
                view_all_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                print("\nExiting Student Record Management System. Goodbye!")
                logging.info("System exited by user")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user. Exiting...")
            logging.info("System interrupted by user (Ctrl+C)")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            logging.error(f"Unexpected error in main loop: {e}")


if __name__ == "__main__":
    main()
