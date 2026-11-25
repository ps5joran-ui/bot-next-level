import discord
from discord.ext import commands
from discord import app_commands
import re
import json
import os

# ============================================
# BOT "ASSISTANCE NEXT LEVEL"
# Discord Bot pour le serveur Next Level
# ============================================

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ============================================
# SYSTÈME D'AVERTISSEMENTS
# ============================================
WARNS_FILE = "warns.json"

def load_warns():
    if os.path.exists(WARNS_FILE):
        with open(WARNS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_warns(warns):
    with open(WARNS_FILE, "w") as f:
        json.dump(warns, f)

# ============================================
# MOTS-CLÉS INSULTES (AUTO-MODÉRATION)
# ============================================
INSULTES = [
    "fdp", "ntm", "tg", "pd", "ptn", "connard", "conard", "conar", "connasse",
    "conasse", "conace", "pute", "salope", "salop", "enculé", "enculer", "encule",
    "enkulé", "nique", "niquer", "niqué", "niké", "niker", "bâtard", "batard",
    "batar", "fils de pute", "fils de", "ta mère", "ta mere", "tamere", "ta mer",
    "ta race", "tarace", "sale merde", "va te faire", "vtf", "vtff", "va mourir",
    "crève", "creve", "bouffon", "boufon", "abruti", "débile", "debile", "crétin",
    "cretin", "imbécile", "imbecile", "enfoiré", "enfoire", "anfoiré", "pédé",
    "pede", "pédale", "pedale", "tapette", "tapet", "tafiole", "tarlouze",
    "lopette", "triso", "mongol", "mongole", "attardé", "attarde", "gogol",
    "gogole", "tocard", "tokar", "minable", "déchet", "déché", "ordure",
    "pourriture", "pourri", "pouri", "dégage", "degage", "casse-toi", "casse toi",
    "barre-toi", "barre toi", "ferme ta gueule", "ferme ta geule", "ftg",
    "ta gueule", "ta geule", "stfu", "shut up", "fuck", "fuk", "fck", "bitch",
    "bich", "shit", "asshole", "dick", "nigga", "negro", "pétasse", "petasse",
    "grognasse", "grognace", "nazi", "nazy", "raciste", "rasiste", "homophobe",
    "omofobe", "suceur", "suceuse", "ntm", "ntm", "fils de chien"
]

# ============================================
# MOTS-CLÉS AUTO-RÉPONSES
# ============================================

KEYWORDS = {
    "livraison": {
        "mots": [
            "livraison", "livré", "livrée", "livrer", "livraisons", "livrason",
            "livrezon", "livraizon", "livrison", "livreson", "livraisont", "livree",
            "livrè", "délai", "délais", "delai", "delais", "delay", "delait",
            "combien de temps", "quand je reçois", "quand je recois", "quand je recoi",
            "envoi", "envoyé", "envoyer", "envoyee", "envoye", "anvoi", "anvoyé",
            "expédition", "expédié", "expedition", "expedie", "expedié", "colis",
            "collis", "colie", "coli", "suivi", "suivie", "suivis", "suivit",
            "tracking", "traking", "transporteur", "shipping", "delivery", "delivry",
            "pas reçu", "pas recu", "pa recu", "pa reçu", "en retard", "en retar",
            "retard", "j'attends", "jattends", "jaten", "jatend", "jatten",
            "ça arrive quand", "sa arrive quand", "ca arrive quand", "sa arive quand",
            "ça met combien", "sa met combien", "ca met combien", "temps de livraison",
            "temp de livraison", "réception", "reception", "reseption", "recevoir",
            "ressevoir", "en chemin", "en route", "en transit", "combien de jours",
            "combien de jour", "conbien de jour", "conbien de jours", "semaine",
            "semaines", "long", "trop long", "c'est long", "cé long", "sé long",
            "rapide", "express", "urgent", "urgen", "ouvré", "ouvrés", "jours ouvrés",
            "jour ouvré"
        ],
        "reponse": "🚚 **Délais de livraison : 7 à 13 jours ouvrés** 📦"
    },

    "paiement": {
        "mots": [
            "paiement", "payement", "paieman", "paiment", "paimant", "payment",
            "payer", "payé", "payee", "paye", "paié", "paier", "carte", "karte",
            "CB", "cb", "visa", "viza", "mastercard", "mastercar", "masterkard",
            "paypal", "payepal", "paypale", "pay pal", "apple pay", "applepay",
            "google pay", "googlepay", "virement", "viremen", "virmant", "moyens de paiement",
            "moyen de paiement", "comment payer", "commen payer", "coment payer",
            "paiement refusé", "paiement refuse", "erreur paiement", "transaction",
            "transaxion", "sécurisé", "securisé", "securise", "sécurité", "securité",
            "securite", "acheter", "acheté", "achete", "achetter", "achat", "acha",
            "commander", "commandé", "commande", "comande", "comander", "carte bancaire",
            "carte banquaire", "carte bankaire", "carte bleue", "carte bleu",
            "carte de crédit", "carte de credit", "crédit", "credit", "débit", "debit",
            "facture", "factur", "refusé", "refuse", "décliné", "decline",
            "marche pas", "marche pa", "fonctionne pas", "fonctionne pa", "bug",
            "erreur", "ereur", "problème paiement", "probleme paiement",
            "impossible de payer", "je peux pas payer", "jpeux pas payer",
            "ça passe pas", "sa passe pas", "ca passe pas", "panier", "panié",
            "ajouter au panier", "finaliser", "passer commande", "débité", "debité",
            "prélevé", "preleve", "montant", "montan", "total", "totale"
        ],
        "reponse": "💳 **Moyens de paiement acceptés :**\n✅ Carte bancaire (Visa, Mastercard)\n✅ PayPal\n✅ Apple Pay / Google Pay\n🔒 Paiements 100% sécurisés !\nUn souci ? Demande sur Discord 💬"
    },

    "prix_promo": {
        "mots": [
            "prix", "pris", "pri", "prit", "combien", "conbien", "konbien",
            "combien ça coûte", "combien sa coute", "combien ca coute", "conbien sa coute",
            "coûte", "coute", "cout", "tarif", "tarife", "tarifs", "cher", "chère",
            "trop cher", "pas cher", "pa cher", "réduction", "reduction", "réduc",
            "reduc", "promo", "promos", "promotion", "promotions", "code promo",
            "codepromo", "coupon", "coupons", "remise", "remize", "soldes", "solde",
            "offre", "ofre", "offres", "bon plan", "bonplan", "gratuit", "gratuie",
            "gratos", "free", "frais", "frais de port", "frai de port", "fdp",
            "moins cher", "moin cher", "discount", "diskaunt", "pourcentage",
            "pourcent", "deal", "affaire", "offre spéciale", "offre special",
            "vente flash", "flash", "déstockage", "destockage", "économie",
            "economie", "budget", "budjet", "qualité prix", "qualite prix",
            "vaut le coup", "rentable"
        ],
        "reponse": "💰 **Promos & Bons Plans**\n🔥 Check le salon #annonces pour les codes promo en cours !\n🎁 Deviens VIP pour des réduc exclusives"
    },

    "produits": {
        "mots": [
            "produit", "produits", "produi", "article", "articles", "catalogue",
            "cataloge", "katalog", "collection", "colection", "gamme", "dispo",
            "disponible", "disponibilité", "stock", "stok", "en stock", "rupture",
            "plus de stock", "quoi de neuf", "koi de neuf", "nouveau", "nouveaux",
            "nouvo", "nouveauté", "nouveautés", "nouveaute", "sortie", "sorti",
            "drop", "boutique", "boutik", "butik", "shop", "store", "magasin",
            "magazin", "voir", "regarder", "montrer", "montre", "vous vendez quoi",
            "quoi comme produit", "type de produit", "liste", "photo", "photos",
            "image", "images", "aperçu", "apercu", "qualité", "qualite",
            "matière", "matiere", "led", "LED", "rgb", "RGB", "néon", "neon",
            "projecteur", "projeteur", "casquette", "casket", "kaskette", "cap",
            "t-shirt", "tshirt", "tee-shirt", "hoodie", "hoody", "sweat",
            "accessoire", "accessoires", "gadget", "setup", "sétup", "déco",
            "deco", "décoration", "decoration", "chambre", "ambiance"
        ],
        "reponse": "📦 **Nos produits**\n🎮 Casquettes, projecteurs LED, accessoires gaming & lifestyle\n👀 Découvre tout dans le salon #catalogue !\n🆕 Dernières sorties → #Nouveautés"
    },

    "retour_sav": {
        "mots": [
            "retour", "retours", "retore", "retourner", "retourné", "rembourser",
            "remboursé", "remboursement", "rembourssement", "rembourcement",
            "renbourser", "ranboursement", "échange", "échanger", "echanger",
            "echange", "garantie", "garanti", "défectueux", "defectueux", "cassé",
            "casse", "kasé", "abîmé", "abimé", "endommagé", "endomage",
            "problème", "probleme", "soucis", "souci", "mauvaise taille",
            "erreur", "ereur", "trompé", "tronpé", "pas content", "pa conten",
            "mécontent", "mecontent", "déçu", "decu", "arnaque", "arnak", "arnac",
            "faux", "fausse", "nul", "nule", "mauvais", "movais", "merde",
            "pourri", "pouri", "dégueulasse", "catastrophe", "horrible", "orible",
            "honteux", "inacceptable", "inadmissible", "voleur", "voleurs",
            "escroquerie", "escroc", "eskroc", "menteur", "fausse pub",
            "pas conforme", "pa conforme", "différent", "diferent", "ressemble pas",
            "correspond pas", "satisfait ou remboursé", "réclamation", "reclamation",
            "plainte", "litige", "signaler", "signalé"
        ],
        "reponse": "🔄 **Retours & SAV**\n📩 Contacte-nous sur Discord\n📸 Envoie des photos du problème\n⏰ Réponse sous 24h ! 💪"
    },

    "contact": {
        "mots": [
            "contact", "contacter", "contacté", "kontact", "joindre", "email",
            "e-mail", "mail", "adresse", "adrese", "téléphone", "telephone",
            "telefone", "tel", "numéro", "numero", "support", "suport",
            "service client", "service clien", "aide", "aidé", "aider", "help",
            "besoin d'aide", "bezoin d'aide", "question", "questions", "kestion",
            "répondez", "repondez", "réponse", "reponse", "quelqu'un", "kelkun",
            "y'a quelqu'un", "ya kelkun", "allo", "allô", "alo", "sav", "SAV",
            "réclamation", "reclamation", "parler", "discuter", "humain",
            "vrai personne", "responsable", "gérant", "gerant", "patron", "boss",
            "manager", "comment vous joindre", "dm", "DM", "mp", "MP",
            "message privé", "message prive", "écrire", "ecrire", "envoyer un message"
        ],
        "reponse": "📞 **Contact**\n📩 Écris-nous sur Discord !\n💬 On est là pour t'aider\n⏰ Réponse sous 24h 💪"
    },

    "reseaux": {
        "mots": [
            "instagram", "insta", "ig", "instagramme", "tiktok", "tik tok",
            "tikto", "tiktoc", "tt", "twitter", "snap", "snapchat", "facebook",
            "fb", "fessebook", "youtube", "yt", "you tube", "utube", "réseau",
            "réseaux", "reseau", "reseaux", "rezo", "rézo", "réseaux sociaux",
            "reseaux sociaux", "abonne", "abonner", "abonné", "abonnement",
            "follow", "folow", "suivre", "lien", "liens", "site", "cite",
            "site web", "siteweb", "boutique en ligne", "url", "website", "www",
            ".com", ".fr", "profil", "page", "compte", "chaîne", "chaine",
            "channel", "vidéo", "video", "vidéos", "post", "publication",
            "story", "stories", "reel", "reels", "live", "stream", "streamer",
            "influenceur", "influenceuse", "créateur", "createur", "content creator",
            "collab", "collaboration", "partenariat", "ambassadeur", "sponsor"
        ],
        "reponse": "📱 **Nos réseaux**\n🎵 TikTok : www.tiktok.com/@bobby_miamioff\n🛒 Site : vicedrop.fr\nAbonne-toi pour ne rien rater ! 🔥"
    },

    "regles": {
        "mots": [
            "règle", "règles", "regle", "regles", "règlement", "reglement",
            "interdit", "interdi", "autorisé", "autorise", "ban", "banni",
            "banie", "kick", "kik", "mute", "muté", "warn", "avertissement",
            "avertisement", "modération", "moderation", "modo", "modérateur",
            "moderateur", "admin", "administrateur", "signaler", "signalé",
            "report", "spam", "spame", "pub", "publicité", "insulte", "insulté",
            "respect", "respet", "comportement", "conduite", "charte", "tolérance",
            "tolerance", "sanction", "punition", "exclusion", "virer", "viré",
            "dégagé", "dehors"
        ],
        "reponse": "📜 **Règles du serveur**\nConsulte le salon #règles pour tout savoir !\n✅ Respect entre membres\n✅ Pas de spam ni pub\n✅ Pas de contenu inapproprié\n⚠️ Tout manquement = sanction"
    },

    "vip": {
        "mots": [
            "vip", "VIP", "vipe", "v.i.p", "premium", "prémium", "avantage",
            "avantages", "avantagé", "exclusif", "exklusif", "membre", "fidélité",
            "fidelite", "récompense", "recompense", "cadeau", "kado", "cado",
            "giveaway", "givaway", "give away", "concours", "concour", "conkours",
            "gagner", "gagne", "gagné", "participer", "participé", "tirage",
            "lot", "lucky", "luki", "grade", "rang", "rôle", "role", "rôles",
            "niveau", "nivau", "nivo", "level", "up", "monter", "monté",
            "évoluer", "evoluer", "spécial", "special", "privilège", "privilege",
            "accès", "acces", "salon privé", "salon prive", "privé", "prive",
            "early access", "avant-première", "priorité", "priorite",
            "comment devenir", "devenir vip", "être vip", "passer vip", "upgrade",
            "statut", "statu", "classement", "top", "meilleur", "actif", "aktivité"
        ],
        "reponse": "🏆 **Programme VIP**\n💬 Accès au salon privé exclusif\n🎁 Avantages produits\n💰 Découvre comment générer des revenus avec nous\n➡️ Contacte-nous en privé sur Discord pour en savoir plus ! 🚀"
    },

    "suggestions": {
        "mots": [
            "suggestion", "suggestions", "sujestion", "sugestion", "suggérer",
            "sugerer", "idée", "idee", "idé", "proposer", "proposé", "proposition",
            "avis", "avie", "avi", "feedback", "fidback", "améliorer", "ameliorer",
            "amélioration", "amelioration", "ajouter", "ajouté", "rajouter",
            "rajouté", "j'aimerais", "jaimerais", "je voudrais", "je voudrai",
            "ce serait bien", "se serait bien", "vous devriez", "il faudrait",
            "il fodrait", "manque", "il manque", "opinion", "pensée", "conseil",
            "recommandation", "vote", "voter", "sondage", "demande", "demander"
        ],
        "reponse": "💡 **Une idée ? Une suggestion ?**\n📝 Propose ton idée directement ici !\n💬 Ou envoie-nous un message privé\nOn lit tout ! 👀"
    },

    "salutations": {
        "mots": [
            "salut", "salu", "salue", "hello", "helo", "bonjour", "bonsoir",
            "coucou", "koukou", "cucou", "hey", "yo", "yoo", "yooo", "wesh",
            "wech", "wsh", "ouesh", "slt", "bjr", "bsr", "cc", "re", "ree",
            "merci", "mersi", "merssi", "thanks", "thx", "au revoir", "aurevoir",
            "bye", "bonne nuit", "bonne journée", "bonne journee", "à plus",
            "a plus", "a+", "comment ça va", "comment sa va", "ça va", "sa va",
            "quoi de neuf", "koi de neuf", "bienvenue", "bienvenu", "kikou",
            "hola", "ola", "plop", "ciao", "tchao", "tcho", "bonne soirée",
            "bonne soiree"
        ],
        "reponse": "👋 Yo ! Bienvenue sur **Next Level** ! 🎮\nN'hésite pas à explorer les salons et à participer 💪\n🕹️ Check #catalogue pour voir nos produits !"
    },

    "compliments": {
        "mots": [
            "c'est cool", "c cool", "c kool", "j'adore", "jadore", "trop bien",
            "tro bien", "stylé", "style", "stilé", "fire", "faya", "goat", "GOAT",
            "incroyable", "magnifique", "beau", "bo", "belle", "ouf", "lourd",
            "lour", "dingue", "malade", "malad", "sick", "top", "au top", "o top",
            "parfait", "parfé", "génial", "genial", "super", "excellent", "wow",
            "wahou", "waouh", "grave bien", "trop beau", "trop bo", "j'aime",
            "jaime", "classe", "klass", "dope", "fresh", "nice", "naice", "cool",
            "kool", "bravo", "respect", "big up", "bigup", "GG", "gg",
            "bien joué", "chapeau"
        ],
        "reponse": "🔥 Merci pour le soutien ! On est là pour vous 💪\nAbonne-toi sur TikTok @bobby_miamioff 🚀"
    },

    "emojis_reactions": {
        "mots": [
            "lol", "LOL", "lool", "loool", "mdr", "MDR", "mdrrr", "mdrr",
            "ptdr", "PTDR", "ptdrrr", "xd", "XD", "haha", "hahaha", "hihi",
            "héhé", "hehe", "lmao", "lmfao", "rofl", "dead", "ded", "mort",
            "je suis mort", "jsuis mort", "chui mort", "mort de rire"
        ],
        "reponse": "😂🔥 L'ambiance est là ! Profite du serveur et check #catalogue si t'as pas encore vu nos produits 🕹️"
    },

    "ennui": {
        "mots": [
            "je m'ennuie", "je mennuie", "jmennui", "quoi faire", "koi faire",
            "c'est mort", "cé mort", "dead", "rien à faire", "rien a faire",
            "boring", "chiant", "chian", "ya rien", "y'a rien", "jsp",
            "je sais pas quoi faire", "bof", "bof bof", "mouais", "pff", "pfff",
            "flemme", "flem", "la flemme"
        ],
        "reponse": "😏 T'as rien à faire ? Profite pour :\n👀 Checker les nouveaux produits → #catalogue\n💬 Discuter avec la commu !\n🏆 Être actif pour monter VIP 🚀"
    },

    "commande_passee": {
        "mots": [
            "j'ai commandé", "j'ai commande", "jai commandé", "jai comande",
            "j'ai acheté", "jai acheté", "jai achete", "ma commande", "ma comande",
            "mon achat", "j'ai passé commande", "jai passé comande",
            "commandé hier", "commandé aujourd'hui", "j'attend ma commande",
            "jattend ma comande", "suivi commande", "suivi de commande",
            "état commande", "etat comande", "statut commande", "statu comande",
            "confirmation commande"
        ],
        "reponse": "🛍️ **Délais de livraison : 7 à 13 jours ouvrés** 📦\nTu recevras un mail avec ton suivi dès l'expédition !"
    },

    "confiance": {
        "mots": [
            "fiable", "fyable", "légit", "legit", "légitime", "legitime",
            "sérieux", "serieux", "confiance", "konfiance", "pas une arnaque",
            "pa une arnaque", "scam", "skam", "fake", "fausse boutique",
            "faux site", "fo site", "vrai", "de confiance", "digne de confiance",
            "sûr", "risque", "risqué", "douteux", "louche", "louch", "suspect",
            "bizarre", "bizar", "chelou", "shelou", "shady"
        ],
        "reponse": "✅ **Vice Drop est une boutique 100% fiable**\n🔒 Paiements sécurisés (Stripe)\n📦 Livraison suivie\n💬 Avis clients sur Discord\n💪 Une question ? On répond toujours !"
    },

    "age": {
        "mots": [
            "quel âge", "kel age", "quel age", "faut avoir quel âge", "mineur",
            "mineure", "majeur", "majeure", "13 ans", "14 ans", "15 ans",
            "16 ans", "17 ans", "18 ans", "trop jeune", "tro jeune",
            "age minimum", "âge minimum", "limite d'âge", "limite d age"
        ],
        "reponse": "👤 Aucune limite d'âge pour rejoindre la commu ! 🎮\n🛒 Pour commander, il faut un moyen de paiement valide"
    },

    "partenariat": {
        "mots": [
            "partenariat", "partenarya", "partenaire", "collab", "collaboration",
            "colaboration", "ambassadeur", "anbassadeur", "ambassadrice",
            "influenceur", "influenceuse", "influenseur", "sponsor", "sponsore",
            "sponsoring", "sponsorisé", "je suis influenceur", "je sui influenseur",
            "proposition", "créateur de contenu", "createur de contenu",
            "content creator", "deal", "promo en échange"
        ],
        "reponse": "🤝 **Partenariat / Collab**\n📩 Envoie ta proposition en privé sur Discord\n📊 Précise ton réseau et ton nombre d'abonnés\nOn étudie toutes les demandes ! 🔥"
    },

    "recrutement": {
        "mots": [
            "vous recrutez", "vou recruté", "recrutement", "recruter", "embauche",
            "enbauche", "embauché", "job", "jobe", "emploi", "emploie", "travail",
            "travaille", "travailler", "bosser", "bossé", "poste", "candidature",
            "CV", "cv", "stage", "staj", "alternance", "bénévole", "benevole"
        ],
        "reponse": "💼 On ne recrute pas pour le moment !\n💬 Mais reste actif, les opportunités viendront 😉\n📩 Pour toute question → écris sur Discord"
    },

    "serveur_discord": {
        "mots": [
            "c'est quoi ce serveur", "cé koi ce serveur", "sé koi se serveur",
            "le serveur il sert à quoi", "serveur discord", "ce discord",
            "ce serveur", "pourquoi ce discord", "pourkoi ce discord",
            "à quoi ça sert", "a koi sa sert", "le but", "le principe",
            "comment ça marche ici", "comen sa marche ici", "nouveau ici",
            "nouvo ici", "je viens d'arriver", "je vien d'arivé",
            "c'est quoi next level", "cé koi next level", "next level c'est quoi"
        ],
        "reponse": "🎮 **Bienvenue sur Next Level !**\nC'est la commu gaming & lifestyle de Vice Drop 🔥\n💬 Discute avec les membres\n🛒 Découvre nos produits → #catalogue\n🆕 Suis les nouveautés → #Nouveautés\n🏆 Deviens VIP en étant actif !"
    },

    "hors_sujet": {
        "mots": [
            "t'es un robot", "tes un robot", "té un robot", "t'es humain",
            "tes humain", "t'es qui", "té ki", "tes qui", "qui ta créé",
            "ki ta créé", "qui t'a fait", "ki ta fé", "t'es une IA", "tes une ia",
            "intelligence artificielle", "tu penses", "tu pense",
            "t'as des sentiments", "t'es vivant", "tes vivan", "il fait beau",
            "il fé bo", "quel temps"
        ],
        "reponse": "🤖 Je suis le bot **Next Level** !\nJe suis là pour t'aider et répondre à tes questions 💬\n🕹️ Tape une question sur nos produits, la livraison, les promos..."
    }
}


# ============================================
# COMMANDES SLASH
# ============================================

@bot.tree.command(name="livraison", description="Délais de livraison")
async def cmd_livraison(interaction: discord.Interaction):
    await interaction.response.send_message("🚚 **Délais de livraison : 7 à 13 jours ouvrés** 📦")

@bot.tree.command(name="paiement", description="Moyens de paiement acceptés")
async def cmd_paiement(interaction: discord.Interaction):
    await interaction.response.send_message(
        "💳 **Moyens de paiement acceptés :**\n"
        "✅ Carte bancaire (Visa, Mastercard)\n"
        "✅ PayPal\n"
        "✅ Apple Pay / Google Pay\n"
        "🔒 Paiements 100% sécurisés !\n"
        "Un souci ? Demande sur Discord 💬"
    )

@bot.tree.command(name="promo", description="Codes promo en cours et offres du moment")
async def cmd_promo(interaction: discord.Interaction):
    await interaction.response.send_message(
        "💰 **Promos & Bons Plans**\n"
        "🔥 Check le salon #annonces pour les codes promo en cours !\n"
        "🎁 Deviens VIP pour des réduc exclusives"
    )

@bot.tree.command(name="regles", description="Rappel des règles du serveur")
async def cmd_regles(interaction: discord.Interaction):
    await interaction.response.send_message(
        "📜 **Règles du serveur**\n"
        "Consulte le salon #règles pour tout savoir !\n"
        "✅ Respect entre membres\n"
        "✅ Pas de spam ni pub\n"
        "✅ Pas de contenu inapproprié\n"
        "⚠️ Tout manquement = sanction"
    )

@bot.tree.command(name="catalogue", description="Voir les produits disponibles")
async def cmd_catalogue(interaction: discord.Interaction):
    await interaction.response.send_message(
        "📦 **Nos produits**\n"
        "🎮 Casquettes, projecteurs LED, accessoires gaming & lifestyle\n"
        "👀 Découvre tout dans le salon #catalogue !\n"
        "🆕 Dernières sorties → #Nouveautés"
    )

@bot.tree.command(name="nouveautes", description="Derniers produits ajoutés")
async def cmd_nouveautes(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🆕 **Nouveautés**\n"
        "👀 Check le salon #Nouveautés pour les derniers produits !\n"
        "🔔 Active les notifs pour ne rien rater 🔥"
    )

@bot.tree.command(name="reseaux", description="Nos réseaux sociaux")
async def cmd_reseaux(interaction: discord.Interaction):
    await interaction.response.send_message(
        "📱 **Nos réseaux**\n"
        "🎵 TikTok : www.tiktok.com/@bobby_miamioff\n"
        "🛒 Site : vicedrop.fr\n"
        "Abonne-toi pour ne rien rater ! 🔥"
    )

@bot.tree.command(name="vip", description="Comment devenir VIP et les avantages")
async def cmd_vip(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🏆 **Programme VIP**\n"
        "💬 Accès au salon privé exclusif\n"
        "🎁 Avantages produits\n"
        "💰 Découvre comment générer des revenus avec nous\n"
        "➡️ Contacte-nous en privé sur Discord pour en savoir plus ! 🚀"
    )

@bot.tree.command(name="suggestion", description="Proposer un produit ou une idée")
async def cmd_suggestion(interaction: discord.Interaction, idee: str):
    await interaction.response.send_message(
        f"💡 Merci pour ta suggestion !\n"
        f"📝 **Ton idée :** {idee}\n"
        f"✅ On a bien noté, on regarde ça ! 👀"
    )


# ============================================
# EVENT: BOT PRÊT
# ============================================

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est en ligne !")
    print(f"📡 Connecté à {len(bot.guilds)} serveur(s)")

    # Synchroniser les commandes slash
    try:
        synced = await bot.tree.sync()
        print(f"🔄 {len(synced)} commandes slash synchronisées")
    except Exception as e:
        print(f"❌ Erreur sync: {e}")

    # Statut du bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Next Level 🎮"
        )
    )


