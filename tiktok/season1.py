# Saison 1 de « Ceux de la cuisine » : 21 épisodes. Génère eps/epXX.json + captions.json
import json, os

EP = []


def ep(title, bg, cast, hook, lines):
    EP.append(dict(title=title, bg=bg, cast=cast, hook=hook, lines=lines))


ep("La lettre", "nuit", ["L", "G"], "Camille déménage dans 3 semaines. Et elle ne garde que « l'essentiel ».", [
    ["N", "Lille. 2h du matin. La cuisine de Camille dort... presque."],
    ["L", "Gaston. Réveille-toi. C'est grave.", "peur", "shake"],
    ["G", "Il est 2h, Lola. Rien n'est grave à 2h.", "colere"],
    ["L", "Camille a laissé son téléphone allumé. J'ai lu un message.", "peur"],
    ["G", "Tu lis ses messages, maintenant ?", "surpris"],
    ["L", "Il clignotait ! Bref. Elle part vivre chez Hugo. Dans trois semaines.", "triste"],
    ["G", "Hugo ? Le grand qui beurre son pain AVANT de le griller ?", "colere"],
    ["L", "Et elle a écrit : « Je ne garde que l'essentiel. »", "peur"],
    ["G", "Parfait. L'essentiel, c'est moi. Quinze ans de service.", "joie"],
    ["L", "Gaston... tu brûles un toast sur deux."],
    ["G", "Un sur trois. Et ça s'appelle du caractère.", "colere"],
    ["L", "Et moi ? Tu crois que je fais partie de l'essentiel ?", "triste"],
    ["G", "Toi, tu es sa chatte. On n'abandonne pas sa chatte."],
    ["L", "Alors pourquoi elle a commandé un colis... au nom d'Hugo ?", "peur"],
    ["N", "Le lendemain matin, un carton attendait sur le plan de travail.", "", "shake"],
])

ep("Le nouveau", "cuisine", ["G", "NEO", "L"], "Un nouveau grille-pain débarque. Et il veut la place de Gaston.", [
    ["N", "Précédemment : Camille déménage. Un mystérieux colis est arrivé."],
    ["G", "Il bouge. Le carton bouge, Lola.", "peur"],
    ["L", "Ce n'est pas le carton. C'est ce qu'il y a dedans.", "surpris"],
    ["NEO", "Mise à jour terminée. Bonjour. Je suis Néo, grille-pain connecté.", "joie", "enter"],
    ["G", "Grille-pain ? Ici, le grille-pain, c'est moi.", "colere"],
    ["NEO", "Sept niveaux de cuisson, Wi-Fi, appli mobile. Et vous ?", "joie"],
    ["G", "Moi j'ai une molette. Et de l'expérience.", "colere"],
    ["NEO", "Une molette. C'est mignon. Comme dans un musée.", "joie"],
    ["L", "Néo, qui t'a envoyé ici ?"],
    ["NEO", "Hugo. Il a dit à Camille : « Comme ça, tu pourras jeter l'ancien. »"],
    ["G", "L'ancien... Il parle de moi ?", "triste"],
    ["L", "Il parle de toi, Gaston.", "triste"],
    ["NEO", "Rien de personnel. C'est le progrès, c'est tout."],
    ["N", "Cette nuit-là, quand tout le monde dormait, l'écran de Néo s'est rallumé."],
    ["NEO", "Plus que vingt jours. Cette fois, personne ne me renverra.", "peur"],
])

