import struct

dd = 0x00    # Usually a value to write to register aa
aa = 0x00    # Usually a register to write value dd to
nn = 0x00    # Usually a number
tt = 0x00    # Usually data type that is used in command 0x67
ss = 0x00    # Usually data size that is used in command 0x67
data = 0x00  # Usually data in data block
cc = 0x00    # Usually chip type
oo = 0x00    # Usually offset to write or read data from and to
pp = 0x00    # Usually a port number
chip_types_header_order = ['SN76489',  'YM2413',   'YM2612',     'YM2151',   'RF5C68',
                           'YM2203',   'YM2608',   'YM2610/B',   'YM3812',   'YM3526',
                           'Y8950',    'YMF262',   'YMF278B',    'YMF271',   'YMZ280B',
                           'RF5C164',  'PWM',      'AY8910',     'GB DMG',   'NES APU',
                           'MultiPCM', 'uPD7759',  'OKIM6258',   'OKIM6295', 'K051649',
                           'K054539',  'HuC6280',  'C140',       'K053260',  'Pokey',
                           'Q-Sound',  'SCSP',     'WonderSwan', 'VSU',      'SAA1099',
                           'ES5503',   'ES5505/6', 'X1-010',     'C352',     'GA20',
                           'Mikey']
data_types_base = ['YM2612 PCM data',     'RF5C68 PCM data',  'RF5C164 PCM data',  'PWM PCM data',
                   'OKIM6258 ADPCM data', 'HuC6280 PCM data', 'SCSP PCM data',     'NES APU DPCM data']
data_types_comp = ['Compressed YM2612 PCM data', 'Compressed RF5C68 PCM data',     'Compressed RF5C164 PCM data',
                   'Compressed PWM PCM data',    'Compressed OKIM6258 ADPCM data', 'Compressed HuC6280 PCM data',
                   'Compressed SCSP PCM data',   'Compressed NES APU DPCM data',   'Unimplemented compressed data']
data_types_cont = ['Sega PCM ROM data',               'YM2608 DELTA-T ROM data', 'YM2610 ADPCM ROM data',
                   'YM2610 DELTA-T ROM data',         'YMF278B ROM data',        'YMF271 ROM data',
                   'YMZ280B ROM data',                'YMF278B RAM data',        'Y8950 DELTA-T ROM data',
                   'MultiPCM ROM data',               'uPD7759 ROM data',        'OKIM6295 ROM data',
                   'K054539 ROM data',                'C140 ROM data',           'K053260 ROM data',
                   'Q-Sound ROM data',                'ES5505/ES5506 ROM data',  'X1-010 ROM data',
                   'C352 ROM data',                   'GA20 ROM data']
data_types_writes = ['RF5C68 RAM write', 'RF5C164 RAM write', 'NES APU RAM write', 'Unknown chip RAM write',
                     'SCSP RAM write',   'ES5503 RAM write',  'Unknown chip RAM write']
