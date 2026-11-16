# « Bâtiment B » — saison 1 (version cartel), 21 épisodes, 17 personnages, voix. -> eps_c/epXX.json
# Règles TikTok : aucune drogue montrée ni nommée, aucune arme visible, pas de violence graphique.
import json, os

EP = []
SERIES = "BÂTIMENT B"


def ep(title, bg, cast, hook, lines):
    EP.append(dict(title=title, bg=bg, cast=cast, hook=hook, lines=lines))


ep("L'arrivée", "cite_nuit", ["I", "LU", "BA"], "Cette nuit-là, trois voitures noires sont entrées dans la cité. Rien n'a plus jamais été pareil.", [
    ["N", "Cité des Tilleuls, dans le Nord. Trois heures du matin."],
    ["I", "Lucien ? Qu'est-ce que tu fais dehors à cette heure-ci ?", "surpris"],
    ["LU", "Rentre chez toi, Inès. Tout de suite. Ne te retourne pas.", "peur"],
    ["I", "Pourquoi ? C'est qui, ces voitures ? Elles sont garées devant le B.", "peur"],
    ["LU", "Trois voitures noires. Les mêmes qui tournaient autour de la cité la semaine dernière.", "peur"],
    ["N", "Une portière s'ouvre. Un homme en costume blanc descend, une canne dorée à la main."],
    ["BA", "Bonsoir. Quelle belle soirée pour visiter son nouveau quartier.", "joie", "enter"],
    ["LU", "Vous êtes perdu, monsieur. Ici, c'est une cité. Pas un palace.", "colere"],
    ["BA", "Pour l'instant, mon cher. Pour l'instant.", "joie"],
    ["I", "Vous êtes qui, au juste ?", "colere"],
    ["BA", "On m'appelle le Baron. Et vous, mademoiselle, vous êtes l'infirmière du troisième.", "neutre"],
    ["I", "Comment vous savez ça ?", "peur"],
    ["BA", "Je sais tout. C'est mon métier.", "joie"],
    ["BA", "À partir de ce soir, cette cité a un nouveau propriétaire.", "colere", "shake"],
])

ep("Le gardien", "hall", ["I", "Y"], "Le lendemain, le gardien avait disparu. Il a laissé une clé. Et un avertissement.", [
    ["N", "Le lendemain. Six heures du matin. Le hall du bâtiment B."],
    ["I", "Yanis, regarde le panneau. Avis de démolition. Bâtiment B.", "surpris", "shake"],
    ["Y", "Démolition ? Attends, ils peuvent pas faire ça. Ma mère vit ici depuis trente ans.", "colere"],
    ["I", "Et Lucien n'est pas dans sa loge. La porte est ouverte. Sa radio est encore allumée.", "peur"],
    ["Y", "Lucien ouvre à sept heures pile. Jamais avant. C'est pas normal.", "peur"],
    ["I", "Il y a une clé sur son bureau. Avec mon prénom écrit dessus.", "surpris"],
    ["Y", "Cave quarante-sept. Et un mot derrière. Lis.", "surpris"],
    ["I", "Ne fais confiance à personne. Même pas à ceux qui te sourient.", "peur"],
    ["Y", "Le type en costume blanc d'hier soir. Il souriait beaucoup, lui.", "peur"],
    ["I", "Lucien savait. Il savait qu'il allait devoir partir.", "triste"],
    ["N", "Dans l'escalier, des pas descendent. Lourds. Lents."],
    ["Y", "Il y a quelqu'un. Éteins ton téléphone. Vite.", "peur"],
    ["N", "Et la lumière du hall s'éteint.", "", "shake"],
])

