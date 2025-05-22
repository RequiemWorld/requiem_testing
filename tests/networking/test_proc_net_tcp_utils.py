import socket
import unittest
from requiem_testing.networking.helper.proc_net_tcp import RelevantProcNetTCPEntry

def _mock_proc_net_tcp_entry_data(
        local_addr: str,
        local_port: int,
        remote_addr: str,
        remote_port: int,
        inode_number: int) -> str:
    # inet_aton converts to the host byte order which is going to be little endian,
    # and /proc/net/tcp has the byte order in big endian
    remote_addr_as_hex = "".join(reversed(socket.inet_aton(remote_addr).hex()))
    local_addr_as_hex = "".join(reversed(socket.inet_aton(local_addr).hex()))
    data = f"   0: {local_addr_as_hex}:{local_port:04x} "
    data += f"{remote_addr_as_hex}:{remote_port:04x} 0A 00000000:00000000 00:00000000 00000000   967        0 {inode_number} 1 0000000037531816 100 0 0 10 0                     \n"
    return data


class TestProcNetTCPEntryReading(unittest.TestCase):
    def setUp(self):
        self._line_one = _mock_proc_net_tcp_entry_data("127.0.0.1", 1400, "0.0.0.0", 0, 1100)
        self._line_two = _mock_proc_net_tcp_entry_data("128.0.2.1", 1401, "129.0.0.1", 40000, 1120)

    def test_should_read_local_port_from_proc_net_tcp_lines_correctly(self):
        entries = RelevantProcNetTCPEntry.from_proc_net_tcp_lines([self._line_one, self._line_two])
        self.assertEqual(1400, entries[0].local_port)
        self.assertEqual(1401, entries[1].local_port)

    def test_should_read_local_address_from_proc_net_tcp_lines_correctly(self):
        entries = RelevantProcNetTCPEntry.from_proc_net_tcp_lines([self._line_one, self._line_two])
        self.assertEqual("127.0.0.1", entries[0].local_addr)
        self.assertEqual("128.0.2.1", entries[1].local_addr)

    def test_should_read_remote_address_from_proc_net_tcp_lines_correctly(self):
        #   5: 0100007F:AFE3 00000000:0000 0A 00000000:00000000 00:00000000 00000000 65536        0 99100682 2 00000000524f337b 100 0 0 10 0
        entries = RelevantProcNetTCPEntry.from_proc_net_tcp_lines([self._line_one, self._line_two])
        self.assertEqual("0.0.0.0", entries[0].remote_addr)
        self.assertEqual("129.0.0.1", entries[1].remote_addr)

    def test_should_read_remote_port_from_proc_net_tcp_lines_correctly(self):
        entries = RelevantProcNetTCPEntry.from_proc_net_tcp_lines([self._line_one, self._line_two])
        self.assertEqual(0, entries[0].remote_port)
        self.assertEqual(40000, entries[1].remote_port)

    def test_should_read_inode_number_from_proc_net_tcp_lines_correctly(self):
        entries = RelevantProcNetTCPEntry.from_proc_net_tcp_lines([self._line_one, self._line_two])
        self.assertEqual(1100, entries[0].inode_number)
        self.assertEqual(1120, entries[1].inode_number)

    def test_should_read_inode_from_lines_with_uid_0_or_at_least_not_as_expected_correctly(self):
        # An implementation of this may read from column -8 from the end after stripping the spaces from it,
        # some entries subsequently don't have all the columns expected there, and it will not work as intended.
        #
        # The rows in question do still have the inode column, it's just 0 along with userid 0.
        sample_line = "  15: 0100007F:A804 0100007F:B657 06 00000000:00000000 03:0000050D 00000000     0        0 0 3 000000005ffd27ac                                      "
        entries = RelevantProcNetTCPEntry.from_proc_net_tcp_lines([sample_line])
        self.assertEqual(0, entries[0].inode_number)