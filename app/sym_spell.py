from symspellpy import SymSpell

async def get_sym_spell():
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

    dictionary_path = "app/data/frequency_dictionary_en_82_765.txt"
    bigram_path = "app/data/frequency_bigramdictionary_en_243_342.txt"

    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
    sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)
    
    print("sym_spell is loaded")
    return sym_spell