ep("L'épicerie", "epicerie", ["PH", "FO", "BI"], "L'épicier de la cité vient de recevoir une visite. On lui a fait une offre qu'il ne peut pas refuser.", [
    ["N", "Épicerie Pham. Huit heures. Le rideau vient de se lever."],
    ["PH", "Bonjour, messieurs. Pain, lait, journal ? Je viens d'ouvrir.", "joie"],
    ["FO", "On vient pas acheter, monsieur Pham. On vient encaisser.", "neutre", "enter"],
    ["PH", "Encaisser ? Je ne vous dois rien. Je ne vous connais même pas.", "surpris"],
    ["FO", "Maintenant, tu nous connais. Le Baron prend trente pour cent. Chaque semaine.", "neutre"],
    ["PH", "Trente pour cent ? Mais je gagne à peine de quoi payer mon loyer !", "colere"],
    ["BI", "Le Baron dit que c'est pour votre sécurité.", "neutre", "enter"],
    ["PH", "Ma sécurité ? Contre qui ?", "peur"],
    ["BI", "Contre nous.", "neutre"],
    ["FO", "Biscotte rigole pas souvent. Mais quand il rigole, c'est pire.", "joie"],
    ["PH", "Et si je refuse ?", "peur"],
    ["FO", "Tu refuses pas. Personne refuse. Les clés du magasin, s'il te plaît.", "colere"],
    ["N", "Dehors, derrière la vitre, quelqu'un a tout vu. Avec son sac de livreur sur le dos."],
])

ep("Cave 47", "cave", ["I", "Y", "T"], "La cave du gardien cache quelque chose. Et quelqu'un est arrivé avant eux.", [
    ["N", "Les caves du bâtiment B. Le couloir sent l'humidité et la peur."],
    ["Y", "J'ai vu les hommes du Baron racketter Pham ce matin. Ils ont pris ses clés.", "colere"],
    ["I", "Ils prennent tout. Les commerces, le bâtiment... Voilà la quarante-sept.", "peur"],
    ["Y", "La clé rentre pas. Le cadenas est neuf. Quelqu'un l'a changé cette nuit.", "colere"],
    ["I", "Regarde par la fente. Il y a des sacs de sport. Plein. Ils débordent.", "surpris"],
    ["Y", "C'est... des liasses de billets. Des dizaines de liasses.", "surpris", "shake"],
    ["I", "De l'argent sale. Caché dans la cave de Lucien.", "peur"],
    ["T", "Vous ne devriez pas être là.", "neutre", "enter"],
    ["Y", "Et toi, t'es qui ? Je t'ai jamais vu dans le bâtiment.", "colere"],
    ["T", "Théo. Septième étage. J'ai emménagé il y a deux semaines.", "neutre"],
    ["I", "Et tu fais quoi dans les caves à six heures du matin ?", "colere"],
    ["T", "Je cherche Lucien. Comme vous.", "neutre"],
    ["T", "Et si vous tenez à lui, oubliez ce que vous venez de voir.", "peur"],
])

ep("Le badge", "cite_jour", ["Y", "I", "T"], "Le nouveau voisin ment. Un badge vient de le trahir.", [
    ["N", "Précédemment : des sacs d'argent dans la cave du gardien."],
    ["Y", "Oublier ? T'as vu ce qu'il y a dans cette cave ? Et tu veux qu'on oublie ?", "colere"],
    ["T", "Je veux que vous restiez en vie. Ce n'est pas pareil.", "peur"],
    ["I", "En vie ? Tu dramatises pas un peu ?", "colere"],
    ["T", "Le Baron n'est pas venu pour visiter. Il vient laver son argent. Ici.", "neutre"],
    ["N", "En repartant, quelque chose tombe de sa veste. Un badge."],
    ["Y", "Verdier Immobilier. Théo M., ingénieur structure.", "surpris", "shake"],
    ["I", "Verdier ? Le promoteur qui veut démolir le B ?", "colere"],
    ["Y", "Donc le voisin bosse pour celui qui nous expulse. Et il nous fait la morale.", "colere"],
    ["I", "Le promoteur démolit. Le Baron cache son argent. C'est le même plan.", "peur"],
    ["Y", "Ils achètent la cité avec de l'argent sale. Et ils nous mettent dehors.", "colere"],
    ["N", "Au bout de l'allée, une voiture noire attend. Théo monte à l'arrière."],
    ["I", "Il y a quelqu'un d'autre dedans. Costume blanc. Canne dorée.", "peur"],
])

