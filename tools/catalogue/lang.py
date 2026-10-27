"""Italian or English: the words of EUROSTAMP's bilingual catalogue (IT / EN) told apart by their frequency in each
language (wordfreq), with the catalogue's own abbreviations and the names that belong to neither."""
import re
import wordfreq

# words the frequency lists get wrong for this catalogue
IT_WORDS = {"fraz", "sez", "scarp", "pag", "vedi", "mmq", "piegatrici", "punzone", "punzoni", "matrice", "matrici",
            "frazionatura", "frazionature", "scarpetta", "scarpette", "inserti", "inserto", "porta", "portainserti",
            "temprato", "induzione", "bonificato", "aperto", "chiuso", "spinta", "testa", "richiesta", "tagli",
            "lunghezze", "lunghezza", "modifiche", "modifica", "raggio", "mobili", "trafilati", "attacchi", "codolo",
            "codoli", "intermedi", "intermedio", "staffa", "staffe", "morsetto", "morsetti", "sicurezza", "pulsante",
            "lama", "piegaschiaccia", "spessore", "schiacciatura", "sezionato", "sezionata", "sezionati", "fresatura",
            "alt", "larg", "corsa", "cuneo", "cunei", "bombatura", "adattatore", "adattatori", "inferiore",
            "superiore", "inferiori", "superiori", "regolabile", "regolabili", "pneumatico", "pneumatici",
            "manuale", "manuali", "ricambi", "ricambio", "accessori", "gommini", "gommino", "poliuretano",
            "nylon", "protezione", "pellicola", "rotolo", "tendipellicola", "squadra", "squadre", "goniometro"}
EN_WORDS = {"sect", "horn", "horns", "punch", "punches", "die", "dies", "tang", "tangs", "holder", "holders", "clamp",
            "clamps", "adaptor", "adaptors", "adapter", "adapters", "insert", "inserts", "gooseneck", "radius", "style",
            "hemming", "flattening", "segmentation", "sectioned", "intermediate", "intermediates", "tooling", "max",
            "mat", "tempered", "induction", "hardened", "thickness", "weigh", "weight", "length", "lengths", "kg",
            "mm", "load", "head", "open", "closed", "film", "cloth", "rod", "rods", "roll", "rolls", "urethane"}
NEUTRAL = {"amada", "promecam", "trumpf", "wila", "bystronic", "beyeler", "lvd", "euro", "eurostamp", "eurogrip",
           "tooling", "c45", "42crmo4", "hrc", "pss", "ppm", "esh", "v", "r", "h", "b", "l", "t", "m", "x", "s", "ri",
           "ton", "max", "mat", "rf", "rfa", "rg", "ras", "safan", "darley", "colgar", "gasparini", "ermaksan",
           "durmazlar", "baykal", "dener", "yawei", "salvagnini", "farina", "gade", "boschert", "boutillon",
           "coastone", "deratech", "oriance", "prima", "power", "rico", "rpc", "schiavi", "smd", "sorg", "somo",
           "vicla", "vimercati", "warcom", "yangli", "ysde", "hammerle", "haco", "cincinnati", "accurpress"}


def word_lang(w):
    w = w.lower().strip("’'.")
    if len(w) < 2 or w in NEUTRAL or re.fullmatch(r"[\d,.x×]+", w):
        return None
    if w in IT_WORDS:
        return "it"
    if w in EN_WORDS:
        return "en"
    e, i = wordfreq.zipf_frequency(w, "en"), wordfreq.zipf_frequency(w, "it")
    if i > e + 0.8:
        return "it"
    if e > i + 0.8:
        return "en"
    if re.search(r"[àèéìòù]$", w):
        return "it"
    return None


def text_lang(t):
    """'it', 'en', 'mixed' or None (numbers, codes, names)"""
    langs = [word_lang(w) for w in re.findall(r"[A-Za-zÀ-ÿ’']+\.?", t)]
    it, en = langs.count("it"), langs.count("en")
    if it and not en:
        return "it"
    if en and not it:
        return "en"
    if it and en:
        return "mixed"
    return None
