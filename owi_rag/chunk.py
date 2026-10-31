def chunk(text, size=220, overlap=40):
    # shortcut: words stand in for tokens (220 words ~ 300 tokens), upgrade if token-exact sizes matter
    w = text.split()
    return [" ".join(w[i : i + size]) for i in range(0, max(len(w) - overlap, 1), size - overlap)
            if w[i : i + size]]