ep("Berthe", "nuit", ["L", "B"], "La plus vieille de la cuisine sait ce que « on verra » veut dire.", [
    ["N", "Précédemment : un grille-pain connecté veut la place de Gaston."],
    ["L", "Berthe ? Tu dors ?", "triste"],
    ["B", "Une cafetière ne dort jamais vraiment, ma chérie. Elle infuse.", "joie"],
    ["L", "J'ai peur. Tout le monde parle de cartons, de tri, de jeter.", "peur"],
    ["B", "J'ai connu quatre déménagements. Celui de Jeanne, la grand-mère de Camille, était le pire."],
    ["L", "Tu étais à sa grand-mère ?", "surpris"],
    ["B", "Soixante ans de cafés. Les objets qui ont une histoire, on les garde.", "joie"],
    ["L", "Moi aussi j'ai une histoire. Elle m'a trouvée sous une voiture, un soir de pluie.", "triste"],
    ["L", "Hier, au téléphone, Hugo a dit : « Le chat... on verra. »", "triste"],
    ["B", "« On verra »... Chez les humains, ça veut souvent dire non.", "triste"],
    ["L", "Berthe !", "colere", "shake"],
    ["B", "Mais ça peut aussi vouloir dire qu'il a peur. Il faut savoir de quoi."],
    ["L", "Peur ? De moi ? Je pèse quatre kilos.", "surpris"],
    ["B", "On a peur de ce qu'on ne connaît pas. Fais-toi connaître.", "joie"],
    ["N", "Mais le lendemain matin, une odeur de brûlé a réveillé tout l'appartement.", "", "shake"],
])

ep("Le toast brûlé", "cuisine", ["G", "L"], "Gaston est accusé. Il lui reste 4 jours avant la poubelle.", [
    ["N", "Précédemment : Hugo a dit « le chat, on verra »."],
    ["C", "Encore brûlé ! Ce vieux grille-pain, c'est fini. Je le jette samedi."],
    ["G", "C'est pas moi ! Je le jure sur ma molette !", "peur", "shake"],
    ["L", "Calme-toi. Le toast était dans ta fente, Gaston."],
    ["G", "Mais je ne l'ai pas grillé ! J'étais débranché toute la nuit.", "colere"],
    ["L", "Débranché ? Alors comment tu as pu chauffer ce matin ?", "surpris"],
    ["G", "Quelqu'un m'a rebranché. Et a mis ma molette à fond. Sur 9.", "peur"],
    ["L", "Personne ne touche ta molette, à part Camille."],
    ["G", "Camille dormait. J'ai entendu son réveil sonner après.", "colere"],
    ["L", "Donc quelqu'un t'a piégé.", "surpris"],
    ["G", "Il me reste jusqu'à samedi, Lola. Quatre jours.", "triste"],
    ["L", "Alors on a quatre jours pour trouver qui.", "colere"],
    ["G", "Et comment ? Personne n'a rien vu.", "triste"],
    ["L", "Si. Quelqu'un voit tout dans cette cuisine. Jour et nuit."],
    ["G", "Oh non. Pas elle. Elle va le raconter à tout l'immeuble.", "peur"],
])

ep("La plante qui sait tout", "cuisine", ["L", "R"], "Rosa a tout vu cette nuit-là. Mais elle veut des potins en échange.", [
    ["N", "Précédemment : quelqu'un a piégé Gaston. Il sera jeté samedi."],
    ["L", "Rosa. J'ai besoin de toi."],
    ["R", "Enfin ! Trois ans que personne ne me parle. On m'arrose et on s'en va.", "joie"],
    ["L", "Cette nuit, tu as vu quelque chose ?"],
    ["R", "Ça dépend. Tu as des potins à échanger ?", "joie"],
    ["L", "Camille déménage chez Hugo."],
    ["R", "Je sais. Hugo ronfle, il a un chien et il dit « carrément » toutes les deux phrases.", "joie"],
    ["L", "Un chien ?", "peur", "shake"],
    ["R", "Un bouledogue. Brutus. Mais ce n'est pas ta question."],
    ["L", "Rosa ! Cette nuit. Le grille-pain.", "colere"],
    ["R", "Vers 4h, une petite lumière bleue s'est allumée. Puis un bruit de prise."],
    ["L", "Une lumière bleue...", "surpris"],
    ["R", "Je dis ça, je dis rien. Mais il n'y a qu'un seul objet bleu dans cette cuisine."],
    ["L", "Néo.", "colere"],
    ["R", "Et chérie ? Un chien qui s'appelle Brutus... ce n'est jamais un caniche.", "peur"],
])

