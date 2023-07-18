from pympq.MpqArchive import MpqArchive

if __name__ == '__main__':
    with MpqArchive('/home/user/.wine/drive_c/Program Files (x86)/WoW/Data/interface.MPQ') as archive:
        for i, entry in enumerate(archive.mpq_entries):
            try:
                file_bytes = archive.read_file_bytes(entry)
                if not file_bytes:
                    continue
                with open(f'{entry.filename}', 'wb') as f:
                    f.write(file_bytes)
            except:
                print(f'Skipped entry {i}, no filename.')