ep("Mamie Rose", "cite_jour", ["RO", "CO", "BR"], "Ils ont voulu acheter l'appartement de la mauvaise grand-mère.", [
    ["N", "Le banc devant le bâtiment B. Mamie Rose, soixante-quinze ans, ancienne championne de boxe."],
    ["CO", "Madame Rose ? Le Comptable. Je représente un acheteur très généreux.", "joie", "enter"],
    ["RO", "Je vends rien, mon petit. Ni mon appartement, ni mes souvenirs.", "neutre"],
    ["CO", "Quinze mille euros. Comptant. Aujourd'hui. C'est une offre unique.", "joie"],
    ["RO", "Mon appartement en vaut quatre fois plus. Et il vaut tout l'or du monde pour moi.", "colere"],
    ["CO", "Le bâtiment va être démoli, madame. Dans un mois, il ne vaudra plus rien.", "neutre"],
    ["BR", "Grrr... Il sent la calculatrice et le mensonge, celui-là.", "colere"],
    ["RO", "Brutus n'aime pas les menteurs. Moi non plus.", "colere"],
    ["CO", "Réfléchissez bien. Il arrive parfois des accidents aux gens têtus.", "colere"],
    ["RO", "Tu me menaces ? J'ai mis K.O. des types deux fois plus gros que toi en trois rounds.", "colere", "shake"],
    ["CO", "Le Baron sera déçu. Très déçu.", "peur"],
    ["N", "Le lendemain matin, sur la porte de Mamie Rose, quelqu'un a peint un corbeau noir."],
    ["RO", "Un corbeau... La signature des Corvo.", "peur"],
])

ep("Les témoins", "toit", ["GA", "BR"], "Les seuls témoins de la disparition du gardien ont des plumes et des poils.", [
    ["N", "Sur le toit du bâtiment B. Là où personne ne monte jamais."],
    ["GA", "Brutus ! Psst ! Brutus ! Par ici, sous l'antenne !", "joie"],
    ["BR", "Gaspard ? T'as encore volé un croissant à la boulangerie ?", "colere"],
    ["GA", "Un demi. Bref. Moi j'ai vu Lucien, la nuit où il a disparu.", "neutre"],
    ["BR", "Quoi ? Et tu le dis que maintenant ?", "surpris", "shake"],
    ["GA", "Personne écoute les pigeons. Les humains nous jettent des miettes et basta.", "triste"],
    ["BR", "Raconte. Vite.", "colere"],
    ["GA", "Il est descendu à la chaufferie. Avec un thermos bleu et une couverture.", "neutre"],
    ["BR", "La chaufferie ? Elle est fermée depuis l'incendie de quatre-vingt-dix-huit.", "surpris"],
    ["GA", "Justement. Personne ne va jamais là-bas. La cachette parfaite.", "joie"],
    ["BR", "Donc il s'est caché tout seul. Il a pas été enlevé.", "joie"],
    ["GA", "Mais le gros en rose, Biscotte, il le cherche partout. Avec une lampe torche.", "peur"],
    ["BR", "Il faut prévenir Mamie Rose. Elle, elle me comprend. Enfin, presque.", "neutre"],
])

ep("Le Comptable", "appart", ["F", "CO"], "Le Comptable frappe chez madame Diallo. Elle fait semblant de ne rien comprendre.", [
    ["N", "Troisième étage. Chez madame Diallo, soixante-huit ans, mémoire de la cité."],
    ["CO", "Madame Diallo, il suffit de signer ici. Et ici. Et là, en bas.", "joie", "enter"],
    ["F", "Mes lunettes... Où sont mes lunettes... Je ne vois rien sans mes lunettes.", "triste"],
    ["CO", "Vous les avez sur le nez, madame.", "neutre"],
    ["F", "Ah oui ! Excusez-moi. L'âge, mon garçon. L'âge.", "joie"],
    ["CO", "Votre appartement contre une prime de relogement. Très généreuse.", "joie"],
    ["F", "Et je signe pour qui, exactement ? Pour la mairie ?", "neutre"],
    ["CO", "Pour une société. Corvo Investissements. Des gens très sérieux.", "neutre"],
    ["F", "Corvo... Comme le corbeau sur la porte de Rose ?", "surpris"],
    ["CO", "Une coïncidence. Signez, madame. Vos voisins ont presque tous signé.", "colere"],
    ["F", "Je vais réfléchir. Revenez demain. Avec des gâteaux, peut-être.", "joie"],
    ["N", "En partant, le Comptable oublie un carnet sur la table. Madame Diallo l'ouvre."],
    ["F", "Bâtiment B... acheté à quatre-vingt-dix pour cent. Payé en espèces.", "peur", "shake"],
])