# ============================================
# EVENT: MESSAGE REÇU (AUTO-RÉPONSES + MODÉRATION)
# ============================================

@bot.event
async def on_message(message):
    # Ignorer les messages du bot lui-même
    if message.author == bot.user:
        return

    # Ignorer les messages des autres bots
    if message.author.bot:
        return

    content_lower = message.content.lower().strip()

    # Si le message est vide, ignorer
    if not content_lower:
        return

    # ========================================
    # 1. VÉRIFIER LES INSULTES D'ABORD
    # ========================================
    for insulte in INSULTES:
        # Chercher le mot comme mot entier ou partie du message
        pattern = r'(?:^|\s|[^a-zà-ÿ])' + re.escape(insulte) + r'(?:$|\s|[^a-zà-ÿ])'
        if re.search(pattern, content_lower) or content_lower == insulte:
            # Supprimer le message
            try:
                await message.delete()
            except discord.errors.Forbidden:
                pass

            # Charger les warns
            warns = load_warns()
            user_id = str(message.author.id)

            if user_id not in warns:
                warns[user_id] = 0
            warns[user_id] += 1
            save_warns(warns)

            if warns[user_id] >= 2:
                # 2ème offense = kick
                try:
                    await message.author.kick(reason="Insultes répétées")
                    await message.channel.send(
                        f"🔨 **{message.author.display_name} a été exclu du serveur.**\n"
                        f"Raison : insultes répétées 🚫"
                    )
                except discord.errors.Forbidden:
                    await message.channel.send(
                        f"⚠️ **{message.author.mention}**, dernier avertissement ! "
                        f"Je n'ai pas les permissions pour t'exclure, mais un admin s'en chargera."
                    )
            else:
                # 1er avertissement
                await message.channel.send(
                    f"⚠️ **{message.author.mention}, ton message a été supprimé.**\n"
                    f"Les insultes ne sont pas tolérées sur Next Level.\n"
                    f"🔴 Prochain manquement = **exclusion du serveur**"
                )
            return

    # ========================================
    # 2. AUTO-RÉPONSES PAR MOTS-CLÉS
    # ========================================
    for categorie, data in KEYWORDS.items():
        for mot in data["mots"]:
            mot_lower = mot.lower()
            # Vérifier si le mot-clé est dans le message
            if len(mot_lower) <= 3:
                # Pour les mots courts (2-3 lettres), chercher le mot exact
                if content_lower == mot_lower or f" {mot_lower} " in f" {content_lower} ":
                    await message.reply(data["reponse"], mention_author=False)
                    return
            else:
                # Pour les mots plus longs, chercher s'ils sont contenus
                if mot_lower in content_lower:
                    await message.reply(data["reponse"], mention_author=False)
                    return

    # Traiter les commandes prefix si nécessaire
    await bot.process_commands(message)


# ============================================
# EVENT: MEMBRE REJOINT
# ============================================

@bot.event
async def on_member_join(member):
    # Chercher le salon #bienvenue
    channel = discord.utils.get(member.guild.text_channels, name="bienvenue")
    if channel:
        member_count = member.guild.member_count

        await channel.send(
            f"🎮 Yo {member.mention}, bienvenue sur **Next Level** ! 🔥\n\n"
            f"Tu es notre membre n°{member_count} — content de t'avoir parmi nous ! 💪\n\n"
            f"Ici on parle gaming, lifestyle et bons plans. "
            f"Jette un œil aux salons et n'hésite pas à te présenter !\n\n"
            f"À tout de suite 🕹️"
        )


# ============================================
# LANCER LE BOT
# ============================================

TOKEN = os.environ.get("DISCORD_TOKEN", "VOTRE_TOKEN_ICI")

if __name__ == "__main__":
    bot.run(TOKEN)