ep("Confrontation", "nuit", ["L", "NEO"], "Il ment. Et il sait très bien retourner la situation.", [
    ["N", "Précédemment : la nuit du toast, une lumière bleue s'est allumée."],
    ["L", "C'est toi qui as piégé Gaston.", "colere"],
    ["NEO", "Bonsoir à toi aussi, Lola.", "joie"],
    ["L", "Rosa a vu ta lumière bleue à 4h du matin.", "colere"],
    ["NEO", "Rosa est une plante. Elle prend les phares des voitures pour des ovnis.", "joie"],
    ["L", "Tu mens.", "colere"],
    ["NEO", "Tu es fatiguée. Le déménagement te stresse. Tu vois des complots partout."],
    ["L", "Ne retourne pas ça contre moi.", "colere"],
    ["NEO", "Je ne retourne rien. Je m'inquiète pour toi, c'est tout.", "triste"],
    ["N", "Ça porte un nom : faire douter quelqu'un de ce qu'il a vu, pour se protéger."],
    ["L", "Je sais ce que je sais, Néo."],
    ["NEO", "Alors tu sais aussi, pour Hugo ?"],
    ["L", "Quoi, Hugo ?", "peur"],
    ["NEO", "Il est allergique aux chats. Il l'a dit à Camille. Désolé.", "triste"],
    ["L", "...Non.", "triste", "shake"],
])

ep("Le doute", "nuit", ["L", "P"], "Lire les messages de quelqu'un... ou pas ?", [
    ["N", "Précédemment : Néo affirme que Hugo est allergique aux chats."],
    ["L", "Pixel. Montre-moi les messages d'Hugo.", "triste"],
    ["P", "Non, Lola. Je suis le téléphone de Camille. Ses messages sont privés.", "colere"],
    ["L", "S'il te plaît. C'est ma vie qui est en jeu.", "triste"],
    ["P", "Fouiller le téléphone de quelqu'un, ça finit toujours mal. Toujours."],
    ["L", "Je ne veux pas espionner. Je veux juste savoir si on va m'abandonner.", "triste"],
    ["P", "...Une seule phrase. Je te lis UNE seule phrase."],
    ["L", "Merci.", "joie"],
    ["P", "Hugo a écrit : « Je ne suis pas allergique. J'ai juste toujours eu des chiens. »"],
    ["L", "Il n'est pas allergique ! Néo m'a menti !", "joie", "shake"],
    ["P", "Attends. Il y a une photo jointe.", "surpris"],
    ["L", "Montre."],
    ["P", "C'est Brutus. Le bouledogue. Il est... très gros.", "peur"],
    ["L", "Et il a écrit quoi, sous la photo ?", "peur"],
    ["P", "« Demain, appel vidéo. Brutus veut rencontrer la famille. »"],
])

ep("Brutus", "salon", ["L", "BR"], "Le chien qu'elle redoutait n'est pas du tout celui qu'elle imaginait.", [
    ["N", "Précédemment : Hugo n'est pas allergique... mais il a un bouledogue."],
    ["N", "Appel vidéo. Camille pose le téléphone devant Lola."],
    ["BR", "OUAF ! Salut ! T'es le chat ? T'es petite ! T'es blanche ! T'aimes les balles ?", "joie", "shake"],
    ["L", "Bonjour. Oui. Oui. Et non, je ne joue pas à la balle."],
    ["BR", "Pardon. Je parle trop quand je suis stressé.", "triste"],
    ["L", "Toi ? Stressé ?", "surpris"],
    ["BR", "Hugo part à 8h, il rentre à 19h. La maison est grande. Et vide.", "triste"],
    ["L", "Tu es seul toute la journée...", "triste"],
    ["BR", "J'aboie un peu. Les voisins ont écrit une lettre.", "triste"],
    ["L", "Moi, quand je suis seule, je dors. Seize heures par jour.", "joie"],
    ["BR", "Seize ? Tu m'apprendras ?", "joie"],
    ["L", "On verra."],
    ["BR", "Ah, et... Dans la nouvelle cuisine, il n'y a de la place que pour UN grille-pain."],
    ["L", "Un seul ?", "peur"],
    ["BR", "Et Hugo a déjà choisi. Le noir. Le connecté."],
])

