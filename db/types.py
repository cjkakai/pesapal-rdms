# db/types.py

class TypeSystem:
    SUPPORTED = {"INT", "TEXT", "BOOL"}

    @staticmethod
    def cast(value, dtype):
        if dtype not in TypeSystem.SUPPORTED:
            raise ValueError(f"Unsupported type: {dtype}")

        try:
            if dtype == "INT":
                return int(value)
            if dtype == "TEXT":
                return str(value)
            if dtype == "BOOL":
                if value in (True, False):
                    return value
                if str(value).lower() in ("true", "1"):
                    return True
                if str(value).lower() in ("false", "0"):
                    return False
        except Exception:
            raise ValueError(f"Invalid value '{value}' for {dtype}")

        raise ValueError(f"Invalid value '{value}' for {dtype}")

# This code:

# Accepts a value and a target type

# Checks if the type is supported

# Converts the value safely

# Throws clear errors when conversion fails

# It’s a clean, defensive way to enforce data integrity in a database or backend system. and converts the value to the specified type if supported.