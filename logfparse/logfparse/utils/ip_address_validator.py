from netaddr import IPAddress, IPNetwork


class IPAddressModel:
    def __init__(self, ip_str: str):
        self.ip = IPAddress(ip_str)

    def __str__(self):
        return str(self.ip)

    @classmethod
    def from_string(cls, value: str) -> "IPAddressModel":
        try:
            return cls(IPNetwork(value).ip)
        except ValueError:
            raise ValueError("invalid ip address format")

    @classmethod
    def __get_validators__(cls):
        yield cls.from_string
