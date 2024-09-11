def calculate_checksum(pseudo_ip_header, tcp_data_zero_cksum):
    # Combine pseudo header and TCP data for checksum calculation
    combined_data = pseudo_ip_header + tcp_data_zero_cksum

    # Initialize sum
    checksum = 0

    # Loop through combined_data in 16-bit (2-byte) steps
    for offset in range(0, len(combined_data), 2):
        # Combine two bytes and add to checksum
        word = int.from_bytes(combined_data[offset : offset + 2], "big")

        # Handle overflow
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)  # carry around

    # Finalize checksum: take one's complement
    checksum = (~checksum) & 0xFFFF
    # checksum = checksum.to_bytes(length=2, byteorder="big")
    return checksum


def process_tcp_data():
    zero = b"\x00"
    protocol = b"\x06"
    for i in range(9):
        # Read source and destination addresses
        filename = "./tcp_data/tcp_addrs_" + str(i) + ".txt"
        with open(filename, "r") as f:
            addrs = f.read()
        s, d = addrs.split()
        print(f"Source: {s}, Destination: {d}")
        source = b"".join([*map(int.to_bytes, [*map(int, s.split("."))])])
        destination = b"".join([*map(int.to_bytes, [*map(int, d.split("."))])])
        print(f"Source: {source.hex()}, Destination: {destination.hex()}")

        # Read raw TCP data
        filename = "./tcp_data/tcp_data_" + str(i) + ".dat"
        with open(filename, "rb") as f:
            tcp_data = f.read()
        tcp_packet_length = len(tcp_data)

        # Create pseudo IP header
        pseudo_ip_header = (
            source
            + destination
            + zero
            + protocol
            + tcp_packet_length.to_bytes(length=2, byteorder="big")
        )

        # Calculate checksum
        tcp_data_zero_cksum = tcp_data[:16] + b"\x00\x00" + tcp_data[18:]
        if len(tcp_data_zero_cksum) % 2 == 1:
            tcp_data_zero_cksum += b"\x00"
        original_cksum = tcp_data[16:18]
        original_cksum = int.from_bytes(original_cksum, "big")
        calculated_checksum = calculate_checksum(pseudo_ip_header, tcp_data_zero_cksum)

        # Print results
        print(f"Original checksum: {original_cksum}")
        print(f"Calculated checksum: {calculated_checksum}")
        if original_cksum != calculated_checksum:
            print(f"❌ Checksum mismatch for packet {i}")
        else:
            print(f"✅ Checksum match for packet {i}")
        print("\n")


process_tcp_data()
