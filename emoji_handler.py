import re

def replace_wyylde_emojis(html_content):
    """
    Remplace les emojis Wyylde et Emojione dans le contenu HTML par un format texte standardisé.
    
    Exemples :
    - <img src="/images/smilies/coeur.gif" class="emojione smilWyylde vaM">  → "smilWyylde#coeur"
    - <img src="/images/emojione/2764.png" class="emojione vaM">  → "emojiOne#2764"
    - <em class="emojione">✨</em>  → ✨ (Conserve uniquement l'emoji)
    """

    # 🔹 1. Remplacement des emojis Wyylde
    wyylde_pattern = r'<img [^>]*?src=["\']/images/smilies/([^.]+)\.gif["\'][^>]*?>'
    
    def wyylde_replacer(match):
        """Transforme un emoji Wyylde en texte"""
        emoji_name = match.group(1)  # Extrait le nom (ex: "coeur")
        return f" smilWyylde#{emoji_name} "  # Format standardisé

    html_content = re.sub(wyylde_pattern, wyylde_replacer, html_content)

    # 🔹 2. Remplacement des images Emojione
    emojione_pattern = r'<img [^>]*?src=["\']/images/emojione/(\w+)\.png["\'][^>]*?>'

    def emojione_replacer(match):
        """Transforme un emoji Emojione en texte"""
        emoji_code = match.group(1)  # Extrait le code Unicode (ex: "2764" pour ❤️)
        return f" emojiOne#{emoji_code} "  # Format standardisé

    html_content = re.sub(emojione_pattern, emojione_replacer, html_content)

    # 🔹 3. Suppression des balises <em class="emojione"> tout en conservant leur contenu Unicode
    emojione_em_pattern = r'<em class=["\']emojione["\'][^>]*?>(.*?)<\/em>'

    def emojione_em_replacer(match):
        """Supprime la balise <em> en gardant l'emoji Unicode"""
        return match.group(1)  # Conserve uniquement l'emoji

    html_content = re.sub(emojione_em_pattern, emojione_em_replacer, html_content)

    return html_content.strip()
