def format_size(bytes_num: int) -> str:
    """Pretty-print a byte size as MB or GB."""
    if bytes_num is None:
        return "0 MB"

    gb = bytes_num / (1024 ** 3)
    mb = bytes_num / (1024 ** 2)

    if gb >= 1:
        return f"{gb:.2f} GB"
    return f"{mb:.2f} MB"
