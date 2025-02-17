Absolument ! Merci de me fournir ce tableau. Je vais le compléter avec les informations que nous avons résolues ensemble.

Voici le tableau complété :

 **Journal de bord des tests & debugging**  

|  **Date** | ️ **Action réalisée** |  **Problème rencontré** | ⚠️ **Solution apportée** | ✅ **Statut** |
|------------|-----------------|-----------------|-----------------|-----------------|
| `JJ/MM/AAAA` | Capture Scapy | Duplication dans `known_devices` | Vérification `MAC + IP` avant insertion | ✅ Résolu |
| `JJ/MM/AAAA` | TCPDump désactivé | TCPDump ne fonctionne pas sur Windows | Passage en 100% Scapy | ✅ Résolu |
| `JJ/MM/AAAA` | Détection des sites | Pas d'affichage des sites visités | Ajout d’un filtre DNS |  En cours |
| `JJ/MM/AAAA` | Gestion des erreurs | `fetch_data()` retournait un objet non utilisable | Conversion `response.data` en `list` | ✅ Résolu |
| `JJ/MM/AAAA` | Mise à jour `last_seen` | Erreur de sérialisation JSON pour `datetime` | Conversion `datetime` en chaîne ISO 8601 | ✅ Résolu |
| `JJ/MM/AAAA` | Suivi des appareils | Adresse IP dynamique | Ajout du champ `last_ip` et mise à jour si l'IP change | ✅ Résolu |

 **Tableau détaillé des erreurs rencontrées et comment on les a corrigées**  

|  **Problème** |  **Cause possible** |  **Solution apportée** | ✅ **Statut** |
|-----------------|----------------------|-------------------------|--------------|
| `fetch_data() got an unexpected keyword argument 'condition'` | Mauvais paramètre passé | Utilisation de `conditions={}` au lieu de `condition=` | ✅ Résolu |
| `APIResponse object is not subscriptable` | `fetch_data()` retourne `APIResponse` au lieu d’un dict | Conversion `response.data` en liste | ✅ Résolu |
| **TCPDump non reconnu sur Windows** | `tcpdump.exe` non installé | Suppression de TCPDump pour le mini-projet | ✅ Résolu |
| **Sites visités non détectés** | Scapy ne capture pas bien les requêtes DNS | Ajout d’un meilleur filtre DNS |  En cours |
| **Erreur de sérialisation JSON pour `datetime`** | Objet `datetime` non sérialisable en JSON | Conversion `datetime` en chaîne ISO 8601 (`now.isoformat()`) | ✅ Résolu |
| **Suivi imprécis des appareils avec IP dynamique** | Seul l'adresse MAC était suivi | Ajout du champ `last_ip` et mise à jour dans `insert_known_device` | ✅ Résolu |

