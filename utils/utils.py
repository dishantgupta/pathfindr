

from datetime import datetime
from datetime import timezone


def validate_date(date_string, date_format="%Y-%m-%d"):
    try:
        # Parse the date string according to the given format
        valid_date = datetime.strptime(date_string, date_format)
        valid_date = valid_date.astimezone(timezone.utc)
        return valid_date
    except ValueError:
        # If there's a ValueError, the date is invalid
        return None