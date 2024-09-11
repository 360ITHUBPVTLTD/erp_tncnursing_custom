def simulate_message_sending(instance_id, file_url, phone_numbers, log_file='send_log.txt'):
    with open(log_file, 'w') as file:
        for phone_number in phone_numbers:
            # Simulate sending the message
            log_entry = f"Dear {phone_number}, message is successfully sent.\n"
            file.write(log_entry)

# Example usage
instance_id = "7777777737333"
file_url = ""
phone_numbers = [
    "1234567890",
    "0987654321",
    "1122334455",
    "2233445566",
    "3344556677",
    "4455667788",
    "5566778899",
    "6677889900",
    "7788990011",
    "8899001122"
]

simulate_message_sending(instance_id, file_url, phone_numbers)
