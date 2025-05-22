import re
from socket import inet_ntoa


def _split_variably_spaced_columns(string: str) -> list[str]:
    string_with_multiple_spaces_replaced_with_single = re.sub(" +", " ", string)
    return string_with_multiple_spaces_replaced_with_single.split(" ")


class RelevantProcNetTCPEntry:
    """
    The parts relevant to us from the entries that can be found in /proc/net/tcp.

    NOTES:
        - A socket can be bound, and while it is bound, no other socket can bind to it, but it will not show up in /proc/net/tcp
        - A socket that is connected or is for an accepted connection will show up in the list with a specific remote address and port e.g., 5.5.5.5:32600
        - A socket which is listening for connections will show up in the list with a remote address of 0.0.0.0 and port of 0
    """
    def __init__(self,
                 local_addr: str,
                 local_port: int,
                 remote_addr: str,
                 remote_port: int,
                 inode_number: int):
        """
        :param local_addr: the local address the socket is for, converted
        :param remote_addr: the remote IP address the socket is for converted to dotted decimal form.
        :param remote_port: the remote TCP port that the socket is for converted to decimal.
        :param inode_number: the number of inode the socket is for.
        """
        self._local_addr = local_addr
        self._local_port = local_port
        self._remote_addr = remote_addr
        self._remote_port = remote_port
        self._inode_number = inode_number

    @property
    def local_addr(self):
        return self._local_addr

    @property
    def local_port(self):
        return self._local_port

    @property
    def remote_addr(self):
        return self._remote_addr

    @property
    def remote_port(self):
        return self._remote_port

    @property
    def inode_number(self):
        return self._inode_number

    @staticmethod
    def _read_dotted_decimal_and_port_from_hex_pair(hex_pair: str) -> (str, int):
        # the one from the entry will be in big endian, reading the address happens from little endian
        addr_hex_little_endian = "".join(reversed(hex_pair.split(":")[0]))
        addr = inet_ntoa(bytes.fromhex(addr_hex_little_endian.split(":")[0]))
        port = int(hex_pair.split(":")[1], 16)
        return addr, port

    @classmethod
    def from_proc_net_tcp_lines(cls, lines: list[str]) -> list["RelevantProcNetTCPEntry"]:
        #   sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
        #    0: 00000000:6B6C 00000000:0000 0A 00000000:00000000 00:00000000 00000000   967        0 35712 1 0000000037531816 100 0 0 10 0
        proc_net_tcp_entries = list()
        for line in lines:
            line_columns = _split_variably_spaced_columns(line.lstrip(" "))
            local_address_hex = line_columns[1]
            remote_address_hex = line_columns[2]
            inode_number = int(line_columns[9])
            local_addr, local_port = cls._read_dotted_decimal_and_port_from_hex_pair(local_address_hex)
            remote_addr, remote_port = cls._read_dotted_decimal_and_port_from_hex_pair(remote_address_hex)
            proc_net_tcp_entry = RelevantProcNetTCPEntry(
                local_addr=local_addr,
                local_port=local_port,
                remote_addr=remote_addr,
                remote_port=remote_port,
                inode_number=inode_number)
            proc_net_tcp_entries.append(proc_net_tcp_entry)
        return proc_net_tcp_entries

    @classmethod
    def from_proc_net_tcp_file(cls, file_path: str = "/proc/net/tcp") -> list["RelevantProcNetTCPEntry"]:
         with open(file_path) as f:
             return cls.from_proc_net_tcp_lines(f.readlines())
