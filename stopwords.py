from HindiTokenizer import Tokenizer

t=Tokenizer("यह वाक्य हिन्दी में है।")
#t=Tokenizer()
#t.read_from_file('filename_here') // t.read_from_file('hindi_file.txt')

#to generate sentences
print(t.generate_sentences())