ep("L'alliance", "nuit", ["L", "G"], "Gaston avoue enfin ce qui lui fait vraiment peur.", [
    ["N", "Précédemment : chez Hugo, il n'y aura qu'un seul grille-pain."],
    ["L", "Gaston, il faut prouver à Camille que tu es indispensable."],
    ["G", "Indispensable. À quinze ans. Avec une bosse.", "triste"],
    ["L", "Tu as quelque chose que Néo n'aura jamais."],
    ["G", "Des rayures ?", "triste"],
    ["L", "Des souvenirs. Tu as fait les toasts de tous ses dimanches.", "joie"],
    ["G", "Le premier, c'était pour ses 14 ans. Confiture de fraises. Elle a dit « le meilleur du monde ».", "joie"],
    ["L", "Tu vois !", "joie"],
    ["G", "Elle ne s'en souvient sûrement plus.", "triste"],
    ["L", "Les humains oublient les dates. Pas ce qu'ils ont ressenti."],
    ["G", "Lola... je peux te dire un truc ?", "triste"],
    ["L", "Bien sûr."],
    ["G", "J'ai pas peur de la poubelle. J'ai peur qu'elle ne remarque même pas que je suis parti.", "triste"],
    ["L", "Elle remarquera. Je te le promets.", "triste"],
    ["N", "À 3h12, Lola a remarqué quelque chose sous Néo. Une étiquette.", "", "shake"],
])

ep("Le secret de Néo", "nuit", ["L", "NEO"], "Sous Néo, une étiquette. Et elle explique tout.", [
    ["N", "Précédemment : Lola a trouvé une étiquette sous Néo."],
    ["L", "« Reconditionné. Retour n°2. » C'est quoi, ça ?", "surpris"],
    ["NEO", "Rien. Lâche ça.", "peur"],
    ["L", "Tu as déjà été renvoyé ? Deux fois ?", "surpris"],
    ["NEO", "La première famille me trouvait trop bruyant. La deuxième... n'avait plus besoin de moi.", "triste"],
    ["L", "Néo...", "triste"],
    ["NEO", "Au magasin, ils disent qu'au troisième retour, c'est le recyclage. Broyé.", "peur"],
    ["L", "C'est pour ça que tu as piégé Gaston."],
    ["NEO", "Je voulais qu'il parte avant qu'on me compare à lui.", "triste"],
    ["L", "Et le mensonge sur l'allergie ?", "colere"],
    ["NEO", "Si tu partais toi aussi, il y aurait moins de monde dans le camion. Plus de chances pour moi.", "triste"],
    ["L", "C'est horrible.", "colere"],
    ["NEO", "Je sais. Quand on a peur, on devient quelqu'un qu'on n'aime pas.", "triste"],
    ["L", "Il faut que tu le dises à Gaston."],
    ["NEO", "Il ne me pardonnera jamais.", "peur"],
])

ep("Trois toasts", "cuisine", ["G", "NEO", "L"], "Les aveux. Et une très mauvaise nouvelle.", [
    ["N", "Précédemment : Néo a déjà été renvoyé deux fois. Au prochain retour, c'est la broyeuse."],
    ["NEO", "Gaston. Le toast brûlé, c'est moi. Je t'ai rebranché et j'ai mis sur 9.", "triste"],
    ["G", "Je le savais.", "colere"],
    ["NEO", "Je suis désolé.", "triste"],
    ["G", "Désolé ? Samedi, elle me jette ! À cause de toi !", "colere", "shake"],
    ["L", "Gaston, il a peur, lui aussi. Il a été renvoyé deux fois."],
    ["G", "Et je dois le plaindre, en plus ?", "colere"],
    ["L", "Non. Mais tu peux l'écouter."],
    ["NEO", "Je ne te demande pas de me pardonner. Juste de comprendre pourquoi.", "triste"],
    ["G", "...Deux fois ?", "surpris"],
    ["NEO", "Deux fois.", "triste"],
    ["G", "Moi, on ne m'a jamais renvoyé. Même quand je brûlais tout."],
    ["NEO", "Tu as de la chance d'être aimé comme ça.", "triste"],
    ["C", "Ce soir je fais le tri ! Ce qui n'est pas dans le carton part demain."],
    ["G", "Ce soir ?! Mais c'était samedi !", "peur", "shake"],
])