ep("MC Lampadaire", "cite_jour", ["LA", "Y"], "Le rappeur de la cité filme tout. Cette fois, il a filmé la mauvaise chose.", [
    ["N", "MC Lampadaire. Deux mètres de haut, trois cent mille abonnés, et toujours en train de filmer."],
    ["LA", "Yo, Yanis ! Viens voir, j'ai un truc de fou. Ça va exploser les vues.", "joie", "enter"],
    ["Y", "Lampadaire, j'ai pas le temps pour tes clips, là.", "colere"],
    ["LA", "C'est pas un clip, frère. Hier soir, je filmais le coucher de soleil depuis ma fenêtre.", "neutre"],
    ["LA", "Et regarde qui passe derrière. Le gros en rose. Avec des sacs. Vers les caves.", "surpris"],
    ["Y", "C'est Biscotte. L'homme du Baron. Et ce sont les sacs de la cave quarante-sept.", "surpris", "shake"],
    ["LA", "Je l'ai postée ce matin. Déjà cinquante mille vues. Le peuple veut savoir.", "joie"],
    ["Y", "Tu l'as postée ? Tu te rends compte de ce que t'as fait ?", "peur"],
    ["LA", "Ben quoi ? C'est mon métier. Je montre la vérité de la cité.", "neutre"],
    ["Y", "Le Baron va voir cette vidéo. Il va savoir que quelqu'un l'a filmé.", "peur"],
    ["LA", "Et alors ? Il va faire quoi ? M'abonner ?", "joie"],
    ["N", "Au même moment, dans une voiture noire, le Baron regarde la vidéo. Il ne sourit plus."],
    ["N", "Il compose un numéro. Une seule phrase : « Trouvez-moi le grand avec la coiffure. »", "", "shake"],
])

ep("La chaufferie", "cave", ["I", "Y"], "Sous la chaufferie, quelqu'un vit en cachette. Depuis trois jours.", [
    ["N", "Précédemment : un pigeon a vu Lucien descendre à la chaufferie."],
    ["Y", "La chaufferie est condamnée depuis l'incendie. Personne n'y met les pieds.", "peur"],
    ["I", "Alors pourquoi la poignée est propre ? Tout le reste est couvert de poussière.", "surpris"],
    ["Y", "Un sac de couchage. Des boîtes de conserve. Une lampe frontale.", "surpris"],
    ["I", "Et un thermos bleu. Avec l'autocollant du LOSC. C'est celui de Lucien.", "surpris", "shake"],
    ["Y", "Il est encore chaud. Il est parti y'a dix minutes, maximum.", "peur"],
    ["I", "Il est vivant. Il se cache.", "joie"],
    ["Y", "Il se cache du Baron. Comme tout le monde dans cette cité.", "colere"],
    ["I", "Regarde le mur. Écrit à la craie.", "surpris"],
    ["Y", "Quarante-sept, flèche, toit. Et une heure : vingt-trois heures.", "surpris"],
    ["I", "Il nous donne rendez-vous. Ce soir. Sur le toit.", "peur"],
    ["N", "Derrière eux, la porte de la chaufferie se referme. Toute seule.", "", "shake"],
])

ep("Lucien", "toit", ["LU", "I", "Y"], "Le gardien est vivant. Et ce qu'il a vu peut faire tomber tout le cartel.", [
    ["N", "Vingt-trois heures. Le toit du bâtiment B."],
    ["LU", "Vous êtes têtus, tous les deux. Comme moi à votre âge.", "joie", "enter"],
    ["I", "Lucien ! On t'a cru mort. Pourquoi t'as disparu ?", "triste"],
    ["LU", "Parce que j'ai vu ce qu'il ne fallait pas voir. Dans ma propre cave.", "peur"],
    ["Y", "L'argent. On l'a vu aussi.", "neutre"],
    ["LU", "Pas que l'argent. J'ai vu Verdier, le promoteur, signer des papiers avec le Baron.", "colere"],
    ["LU", "La démolition, c'est leur plan. Ils rachètent tout pour rien, avec l'argent sale.", "colere"],
    ["I", "Il faut aller voir la police. Tout de suite.", "neutre"],
    ["LU", "Sans preuve, ils rient de nous. Et le Baron le saura dans l'heure.", "peur"],
    ["Y", "Comment il le saurait ?", "surpris"],
    ["LU", "Parce que quelqu'un dans ce bâtiment lui donne des informations. Tous les jours.", "peur", "shake"],
    ["I", "Quelqu'un qu'on connaît ?", "peur"],
    ["LU", "Quelqu'un à qui vous apportez des fleurs à son anniversaire.", "triste"],
])

