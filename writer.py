class Writer:
    def __init__(self, fp):
        self.fp = fp

        self.file = open(self.fp, 'w', encoding='utf-8')

    def write(self, message):
        self.file.write(message + "\n")

    def new_test_file(self, file_name):
        self.file.write("\n\nФайл для проверки " + file_name + ":\n")

    def close(self):
        self.file.close()