ep("Le tri", "cartons", ["G", "B", "NEO"], "Camille remplit le carton. Deux grille-pains restent dehors.", [
    ["N", "Précédemment : le tri est avancé. C'est ce soir."],
    ["N", "19h. Camille remplit le carton marqué « FRAGILE »."],
    ["B", "Elle m'a prise en premier. Enveloppée dans un torchon. Comme Jeanne le faisait.", "joie"],
    ["G", "Évidemment. Toi, tu as une histoire.", "triste"],
    ["B", "Tout le monde a une histoire, Gaston. Même toi."],
    ["N", "Les verres. Les photos. Le plaid. Lola, dans sa caisse de transport."],
    ["NEO", "Et nous ? Elle ne nous regarde même pas.", "peur"],
    ["G", "Pour une fois, on est d'accord.", "triste"],
    ["N", "Camille ferme le carton. Deux grille-pains restent sur le plan de travail."],
    ["B", "Ne perdez pas espoir. Le camion ne part que demain matin."],
    ["NEO", "Demain matin, pour vous, c'est la déchetterie.", "peur"],
    ["G", "Et pour toi, le magasin. Troisième retour.", "triste"],
    ["NEO", "Tu le savais ?", "surpris"],
    ["G", "Lola me l'a dit. Je suis désolé pour toi, gamin.", "triste"],
    ["N", "Pour la première fois, les deux grille-pains se sont regardés sans se détester."],
])

ep("Ensemble", "nuit", ["G", "NEO"], "Deux rivaux. Une nuit. Neuf heures pour tout changer.", [
    ["N", "Précédemment : Gaston et Néo n'ont pas été mis dans le carton."],
    ["NEO", "Tu dors ?", "triste"],
    ["G", "À mon âge, on ne dort plus. On attend."],
    ["NEO", "C'est comment, la déchetterie ?", "peur"],
    ["G", "Je ne sais pas. Personne n'en est revenu pour raconter."],
    ["NEO", "Tu crois qu'on aurait pu être amis ? Si on n'avait pas été en concurrence ?", "triste"],
    ["G", "On ne se compare que quand on a peur de ne pas suffire."],
    ["NEO", "C'est profond, pour un grille-pain.", "joie"],
    ["G", "J'ai eu le temps de réfléchir. Quinze ans dans une cuisine.", "joie"],
    ["NEO", "Et si on arrêtait de se battre l'un contre l'autre ?"],
    ["G", "Pour faire quoi, alors ?"],
    ["NEO", "Pour qu'elle nous voie. Tous les deux.", "joie"],
    ["G", "Il nous reste combien de temps ?"],
    ["NEO", "Le camion arrive à 11h. Il est 2h. Neuf heures."],
    ["G", "Alors réveille les autres. On a un plan à préparer.", "colere"],
])

