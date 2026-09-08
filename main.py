from Gmail.mailing import get_latest_email


def main():

    email = get_latest_email()

    if email is None:
        print("No email found.")
        return

    print("\n========== EMAIL ==========\n")

    print("Message ID :", email["message_id"])
    print("Thread ID  :", email["thread_id"])
    print("From       :", email["from"])
    print("To         :", email["to"])
    print("Subject    :", email["subject"])
    print("Date       :", email["date"])

    print("\n---------- BODY -----------\n")

    print(email["body"])

    print("\n============================")


if __name__ == "__main__":
    main()