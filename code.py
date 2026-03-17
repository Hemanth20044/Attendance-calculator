import time
import math
import os

# Color codes for better UI
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print a nice header for the application"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'ATTENDANCE CALCULATOR':^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def get_valid_input(prompt, input_type=int):
    """Get valid input from user with error handling"""
    while True:
        try:
            value = input_type(input(f"{Colors.CYAN}{prompt}{Colors.ENDC}"))
            if value < 0:
                print(f"{Colors.FAIL}❌ Please enter a positive number!{Colors.ENDC}")
                continue
            return value
        except ValueError:
            print(f"{Colors.FAIL}❌ Invalid input! Please enter a valid number.{Colors.ENDC}")

def calculate_classes_needed(attended, total, target_percent):
    """
    Calculate how many consecutive classes need to be attended to reach target percentage
    Formula: (attended + n) / (total + n) >= target/100
    Solving: n >= (target*total - 100*attended) / (100 - target)
    """
    if target_percent >= 100:
        return float('inf')
    
    numerator = (target_percent * total) - (100 * attended)
    denominator = 100 - target_percent
    
    if denominator == 0 or numerator <= 0:
        return 0
    
    return math.ceil(numerator / denominator)

def calculate_classes_can_bunk(attended, total, target_percent):
    """
    Calculate how many classes can be bunked while maintaining target percentage
    Formula: attended / (total + n) >= target/100
    Solving: n <= (100*attended - target*total) / target
    """
    if target_percent == 0:
        return float('inf')
    
    numerator = (100 * attended) - (target_percent * total)
    
    if numerator <= 0:
        return 0
    
    return math.floor(numerator / target_percent)