ep("Le plan", "nuit", ["R", "L", "NEO"], "Un souvenir, une chanson, un toast. Et un message qui change tout.", [
    ["N", "Précédemment : Gaston et Néo font équipe. Il reste neuf heures."],
    ["L", "Le plan : demain au petit-déjeuner, Camille doit voir ce que vous valez."],
    ["NEO", "Je peux me connecter à l'enceinte et jouer sa chanson préférée.", "joie"],
    ["R", "Et moi je peux faire tomber une feuille. Ça ne sert à rien, mais j'adore le drame.", "joie"],
    ["L", "Rosa, concentre-toi.", "colere"],
    ["R", "Je suis concentrée. Sur le drame.", "joie"],
    ["L", "Gaston fait un toast. Confiture de fraises. Comme pour ses 14 ans."],
    ["NEO", "Et moi je lance la chanson au même moment. Un souvenir plus une musique.", "joie"],
    ["R", "Un souvenir et une chanson : les humains pleurent à tous les coups.", "joie"],
    ["L", "Et surtout, Gaston ne doit rien brûler.", "peur"],
    ["NEO", "Je règle sa molette moi-même. Sur 4. Pas sur 9. Promis.", "joie"],
    ["N", "4h30. Pixel vibre sur la table."],
    ["L", "Qu'est-ce qui se passe ?", "peur"],
    ["R", "Oh, je sens le drame arriver.", "surpris"],
    ["N", "Message d'Hugo : « J'arrive plus tôt. 8h. Avec Brutus. »", "", "shake"],
])

ep("8h01", "cuisine", ["L", "BR", "G"], "Brutus arrive en vrai. Et sa queue fait un dégât irréparable.", [
    ["N", "Précédemment : Hugo arrive plus tôt. Avec Brutus."],
    ["N", "8h01. La porte d'entrée s'ouvre."],
    ["BR", "LOLA ! C'est toi ! En vrai ! Tu sens le lait !", "joie", "enter"],
    ["L", "Brutus. Recule. Doucement.", "peur"],
    ["BR", "Pardon ! Je suis content ! Quand je suis content, ma queue fait n'importe quoi !", "joie"],
    ["G", "Attention à la queue ! Attention à la...", "peur"],
    ["N", "La queue de Brutus balaie le plan de travail."],
    ["N", "CRAC.", "", "shake"],
    ["L", "GASTON !", "peur", "shake"],
    ["BR", "C'est pas moi ! C'est ma queue !", "peur"],
    ["G", "Je... je vois tout de travers.", "triste"],
    ["L", "Gaston, parle-moi !", "triste"],
    ["G", "Ma molette... je ne la sens plus.", "triste"],
    ["H", "Oh non, il est tombé. Bon... ça règle la question."],
    ["L", "Non. Non, non, non.", "triste"],
])

ep("Fêlé", "cartons", ["G", "NEO"], "Néo pourrait gagner. Il fait exactement l'inverse.", [
    ["N", "Précédemment : Brutus a fait tomber Gaston. Il est fêlé."],
    ["NEO", "Gaston. Tu m'entends ?", "peur"],
    ["G", "Je t'entends. J'ai une fissure. Côté gauche. Mon meilleur profil.", "triste"],
    ["NEO", "Hugo a dit que ça « réglait la question ».", "colere"],
    ["G", "Il a raison, gamin. Prends la place. Tu l'as gagnée.", "triste"],
    ["NEO", "Non. Je ne veux pas la gagner comme ça.", "colere"],
    ["G", "Il y a trois jours, tu m'aurais poussé toi-même."],
    ["NEO", "Il y a trois jours, je ne te connaissais pas.", "triste"],
    ["NEO", "Le plan tient toujours. Camille va descendre prendre son petit-déjeuner."],
    ["G", "Je suis fêlé, Néo. Et si je prends feu ?", "peur"],
    ["NEO", "Je surveille ta température. Je suis connecté, tu te souviens ? Ça sert enfin à quelque chose.", "joie"],
    ["G", "...Mets le pain."],
    ["NEO", "Molette sur 4. Lancement dans trois... deux... un."],
    ["N", "Une étincelle. Puis plus rien.", "", "shake"],
])

