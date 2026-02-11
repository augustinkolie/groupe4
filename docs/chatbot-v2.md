# 🧠 Chatbot V2 : Mémoire, Analyse & Expérience Utilisateur

Ce document détaille l'implémentation technique des nouvelles fonctionnalités du Chatbot (V2).

## 1. 🧠 Mémoire Coversationnelle (Session)

**Problème V1 :** L'IA oubliait tout dès la réponse suivante.
**Solution V2 :** Stockage de l'historique dans la session Django.

### Implémentation
- **Stockage** : `request.session['chat_history']` (Liste de dictionnaires `{"role": "...", "content": "..."}`).
- **Limite** : Rotation sur les 10 derniers messages pour ne pas saturer la session.
- **Injection** : Le service IA reçoit cet historique et le formate pour le LLM.

**Fichiers Clés :**
- [`monitoring/views_htmx.py`](file:///d:/Projet_Python/groupe4/monitoring/views_htmx.py) (Gestion de la session)
- [`monitoring/services/gemini/service.py`](file:///d:/Projet_Python/groupe4/monitoring/services/gemini/service.py) (Formatage du prompt)

---

## 2. 📊 Data Analyst (Tendances 24h)

**Problème V1 :** L'IA ne voyait que l'instant T (les 5 derniers relevés). Impossible de voir une évolution.
**Solution V2 :** Calcul d'agrégats sur 24h avant l'appel.

### Implémentation
Avant chaque question, le backend calcule :
1.  **Moyenne PM2.5** sur 24h.
2.  **Température Moyenne** sur 24h.

Ce "résumé" est injecté dans le contexte système via la variable `trends_summary`.

**Code :**
```python
# monitoring/views_htmx.py
time_threshold = timezone.now() - timedelta(hours=24)
avg_pm25 = Reading.objects.filter(...).aggregate(Avg('pm25'))['pm25__avg']
```

---

## 3. ⚡ UX "Machine à Écrire" (Streaming & Curseur)

**Problème V1 :** L'utilisateur attendait 2-3 secondes devant un écran vide, puis tout le texte apparaissait d'un coup.
**Solution V2 :** Simulation JavaScript de l'effet ChatGPT.

### Implémentation Front-End
- **ID Unique** : Chaque message reçoit un ID unique (`uuid`) généré par le serveur pour un ciblage JS parfait.
- **Script JS** :
    - Récupère le texte brut caché (`.raw-response`).
    - L'injecte caractère par caractère dans `.stream-output`.
    - **Vitesse Variable** : Entre 10ms et 30ms pour un effet "humain".
- **Curseur** : Une classe CSS `.typing-cursor` ajoute un rond clignotant (`●`) à la fin du texte pendant la frappe.

**Fichier Clé :**
- [`monitoring/templates/monitoring/partials/chatbot_message.html`](file:///d:/Projet_Python/groupe4/monitoring/templates/monitoring/partials/chatbot_message.html)

---

## 4. 🛠️ Robustesse (Gestion d'Erreurs)

- **Calculs** : Si aucune donnée n'existe pour la moyenne (retour `None`), le code utilise `0` par défaut pour éviter le crash (Erreur 500).
- **Service IA** : Si l'API échoue, un message d'erreur convivial est retourné ("Mon cerveau IA est déconnecté 🧠⚠️") au lieu de faire planter la vue.