ep("Commandante Morel", "hall", ["MO", "I"], "La police arrive enfin. Mais la commandante a ses propres secrets.", [
    ["N", "Le hall du bâtiment B. Une femme en imperméable examine les boîtes aux lettres."],
    ["MO", "Commandante Morel, brigade financière. C'est vous, Inès ?", "neutre", "enter"],
    ["I", "Comment vous connaissez mon nom ?", "surpris"],
    ["MO", "La vidéo de votre ami rappeur. Trois cent mille vues. Elle est arrivée jusqu'à mon bureau.", "neutre"],
    ["I", "Alors vous savez pour le Baron. Pour l'argent dans les caves.", "joie"],
    ["MO", "Ça fait deux ans que je suis la famille Corvo. Deux ans qu'ils m'échappent.", "colere"],
    ["I", "Arrêtez-les ! Les sacs sont encore en bas, j'en suis sûre.", "colere"],
    ["MO", "Si j'ouvre la cave, je trouve de l'argent. Je ne trouve pas le chef.", "neutre"],
    ["I", "Le chef, c'est le Baron. Costume blanc, canne dorée.", "colere"],
    ["MO", "Le Baron n'est qu'une vitrine. Quelqu'un au-dessus de lui donne les ordres.", "neutre"],
    ["I", "Et comment vous savez ça ?", "surpris"],
    ["MO", "Parce que j'ai un informateur chez eux. Vous le connaissez.", "neutre"],
    ["MO", "Les gens l'appellent La Fouine.", "neutre", "shake"],
])

ep("La Fouine", "cite_nuit", ["FO", "I"], "L'homme qui rackette l'épicier travaille pour la police. Ou pas.", [
    ["N", "Minuit. Derrière le city-stade. Un rendez-vous secret."],
    ["FO", "Vite, vite, vite. Si on me voit avec toi, je suis fini. Fini, tu comprends ?", "peur", "enter"],
    ["I", "Tu as volé les clés de monsieur Pham. Pourquoi je te ferais confiance ?", "colere"],
    ["FO", "Parce que je les ai rendues à la police le soir même. Double des clés. Malin, non ?", "joie"],
    ["I", "Morel dit que le Baron n'est pas le vrai chef.", "neutre"],
    ["FO", "Le Baron, c'est un costume. Il obéit. Il tremble au téléphone.", "neutre"],
    ["I", "Il tremble devant qui ?", "peur"],
    ["FO", "Personne la voit jamais. Elle vit dans la cité. Elle connaît tout le monde.", "peur"],
    ["I", "« Elle » ? C'est une femme ?", "surpris", "shake"],
    ["FO", "Une femme que tout le monde adore. C'est ça le pire.", "peur"],
    ["I", "Dis-moi son nom.", "colere"],
    ["FO", "Son nom, c'est...", "peur"],
    ["N", "Des phares s'allument au bout de la rue. Quand Inès se retourne, La Fouine a disparu.", "", "shake"],
])

ep("Le Baron", "appart", ["BA", "I"], "Le Baron l'attendait chez elle. Avec une proposition.", [
    ["N", "Inès rentre chez elle. La lumière est allumée. Quelqu'un est assis dans son canapé."],
    ["BA", "Entrez, mademoiselle. Faites comme chez vous. Ah, mais vous êtes chez vous.", "joie"],
    ["I", "Sortez de chez moi. Ou j'appelle la police.", "colere"],
    ["BA", "La commandante Morel ? Elle dort à cette heure-ci. Rue des Lilas, numéro douze.", "joie"],
    ["I", "Qu'est-ce que vous voulez ?", "peur"],
    ["BA", "La clé de la cave quarante-sept. Et le carnet que le Comptable a si bêtement oublié.", "neutre"],
    ["I", "Je ne sais pas de quoi vous parlez.", "colere"],
    ["BA", "Vous travaillez de nuit. Vous rentrez à six heures. Vous prenez toujours l'escalier B.", "neutre"],
    ["I", "Vous me surveillez ?", "peur"],
    ["BA", "Je surveille tout le monde. Je vous offre un appartement neuf, loin d'ici. Pensez-y.", "joie"],
    ["N", "Son téléphone vibre. Le Baron se lève d'un bond. Sa voix change complètement."],
    ["BA", "Oui, Mamie. Oui. Tout de suite, Mamie. Pardon, Mamie.", "peur", "shake"],
])

