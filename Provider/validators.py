def validate_request_data(data):
    for key, value in data.items():
        if not key.isnumeric():
            raise ValueError("Key must be numeric")
        elif value is None:
            raise ValueError("Value cannot be empty!")


if __name__ == "__main__":
    pass