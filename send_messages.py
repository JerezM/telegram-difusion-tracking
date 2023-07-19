import csv
from telethon.sync import TelegramClient
from telethon.errors import UserPrivacyRestrictedError
from telethon.tl.functions.messages import SendMessageRequest

api_id = 20066700
api_hash = 'af5de23471cd3ce06be10478e567c762'
phone_number = '+542914733243'  # Your phone number with country code, e.g., +1234567890

# Dictionary of group IDs and their names
groups = {
    -838510899: 'Testing script group',
    #'group2_id': 'Group 2 Name',
    # Add more groups as needed
}

# Function to update the CSV file
def update_csv_file(group_name, member, message_sent):
    with open('messages_tracker.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Check if the file is empty and write the header row if it is
        if file.tell() == 0:
            writer.writerow(['GROUP_NAME', 'USERNAME', 'FIRST_NAME', 'LAST_NAME', 'ID', 'STATUS'])

        writer.writerow([group_name, member.username, member.first_name, member.last_name, member.id, message_sent])

client = TelegramClient(phone_number, api_id, api_hash)

async def main():
    try:
        await client.start()

        # Prompt for the message to send
        message = input("Enter the message you want to send:\n")

        # Display list of groups for selection
        selected_groups = {}  # Variable to store selected groups
        print("Select groups to send the message to:")
        for group_id, group_name in groups.items():
            selected = input(f"Group: {group_name} (Y/N): ").strip().lower()
            selected_groups[group_id] = selected == 'y'

        # Send the message to selected groups and update the CSV file
        for group_id, is_selected in selected_groups.items():
            if is_selected:
                group_name = groups[group_id]
                groupEntity = await client.get_entity(group_id)
                async for member in client.iter_participants(entity=groupEntity):
                    if not member.bot:
                        try:
                            #await client(SendMessageRequest(peer=member, message=message))
                            print(f"Message sent to {member.username} - {member.first_name} {member.last_name}")
                            update_csv_file(group_name, member, "SENDED")
                        except UserPrivacyRestrictedError:
                            print(f"Message could not be sent to {member.username} - {member.first_name} {member.last_name}. Privacy settings restricted.")
                            update_csv_file(member, "NOT SENDED")
    finally:
        await client.disconnect()

with client:
    client.loop.run_until_complete(main())
