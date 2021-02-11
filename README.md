# Big Bounty Deliveroo

> Groupe Jullian BACLE - Clément JELEFF

## Sommaire

- [Contexte](#contexte)
- [Timezone](#timezone)
- [Cible](#cible)
- [Modus operandi](#Modus-operandi)
- [Outils utilisés](#Outils-utilisés)
- [Données découvertes](#Données-découvertes)
  - [Assetfinder](#assetfinder)
  - [Shuffledns](#shuffledns)
  - [Nmap](#nmap)
  - [Gospider](#gospider)
  - [Dirsearch](#dirsearch)
- [Petit script](#petit-script)

## Contexte

Suite à un cours sur la méthodologie d'attaque d'une cible, dans un
contexte de bug bounty. Nous sommes passés à la pratique, en utilisant
cette même méthodologie sur une cible réelle.

## Timezone

Actions de reconnaissance effectuées :

    Le 05/02/2021 de 11h00 à 20h00
    Le 06/02/2021 de 14h00 à 19h00
    Le 07/02/2021 de 11h00 à 19h00
    Le 08/02/2021 de 15h00 à 20h00
    Le 09/02/2021 de 13h00 à 17h00

## Cible

Bug Bounty Deliveroo

> <https://hackerone.com/deliveroo?type=team>

Reconnaissance établie sur le scope :

    .deliveroo.

## Modus operandi

Afin de se faire une idée de la surface d'attaque possible de notre
cible. Une première énumération des sous-domaines est effectuée. Une
2ème énumération plus poussée en utilisant différentes bases de données nous permet d'avoir une énumération plutôt complète, des sous-domaines valides de notre cible.

Pour chaques hôtes identifiés durant l'étape précèdente, nous effectuons
un scan des ports. Nous permettant d'apprécier de possible portes
d'entrées.

De plus une phase de "spidering" est faite. Celle-ci nous permet de
découvrir les endpoints accessible. Toujours dans un objectif
d'augmenter notre surface d'attaque.

Pour finir une recherche de dossiers et/ou fichiers cachés sur chaques
hôtes est faite. Cette phase utilise des banques de données de mots,
permettant de "bruteforce".

## Outils utilisés

- Assetfinder
  - Trouve des domaines et sous-domaines lié au domaine cible.
- Shuffledns (massdns, dnsvalidator)
  - Outil de reconnaissance, regroupant et se servant de plusieurs autres outils tel que *massdns* et *dnsvalidator*. Il permet d'énumérer les sous-domaines valide d'une cible.
- Nmap
  - Scanne les ports de la cible.
- Gospider
  - Cherche des point d'accès lié aux domaines la cible grâce à du bruteforce et en explorant les ressources trouvés.
- Dirsearch
  - Cherche des accès à des répertoires ou fichiers liés à la cible, en bruteforçant.

## Données découvertes

### Assetfinder

Commande utilsée :
```
assetfinder deliveroo.com
```

> [Données récupérées](./result-assetfinder.txt)
---
### Shuffledns

Commande utilsée :
```
shuffledns -r resolvers.txt -list result-assetfinder.txt
```

> [Données récupérées ](./result-shuffledns.txt)
---
### Nmap

Commande utilsée :
```
nmap -Pn -iL result-assetfinder.txt
```

> [Données récupérées ](./result-nmap.txt)
---
### Gospider

Commande utilsée :
```
gospider -S result-shuffledns.txt
```

> [Données récupérées ](./result-gospider.txt)
---
### Dirsearch

Commande utilsée :
```
python3 dirsearch.py -l result-shuffledns.txt -e php --exclude-status 403
```

> [Données récupérées ](./result-dirsearch.txt)
---

## Petit script

Afin que `Gospider` prenne en compte notre liste de domaines, un petit script en python à été créé. Il ajoute le préfixe `https://` devant chaques domaines de la liste.

> [Script](./ajout-https.py)
