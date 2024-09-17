Evaluation phase métier : Prix Goncourt 2024
Le prix Goncourt 2024 sera attribué lundi 4 novembre, au restaurant Drouant à Paris, à l'issue de trois sélections successives :
•
mardi 3/9 : première sélection comportant une liste de 16 romans ;
•
mardi 1/10 : deuxième sélection ;
•
mardi 22/10 : troisième sélection.
Chaque livre* porte un titre, est décrit par un résumé, écrit par un auteur, publié par un éditeur et comporte un ou plusieurs personnages principaux**. Il est également caractérisé par une date de parution, un nombre de pages, un ISBN et un prix éditeur. En outre, chaque auteur peut être décrit – de façon optionnelle – par une biographie.
Le jury est constitué par les membres de l'académie Goncourt qui est composée d'un ensemble de personnalités de l'écriture et présidée par l'une d'elles. Celui-ci établit trois sélections successives et attribut le prix Goncourt à l'auteur du roman primé à l'issue d'un dernier tour de scrutin lors duquel il obtient un certain nombre de voix, suivi par d'autres romans ayant obtenu moins de voix.
Il est demandé d'écrire une application en mode console permettant :
•
à tout utilisateur d’afficher les livres composant chaque sélection, avec toutes les informations figurant ci-dessus ;
•
au président du jury d’indiquer les livres faisant partie de la deuxième et troisième sélection ;
•
au président du jury d’indiquer le nombre de votes obtenus par chaque livre présent au dernier tour de scrutin ;
•
en option, d’ajouter une authentification pour chaque membre du jury, et de leur permettre de voter pour les deuxième et troisième sélections, ainsi que pour le lauréat (l’ensemble étant alors calculé automatiquement).
L’ensemble des données de départ pourra être entré en dur dans la base de données MySQL utilisée, en se limitant à la description détaillée des huit titres des huit premiers auteurs dans l'ordre alphabétique de leur nom, et ne renseignant pour les autres que le titre, l'auteur et l'éditeur. On veillera à limiter au maximum la redondance dans le modèle de données choisi et à permettre facilement l'extension de ce modèle à un ensemble de livres plus large (dans lequel notamment, un même auteur pourrait apparaitre pour plusieurs livres***), par exemple l'ensemble des livres sélectionnés pour le prix Goncourt depuis sa création, ou celui des livres sélectionnés pour tous les prix littéraires en France en 2024.
* obligatoirement écrit en français et publié par un éditeur francophone dans le cas de ce prix ; il s'agit généralement d'un roman.
** il s'agit des personnages cités dans le résumé du livre.
*** mais par souci de simplicité, on ne traitera pas du cas d'un même personnage principal pouvant apparaitre dans plusieurs livres (formant généralement une série).
Webographie :
•
Première sélection Prix Goncourt 2024 : permet d'obtenir toutes les données demandées
•
http://academie-goncourt.fr > Première sélection du Prix Goncourt 2024, Le Prix GONCOURT: Sélections et Lauréats par année (voir l'exemple de 2022)
•
Prix Goncourt — Wikipédia
Vous aurez une heure pour poser toutes vos questions au client avant de commencer le projet.
Contrainte technique : Votre application doit respecter – ou s’inspirer de – l’architecture multicouches vue lors du module Python avancé (application Ecole).
L’ensemble des productions attendues (feuille de route) :
•
démonstration ;
•
diagrammes UML (cas d’utilisation, classe, en option séquence) ;
•
spécifications fonctionnelles ;
•
base de données : MCD, script SQL de création, droit restreint sur celle-ci ;
•
couche modèle conforme au diagramme de classes ;
•
couche DAO ;
•
couche métier, puis couche application ;
•
utilisation de Git et de toutes les bonnes pratiques vues depuis le début (POO, exceptions, journalisation éventuellement, anglais, lisibilité, docstrings, tests éventuellement).

