def validate_request_data(data: dict) -> None:
    if data:
        for key, value in data.items():
            if not key.isnumeric():
                raise ValueError()
            elif value is None:
                raise ValueError()
    else:
        raise ValueError()


def validate_result_from_queue(result_list: list) -> None:
    for result in result_list:
        if result is not None:
            raise ValueError()


if __name__ == "__main__":
    pass