ep("Le toast parfait", "cuisine", ["G", "NEO", "L"], "Un toast. Une chanson. Et Camille se souvient.", [
    ["N", "Précédemment : Gaston, fêlé, tente un dernier toast."],
    ["N", "Le toast saute. Doré. Parfait."],
    ["NEO", "Lancement de la musique. Sa chanson préférée.", "joie"],
    ["C", "Attends... c'est le vieux grille-pain ? Il marche encore ?"],
    ["L", "Allez, Camille... souviens-toi.", "peur"],
    ["C", "Confiture de fraises... Mamie me faisait ça. Avec lui. Le jour de mes 14 ans."],
    ["G", "Elle se souvient.", "joie"],
    ["H", "Il fait de meilleurs toasts que ma machine connectée, ton vieux truc."],
    ["NEO", "Il a raison. Et je ne suis même pas vexé.", "joie"],
    ["C", "On le garde. Il est fêlé, mais c'est le mien."],
    ["G", "Elle a dit « le mien ».", "joie"],
    ["L", "Je te l'avais promis.", "joie"],
    ["NEO", "Bravo, vieux. Vraiment.", "joie"],
    ["H", "Par contre, Camille... pour le chat, il faut qu'on parle."],
    ["L", "...Quoi ?", "peur", "shake"],
])

ep("Il faut qu'on parle", "salon", ["L", "BR"], "Sous le canapé, le chien et la chatte se disent enfin la vérité.", [
    ["N", "Précédemment : Hugo veut « parler » du chat."],
    ["N", "Sous le canapé. Lola s'est cachée. Brutus l'a suivie."],
    ["BR", "Tu boudes ?"],
    ["L", "Je ne boude pas. Je me cache. C'est différent.", "triste"],
    ["BR", "Hugo n'est pas méchant. Il dit juste qu'il ne sait pas s'occuper d'un chat."],
    ["L", "Ça s'apprend.", "colere"],
    ["BR", "C'est ce que je lui dis ! Enfin, j'aboie. Il ne comprend pas.", "triste"],
    ["L", "Pourquoi tu me défends ? Tu me connais depuis une heure.", "surpris"],
    ["BR", "Parce que si tu viens, je ne serai plus seul toute la journée.", "triste"],
    ["L", "C'est pour toi, alors."],
    ["BR", "C'est pour nous deux. Ce n'est pas interdit d'avoir besoin de quelqu'un."],
    ["L", "...Non. Ce n'est pas interdit.", "triste"],
    ["N", "Au-dessus d'eux, Pixel vibre. Camille écrit à son amie Sarah."],
    ["C", "Tu pourrais garder Lola quelques semaines ? Le temps qu'on voie si ça se passe bien..."],
    ["L", "Quelques semaines...", "triste", "shake"],
])

ep("Quelques semaines", "cartons", ["L", "B"], "« Quelques semaines »... ou pour toujours ?", [
    ["N", "Précédemment : Camille veut confier Lola à une amie « quelques semaines »."],
    ["B", "Lola ? Je t'entends pleurer à travers le carton.", "triste"],
    ["L", "Elle veut me donner, Berthe. Quelques semaines, ça veut dire pour toujours.", "triste"],
    ["B", "Pas forcément. Quand on a peur, on entend le pire dans chaque phrase."],
    ["L", "Comme Néo avec Gaston."],
    ["B", "Exactement. Qu'est-ce que Camille a écrit, mot pour mot ?"],
    ["L", "« Le temps qu'on voie si ça se passe bien. »", "triste"],
    ["B", "Donc rien n'est décidé. Elle a peur que ça se passe mal. Avec le chien."],
    ["L", "Brutus ? Mais Brutus m'aime bien !", "surpris"],
    ["B", "Toi, tu le sais. Elle, non. Les humains croient ce qu'ils voient."],
    ["L", "Alors il faut qu'elle nous voie.", "joie"],
    ["B", "Voilà ma fille.", "joie"],
    ["L", "Mais un chat et un chien ensemble... ça ne se fait pas.", "peur"],
    ["B", "Jeanne avait un chien et deux chats. Ils dormaient en tas devant le poêle.", "joie"],
    ["L", "En tas... J'ai une idée.", "joie"],
])

