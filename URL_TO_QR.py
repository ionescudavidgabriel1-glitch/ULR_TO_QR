import sys
from PIL import Image, ImageDraw

# -----------------------------------------------------------------------------
# STEP 1: URL VALIDATION & SPECIFICATION LIMIT (Versions 1-7)
# -----------------------------------------------------------------------------

def generate_qr_code(url, ec_level='L'):
    QR_SPECS = {
        # Version 1
        (1, 'L'): {'total_data_bytes': 19, 'ec_per_block': 7,  'g1_blocks': 1, 'g1_bytes': 19, 'g2_blocks': 0, 'g2_bytes': 0},
        (1, 'M'): {'total_data_bytes': 16, 'ec_per_block': 10, 'g1_blocks': 1, 'g1_bytes': 16, 'g2_blocks': 0, 'g2_bytes': 0},
        (1, 'Q'): {'total_data_bytes': 13, 'ec_per_block': 13, 'g1_blocks': 1, 'g1_bytes': 13, 'g2_blocks': 0, 'g2_bytes': 0},
        (1, 'H'): {'total_data_bytes': 9,  'ec_per_block': 17, 'g1_blocks': 1, 'g1_bytes': 9,  'g2_blocks': 0, 'g2_bytes': 0},
        # Version 2
        (2, 'L'): {'total_data_bytes': 34, 'ec_per_block': 10, 'g1_blocks': 1, 'g1_bytes': 34, 'g2_blocks': 0, 'g2_bytes': 0},
        (2, 'M'): {'total_data_bytes': 28, 'ec_per_block': 16, 'g1_blocks': 1, 'g1_bytes': 28, 'g2_blocks': 0, 'g2_bytes': 0},
        (2, 'Q'): {'total_data_bytes': 22, 'ec_per_block': 22, 'g1_blocks': 1, 'g1_bytes': 22, 'g2_blocks': 0, 'g2_bytes': 0},
        (2, 'H'): {'total_data_bytes': 16, 'ec_per_block': 28, 'g1_blocks': 1, 'g1_bytes': 16, 'g2_blocks': 0, 'g2_bytes': 0},
        # Version 3
        (3, 'L'): {'total_data_bytes': 55, 'ec_per_block': 15, 'g1_blocks': 1, 'g1_bytes': 55, 'g2_blocks': 0, 'g2_bytes': 0},
        (3, 'M'): {'total_data_bytes': 44, 'ec_per_block': 26, 'g1_blocks': 1, 'g1_bytes': 44, 'g2_blocks': 0, 'g2_bytes': 0},
        (3, 'Q'): {'total_data_bytes': 34, 'ec_per_block': 18, 'g1_blocks': 2, 'g1_bytes': 17, 'g2_blocks': 0, 'g2_bytes': 0},
        (3, 'H'): {'total_data_bytes': 26, 'ec_per_block': 22, 'g1_blocks': 2, 'g1_bytes': 13, 'g2_blocks': 0, 'g2_bytes': 0},
        # Version 4
        (4, 'L'): {'total_data_bytes': 80, 'ec_per_block': 20, 'g1_blocks': 1, 'g1_bytes': 80, 'g2_blocks': 0, 'g2_bytes': 0},
        (4, 'M'): {'total_data_bytes': 64, 'ec_per_block': 18, 'g1_blocks': 2, 'g1_bytes': 32, 'g2_blocks': 0, 'g2_bytes': 0},
        (4, 'Q'): {'total_data_bytes': 48, 'ec_per_block': 26, 'g1_blocks': 2, 'g1_bytes': 24, 'g2_blocks': 0, 'g2_bytes': 0},
        (4, 'H'): {'total_data_bytes': 36, 'ec_per_block': 16, 'g1_blocks': 4, 'g1_bytes': 9,  'g2_blocks': 0, 'g2_bytes': 0},
        # Version 5
        (5, 'L'): {'total_data_bytes': 108, 'ec_per_block': 26, 'g1_blocks': 1, 'g1_bytes': 108, 'g2_blocks': 0, 'g2_bytes': 0},
        (5, 'M'): {'total_data_bytes': 86,  'ec_per_block': 24, 'g1_blocks': 2, 'g1_bytes': 43,  'g2_blocks': 0, 'g2_bytes': 0},
        (5, 'Q'): {'total_data_bytes': 62,  'ec_per_block': 18, 'g1_blocks': 2, 'g1_bytes': 15,  'g2_blocks': 2, 'g2_bytes': 16},
        (5, 'H'): {'total_data_bytes': 46,  'ec_per_block': 22, 'g1_blocks': 2, 'g1_bytes': 11,  'g2_blocks': 2, 'g2_bytes': 12},
        # Version 6
        (6, 'L'): {'total_data_bytes': 136, 'ec_per_block': 18, 'g1_blocks': 2, 'g1_bytes': 68, 'g2_blocks': 0, 'g2_bytes': 0},
        (6, 'M'): {'total_data_bytes': 108, 'ec_per_block': 16, 'g1_blocks': 4, 'g1_bytes': 27, 'g2_blocks': 0, 'g2_bytes': 0},
        (6, 'Q'): {'total_data_bytes': 76,  'ec_per_block': 24, 'g1_blocks': 4, 'g1_bytes': 19, 'g2_blocks': 0, 'g2_bytes': 0},
        (6, 'H'): {'total_data_bytes': 60,  'ec_per_block': 28, 'g1_blocks': 4, 'g1_bytes': 15, 'g2_blocks': 0, 'g2_bytes': 0},
        # Version 7
        (7, 'L'): {'total_data_bytes': 156, 'ec_per_block': 20, 'g1_blocks': 2, 'g1_bytes': 78, 'g2_blocks': 0, 'g2_bytes': 0},
        (7, 'M'): {'total_data_bytes': 124, 'ec_per_block': 18, 'g1_blocks': 4, 'g1_bytes': 31, 'g2_blocks': 0, 'g2_bytes': 0},
        (7, 'Q'): {'total_data_bytes': 88,  'ec_per_block': 18, 'g1_blocks': 2, 'g1_bytes': 14, 'g2_blocks': 4, 'g2_bytes': 15},
        (7, 'H'): {'total_data_bytes': 66,  'ec_per_block': 26, 'g1_blocks': 4, 'g1_bytes': 13, 'g2_blocks': 1, 'g2_bytes': 14},
    }

    # -----------------------------------------------------------------------------
    # STEP 2: USER INPUT & VERSION SELECTION
    # -----------------------------------------------------------------------------


    url_bytes = url.encode("utf-8")
    num_bytes = len(url_bytes)

    selected_version = None
    selected_spec = None

    for v in range(1, 8):
        spec = QR_SPECS[(v, ec_level)]
        max_user_bytes = (spec['total_data_bytes'] * 8 - 12) // 8
        if num_bytes <= max_user_bytes:
            selected_version = v
            selected_spec = spec
            break

    # Graceful exit if payload exceeds Version 7 capacity
    if not selected_version:
        print(f"\n[-] Error: URL payload ({num_bytes} bytes) exceeds maximum capacity for QR Code Version 7.")
        sys.exit(1)

    print(f"\n[+] Selected Version: {selected_version}-{ec_level}")
    print(f"[+] Total Data Capacity: {selected_spec['total_data_bytes']} bytes")

    # -----------------------------------------------------------------------------
    # STEP 3: DATA ENCODING & PADDING
    # -----------------------------------------------------------------------------
    mode_indicator = "0100"  # Byte mode
    count_bits = 8           # 8 bits for Versions 1-9 in Byte Mode
    count_indicator = f"{num_bytes:0{count_bits}b}"
    payload_bits = "".join(f"{b:08b}" for b in url_bytes)

    binary_sequence = mode_indicator + count_indicator + payload_bits
    target_bits = selected_spec['total_data_bytes'] * 8

    # 1. Terminator bits
    if len(binary_sequence) < target_bits:
        binary_sequence += "0" * min(4, target_bits - len(binary_sequence))

    # 2. Bit alignment
    if len(binary_sequence) % 8 != 0:
        binary_sequence += "0" * (8 - (len(binary_sequence) % 8))

    # 3. Convert bit string to integers
    data_codewords = [int(binary_sequence[i:i+8], 2) for i in range(0, len(binary_sequence), 8)]

    # 4. Byte padding with alternating 236 (0xEC) and 17 (0x11)
    pad_bytes = [236, 17]
    p_idx = 0
    while len(data_codewords) < selected_spec['total_data_bytes']:
        data_codewords.append(pad_bytes[p_idx])
        p_idx = (p_idx + 1) % 2 

    # -----------------------------------------------------------------------------
    # STEP 4: REED-SOLOMON EC GENERATION & INTERLEAVING
    # -----------------------------------------------------------------------------
    GF_EXP = [0] * 512
    GF_LOG = [0] * 256
    x = 1
    for i in range(255):
        GF_EXP[i] = x
        GF_LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 285

    for i in range(255, 512):
        GF_EXP[i] = GF_EXP[i - 255]

    def gf_mul(x: int, y: int) -> int:
        if x == 0 or y == 0:
            return 0
        return GF_EXP[GF_LOG[x] + GF_LOG[y]]

    def rs_generator_poly(degree: int):
        poly = [1]
        for i in range(degree):
            next_poly = [0] * (len(poly) + 1)
            for j in range(len(poly)):
                next_poly[j] ^= gf_mul(poly[j], GF_EXP[i])
                next_poly[j + 1] ^= poly[j]
            poly = next_poly
        return poly[::-1]

    def generate_ec_bytes(data_bytes: list, ec_count: int) -> list:
        gen_poly = rs_generator_poly(ec_count)
        msg = data_bytes + [0] * ec_count
        for i in range(len(data_bytes)):
            coef = msg[i]
            if coef != 0:
                for j in range(len(gen_poly)):
                    msg[i + j] ^= gf_mul(gen_poly[j], coef)
        return msg[len(data_bytes):]
    blocks_data = []
    idx = 0

    for _ in range(selected_spec['g1_blocks']):
        blocks_data.append(data_codewords[idx : idx + selected_spec['g1_bytes']])
        idx += selected_spec['g1_bytes']

    for _ in range(selected_spec['g2_blocks']):
        blocks_data.append(data_codewords[idx : idx + selected_spec['g2_bytes']])
        idx += selected_spec['g2_bytes']

    blocks_ec = [generate_ec_bytes(b_data, selected_spec['ec_per_block']) for b_data in blocks_data]

    interleaved_data = []
    max_data_len = max(len(b) for b in blocks_data)
    for i in range(max_data_len):
        for b in blocks_data:
            if i < len(b):
                interleaved_data.append(b[i])

    interleaved_ec = []
    max_ec_len = max(len(b) for b in blocks_ec)
    for i in range(max_ec_len):
        for b in blocks_ec:
            if i < len(b):
                interleaved_ec.append(b[i])

    final_payload = interleaved_data + interleaved_ec

    print(f"[+] Total Blocks: {len(blocks_data)}")
    print(f"[+] Interleaved Data Bytes: {len(interleaved_data)}")
    print(f"[+] Interleaved EC Bytes: {len(interleaved_ec)}")
    print(f"[+] Final Matrix Payload Stream Length: {len(final_payload)} bytes")

    # -----------------------------------------------------------------------------
    # STEP 5: MATRIX INITIALIZATION & FUNCTIONAL PATTERNS
    # -----------------------------------------------------------------------------
    size = 4 * selected_version + 17
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    is_reserved = [[False for _ in range(size)] for _ in range(size)]

    def set_module(r, c, val, reserve=True):
        if 0 <= r < size and 0 <= c < size:
            matrix[r][c] = val
            is_reserved[r][c] = reserve

    def draw_finder_pattern(row, col):
        for r in range(-1, 8):
            for c in range(-1, 8):
                if row + r < 0 or row + r >= size or col + c < 0 or col + c >= size:
                    continue
                is_black = (
                    (0 <= r <= 6 and c in [0, 6]) or
                    (0 <= c <= 6 and r in [0, 6]) or
                    (2 <= r <= 4 and 2 <= c <= 4)
                )
                set_module(row + r, col + c, 1 if is_black else 0)

    def draw_alignment_pattern(row, col):
        for r in range(-2, 3):
            for c in range(-2, 3):
                is_black = (r in [-2, 2] or c in [-2, 2] or (r == 0 and c == 0))
                set_module(row + r, col + c, 1 if is_black else 0)

    # 1. Finder Patterns (Top-Left, Top-Right, Bottom-Left)
    draw_finder_pattern(0, 0)
    draw_finder_pattern(0, size - 7)
    draw_finder_pattern(size - 7, 0)

    # 2. Alignment Patterns
    alignment_coords = {
        1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30],
        6: [6, 34], 7: [6, 22, 38]
    }
    centers = alignment_coords.get(selected_version, [])
    for r in centers:
        for c in centers:
            if not ((r < 10 and c < 10) or (r < 10 and c > size - 10) or (r > size - 10 and c < 10)):
                draw_alignment_pattern(r, c)

    # 3. Timing Patterns
    for i in range(8, size - 8):
        if not is_reserved[6][i]:
            set_module(6, i, 1 if i % 2 == 0 else 0)
        if not is_reserved[i][6]:
            set_module(i, 6, 1 if i % 2 == 0 else 0)

    # 4. Dark Module
    set_module((4 * selected_version) + 9, 8, 1)

    # 5. Format String Reservation
    for i in range(9):
        set_module(8, i, 0)
        set_module(i, 8, 0)
    for i in range(size - 8, size):
        set_module(8, i, 0)
        set_module(i, 8, 0)

    # 6. Version String Reservation (Only Version 7)
    if selected_version == 7:
        for i in range(18):
            bl_x = i // 3
            bl_y = (size - 11) + (i % 3)
            set_module(bl_y, bl_x, 0)
            
            tr_y = i // 3
            tr_x = (size - 11) + (i % 3)
            set_module(tr_y, tr_x, 0)

    # -----------------------------------------------------------------------------
    # STEP 6: DATA PLACEMENT (Zig-Zag)
    # -----------------------------------------------------------------------------
    bit_stream = "".join(f"{b:08b}" for b in final_payload)
    remainder_bits = {2: 7, 3: 7, 4: 7, 5: 7, 6: 7, 7: 0}.get(selected_version, 0)
    bit_stream += "0" * remainder_bits

    bit_idx = 0
    row = size - 1
    col = size - 1
    upward = True

    while col > 0:
        if col == 6:  
            col -= 1
        
        for _ in range(size):
            for c in range(2):
                c_actual = col - c
                if not is_reserved[row][c_actual]:
                    bit = int(bit_stream[bit_idx]) if bit_idx < len(bit_stream) else 0
                    matrix[row][c_actual] = bit
                    bit_idx += 1
            
            row += -1 if upward else 1
            if row < 0 or row >= size:
                row += 1 if upward else -1
                upward = not upward
                col -= 2
                break

    # -----------------------------------------------------------------------------
    # STEP 7 & 8: MASKING & FORMAT INFORMATION
    # -----------------------------------------------------------------------------
    MASK_ID = 0

    for r in range(size):
        for c in range(size):
            if not is_reserved[r][c]:
                if (r + c) % 2 == 0:
                    matrix[r][c] ^= 1

    ec_bits = {'L': 1, 'M': 0, 'Q': 3, 'H': 2}[ec_level]
    format_data = (ec_bits << 3) | MASK_ID

    format_bch = format_data << 10
    for i in range(4, -1, -1):
        if (format_bch >> (i + 10)) & 1:
            format_bch ^= (1335 << i)
            
    format_bits = ((format_data << 10) | format_bch) ^ 0x5412
    format_str = f"{format_bits:015b}"

    format_order_r1 = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8), (7, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)]
    format_order_r2 = [(8, size - 1), (8, size - 2), (8, size - 3), (8, size - 4), (8, size - 5), (8, size - 6), (8, size - 7), (8, size - 8), (size - 7, 8), (size - 6, 8), (size - 5, 8), (size - 4, 8), (size - 3, 8), (size - 2, 8), (size - 1, 8)]

    for i in range(15):
        matrix[format_order_r1[i][0]][format_order_r1[i][1]] = int(format_str[i])
        matrix[format_order_r2[i][0]][format_order_r2[i][1]] = int(format_str[i])

    # Version String Placement (Only Version 7)
    if selected_version == 7:
        # 18-bit BCH for Version 7: 0x07C94 (LSB to MSB array mapping)
        v_bits_lsb_first = [0,0,1,0,1,0,0,1,0,0,1,1,1,1,1,0,0,0]
        
        for i in range(18):
            bl_x = i // 3
            bl_y = (size - 11) + (i % 3)
            matrix[bl_y][bl_x] = v_bits_lsb_first[i]
            
            tr_y = i // 3
            tr_x = (size - 11) + (i % 3)
            matrix[tr_y][tr_x] = v_bits_lsb_first[i]

    # -----------------------------------------------------------------------------
    # STEP 9: FINAL RENDERING TO IMAGE
    # -----------------------------------------------------------------------------
    quiet_zone = 4
    full_size = size + 2 * quiet_zone
    module_px = 10 
    img_size = full_size * module_px

    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    for r in range(size):
        for c in range(size):
            if matrix[r][c] == 1:
                x0 = (c + quiet_zone) * module_px
                y0 = (r + quiet_zone) * module_px
                x1 = x0 + module_px
                y1 = y0 + module_px
                draw.rectangle([x0, y0, x1, y1], fill="black")
    import sys
    import io

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
        
    return img_io