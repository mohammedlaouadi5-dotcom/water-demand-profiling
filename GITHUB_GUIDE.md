# GUIDE GITHUB ULTRA-SIMPLE (Pour Débutants)

Pas de panique ! Voici les étapes exactes, une par une. Suivez simplement les instructions.

---

## 🚨 ÉTAPE 0 : Installer Git (INDISPENSABLE)

⚠️ **Je n'ai pas trouvé Git sur votre ordinateur.** Vous devez l'installer avant de continuer.

1. Téléchargez Git ici : **[git-scm.com/download/win](https://git-scm.com/download/win)**
2. Cliquez sur **"Click here to download"** (la version 64-bit).
3. Lancez l'installation et cliquez sur **Next** à chaque fois (ne changez rien, faites juste Next > Next > Install).
4. Une fois fini, **REDÉMARREZ VOTRE ORDINATEUR** (ou fermez/rouvrez toutes les fenêtres).

---

## ÉTAPE 1 : Créer le "coffre-fort" sur GitHub (Site Web)

1. Connectez-vous à votre compte sur **[github.com](https://github.com)**.
2. En haut à droite, cliquez sur le petit **+** et choisissez **New repository**.
3. Remplissez juste ces cases :
   - **Repository name** : `water-demand-profiling`
   - **Description** : (Optionnel) Code for Water Science and Engineering paper
   - **Public/Private** : Choisissez **Public** (pour que les reviewers puissent le voir).
   - **Initialize this repository with**: NE COCHEZ RIEN (laissez tout vide).
4. Cliquez sur le bouton vert **Create repository**.

🎉 Bravo ! Votre repo est créé.
**IMPORTANT** : Sur la page suivante, copiez le lien HTTPS qui ressemble à ça :
`https://github.com/VOTRE-NOM/water-demand-profiling.git`
(Gardez-le sous la main).

---

## ÉTAPE 2 : Préparer votre ordinateur (Terminal)

On va utiliser le terminal de votre ordinateur pour envoyer les fichiers.

1. Ouvrez le dossier de votre projet sur votre ordinateur.
2. Faites un **clic droit** dans le vide du dossier > **Open in Terminal** (ou Ouvrir PowerShell / Git Bash).
3. Une fenêtre noire ou bleue s'ouvre. Tapez les commandes suivantes UNE PAR UNE (appuyez sur Entrée à chaque fois) :

### Commande 1 : Dire "Bonjour" à Git
```bash
git init
```
*(Il va dire "Initialized empty Git repository..." -> C'est bon !)*

### Commande 2 : Ajouter tous vos fichiers
```bash
git add .
```
*(Il ne dira rien ou listera des fichiers. C'est normal, il prépare le paquet.)*

### Commande 3 : Fermer le paquet (Commit)
```bash
git commit -m "Premier commit : Code complet du papier WSE"
```
*(Il va lister tous les fichiers ajoutés. C'est bon !)*

### Commande 4 : Nommer la branche principale
```bash
git branch -M main
```
*(Rien ne s'affiche, c'est normal.)*

---

## ÉTAPE 3 : Connecter et Envoyer (Le moment de vérité)

C'est ici qu'on relie votre ordinateur à GitHub.

### Commande 5 : Faire le lien (Remplacez l'URL !)
Collez votre lien copié à l'étape 1 à la place de `VOTRE-LIEN-ICI`.
```bash
git remote add origin https://github.com/VOTRE-NOM/water-demand-profiling.git
```

### Commande 6 : Envoyer les fichiers (Push)
```bash
git push -u origin main
```

---

## 🛑 SI ÇA DEMANDE UN MOT DE PASSE...

Si une fenêtre s'ouvre pour vous connecter :
1. Connectez-vous avec votre navigateur (c'est le plus simple).
2. Autorisez l'accès.

Si ça demande un mot de passe dans le terminal et que votre mot de passe GitHub ne marche pas :
- C'est normal, GitHub n'accepte plus les mots de passe simples ici.
- **Solution simple** : Installez "GitHub Desktop" (logiciel visuel) si vous bloquez ici. Mais normalement, la fenêtre de connexion navigateur devrait apparaître.

---

## ÉTAPE 4 : Vérifier

Retournez sur la page de votre repo sur **github.com** et rafraîchissez la page (F5).
Vous devriez voir tous vos fichiers (README.md, src, etc.) !

C'est fini ! Copiez le lien de la page (ex: `https://github.com/mohammed/water-demand-profiling`) et collez-le dans votre manuscrit si besoin.