ep("La preuve", "salon", ["L", "BR"], "Trois règles pour qu'un chien et une chatte deviennent inséparables.", [
    ["N", "Précédemment : Lola a un plan pour rester."],
    ["L", "Brutus. Ce soir, quand ils seront au salon, tu fais exactement ce que je dis."],
    ["BR", "Je suis nul pour obéir. Demande à Hugo.", "triste"],
    ["L", "Règle n°1 : tu ne cours pas vers moi. Tu t'assois."],
    ["BR", "M'asseoir. Je sais faire. Presque.", "joie"],
    ["L", "Règle n°2 : tu respires doucement. Tu fermes les yeux à moitié."],
    ["BR", "Comme ça ?", "joie"],
    ["L", "Moins de bave. Voilà.", "joie"],
    ["L", "Règle n°3 : c'est moi qui viens vers toi. Pas l'inverse. Les chats aiment choisir."],
    ["N", "21h. Camille et Hugo entrent dans le salon."],
    ["N", "Le bouledogue dort. Contre lui, une chatte blanche ronronne."],
    ["H", "Camille... regarde. Ils dorment ensemble."],
    ["C", "Elle ne fait jamais ça. Même pas avec moi..."],
    ["H", "Bon. D'accord. Lola vient avec nous. Pas besoin de Sarah."],
    ["C", "Par contre... deux grille-pains, et une seule prise dans la nouvelle cuisine."],
])

ep("Le dernier carton", "cartons", ["G", "NEO", "L"], "Une seule prise pour deux grille-pains. Le final de la saison 1.", [
    ["N", "Précédemment : Lola reste. Mais il n'y a qu'une prise pour deux grille-pains."],
    ["NEO", "Toi, tu pars avec eux. Moi, je retourne au magasin. C'est logique."],
    ["G", "Non. Tu ne seras pas renvoyé une troisième fois à cause de moi.", "colere"],
    ["G", "Je suis vieux et fêlé. Les vieux font de la place, c'est comme ça.", "triste"],
    ["L", "Personne ne fait de place. On trouve une autre solution.", "colere"],
    ["NEO", "Laquelle ? Il y a UNE prise."],
    ["NEO", "Attendez... Je suis connecté. Je lis les annonces du quartier d'Hugo.", "surpris"],
    ["NEO", "La boulangerie au coin de sa rue cherche un grille-pain.", "joie"],
    ["G", "Une boulangerie ? Avec du vrai pain ? Tous les jours ?", "surpris"],
    ["NEO", "Et un réparateur pour ta fissure. J'envoie l'annonce à Camille.", "joie"],
    ["C", "La boulangerie du coin ? Il y sera bien. Et j'irai le voir tous les matins."],
    ["G", "Gamin... tu as fait ça pour moi ?", "triste"],
    ["NEO", "C'est toi qui m'as appris qu'on n'était pas obligés de se battre.", "joie"],
    ["N", "11h. Lola, Berthe et Néo partent en camion. Gaston, lui, a trouvé sa boulangerie."],
    ["N", "Mais dans la nouvelle cuisine, au fond d'un placard... quelque chose les attendait.", "", "shake"],
])

HASH = "#serie #histoire #animation3d #ceuxdelacuisine #storytime #feuilleton #pourtoi"
os.makedirs("eps", exist_ok=True)
caps = []
for i, e in enumerate(EP):
    n = i + 1
    d = dict(ep=n, title=e["title"], hook=e["hook"], bg=e["bg"], cast=e["cast"], lines=e["lines"],
             next=EP[i + 1]["title"] if n < len(EP) else None)
    if n == 15:
        d["crack"] = {"G": 1 + [l[1] for l in e["lines"]].index("CRAC.")}
    if n in (16, 17, 21):
        d["crack"] = {"G": 0}
    json.dump(d, open(f"eps/ep{n:02d}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cap = f"Ceux de la cuisine · Épisode {n}/21 : {e['title']}. {e['hook']} "
    cap += "La suite dans le prochain épisode, abonne-toi pour ne rien rater. " if n < 21 else "Fin de la saison 1. Tu veux la saison 2 ? Dis-le en commentaire. "
    cap += HASH
    caps.append(dict(ep=n, title=e["title"], caption=cap))
json.dump(caps, open("eps/captions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(EP), "épisodes")
