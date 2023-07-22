import csv
import time
from telethon.sync import TelegramClient
from telethon.errors import UserPrivacyRestrictedError
from telethon.tl.functions.messages import SendMessageRequest

api_id = 20066700
api_hash = 'af5de23471cd3ce06be10478e567c762'
phone_number = '+542914733243'  # Your phone number with country code, e.g., +1234567890
MESSAGE_SENT_THRESHOLD = 2 # Quantity of message that the script will sent
MESSAGE_COOLDOWN_IN_SECONDS = 20 # Expressed in seconds 

global_file_name = ""  # Global variable to store the file name

# Dictionary of group IDs and their names
groups = {
    -838510899: 'Testing script group',
    #'group2_id': 'Group 2 Name',
}

client = TelegramClient(phone_number, api_id, api_hash)

# Function to update the CSV file
def update_csv_file(group_name, member, message_sent):
    global global_file_name

    if global_file_name == "":
        global_file_name = input("Enter the name of the CSV file to store the tracking(include the '.csv'): ")

    with open(global_file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Check if the file is empty and write the header row if it is
        if file.tell() == 0:
            writer.writerow(['GROUP_NAME', 'USERNAME', 'FIRST_NAME', 'LAST_NAME', 'ID', 'STATUS'])

        writer.writerow([group_name, member.username, member.first_name, member.last_name, member.id, message_sent])

def check_pending_status():
    global global_file_name # Declare file_name as a global variable
    pending_ids = []  # Lista para almacenar los ID con STATUS = "PENDING"

    # Prompt the user to enter the name of the CSV file
    global_file_name = input("Enter the name of the CSV file to check the pending status(include the '.csv'): ")

    try:
        with open(global_file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['STATUS'] == 'PENDING':
                    pending_ids.append(int(row['ID']))

        if not pending_ids: 
            print("The CSV selected has finished with the task. Restarting the program.")
            global_file_name = ""
    except FileNotFoundError:
        print("The CSV selected doesn't exists. Restarting the program.")
        global_file_name = ""
        pass

    return pending_ids

def update_status_in_bulk(updated_statuses):
    global global_file_name

    try:
        # Open the CSV file and read all the rows
        with open(global_file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Update the statuses in the rows based on the updated_statuses dictionary
        for row in rows:
            user_id = int(row['ID'])
            if user_id in updated_statuses:
                row['STATUS'] = updated_statuses[user_id]

        # Write the updated rows back to the CSV file
        with open(global_file_name, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['GROUP_NAME', 'USERNAME', 'FIRST_NAME', 'LAST_NAME', 'ID', 'STATUS']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    except FileNotFoundError:
        print(f"File {global_file_name} not found.")
    except ValueError:
        print("Invalid ID. Please provide a valid integer ID.")

def parse_msg_from_file():
    try:
        with open("message-file.txt", 'r', encoding='utf-8') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"File 'message-file.txt' not found.")
        return ""

async def process_initial_flow():
    # Prompt for the message to send
    msg = parse_msg_from_file()

    # Display list of groups for selection
    selected_groups = {}  # Variable to store selected groups
    print("Select groups to send the message to:")
    for group_id, group_name in groups.items():
        selected = input(f"Group: {group_name} (Y/N): ").strip().lower()
        selected_groups[group_id] = selected == 'y'

    # Send the message to selected groups and update the CSV file
    message_count = 0
    for group_id, is_selected in selected_groups.items():
        if is_selected:
            group_name = groups[group_id]
            groupEntity = await client.get_entity(group_id)
            async for member in client.iter_participants(entity=groupEntity):
                if message_count < MESSAGE_SENT_THRESHOLD:
                    if not member.bot:
                        try:
                            await client(SendMessageRequest(peer=member, message=msg))
                            print(f"Message sent to {member.username} - {member.first_name} {member.last_name}")
                            update_csv_file(group_name, member, "SENDED")
                            message_count += 1
                        except UserPrivacyRestrictedError:
                            print(f"Message could not be sent to {member.username} - {member.first_name} {member.last_name}. Privacy settings restricted.")
                            update_csv_file(group_name, member, "NOT SENT")
                            message_count += 1

                        # Sleep for 1 minute before sending the next message
                        print("1 min pause started...")
                        time.sleep(MESSAGE_COOLDOWN_IN_SECONDS)
                        print("1 min pause ended")

                elif not member.bot:
                    print(f"Message pending to {member.username} - {member.first_name} {member.last_name}")
                    update_csv_file(group_name, member, "PENDING")

async def process_in_progress_flow(pending_user_ids):
    selected = input("You have a flow in progress, do you want to continue sending the messages? (Y/N): ").strip().lower() == 'y'

    if selected:
        msg = parse_msg_from_file()
        message_count = 0

        # Dictionary to store the updated statuses for each user ID
        updated_statuses = {}

        for user_id in pending_user_ids:
            if message_count < MESSAGE_SENT_THRESHOLD:
                member = await client.get_entity(user_id)
                if (not member.bot):
                        try:
                            await client(SendMessageRequest(peer=member, message=msg))
                            print(f"Message sent to {member.username} - {member.first_name} {member.last_name}")
                            updated_statuses[user_id] = "SENDED"
                            message_count += 1
                        except UserPrivacyRestrictedError:
                            print(f"Message could not be sent to {member.username} - {member.first_name} {member.last_name}. Privacy settings restricted.")
                            updated_statuses[user_id] = "NOT SENT"
                            message_count += 1

                        print("1 min pause started...")
                        time.sleep(MESSAGE_COOLDOWN_IN_SECONDS)
                        print("1 min pause ended")

            else:
                print(f"Message pending to {user_id}")
                updated_statuses[user_id] = "PENDING"
        
        # Update all the user IDs in the CSV file at once
        update_status_in_bulk(updated_statuses)
        return True

    else:
        return False

async def main():
    try:
        await client.start()

        in_progress_finish = False
        pending_user_ids = check_pending_status()
        
        if pending_user_ids:
            in_progress_finish = await process_in_progress_flow(pending_user_ids)

        if not in_progress_finish:
            await process_initial_flow()

    finally:
        await client.disconnect()

with client:
    client.loop.run_until_complete(main())