vgm_commands_ids = [0x31,  # AY Stereo Mask. Format: 0x31 dd
                    0x40,  # Mikey, write value dd to register aa.                Format: 0x40 aa dd
                    0x4F,  # Game Gear PSG stereo, write dd to port 0x06.         Format: 0x4F dd
                    0x50,  # PSG (SN76489/SN76496) write value dd.                Format: 0x50 dd
                    0x51,  # YM2413, write value dd to register aa.               Format: 0x51 aa dd
                    0x52,  # YM2612 port 0, write value dd to register aa.        Format: 0x52 aa dd
                    0x53,  # YM2612 port 1, write value dd to register aa.        Format: 0x53 aa dd
                    0x54,  # YM2151, write value dd to register aa.               Format: 0x54 aa dd
                    0x55,  # YM2203, write value dd to register aa.               Format: 0x55 aa dd
                    0x56,  # YM2608 port 0, write value dd to register aa.        Format: 0x56 aa dd
                    0x57,  # YM2608 port 1, write value dd to register aa.        Format: 0x57 aa dd
                    0x58,  # YM2610 port 0, write value dd to register aa.        Format: 0x58 aa dd
                    0x59,  # YM2610 port 1, write value dd to register aa.        Format: 0x59 aa dd
                    0x5A,  # YM3812 (OPL), write value dd to register aa.         Format: 0x5A aa dd
                    0x5B,  # YM3526 (OPL2), write value dd to register aa.        Format: 0x5B aa dd
                    0x5C,  # Y8950 (MSX-AUDIO), write value dd to register aa.    Format: 0x5C aa dd
                    0x5D,  # YMZ280B, write value dd to register aa.              Format: 0x5D aa dd
                    0x5E,  # YMF262 (OPL3) port 0, write value dd to register aa. Format: 0x5E aa dd
                    0x5F,  # YMF262 (OPL3) port 1, write value dd to register aa. Format: 0x5F aa dd
                    0x61,  # Wait n samples.                                      Format: 0x61 nn nn
                    0x62,  # wait 735 samples (60th of a second)                  Format: 0x62
                    0x63,  # wait 882 samples (50th of a second)                  Format: 0x63
                    0x66,  # IMPORTANT: end of sound data                         Format: 0x66

                    0x67,  # IMPORTANT: data block.    Format: 0x67 0x66 tt ss ss ss ss data
                           # t is data type, s is data size, data is data itself of size s

                    0x68,  # IMPORTANT: PCM RAM write. Format: 0x68 0x66 cc oo oo oo dd dd dd ss ss ss
                           # c is chip type,         | o is read offset in data block
                           # same as data block type | d is write offset in chip's ram
                           #                         | (affected by chip's registers)
                           # s is size of data, in bytes
                           # Since size can't be zero, a size of 0 bytes means 0x0100 0000 bytes.

                    # Wait N+1 Samples Commands
                    0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F,

                    # YM2612 port 0 address 2A write from the data bank, then wait n samples
                    0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F,

                    # DAC Stream Control Write. 4 Operands
                    # Usage:

                    # Setup stream:
                    #  0x90 ss tt pp cc
                    #      ss = Stream ID, FF is reserved and ignored
                    #      tt = Chip Type (see clock-order in header, e.g. YM2612 = 0x02)
                    #            bit 7 is used to select the 2nd chip
                    #      pp cc = write command/register cc at port pp
                    #      Note: For chips that use Channel Select Registers (like the RF5C-family
                    #            and the HuC6280), the format is pp cd where pp is the channel
                    #            number, c is the channel register and d is the data register.
                    #            If you set pp to FF, the channel select write is skipped.

                    # Set stream data:
                    #  0x91 ss dd ll bb
                    #      ss = Stream ID, FF is reserved and ignored
                    #      dd = Data Bank ID (see data block types 0x00..0x3f)
                    #      ll = Step Size (how many data is skipped after every write, usually 1)
                    #            Set to 2, if you're using an interleaved stream (e.g. for
                    #             left/right channel).
                    #      bb = Step Base (data offset added to the Start Offset when starting
                    #            stream playback, usually 0)
                    #            If you're using an interleaved stream, set it to 0 in one stream
                    #            and to 1 in the other one.
                    #      Note: Step Size/Step Step are given in command-data-size
                    #             (i.e. 1 for YM2612, 2 for PWM), not bytes

                    # Set stream frequency:
                    #  0x92 ss ff ff ff ff
                    #      ss = Stream ID, FF is reserved and ignored
                    #      ff = Frequency (or Sample Rate, in Hz) at which the writes are done

                    # Start stream:
                    #  0x93 ss aa aa aa aa mm ll ll ll ll
                    #      ss = Stream ID
                    #      aa = Data Start offset in data bank (byte offset in data bank)
                    #            Note: if set to -1, the Data Start offset is ignored
                    #      mm = Length Mode (how the Data Length is calculated)
                    #            00 - ignore (just change current data position)
                    #            01 - length = number of commands
                    #            02 - length in msec
                    #            03 - play until end of data
                    #            1? - (bit 4) Reverse Mode
                    #            8? - (bit 7) Loop (automatically restarts when finished)
                    #      ll = Data Length

                    # Stop stream:
                    #  0x94 ss
                    #      ss = Stream ID
                    #            Note: 0xFF stops all streams

                    # Start stream (fast call):
                    #  0x95 ss bb bb ff
                    #      ss = Stream ID
                    #      bb = Block ID (number of the data block that is part of the data bank set
                    #            with command 0x91)
                    #      ff = Flags
                    #            bit 0 - Loop (see command 0x93, mm bit 7)
                    #            bit 4 - Reverse Mode (see command 0x93)
                    0x90, 0x91, 0x92, 0x93, 0x94, 0x95,
                    0xA0,
                    0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF,
                    0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8,
                    0xE0, 0xE1]
vgm_commands_bytes = [2,                                               # 0x31
                      2, 1,                                            # 0x40-0x4F
                      1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 0x50-0x5F
                      2, 0, 0, 0, 6, 10,                               # 0x60-0x6F
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x70-0x7F
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x80-0x8F
                      4, 4, 5, 10, 1, 4,                               # DAC Stream control
                      2,                                               # 0xA0
                      2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 0xB0-0xBF
                      3, 3, 3, 3, 3, 3, 3, 3,                          # 0xC0-0xC8
                      3, 3, 3, 3, 3, 3, 3,                             # 0xD0-0xD6
                      4, 4                                             # 0xE0-0xE1
                      ]
