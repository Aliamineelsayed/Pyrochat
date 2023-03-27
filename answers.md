Prise en main

Question 1:

Il sagit d'un topologie en étoile dans laquelle tous les serveur sont connectés a un point central.

Question 2:

On remarque que dans les logs, les messages sont stockés en clair sur le serveur (ne sont pas chiffrés)

Question 3:

Le fait que quelqu'un puisse accéder au serveur et lire les messages échangés entre les utilisateurs pose un problème de sécurité et de confidentialité et cela viole le principe de la confidentialité.

Question 4:

Pour éviter le problème de la lisibilité des messages entre les clients, il est recommandé d'utiliser des protocoles de communication qui assurent la confidentialité des messages échangées comme les clés de chiffrement.


Chiffrement

Question 1 :

La fonction urandom de Python peut être exploitée pour générer des clés de chiffrement ou de signature en se servant d'une source de nombres aléatoires. Donc, cette fonction ne convient pas pour la cryptographie en raison de la qualité insuffisante des nombres aléatoires qu'elle génère, ce qui ne garantit pas la sécurité de l'algorithme de chiffrement.

Question 2:

L'utilisation de primitives cryptographiques de manière incorrecte peut être dangereuse car cela peut disloquer la sécurité du système et des données.

Question 3:

Le chiffrement ne garantit pas la sécurité totale, car le serveur peut toujours avoir accès aux messages chiffrés et les modifier.

Question 4:

la propriéte qui manque ici est la controle des données.

Authenticated Symmetric Encryption

Question 1:

Fernet est moins risqué que le précédent chapitre en termes d'implémentation car il utilise un schéma de chiffrement authentifié qui garantit l'intégrité du message. De plus, la bibliothèque cryptography permet d'évite les erreurs d'implémentation.

Question 2:

Cette attaque est appelée "attaque de rejeu".

Question 3:

Une méthode simple pour éviter les attaques de rejeu est d'utiliser des numéros de séquence dans les messages pour garantir que chaque message est unique.

TTL

Question 1:

Pas de différence visible, la longueur du message inchangée.

Question 2:

Si l'on soustrait 45 du temps d'émission, le message chiffré ne pourra pas être déchiffré car son temps de réception sera considéré comme antérieur au temps d'émission, ce qui le fera expirer. On a TTL est de 30 secondes, si on soustrait 45 du temps d'émission, le temps de réception sera décalé de 15 secondes avant l'émission, ce qui dépasse la durée de vie du message.

Question 3:

Oui, l'utilisation de TTL est efficace pour ce protéger de l'attaque de rejeu.

Question 4:

Il est nécessaire de réduire le temps de sécurisation des messages dans la pratique, car en moins de 30 secondes, une machine peut mener une attaque de rejeu. De plus, la latence sur la connexion peut causer des messages valides à être considérés comme invalides.

Regard critique

Il existe une vulnérabilité potentielle dans la méthode de chiffrement symétrique qui utilise une clé générée à partir d'un mot de passe, qui pourrait être exploitée par un attaquant qui peut utiliser une attaque par force brute pour déchiffrer les données. De plus, un problème dans le code peut permettre à un attaquant d'envoyer des données malveillantes qui peuvent être traitées par le serveur comme des données légitimes, il est donc important que le serveur vérifie l'authenticité du message avant de le déchiffrer pour éviter cette vulnérabilité de sécurité.


