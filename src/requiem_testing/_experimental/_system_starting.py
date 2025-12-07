import time
import socket


def wait_for_tcp4_port_connectivity(host: str, port: int, keep_trying_for: int | float) -> None:
	"""
	:param host: The hostname or IPv4 address to connect to at the given port.
	:param keep_trying_for: The number of seconds to give up after when a connection doesn't go through.
	:raises TimeoutError: When the port can't be reached in the given time period.
	"""
	time_started_trying = None
	seconds_since_started_trying = 0
	if keep_trying_for < 0.1:
		socket_timeout_value = keep_trying_for
	else:
		socket_timeout_value = 0.1  # this should be an eternity for local connections.
	while seconds_since_started_trying < keep_trying_for:
		if time_started_trying is None:
			time_started_trying = time.time()
		else:
			seconds_since_started_trying = time.time() - time_started_trying
		sock = socket.socket()
		sock.settimeout(socket_timeout_value)
		try:
			sock.connect((host, port))
			return
		except ConnectionRefusedError:
			continue
		except TimeoutError:
			continue
		finally:
			sock.close()
	raise TimeoutError(f"no {host}:{port} could be reached while trying in the given retry for period.")
