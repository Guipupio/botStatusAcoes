def string2float(string: str) -> float:
    try:
        if "%" in string:
            return float(string[0:-1])/100
        elif "R$" in string:
            return float(string.replace("R$", ''))
        elif "N/A" in string:
            return ''
        else:
            return float(string)
    except ValueError:
        return string