ep("Mamie Corvo", "appart", ["MC", "BA"], "La gentille mamie du quatrième prépare des gâteaux pour toute la cité. Et elle dirige le cartel.", [
    ["N", "Quatrième étage. Chez la gentille mamie qui offre des madeleines à tous les enfants du bâtiment."],
    ["MC", "Assieds-toi, mon petit. Une madeleine ? Je viens de les sortir du four.", "joie"],
    ["BA", "Merci, Mamie. Je... je n'ai pas faim.", "peur"],
    ["MC", "Tu n'as pas faim parce que tu as peur. Tu as raison d'avoir peur.", "neutre"],
    ["BA", "La vidéo du rappeur, c'était un accident. Biscotte a été imprudent.", "peur"],
    ["MC", "Un accident ? Trois cent mille personnes ont vu nos sacs. Ce n'est pas un accident. C'est une catastrophe.", "colere", "shake"],
    ["BA", "Le vote de la démolition est dans quatre jours. Après, tout sera à nous.", "neutre"],
    ["MC", "Après, oui. Mais d'ici là, il reste trois petits problèmes.", "neutre"],
    ["MC", "Le gardien qui se cache. La vieille boxeuse. Et la petite infirmière.", "neutre"],
    ["BA", "Que voulez-vous que je fasse ?", "peur"],
    ["MC", "Rien. Toi, tu as assez fait de bêtises. Je m'occupe de l'infirmière moi-même.", "joie"],
    ["N", "Elle reprend son tricot. Une écharpe noire. Avec un corbeau brodé dessus."],
])

ep("Le thé", "appart", ["MC", "I", "F"], "Mamie Corvo invite Inès à prendre le thé. Inès ne sait pas qui elle est.", [
    ["N", "Le lendemain. Mamie Corvo a invité Inès et madame Diallo à prendre le thé."],
    ["MC", "Ma petite Inès, tu as une mine affreuse. Tu travailles trop, ma chérie.", "triste"],
    ["I", "C'est gentil, Mamie. Il se passe des choses graves dans la cité en ce moment.", "triste"],
    ["MC", "J'ai entendu. Des voitures noires. Un baron. Quelle horreur. On n'est plus en sécurité nulle part.", "peur"],
    ["F", "Vous avez une très jolie écharpe noire, Mamie. Avec un oiseau brodé.", "neutre"],
    ["MC", "Un corbeau. J'adore les corbeaux. Ils sont intelligents. Et patients.", "joie"],
    ["F", "Comme celui peint sur la porte de Rose ?", "neutre"],
    ["MC", "Vraiment ? Quelle coïncidence.", "joie"],
    ["I", "Je dois y aller. Merci pour le thé, Mamie.", "neutre"],
    ["MC", "Prends tes affaires, ma chérie. Ton sac est sur la chaise.", "joie"],
    ["N", "Dans l'escalier, Inès fouille son sac. La clé de la cave quarante-sept a disparu."],
    ["F", "Inès... Le carnet du Comptable était dans ton sac aussi ?", "peur"],
    ["I", "Oui. Il a disparu aussi.", "peur", "shake"],
])