file_path = input("Path to VGM file: ")
metadata = {}
with open(file_path, 'rb') as f:
    header = f.read()

    print(f'VGM Length: {hex(len(header))}')
    # Extracting relevant data from VGM
    metadata['VGMID'] = header[0:4].decode('utf-8')
    metadata['EOFOffset'] = struct.unpack('<I', header[0x04:0x08])[0] + 0x04
    metadata['Version'] = struct.unpack('<I', header[0x08:0x0C])[0]
    metadata['DataOffset'] = struct.unpack('<I', header[0x34:0x38])[0] + 0x34
    print(f"VGM Info: \nSignature: '{metadata['VGMID']}'\nEnd-of-file Offset: {metadata['EOFOffset']}")
    if metadata['Version'] == 0x100:
        print("VGM Version is 1.00!.. Header size 0x40")
        offset = 0x40
    elif metadata['Version'] == 0x101:
        print("VGM Version is 1.01!.. Header size 0x40")
        offset = 0x40
    elif metadata['Version'] == 0x110:
        print("VGM Version is 1.10!.. Header size 0x40")
        offset = 0x40
    elif metadata['Version'] == 0x150:
        print(f"VGM Version is 1.50!.. Data offset {hex(metadata['DataOffset'])}")
        offset = metadata['DataOffset']
    elif metadata['Version'] == 0x151:
        print(f"VGM Version is 1.51!.. Data offset {hex(metadata['DataOffset'])}")
        offset = metadata['DataOffset']
    elif metadata['Version'] == 0x160:
        print(f"VGM Version is 1.60!.. Data offset {hex(metadata['DataOffset'])}")
        offset = metadata['DataOffset']
    elif metadata['Version'] == 0x161:
        print(f"VGM Version is 1.61!.. Data offset {hex(metadata['DataOffset'])}")
        offset = metadata['DataOffset']
    elif metadata['Version'] == 0x170:
        print(f"VGM Version is 1.70!.. Data offset {hex(metadata['DataOffset'])}")
        offset = metadata['DataOffset']
    elif metadata['Version'] == 0x171:
        print(f"VGM Version is 1.71!.. Data offset {hex(metadata['DataOffset'])}")
        offset = metadata['DataOffset']
    elif metadata['Version'] == 0x172:
        print(f"VGM Version is 1.72!.. Data offset {hex(metadata['DataOffset'])}")
        offset = metadata['DataOffset']
    data_block = 0
    while True:
        metadata['CommandID'] = header[offset]
        print(hex(metadata['CommandID']))
        metadata['NextByte'] = header[offset + 0x01]
        print('next byte ', hex(metadata['NextByte']))
        DataBlockType = 'Unknown'
        if (metadata['CommandID'] == 0x67) and (metadata['NextByte']) == 0x66:
            print('Data block command found!')
            metadata['DataBlockType'] = header[offset + 0x02]
            if metadata['DataBlockType'] >= 0x80:
                DataBlockType = data_types_cont[metadata['DataBlockType'] - 0x80]
            elif metadata['DataBlockType'] in range(0x40, 0x47):
                DataBlockType = data_types_comp[metadata['DataBlockType'] - 0x40]
            elif metadata['DataBlockType'] in range(0x48, 0x7F):
                DataBlockType = data_types_comp[8]
            elif metadata['DataBlockType'] in range(0x00, 0x07):
                DataBlockType = data_types_base[metadata['DataBlockType']]
            elif metadata['DataBlockType'] in range(0x08, 0x3F):
                DataBlockType = data_types_base[8]
            print(f'Data block type: {hex(metadata['DataBlockType'])}, {DataBlockType}')
            print(f'{hex(header[offset])} {hex(header[offset] + 0x01)} '
                  f'{hex(header[offset + 0x02])} '
                  f'{hex(header[offset + 0x03])} {hex(header[offset + 0x04])} {hex(header[offset + 0x05])} {hex(header[offset + 0x06])}')
            metadata['DataBlockSize'] = struct.unpack('<I', header[offset + 0x03:offset + 0x07])[0]
            print(f'Data block size: {hex(metadata['DataBlockSize'])} bytes')
            print(f'Data block ends at: {hex(metadata['DataBlockSize'] + offset + 0x03)}')
            print(f'Data block start offset: {hex(offset + 0x07)}')
            pcm_data = header[offset + 0x0E:offset + 0x07 + metadata['DataBlockSize']]
            offset += 0x07 + metadata['DataBlockSize']
            with open(f'{file_path}_data_block_{hex(data_block)}.raw', 'wb') as g:
                print(f'opened data_block_{hex(data_block)}.raw for writing')
                g.write(pcm_data)
                print(f'wrote to data_block_{hex(data_block)}.raw')
                g.close()
                print(f'closed data_block_{hex(data_block)}.raw')
            data_block += 1
        else:
            print('wtf nothing found wtfffff omagaaaahhh')
            break
