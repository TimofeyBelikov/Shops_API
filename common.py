def make_lines_reader(fobj, number_of_lines):
    def reader():
        lines = [line for line in (fobj.readline() for _ in range(number_of_lines))]
        return ''.join(lines)
    return reader

def make_lines_reader_from_end(fobj, number_of_lines):
    def reader():
        # Список для хранения считанных строк
        lines = []
        # Смещаем указатель файла в конец
        fobj.seek(0, 2)
        # Начинаем считывать строки с конца файла
        for _ in range(number_of_lines):
            # Перемещаем указатель на одну позицию назад
            fobj.seek(-1, 1)
            # Читаем символ
            char = fobj.read(1)
            # Если символ - перевод строки, читаем строку и добавляем её в список
            if char == '\n':
                lines.append(fobj.readline())
            else:
                # Если символ не является переводом строки, значит мы дошли до начала файла
                break
        # Инвертируем порядок строк, так как мы считываем их с конца
        lines.reverse()
        return ''.join(lines)
    return reader