ep("Opération croissant", "toit", ["GA", "BR"], "Un pigeon borgne et un bouledogue vont tenter le cambriolage du siècle.", [
    ["N", "Précédemment : Mamie Corvo a volé la clé et le carnet dans le sac d'Inès."],
    ["GA", "Brutus, j'ai tout vu depuis le rebord de la fenêtre. La mamie a mis le carnet dans sa boîte à biscuits.", "neutre"],
    ["BR", "La mamie aux madeleines ? Elle me donne toujours des bouts de jambon...", "triste"],
    ["GA", "Elle donne du jambon à tout le monde. C'est comme ça qu'on achète la confiance.", "neutre"],
    ["BR", "OK. Le plan ?", "colere"],
    ["GA", "Tu aboies devant sa porte. Elle sort. Moi je rentre par la fenêtre ouverte.", "joie"],
    ["BR", "Et tu portes un carnet comment ? T'es un pigeon.", "surpris"],
    ["GA", "J'ai transporté une baguette entière jusqu'au toit en deux mille vingt-quatre. Respect.", "colere"],
    ["N", "Dix minutes plus tard. Brutus aboie comme jamais. Mamie Corvo sort sur le palier."],
    ["GA", "Je l'ai ! Je l'ai ! C'est lourd ! C'est très lourd !", "joie", "shake"],
    ["BR", "Et la clé ?", "surpris"],
    ["GA", "Pas trouvé la clé. Mais regarde ce qui est écrit sur la dernière page du carnet.", "peur"],
    ["BR", "« Vote dans trois jours. Après, on vide la cité. » Signé : Mamie.", "peur", "shake"],
])

ep("L'offre", "cite_jour", ["BA", "Y", "LA"], "Dix mille euros pour une vidéo. Yanis doit choisir.", [
    ["N", "Le Baron a retrouvé MC Lampadaire. Yanis était avec lui."],
    ["BA", "Messieurs. La vidéo d'hier. Je veux le fichier original. Et que tu la supprimes.", "neutre", "enter"],
    ["LA", "Supprimer ? Trois cent mille vues, mon gars. C'est mon meilleur score.", "colere"],
    ["BA", "Dix mille euros. En liquide. Pour le téléphone qui l'a filmée.", "joie"],
    ["Y", "Et s'il dit non ?", "colere"],
    ["BA", "Alors sa mère ne trouvera plus jamais d'appartement dans cette ville. Jamais.", "colere"],
    ["LA", "Laisse ma mère en dehors de ça.", "colere"],
    ["BA", "Toi, le livreur. Ta mère a besoin d'un rez-de-chaussée. Ses genoux, je crois.", "neutre"],
    ["Y", "Comment vous savez ça ?", "peur"],
    ["BA", "Je sais tout. Dix mille. Chacun. Maintenant.", "joie"],
    ["N", "Yanis regarde Lampadaire. Puis le bâtiment B. Puis la fenêtre de sa mère."],
    ["Y", "D'accord. Donne-lui le téléphone, Lampadaire.", "triste"],
    ["LA", "Quoi ?! Yanis, t'es sérieux ?", "surpris", "shake"],
])

ep("La copie", "hall", ["I", "Y", "LA"], "Yanis a-t-il vendu la cité ? La vérité est bien plus maline.", [
    ["N", "Précédemment : Yanis a accepté l'argent du Baron."],
    ["I", "Tu as vendu la vidéo. Tu nous as vendus. Pour dix mille euros !", "colere", "shake"],
    ["Y", "Inès. Respire. Écoute-moi deux secondes.", "neutre"],
    ["LA", "Moi aussi j'étais vénère. Puis il m'a expliqué. Vas-y, raconte-lui.", "joie"],
    ["Y", "Le téléphone qu'on lui a donné, c'est mon vieux. Écran fissuré, rien dedans.", "joie"],
    ["I", "Et la vraie vidéo ?", "surpris"],
    ["LA", "Envoyée à la commandante Morel il y a deux jours. Et sauvegardée dans trois nuages.", "joie"],
    ["Y", "Et l'argent, on l'a pas touché. Enveloppe fermée. Avec ses empreintes dessus.", "joie"],
    ["I", "Une preuve de corruption... Vous êtes fous. Et géniaux.", "joie"],
    ["LA", "Je vais faire un clip de cette histoire. Ça va être légendaire.", "joie"],
    ["I", "Il faut prévenir Théo. Il a le vrai rapport sur l'immeuble. Le vote est demain.", "neutre"],
    ["N", "Le téléphone de Théo sonne dans le vide. Une fois. Deux fois. Dix fois."],
    ["Y", "Sa porte au septième est grande ouverte. Et sa valise a disparu.", "peur", "shake"],
])