def print_current_status(attended, total, percentage):
    """Print current attendance status with visual indicators"""
    print(f"\n{Colors.BOLD}📊 CURRENT STATUS{Colors.ENDC}")
    print(f"{Colors.BLUE}{'─'*60}{Colors.ENDC}")
    print(f"  Total Classes: {Colors.BOLD}{total}{Colors.ENDC}")
    print(f"  Classes Attended: {Colors.BOLD}{attended}{Colors.ENDC}")
    print(f"  Classes Missed: {Colors.BOLD}{total - attended}{Colors.ENDC}")
    
    # Color-code the percentage based on value
    if percentage >= 80:
        color = Colors.GREEN
        emoji = "✅"
        status = "Excellent"
    elif percentage >= 75:
        color = Colors.WARNING
        emoji = "⚠️"
        status = "Good"
    else:
        color = Colors.FAIL
        emoji = "❌"
        status = "Below Required"
    
    print(f"  Current Attendance: {color}{Colors.BOLD}{percentage:.2f}%{Colors.ENDC} {emoji} ({status})")
    
    # Visual progress bar
    bar_length = 40
    filled = int(bar_length * percentage / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\n  [{bar}] {percentage:.1f}%")
    print(f"{Colors.BLUE}{'─'*60}{Colors.ENDC}\n")

def print_recommendations(attended, total, percentage):
    """Print recommendations based on current attendance"""
    print(f"\n{Colors.BOLD}💡 RECOMMENDATIONS{Colors.ENDC}")
    print(f"{Colors.BLUE}{'─'*60}{Colors.ENDC}\n")
    
    # Scenario 1: Below 75%
    if percentage < 75:
        classes_for_75 = calculate_classes_needed(attended, total, 75)
        classes_for_80 = calculate_classes_needed(attended, total, 80)
        
        print(f"{Colors.WARNING}  ⚠️  Your attendance is below the minimum requirement!{Colors.ENDC}\n")
        print(f"  {Colors.BOLD}To reach 75%:{Colors.ENDC}")
        print(f"    → Attend {Colors.GREEN}{Colors.BOLD}{classes_for_75}{Colors.ENDC} consecutive class(es)")
        print(f"    → New attendance will be: {Colors.GREEN}{((attended + classes_for_75) / (total + classes_for_75) * 100):.2f}%{Colors.ENDC}\n")
        
        print(f"  {Colors.BOLD}To reach 80%:{Colors.ENDC}")
        print(f"    → Attend {Colors.GREEN}{Colors.BOLD}{classes_for_80}{Colors.ENDC} consecutive class(es)")
        print(f"    → New attendance will be: {Colors.GREEN}{((attended + classes_for_80) / (total + classes_for_80) * 100):.2f}%{Colors.ENDC}\n")
    
    # Scenario 2: Between 75% and 80%
    elif 75 <= percentage < 80:
        classes_can_bunk_75 = calculate_classes_can_bunk(attended, total, 75)
        classes_for_80 = calculate_classes_needed(attended, total, 80)
        
        print(f"{Colors.GREEN}  ✅ Your attendance meets the minimum requirement.{Colors.ENDC}\n")
        print(f"  {Colors.BOLD}To maintain 75%:{Colors.ENDC}")
        if classes_can_bunk_75 > 0:
            print(f"    → You can bunk {Colors.WARNING}{Colors.BOLD}{classes_can_bunk_75}{Colors.ENDC} class(es)")
            print(f"    → Attendance will drop to: {Colors.WARNING}{(attended / (total + classes_can_bunk_75) * 100):.2f}%{Colors.ENDC}\n")
        else:
            print(f"    → {Colors.FAIL}Cannot bunk any classes!{Colors.ENDC}\n")
        
        print(f"  {Colors.BOLD}To reach 80%:{Colors.ENDC}")
        print(f"    → Attend {Colors.GREEN}{Colors.BOLD}{classes_for_80}{Colors.ENDC} consecutive class(es)")
        print(f"    → New attendance will be: {Colors.GREEN}{((attended + classes_for_80) / (total + classes_for_80) * 100):.2f}%{Colors.ENDC}\n")
    
    # Scenario 3: Above 80%
    else:
        classes_can_bunk_80 = calculate_classes_can_bunk(attended, total, 80)
        classes_can_bunk_75 = calculate_classes_can_bunk(attended, total, 75)
        
        print(f"{Colors.GREEN}  🎉 Excellent! Your attendance is above 80%!{Colors.ENDC}\n")
        print(f"  {Colors.BOLD}To maintain 80%:{Colors.ENDC}")
        if classes_can_bunk_80 > 0:
            print(f"    → You can bunk {Colors.WARNING}{Colors.BOLD}{classes_can_bunk_80}{Colors.ENDC} class(es)")
            print(f"    → Attendance will drop to: {Colors.WARNING}{(attended / (total + classes_can_bunk_80) * 100):.2f}%{Colors.ENDC}\n")
        else:
            print(f"    → {Colors.WARNING}Cannot bunk any classes without dropping below 80%!{Colors.ENDC}\n")
        
        print(f"  {Colors.BOLD}To maintain 75%:{Colors.ENDC}")
        if classes_can_bunk_75 > 0:
            print(f"    → You can bunk {Colors.WARNING}{Colors.BOLD}{classes_can_bunk_75}{Colors.ENDC} class(es)")
            print(f"    → Attendance will drop to: {Colors.WARNING}{(attended / (total + classes_can_bunk_75) * 100):.2f}%{Colors.ENDC}\n")
        else:
            print(f"    → {Colors.FAIL}Cannot bunk any classes!{Colors.ENDC}\n")
    
    print(f"{Colors.BLUE}{'─'*60}{Colors.ENDC}")

def main():
    """Main function to run the attendance calculator"""
    clear_screen()
    print_header()
    
    # Get user input
    total = get_valid_input("📚 Enter total number of classes: ")
    attended = get_valid_input("✅ Enter number of classes attended: ")
    
    # Validate input
    if attended > total:
        print(f"\n{Colors.FAIL}❌ Error: Classes attended cannot be more than total classes!{Colors.ENDC}")
        print(f"{Colors.WARNING}Please run the program again with valid inputs.{Colors.ENDC}\n")
        return
    
    # Calculate percentage
    time.sleep(0.3)
    percentage = (attended / total) * 100 if total > 0 else 0
    
    # Display results
    print_current_status(attended, total, percentage)
    time.sleep(0.3)
    print_recommendations(attended, total, percentage)
    
    # Footer
    print(f"\n{Colors.CYAN}{'─'*60}{Colors.ENDC}")
    print(f"{Colors.CYAN}💡 Tip: Regular attendance helps maintain good academic standing!{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─'*60}{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Program interrupted by user. Goodbye!{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n{Colors.FAIL}An error occurred: {e}{Colors.ENDC}\n")
