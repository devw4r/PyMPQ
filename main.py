from pympq.MpqArchive import MpqArchive

if __name__ == '__main__':
    archive = MpqArchive('/home/user/.wine/drive_c/Program Files (x86)/WoW/Data/interface.MPQ')
    archive.initialize()
    for i, entry in enumerate(archive.mpq_entries):
        try:
            filename = entry.get_filename().rsplit("\\")[-1]
            file_bytes = archive.read_file_bytes(entry)
            if file_bytes:
                with open(f'{filename}', 'wb') as f:
                    f.write(file_bytes)
        except:
            print(f'Skipped entry {i}, no filename.')
