import reader
import lineLexer

with open('content.txt') as f:
    lr = reader.get_line_reader(f)
    lts = lineLexer.get_line_tokens(lr)
    for token in lts:
        print(token)
