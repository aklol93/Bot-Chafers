import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import json
import sqlite3

# Connexion à SQLite
conn = sqlite3.connect("progress.db")
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        user_id TEXT PRIMARY KEY,
        progress INTEGER NOT NULL
    )
''')
conn.commit()

load_dotenv()

ADMIN_ID = 611658274445721618

# Chemin racine des membres
MEMBERS_DIR = "DDGquetes/Membres"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

# Données des quêtes 
quest_data = [
    {"Quête": "La terre banquise", "Remarque": "Arrivé Frigost"},
    {"Quête": "La maire de glace", "Remarque": "Parler à Maire Cantille"},
    {"Quête": "Full Contact", "Remarque": "Ne pas suivre directement, juste parler au pnj avec un '?' pendant les precedentes quetes et valider une fois monologues fini"},
    {"Quête": "Monologue du vaccin", "Remarque": "https://www.dofuspourlesnoobs.com/les-monologues-du-vaccin.html"},
    {"Quête": "Bienvenue à Frigost", "Remarque": "Aller parler à Maire Cantille"},
    {"Quête": "Bricole Girl", "Remarque": "https://www.dofuspourlesnoobs.com/bricole-girl.html"},
    {"Quête": "Promenons-nous dans les bois", "Remarque": "https://www.dofuspourlesnoobs.com/promenons-nous-dans-les-bois.html"},
    {"Quête": "Chasseurs", "Remarque": "Faire la quete jusqu'à devoir faire le Mansot Royal","Lien":"https://www.dofuspourlesnoobs.com/les-chasseurs.html"},
    {"Quête": "Pêche en eaux gelées.", "Remarque": "Faire la quete , il faut faire un Mansot Royal", "Lien":"https://www.dofuspourlesnoobs.com/pecircche-en-eaux-geleacutees.html"},
    {"Quête": "La pêche à Mel", "Remarque": "https://www.dofuspourlesnoobs.com/la-pecircche-agrave-mel.html"},
    {"Quête": "Mel Odieuse", "Remarque": "https://www.dofuspourlesnoobs.com/mel-odieuse.html"},
    {"Quête": "Mel au drame", "Remarque": "https://www.dofuspourlesnoobs.com/mel-au-drame.html"},
    {"Quête": "Il est frais mon pichon", "Remarque": "https://www.dofuspourlesnoobs.com/il-est-frais-mon-pichon.html"},
    {"Quête": "La marche de l'impératrice", "Remarque": "Prendre la quete et la faire en meme temps que l'étape 1 de la suivante","Lien":"https://www.dofuspourlesnoobs.com/la-marche-de-limpeacuteratrice.html"},
    {"Quête": "Essentiel dans le lac gelé", "Remarque": "Aller parler à Maire Cantille"},
    {"Quête": "Donjons et Truffions", "Remarque": "Prendre la quete et ne pas la suivre"},
    {"Quête": "Au fion du trou", "Remarque": "Prendre la quete et ne pas la suivre"},
    {"Quête": "Frigost, une île pas comme les autres", "Remarque": "Prendre la quete et ne pas la suivre"},
    {"Quête": "Developpement durable", "Remarque": "Lancer la quete et avancer jusqu'à 'Mauvaise Graine'ou équivalent sans la faire","Lien":"https://www.dofuspourlesnoobs.com/deacuteveloppement-durable.html"},
    {"Quête": "Il préfère la mort en mer", "Remarque": "https://www.dofuspourlesnoobs.com/il-preacutefegravere-la-mort-en-mer.html"},
    {"Quête": "Chauffage à moindre frais", "Remarque": "Faire la quete en validant 'Mauvaise graine'ou équivalent","Lien":"https://www.dofuspourlesnoobs.com/chauffage-agrave-moindre-frais.html"},
    {"Quête": "Champ Pomy", "Remarque": "Prendre la quete"},
    {"Quête": "A la recherche de Dan Lavy", "Remarque": "Faire la quete en recoltant les fleurs dans le donjon pour 'Champ Pomy'","Lien":"https://www.dofuspourlesnoobs.com/a-la-recherche-de-dan-lavy.html"},
    {"Quête": "A qui profite le boufmouth", "Remarque": "https://www.dofuspourlesnoobs.com/a-qui-profite-le-boufmouth.html"},
    {"Quête": "Les rescapés de Frigost", "Remarque": "Aller parler à Maire Cantille"},
    {"Quête": "Dépôt de Ravitaillement", "Remarque": "Commencer la quete entre 8h et 20h","Lien":"https://www.dofuspourlesnoobs.com/deacutepocirct-de-ravitaillement.html"},
    {"Quête": "Chaud du slip", "Remarque": "Finir la quete entre 20h et 8h","Lien":"https://www.dofuspourlesnoobs.com/chaud-du-slip.html"},
    {"Quête": "Gant Graine", "Remarque": "https://www.dofuspourlesnoobs.com/deacuteveloppement-durable.html"},
    {"Quête": "Les graines de la discorde", "Remarque": "Faire la quete et prendre la suivante sans la valider","Lien":"https://www.dofuspourlesnoobs.com/deacuteveloppement-durable.html"},
    {"Quête": "Le champ des héros", "Remarque":"A ne pas valider maintenant"},
    {"Quête": "Un ami qui ne vous veut pas que du bien", "Remarque": "Faire la quete en validant la précedente","Lien":"https://www.dofuspourlesnoobs.com/un-ami-qui-ne-vous-veut-pas-que-du-bien.html"},
    {"Quête": "Maya La belle", "Remarque": "https://www.dofuspourlesnoobs.com/maya-la-belle.html"},
    {"Quête": "Champ borde le château", "Remarque": "Terminer developpement durable en validant cette quete"},
    {"Quête": "Les rescapés du villages Ensevelli", "Remarque": "Aller parler a Grobidet  -77,-72"},
    {"Quête": "Malédiction", "Remarque": "Faire les pré requis en fonction de votre alignement et la quete","Lien":"https://www.dofuspourlesnoobs.com/maleacutediction.html"},
    {"Quête": "Mission Solution", "Remarque": "https://www.dofuspourlesnoobs.com/mission-solution.html"},
    {"Quête": "Chaud et Froid", "Remarque": "Faire la quete jusqu'à devoir drop sur stalak,mansordide et groduche","Lien":"https://www.dofuspourlesnoobs.com/chaud-et-froid.html"},
    {"Quête": "Le tour de Guet", "Remarque": "https://www.dofuspourlesnoobs.com/le-tour-de-guet.html"},
    {"Quête": "Guerre Froide", "Remarque": "Cette quette te fera drop  pour chaud et froid","Lien":"https://www.dofuspourlesnoobs.com/guerre-froide.html"},
    {"Quête": "Rappel à la vie", "Remarque": "https://www.dofuspourlesnoobs.com/rappel-agrave-la-vie.html"},
    {"Quête": "Moteur à explosion", "Remarque": "https://www.dofuspourlesnoobs.com/moteur-agrave-explosion.html"},
    {"Quête": "La fifille à son papa", "Remarque": "https://www.dofuspourlesnoobs.com/la-fifille-agrave-son-papa.html"},
    {"Quête": "Mutinerie chez les Armutins", "Remarque": "https://www.dofuspourlesnoobs.com/mutinerie-chez-les-armutins.html"},
    {"Quête": "Les derniers rescapés", "Remarque": "Valider la quête"},
    {"Quête": "Au-délà du mur", "Remarque": "Faire la quete , et valider Nileza dans chaud et froid en même temps","Lien":"https://www.dofuspourlesnoobs.com/au-delagrave-du-mur.html"},
    {"Quête": "Les desseins de Sylarg", "Remarque": "Faire la quete et valider Sylarg dans chaud et froid","Lien":"https://www.dofuspourlesnoobs.com/les-desseins-de-sylargh.html"},
    {"Quête": "Vous avez demandé la peau lisse", "Remarque": "Faire la quete et valider Klime dans chaud et froid","Lien":"https://www.dofuspourlesnoobs.com/vous-avez-demandeacute-la-peau-lisse.html"},
    {"Quête": "La derniere carte", "Remarque": "Faire la quete et valider Missiz dans chaud et froid","Lien":"https://www.dofuspourlesnoobs.com/la-derniegravere-carte.html"},
    {"Quête": "Crise d'ex-Emma", "Remarque": "https://www.dofuspourlesnoobs.com/crise-dex-emma.html"},
    {"Quête": "La machine à demonter le temps", "Remarque": "Valider Chaud et Froid + Au fion du trou en faisant Sakai","Lien":"https://www.dofuspourlesnoobs.com/la-machine-agrave-deacutemonter-le-temps.html"},
    {"Quête": "La fonte des glaces", "Remarque": "https://www.dofuspourlesnoobs.com/la-fonte-des-glaces.html"},
    {"Quête": "L'ombre et la glace", "Remarque": "https://www.dofuspourlesnoobs.com/lombre-et-la-glace.html"},
    {"Quête": "Lumiere sur l'Ombre", "Remarque": "https://www.dofuspourlesnoobs.com/lumiegravere-sur-lombre.html"},
    {"Quête": "Le givre des revelations", "Remarque": "https://www.dofuspourlesnoobs.com/le-givre-des-reacuteveacutelations.html"},
    {"Quête": "Mille et un jours, un destin", "Remarque":"VALIDE PAS CETTE QUETE, chaque fois où tu devras vaincre Nileza à l'avenir et lui parler tu pourras y aller sans faire le Donjon #Sylvestre"},
]


os.makedirs(MEMBERS_DIR, exist_ok=True)

# Fonctions 
def get_member_dir(user: discord.User):
    # Utiliser l'ID Discord comme nom de dossier (unique)
    return os.path.join(MEMBERS_DIR, str(user.id))

def get_progress_path(user: discord.User):
    return os.path.join(get_member_dir(user), "queteddg.json")

def load_member_progress(user: discord.User):
    cursor.execute("SELECT progress FROM progress WHERE user_id = ?", (str(user.id),))
    result = cursor.fetchone()
    return result[0] if result else 0


def save_member_progress(user: discord.User, progress: int):
    cursor.execute("INSERT OR REPLACE INTO progress (user_id, progress) VALUES (?, ?)", (str(user.id), progress))
    conn.commit()


# Commande 
@tree.command(name="ddg", description="Let's GO CHAFER !")
async def ddg_command(interaction: discord.Interaction):
    user = interaction.user
    progress = load_member_progress(user)
    if progress >= len(quest_data):
        await interaction.response.send_message("🎉 Mais ... t'as déjà tout fait", ephemeral=True)
        return
    quest = quest_data[progress]
    await interaction.response.send_message(
        "C'est parti pour le DDG !\n"
        "Utilise /ok pour valider la quête proposée,\n"
        "/nok pour arrêter.",
        ephemeral=True
    )
    await interaction.followup.send(
        f"**{quest['Quête']}**\nRemarque: _{quest['Remarque']}_\nUtilise /ok quand tu as terminé cette quête, ou /nok pour arrêter.",
        ephemeral=True
    )

@tree.command(name="ok", description="Valide la quête en cours et passe à la suivante.")
async def ok_command(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user = interaction.user
    progress = load_member_progress(user)
    if progress >= len(quest_data):
        await interaction.followup.send("🎉 Mais ... ta déjà tout fait", ephemeral=True)
        return
    progress += 1
    save_member_progress(user, progress)

    if progress >= len(quest_data):
        await interaction.followup.send("🎉 Mais ... ta déjà tout fait", ephemeral=True)
    else:
        next_quest = quest_data[progress]
        await interaction.followup.send(
            f"✅ NICEE ! Tu es maintenant à la quête **{next_quest['Quête']}**.\n"
            f"Remarque : _{next_quest['Remarque']}_\n"
            "Utilise /ok quand tu as fini cette quête, ou /nok pour arrêter.",
            ephemeral=True
        )

@tree.command(name="nok", description="Arrête le dialogue et enregistre ta progression")
async def nok_command(interaction: discord.Interaction):
    user = interaction.user
    progress = load_member_progress(user)
    if progress >= len(quest_data):
        await interaction.response.send_message("🎉 Mais ... ta déjà tout fait", ephemeral=True)
        return
    quest = quest_data[progress]
    await interaction.response.send_message(
        f"📝 Chafer en fuite ! **{quest['Quête']}**.\n"
        f"Tu vas où là ? reviens finir ça !",
        ephemeral=True
    )
@tree.command(name="queteddg", description="Affiche les 5 dernières quêtes validées et les 5 prochaines.")
async def queteddg_command(interaction: discord.Interaction):
    user = interaction.user
    progress = load_member_progress(user)

    total = len(quest_data)
    lines = ["📜 **Progression DDG :**\n"]

    # Index des quêtes à afficher
    start_done = max(0, progress - 5)
    end_done = progress
    start_upcoming = progress
    end_upcoming = min(total, progress + 5)

    # Quêtes validées
    if end_done > start_done:
        lines.append("✅ **5 dernières quêtes validées :**")
        for i in range(start_done, end_done):
            quest = quest_data[i]
            lines.append(f"✅ **{i+1}. {quest['Quête']}** — _{quest['Remarque']}_")
    else:
        lines.append("✅ Aucune quête validée pour le moment.")

    # Quêtes à venir
    if start_upcoming < end_upcoming:
        lines.append("\n🔜 **5 prochaines quêtes à faire :**")
        for i in range(start_upcoming, end_upcoming):
            quest = quest_data[i]
            lines.append(f"* **{i+1}. {quest['Quête']}** — _{quest['Remarque']}_")
    else:
        lines.append("\n🎉 Tu as complété toutes les quêtes !")

    message = "\n".join(lines)
    await interaction.response.send_message(message, ephemeral=True)

@tree.command(name="resetddg", description="Réinitialise ta progression des quêtes")
async def resetddg_command(interaction: discord.Interaction):
    user = interaction.user
    save_member_progress(user, 0)
    await interaction.response.send_message("🔄 Rollback du Comte BOOM ! Retour au bâteauu !", ephemeral=True)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Connecté en tant que {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))