ep("Le vote", "cite_jour", ["MO", "I", "T", "V"], "Le vote de la démolition commence dans cinq minutes. Théo a disparu.", [
    ["N", "Devant la mairie. Dix-sept heures cinquante-cinq. Toute la cité est venue."],
    ["MO", "Sans le rapport de Théo, le vote passera. Et l'argent des Corvo deviendra propre.", "peur"],
    ["I", "Il a écrit un faux rapport une fois. Il ne recommencera pas. J'en suis sûre.", "colere"],
    ["MO", "On a la vidéo, l'enveloppe, le carnet. Mais il manque la preuve que l'immeuble est solide.", "neutre"],
    ["N", "Dix-sept heures cinquante-neuf. Les portes de la salle se referment."],
    ["I", "C'est fini...", "triste"],
    ["N", "Une voiture freine devant la mairie. Théo en sort en courant, un dossier sous le bras."],
    ["T", "Attendez ! J'étais chez l'expert du tribunal. Toute la nuit.", "joie", "enter"],
    ["T", "Le bâtiment B tiendra encore cinquante ans. Le rapport de démolition est un faux.", "colere"],
    ["MO", "Et qui a commandé ce faux ?", "neutre"],
    ["T", "Verdier. Sur ordre d'une certaine société. Corvo Investissements.", "colere", "shake"],
    ["V", "C'est faux ! Enfin... je n'ai fait qu'obéir. Ils me tenaient, moi aussi !", "peur"],
    ["MO", "Brigade financière. Personne ne quitte cette salle.", "colere"],
    ["N", "Le Baron, Verdier et Biscotte sont arrêtés. Mais dans la foule, une vieille dame s'éloigne. En tricotant.", "", "shake"],
])

ep("Bâtiment B", "toit", ["I", "LU", "Y"], "Le final. La cité est libre. Mais pas pour longtemps.", [
    ["N", "Une semaine plus tard. Sur le toit du bâtiment B. Le soleil se couche."],
    ["Y", "Le Baron en prison. Verdier aussi. Le vote est annulé. Le B ne sera pas démoli.", "joie"],
    ["I", "Monsieur Pham a rouvert son épicerie. Mamie Rose a repeint sa porte. En rose, évidemment.", "joie"],
    ["LU", "Et l'argent des caves a été saisi. Il va servir à rénover la chaufferie.", "joie"],
    ["I", "Lucien, sans toi, on n'aurait jamais rien trouvé.", "triste"],
    ["LU", "Sans vous, je serais encore caché dans une chaufferie avec un thermos froid.", "joie"],
    ["LU", "J'ai soixante-douze ans. Il est temps que quelqu'un prenne la relève. Tiens.", "neutre"],
    ["I", "Le passe général ? Moi ? Gardienne ?", "surpris"],
    ["LU", "Tu as fait confiance aux bonnes personnes. C'est tout le métier.", "joie"],
    ["Y", "Madame la gardienne. Ça sonne bien, franchement.", "joie"],
    ["N", "Un pigeon borgne se pose à côté d'eux. Il porte un petit papier dans le bec."],
    ["I", "« Ce n'était qu'un début, ma chérie. Bisous. Mamie. »", "peur", "shake"],
    ["N", "Mamie Corvo n'a jamais été retrouvée. Et le bâtiment A vient d'être vendu. Acheteur : anonyme."],
])

os.makedirs("eps_c", exist_ok=True)
HASH = "#serie #histoire #animation3d #batimentb #cite #thriller #storytime #pourtoi"
caps = []
for i, e in enumerate(EP):
    n = i + 1
    d = dict(ep=n, series=SERIES, cinema=True, voice=True, char_h={"1": 960, "2": 880, "3": 760, "4": 660}, title=e["title"],
             hook=e["hook"], bg=e["bg"], cast=e["cast"], lines=e["lines"], next=EP[i + 1]["title"] if n < len(EP) else None)
    json.dump(d, open(f"eps_c/ep{n:02d}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cap = f"Bâtiment B · Épisode {n}/21 : {e['title']}. {e['hook']} "
    cap += "Suite au prochain épisode, abonne-toi pour ne rien rater. " if n < 21 else "Fin de la saison 1. La saison 2 ? Dis-le en commentaire. "
    cap += HASH
    caps.append(dict(ep=n, title=e["title"], caption=cap))
json.dump(caps, open("eps_c/captions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
chars = sorted({c for e in EP for c in e["cast"]})
print(len(EP), "épisodes,", len(chars), "personnages :", chars)
